#!/bin/bash

pip3 install virtualenv
virtualenv -p python3 .
source ./bin/activate
pip3 install customtkinter
pip3 install pyinstaller 

# save progress before overwriting 
cp dist/LearningGermanWords.app/Contents/Resources/*-known.json word_list/

darkdetect="./lib/python3.10/site-packages/darkdetect:darkdetect/"
ctk_data="./lib/python3.10/site-packages/customtkinter:customtkinter/"


pyinstaller --noconfirm --name 'LearningGermanWords'  --add-data='./word_list/*.json:.'  --add-data=$darkdetect --add-data=$ctk_data  --onedir -w  --additional-hooks-dir .  test.py 
deactivate
