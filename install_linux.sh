#!/bin/sh

echo RUN THIS AS SOURCE '. SHELLFILE'
echo Getting PIP
sudo apt-get update
sudo apt install --upgrade python3
sudo apt install python3-pip
sudo apt-get install python3-tk

echo Pip3 will now setup required modules for python
pip3 install --upgrade --user geopy
pip3 install --upgrade --user google-cloud-vision
pip3 install --upgrade --user pyinstaller
pip3 install --upgrade  --user google-cloud-core

echo Make sure pyinstaller is in path
export APEND=$( find / -name pyinstaller)
export APENDIR=$(dirname "${APEND}")
export PATH=$PATH:$(dirname"${}")

pyinstaller --clean --onefile --additional-hooks-dir=./hooks AppGUI.py
cp ./authen.json ./dist

echo Executable is ready at dist
