# IMG JPG & ZIP CODE IDENTIFIER

By: Quang "Neon" Le

Version: 1.0.0

Date: 11/2/2019

# __Project Description__
#### Introduction  
  
    This project aims to create a portable Python tool that can
    validate an image, check to see if image is a JPG format and 
    return the ZIP CODE of that picture.

    The script works on Linux, OSX, and Windows. Easy to install with shell
    script to setup all required tools/dependencies. Interactive GUI make it 
    easy to use with fast image processing.
    
    The tool can take multiple image input and ensure return of zip code 
    through the use of two location tools which are GoogleCloudPlatform
    and Geopy. User will also be given choices to export data to a CSV
    file as well. The Tool can also be compressed into one single EXE file
    through the setup shells

#### Compromises:

    As of the moment, the tool can only be compressed to a single Windows/Linux
    file as we have trouble with pyinstaller on OSX due to some internal
    naming convention conflict within Pyinstaller and tcl/tk module. 
    Additionally, despite using two image processing platform to get zip code
    from coordinates, the platforms database sometimes don't have information
    regarding zip code.
    The attached setup shellscript is also janky for Windows and its operation
    depends on how the user setup the env

##### Next steps:

    Next steps are figuring out OSX problem with Pyinstaller for full three 
    portable app, using web scraping framework to manually find zip code if 
    both tools fail to ensure 100% data collection, and reconfiguring shell
    script for windows.


## __Setting Up__
#### Requirements

    Programs        : Python3, Pip/brew package manager
    External modules: Geopy, Google Cloud, Google Cloud Vision, Tkinter

    Please install these required tools to use the project.
    You can try the attached shell script for quick setup of the tools.
    
#### Instructions:

    WINDOWS USERS:    
        1. Install Python3 at https://www.python.org/downloads/
        
        2. Get PIP package manager by enter these commands in the terminal:
            curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
            py get-pip.py
            
        3. Install the required modules:
            pip install --upgrade --user geopy
            pip install --upgrade --user google-cloud-vision
            pip install --upgrade --user pyinstaller
            pip install --upgrade  --user google-cloud-core
    
    LINUX USERS:    
        1. Install Python3 with command:
            sudo apt-get update
            sudo apt install --upgrade python3
            
        2. Get PIP package manager with command:
            sudo apt install python3-pip
            sudo apt-get install python3-tk
            
        3. Install the required modules:
            pip install --upgrade --user geopy
            pip install --upgrade --user google-cloud-vision
            pip install --upgrade --user pyinstaller
            pip install --upgrade  --user google-cloud-core
        
    OSX USERS:
        1. Install Python3 with command: 
            /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"            
        2. Get PIP package manager with command:   
            brew install python3
            
        3. Install the required modules:
            brew install tcl-tk
            pip3 install --upgrade --user geopy
            pip3 install --upgrade --user google-cloud-vision
            pip3 install --upgrade --user pyinstaller
            pip3 install --upgrade  --user google-cloud-core

    Afterwards, you can create a single EXE file with:
        pyinstaller --clean --onefile --additional-hooks-dir=./hooks AppGUI.py
    
    If you do that, remember to copy in the authen.json file:
        cp ./authen.json ./dist
    
    Or you can use it like a normal Python Script:
        python AppGUI.py
    
#### IMPORTANT NOTE:
    
```diff
- The authen.json needs to be in the same directory as the application.
- It is used to authenticate with Google Cloud Vision API.
```
    
    pyinstaller often get install not in PATH, follow these commands to fix:
        export APEND=$( find / -name pyinstaller)
        export APENDIR=$(dirname "${APEND}")
        export PATH=$PATH:$(dirname"${}")
  
# Modules/Functions Instruction:

    GUI: AppGUI.py
    User interface to interact with the functions.

    Module: zipcode.py 
    Zip code finder module
        
        ltt_to_zip(ltt_arr)
        ->Based on [latitude,longitude] RETURN the zip code
        
        ltt_to_zip-fom_geopy(ltt_arr)
        ->Based on [latitude,longitude] RETURN the zip code
        uses GeoPy which consists of AzureMaps/Bing/Pelias
        
        ltt_to_zip_from_google(ltt_arr)
        ->Based on [latitude,longitude] RETURN the zip code of the image
        uses GG Maps/GG Geocode/GG Places API

        get_ltt_non_exif(file_path)
        -> read non EXIF image files and RETURN [lat,long]
        uses Google Vision ML API
        
        get_ltt_exif(file_path)
        -> read EXIF image files and RETURN [lat,long]
        uses GPS that is in EXIF images
    
    Module: byte_reader.py   
    Byte reader module.
    
        read_byte( file_desc, num_of_bytes, endian):
        -> Read num_of_bytes from file_desc depending on endian
        and RETURN a bytearray
        
        to_big_endian (byte_arr):
        -> reverse the small endian byte_arr to make big endian
        byte array and RETURN that byte array 
        
        bytearr_to_int(byte_arr):
        -> convert byte array and RETURN that integer
        
        
    Module: checker.py
    Input file type checker module.
    
        test_for_jpg(file_path):
        -> RETURN True if file is JPEG
        
        test_for_exif(file_path):
        -> RETURN True if file is EXIF format JPEG
        
        test_for_gps (file_path):
        -> RETURN True if EXIF store GPS information
    
    Module: mathematics.py 
    Data type converter module.
        
        int_str(input,choice):
        -> Convert non-negative INT input and RETURN string
        Choice determines what type to convert to:
            CHOICE 1 for DEC string
            CHOICE 2 for HEX string
            CHOICE 3 for HEX string without 0x prefix
            
        str_int (input,choice):
        -> Convert STRING input and RETURN int
        Choice determines what to convert from
            CHOICE 1 for HEX string

        reverse_str(input_str):
        -> Reverse the input_str and RETURN string

   
    
