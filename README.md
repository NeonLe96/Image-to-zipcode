# IMG JPG * ZIP CODE IDENTIFIER

By: Quang "Neon" Le

Version: 1.0.0

Date: 11/2/2019

## Project Description
# Introduction  
  
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

# Compromises:

    As of the moment, the tool can only be compressed to a single Windows/Linux
    file as we have trouble with pyinstaller on OSX due to some internal
    naming convention conflict within Pyinstaller and tcl/tk module. 
    Additionally, despite using two image processing platform to get zip code
    from coordinates, the platforms database sometimes don't have information
    regarding zip code.
    The attached setup shellscript is also janky for Windows and its operation
    depends on how the user setup the env

# Next steps:

    Next steps are figuring out OSX problem with Pyinstaller for full three 
    portable app, using web scraping framework to manually find zip code if 
    both tools fail to ensure 100% data collection, and reconfiguring shell
    script for windows.


## Setting Up
# Requirements

    Programs        : Python3, Pip/brew package manager
    External modules: Geopy, Google Cloud, Google Cloud Vision, Tkinter

    Please install these required tools to use the project.
    You can try the attached shell script for quick setup of the tools.
    
# Instructions:
    
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
    
# NOTE:
    
    pyinstaller often get install not in PATH, follow these commands to fix:
        export APEND=$( find / -name pyinstaller)
        export APENDIR=$(dirname "${APEND}")
        export PATH=$PATH:$(dirname"${}")
  
