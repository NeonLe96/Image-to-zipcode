'''
Zipcode functions modules
.Extract GPS info from EXIF if EXIF has GPS info
.If EXIF doesn't have GPS info , find zip code base on google/Geopy
pip install --upgrade google-cloud-vision
do some export
'''
import sys
import io
import os
import requests
from mathematics import *
from byte_reader import *
from geopy.geocoders import Nominatim
from google.cloud import vision
from google.cloud.vision import types
from geopy.exc import GeocoderTimedOut

'''
ltt_to_zip(ltt_arr)
Based on [latitude,longitude] return the zip code
'''
def ltt_to_zip(ltt_arr):
    # Use GeoPy to look for zipcode first because it is more reliable
    zip = ltt_to_zip_from_GeoPy(ltt_arr)

    # if GeoPy fails then we use Google
    if zip == 0:
        zip = ltt_to_zip_from_google(ltt_arr)
    return zip

'''
ltt_to_zip-fom_geopy(ltt_arr)
Based on [latitude,longitude] return the zip code
This function use GeoPy which consists of AzureMaps/Bing/Pelias etc..
No need for API KEY
'''
def ltt_to_zip_from_GeoPy(ltt_arr):
    try:
        zip = 0
        geolocator = Nominatim(user_agent="ImgID")
        location = geolocator.reverse(ltt_arr)
        json_obj = location.raw

        '''
        Make sure that the field we need is in the json_obj
        Otherwise we will use Google
        '''
        if 'error' not in json_obj:
            if 'address' in json_obj:
                if 'postcode' in json_obj.get('address'):
                    zip = json_obj.get('address').get('postcode')

        return zip

        '''
        GeoPy is also well known for timing out so
        If GeoPy timeout then we use Google
        '''
    except GeocoderTimedOut:
        return zip


'''
ltt_to_zip_from_google(ltt_arr)
Based on [latitude,longitude] return the zip code of the image
This function use GG Maps/GG Geocode/GG Places API
Instead of Google Cloud Vision
API_KEY can be used directly here
'''
def ltt_to_zip_from_google(ltt_arr):

    zip = 0

    # Setting up variables for GET request to their API entrypoint
    URL = 'https://maps.googleapis.com/maps/api/geocode/json'
    payload = (
        ('latlng', str(ltt_arr[0]) +','+ str(ltt_arr[1])),
        ('key', 'AIzaSyD7IbJQQdSbPocbM3tH9IyQe9lhK9HJ8jU')
    )
    r= requests.get(URL, payload)

    # Read whatever is returned as JSON
    json_obj=r.json()
    for thing in json_obj.get('results'):
        address = thing.get('address_components')
        if len(address) >=8:
            zip = thing.get('address_components')[7].get('long_name')
    return zip

'''
get_ltt_non_exif(file_path)
Return [lat,long] from input image file_path through Google Cloud Vision API

We use this function for jpgs that are not EXIF standards
Can work with non jpg images too
'''
def get_ltt_non_exif(file_path):

    '''
    Setup the environ constants to be able to use the API
    Cloud Vision API is one of the API that require an authentication json
    file instead of just straight up using API KEY
    '''
    api_cred = os.path.abspath('./authen.json')
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = api_cred

    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # The name of the image file to annotate
    file_name = os.path.abspath(file_path)

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    # Performs Landmark detection on the image file
    response = client.landmark_detection(image=image)
    landmarks = response.landmark_annotations

    if not landmarks:
        #empty landmarks
        return False

    lat_lng = landmarks[0].locations[0].lat_lng


    return [round(lat_lng.latitude,6), round(lat_lng.longitude,6)]

'''
get_ltt_exif(file_path)
Return [lat,long] from input image file_path through EXIF info
'''
def get_ltt_exif(file_path):
    try:
        # Setting up variables
        i = 0
        check = False
        gps_tags_check = [False] * 4
        file = open(file_path, "rb")

        # Setting up the EXIF signature
        exif_sig= bytes([0x45,0x78,0x69,0x66])

        byte = file.read(1)
        #while loop to find where EXIF tag is
        while check == False:
            if byte[0] == exif_sig[0]:
                file.seek(-1, os.SEEK_CUR)
                byte = file.read(4)
                if byte == exif_sig:
                    check = True
            byte = file.read(1)
        # Once we find EXIF tag, tiff_header is 2 bytes after
        file.seek(1, os.SEEK_CUR)
        # Save tiff_header for future usage
        tiff_header = file.tell()
        byte = file.read(2)
        '''
        check if small or big endian
        if 'II' then small endian
        '''
        endian = 1
        if bytearr_to_int(byte) == str_int('x4949',1):
            endian = 0

        file.seek(2,os.SEEK_CUR)
        byte = read_byte(file,4,endian)
        # These next 4 bytes will give us the offset to actual data
        offset_to_first_ifd = bytearr_to_int(byte)

        # Move to offset
        file.seek(tiff_header + offset_to_first_ifd, os.SEEK_SET)

        # Next 2 bytes give us the number of tags
        byte = read_byte(file,2,endian)
        numb_of_tags = bytearr_to_int(byte)

        # Go through all the tags and find GPSINFO tag
        for i in range(0,numb_of_tags):
            byte = read_byte(file,2,endian)
            # GPS Info tag will be 0x8825
            if bytearr_to_int(byte) == str_int('x8825',1):
                break
            # Move to next tag
            file.seek(10, os.SEEK_CUR)

        # Type of GPSINFO is LONG (4 byte of info), skip to byte_count
        file.seek(6,os.SEEK_CUR)
        # Get the offset to gpsinfo data
        byte = read_byte(file,4,endian)
        offset_to_gpsinfo = bytearr_to_int(byte)

        # Move to GPS info data segment
        file.seek(tiff_header + offset_to_gpsinfo, os.SEEK_SET)
        byte = read_byte(file,2,endian)

        # Record the number of gps_tags
        numb_of_gps_tags = bytearr_to_int(byte)
        '''
        We are now at tags for GPS where each tags is 2 bytes
        Look for tags: 0x0001 0x0002 0x0003 0x0004
        Correspond to: LatRef Lat   LongiRef Longi
        Data Type    : Ascii  Rat   Ascii    Rat
        Count        :   2     3      2       3
        In the scenario that we can't find these info, we need to resolve to
        AWS and Google API
        '''
        important_tags = [0x0001, 0x0002, 0x0003, 0x0004]

        for i in range(0,numb_of_gps_tags):
            byte = read_byte(file,2,endian)
            value = bytearr_to_int(byte)
            if value in important_tags:
                gps_tags_check[value - 1] = True
                if all(gps_tags_check):
                    break
            file.seek(10, os.SEEK_CUR)

        # Check if the Exif has all tags needed
        if not all(gps_tags_check):
            return False
        # Move back to where the tags start, take data segment here read will get tag id
        file.seek(tiff_header + offset_to_gpsinfo + 2, os.SEEK_SET)

        '''
        Go through all the tags and look for the tags mentioned above
        '''
        for i in range(0,numb_of_gps_tags):
            byte = read_byte(file,2,endian)
            tag_num = bytearr_to_int(byte)
            if tag_num == 0x0001:
                lat_ref = tag_info_to_ltt_ref(file,endian)
            elif tag_num == 0x0003:
                longi_ref = tag_info_to_ltt_ref(file,endian)
            elif tag_num == 0x0002:
                lat = tag_info_to_ltt(file,endian,tiff_header)
            elif tag_num == 0x0004:
                longi = tag_info_to_ltt(file,endian,tiff_header)
            else:
                try:
                    lat_ref
                    longi_ref
                    lat
                    longi
                    break
                except NameError:
                    file.seek(10, os.SEEK_CUR)

        # Convert the dd/mm/ss or dd/mmmm/0 latitude/longitude to DD

        true_lat = dms_to_dd(lat[0],lat[1],lat[2],lat_ref)
        true_longi= dms_to_dd(longi[0],longi[1],longi[2],longi_ref)

        # Round it up to 6 decimal points
        return [round(true_lat,6),round(true_longi,6)]

    except IOError as e:
        print ("I/O error({0}): {1}".format(e.errno, e.strerror))
    except ValueError or IndexError:
        raise
    finally:
        file.close()

'''
Helper function to get Latitude/Longitude Refence N E S W
Use right after 0x0001 or 0x0003 tag identification
'''
def tag_info_to_ltt_ref(fd,endian):
    try:

        # Move to actualy data
        fd.seek(6, os.SEEK_CUR)

        '''
        Data is within 4 bytes so it get stored in the offset bytes
        Endianess may mess this data read, ensure correct read byte size
        More info on https://www.exif.org/Exif2-2.PDF page 20
        '''
        if endian == 0:
            byte = read_byte(fd,4,endian)
            value = bytearr_to_int(byte)
            return(chr(value))
        else:
            byte = read_byte(fd,1,endian)
            value = bytearr_to_int(byte)
            fd.seek(3,endian)
            return(chr(value))

    except IOError:
        print ("Could not open/read file")
        raise

'''
Helper function to read data from tags and find latitude/longitude
Use right after 0x0002 or 0x0004 tag identification
'''
def tag_info_to_ltt(fd,endian, tiff_header):
    try:
        ret_ltt = [0] * 3
        fd.seek(6, os.SEEK_CUR)
        byte = read_byte(fd,4,endian)
        off_set = bytearr_to_int(byte)
        end_of_tag = fd.tell()
        fd.seek(tiff_header + off_set, os.SEEK_SET)
        for i in range (0,3):
            byte = read_byte(fd,4,endian)
            numer = bytearr_to_int(byte)
            byte = read_byte(fd,4,endian)
            denom = bytearr_to_int(byte)
            ret_ltt[i] = (numer/denom)
        #format could be dd/1,mm/1,ss/1 or dd/1,mmmm/100,0/1
        if ret_ltt[2] == 0:
            ret_ltt[1] = ret_ltt[1]/100
        fd.seek(end_of_tag, os.SEEK_SET)
        return ret_ltt

    except IOError:
        print ("Could not open/read file")
        raise


#Helper function to convert dd/mm/ss to dd format for coordinate
def dms_to_dd(degrees, minutes, seconds,direction):
    ret_dd = float(degrees) + float(minutes)/60 + float(seconds)/(60*60)
    if direction == 'W' or direction == 'S':
        ret_dd *= -1
    return ret_dd
