'''
Img JPEG & Location identification - Test and Develop

By : Quang "Neon" Le
Start Date: 10/29/2019
Last edit : 11/2/2019

Project Description:
Creating an application that can validate whether an image is JPG and return
image's location zipcode

'''
import sys
import os
import ntpath
import csv
#tkinter are for GUI
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from checker import *
from zipcode import *




## MAIN setup
root = Tk()
root.geometry('800x500')
root.title("Image Identification")

enable_zipcode = IntVar()
enable_exif = IntVar()
rows = 0

while rows<50:
    root.rowconfigure(rows,weight=1)
    root.columnconfigure(rows,weight =1)
    rows +=1
## MAIN end

#========================UI Function definitions==============================#
'''
This function triggers when user use Insert Images
Once user select the files, they will store this information
'''
def get_filenames():
    global filenames
    for widget in page1.winfo_children():
        widget.destroy()
    i = 0
    tk_filenames = filedialog.askopenfilenames(initialdir="./"
        , title='Please select one or more files'
        , filetypes=(("JPG files","*.jpg"),("All Files","*")))
    filenames = list(tk_filenames)
    for in_file in filenames:
        Label(page1,text = in_file).grid(row = 2 + i, column=0, sticky = 'W')
        i +=1

def add_verification():
    global is_jpg, is_exif, zip_codes
    is_jpg = []
    is_exif= []
    zip_codes= []
    i = 0
    j = 0
    # Verification step should only run if user input files already
    try:
        filenames
    except NameError:
        return

    # Go through all files that user put in filenames
    for in_file in filenames:
        # Send message to console
        print('Working with file:', i)

        # Always check if file is JPG
        check_for_jpg = test_for_jpg(in_file)

        # If file is not JPG
        if not check_for_jpg:
            new_label = Label(page1, text = 'not JPG')
            new_label.grid(row = 2 + i,column=2, sticky='N')
            is_jpg.append(False)
            is_exif.append(False)
            zip_codes.append('Not Applicable')

        # If file is JPG
        else:
            new_label = Label(page1, text = 'is JPG')
            new_label.grid(row = 2 + i,column=2, sticky='N')
            is_jpg.append(True)

            # Check If the user wants to see if JPG is EXIF
            if enable_exif.get():
                check_for_exif = test_for_exif(in_file)

                # If file is EXIF
                if check_for_exif:
                    new_label = Label(page1, text = 'is EXIF')
                    new_label.grid(row = 2 + i,column=3, sticky='N')
                    is_exif.append(True)

                # If file is not EXIF
                else:
                    new_label = Label(page1, text = 'not EXIF')
                    new_label.grid(row = 2 + i,column=3, sticky='N')
                    is_exif.append(False)

            # Check If the user wants to see the Zipcode
            if enable_zipcode.get():

                '''
                If a file is EXIF AND has GPSINFO
                We can find latitude/longitude base on that
                Otherwise we use GG machine learning to get lat/long
                '''
                if (test_for_exif(in_file) and test_for_gps(in_file)):
                    coordinates = get_ltt_exif(in_file)
                else:
                    coordinates = get_ltt_non_exif(in_file)

                # Convert the coordinates to zipcode if found
                if coordinates:
                    zip_code = ltt_to_zip(coordinates)
                    '''
                    Sometimes both GeoPY and GG Geocode fail to identify
                    img location so we check if it succeed
                    '''
                    if zip_code != 0:
                        zip_codes.append(zip_code)
                    else:
                        zip_codes.append('Not Found')
                else:
                    zip_codes.append('Not Found')
                new_label = Label(page1, text = zip_codes[i])
                new_label.grid(row= 2 + i , column = 4, sticky = 'N')
        #Add more check here
        i +=1

def output_csv():
    i = 0
    # User press output csv without having put in files to read yet
    try:
        if(len(is_jpg) == len(is_exif) == len(zip_codes) == len(filenames)):
            print('Writing out to CSV...')
        else:
            print('Please select imgs & verify ALL attributes before CSV gen')
            return
    except NameError:
        print('Please select imgs & verify ALL attributes before CSV gen')
        return

    with open('out_data.csv', mode='w', newline='') as img_lction:
        fieldnames = ['Img_path', 'is JPG', 'is EXIF', 'Zip Code' ]
        writer = csv.DictWriter(img_lction, fieldnames = fieldnames)
        writer.writeheader()
        for image in filenames:
            writer.writerow({'Img_path' : image,
                             'is JPG'   : is_jpg[i],
                             'is EXIF'  : is_exif[i],
                             'Zip Code' : zip_codes[i]
                             })
            i += 1
    print('CSV file is ready')


#========================Layout/Button Designs==============================#
nb = ttk.Notebook(root)
nb.grid(row=0,column=0, rowspan = 40, columnspan = 50, sticky='NESW')

page1 = ttk.Frame(nb)
nb.add(page1, text ='Verify JPEG')

Label(root, text = "1. Select one or more imagesby clicking Insert Images")\
.grid(row=41, column = 0,columnspan = 3, sticky = "W")
Label(root, text = "2. Tick checkbox for more details ")\
.grid(row=42, column = 0,columnspan = 3, sticky = "W")
Label(root, text = "3. Click on Verify")\
.grid(row=43, column = 0,columnspan = 3, sticky = "W")


# logo = PhotoImage(file = "./logo.png")
# Label(root, image = logo).grid(row =48, column = 0, sticky = 'SW')

button1= ttk.Button(text="Insert Images", command =get_filenames)
button1.grid(row=41, column =49,columnspan = 2)

button2 = Checkbutton(root, text = "Find ZipCode", variable = enable_zipcode)
button2.grid(row = 42, column = 49,columnspan = 2, sticky = 'W')

button3 = Checkbutton(root, text = "Verify EXIF", variable = enable_exif)
button3.grid(row = 43, column = 49,columnspan = 2, sticky = 'W')

button4= ttk.Button(text="Verify", command = add_verification)
button4.grid(row=48, column =45,columnspan = 2, sticky = 'SE')

button5= ttk.Button(text="Export CSV", command = output_csv)
button5.grid(row=48, column =47,columnspan = 2, sticky = 'SE')

button6= ttk.Button(text="Exit", command = root.destroy)
button6.grid(row=48, column =49,columnspan = 2, sticky = 'S')



root.mainloop()
