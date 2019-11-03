#!/bin/sh

echo RUN THIS AS SOURCE '. SHELLFILE'
echo Getting PIP

/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

brew install python3
brew install tcl-tk

echo Pip3 will now setup required modules for python
pip3 install --upgrade --user geopy
pip3 install --upgrade --user google-cloud-vision
pip3 install --upgrade --user pyinstaller
pip3 install --upgrade  --user google-cloud-core

echo find Pyinstaller
export PYINST=$( find / -name pyinstaller)

pyinstaller --clean --onefile --additional-hooks-dir=./hooks AppGUI.py

$PYINST --clean --onefile --additional-hooks-dir=./hooks AppGUI.py


#Naming conventions of tcl-tk and pyinstaller is messing up compiling into application
cp ./authen.json ./dist

echo Naming conventions of tcl-tk and pyinstaller is messing up compiling into application
echo Use normal AppGUI.py

python3 AppGUI.py

