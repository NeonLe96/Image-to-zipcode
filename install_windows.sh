#!/bin/sh

echo Getting PIP

curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
py get-pip.py

echo PLEASE RESTART TERMINAL

echo Pip will now setup required modules for python
pip install --upgrade --user geopy
pip install --upgrade --user google-cloud-vision
pip install --upgrade --user pyinstaller
pip install --upgrade  --user google-cloud-core

pyinstaller --clean --onefile --additional-hooks-dir=./hooks AppGUI.py
cp ./authen.json ./dist

py AppGUI.py
