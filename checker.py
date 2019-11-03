'''
Check functions modules

FUNCTIONS OFFERED:
1. Check if file is JPG
2. Check if JPG is EXIF
3. Check if EXIF has GPS info
'''
import sys
import os
from mathematics import *
from byte_reader import *

'''
test_for_jpg( file_path ) Check 1
This function will take in a file_path check whether file is JPG
It checks the first two bytes and last two bytes of the file
According to JPG Standard
First two bytes are always 0xFF 0xD8
last two bytes are always  0xFF 0xD9
'''
def test_for_jpg( file_path ):
    try:
        check1 = False
        check2 = False

        file = open(file_path, "rb")
        byte = file.read(2)
        '''
        Setup bytesarray 0xffd8 and 0xffd9
        These are magic numbers used to indentify jpg
        '''
        ffd8 = bytes([0xff,0xd8])
        ffd9 = bytes([0xff,0xd9])

        # First check two starting bytes is FF D8
        if byte == ffd8:
            check1 = True

        # Move to last 2 bytes of file and read them
        file.seek(-2, os.SEEK_END)
        byte = file.read(2)

        # Second check two ending bytes is FF D9
        if byte == ffd9:
            check2 = True

        if (check1 & check2):
            return True
        else:
            return False

    except IOError as e:
        print ("I/O error({0}): {1}".format(e.errno, e.strerror))
    except ValueError:
        raise
    finally:
        file.close()

'''
test_for_exif( file_path ) Check 2
This function will take in a JPG and check whether JPG is EXIF
The function will look for EXIF signature which is 0x45 78 69 66
'''
def test_for_exif (file_path):
    try:
        i = 0
        check = False

        # Setting up the EXIF signature
        exif_sig= bytes([0x45,0x78,0x69,0x66])

        file = open(file_path, "rb")
        byte = file.read(1)
        '''
        EXIF APP1 Marker should show during the fist 32 bytes
        Keep reading single byte until 32 bytes read
        If Exif isn't found then it is not EXIF file
        '''
        while i < 32 and check == False:
            # Look for the letter E first
            if byte[0] == exif_sig[0]:
                file.seek(-1, os.SEEK_CUR)
                # Then see if the 4 bytes make up Exif signature
                byte = file.read(4)
                if byte == exif_sig:
                    check = True
            byte = file.read(1)
            i += 1

        if check:
            return True
        else:
            return False

    except IOError as e:
        print ("I/O error({0}): {1}".format(e.errno, e.strerror))
    except ValueError:
        raise
    finally:
        file.close()

'''
test_for_gps( file_path ) Check 3
This function will take in an EXIF JPG and check whether EXIF has gpsinfo
The function will look for IFD tag 0x8825 which is the tag for gpsinfo
'''
def test_for_gps(file_path):
    file = open(file_path, "rb")
    try:
        i = 0
        check = False
        # Setting up the EXIF signature
        exif_sig= bytes([0x45,0x78,0x69,0x66])

        byte = file.read(1)
        # While loop to find where EXIF tag is
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
        These 2 bytes that we just read will tell us if small or big endian
        if 'II' or x4949 then it is small endian
        '''
        endian = 1
        if bytearr_to_int(byte) == str_int('x4949',1):
            endian = 0

        file.seek(2,os.SEEK_CUR)
        byte = read_byte(file,4,endian)
        # These next 4 bytes will give us the offset to actual IFDs
        offset_to_first_ifd = bytearr_to_int(byte)

        # Move to offset
        file.seek(tiff_header + offset_to_first_ifd, os.SEEK_SET)

        # Next 2 bytes give us the number of tags
        byte = read_byte(file,2,endian)
        numb_of_tags = bytearr_to_int(byte)
        check = False
        # Go through all the tags and see if there is GPSINFO tag
        for i in range(0,numb_of_tags):
            byte = read_byte(file,2,endian)
            # GPS Info tag will be 0x8825
            if bytearr_to_int(byte) == str_int('x8825',1):
                check = True
                break
            # Move to next tag
            file.seek(10, os.SEEK_CUR)

        if check:
            return True
        else:
            return False

    except IOError as e:
        print ("I/O error({0}): {1}".format(e.errno, e.strerror))
    except ValueError:
        raise
    finally:
        file.close()
