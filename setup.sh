#!/bin/bash




darkdetect="/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/site-packages/darkdetect:darkdetect/"
ctk_data="/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/site-packages/customtkinter:customtkinter/"

pyinstaller --noconfirm --name 'LearningGermanWords'  --add-data='./word_list/*.json:.'  --add-data=$darkdetect --add-data=$ctk_data  --onedir -w  --additional-hooks-dir .  test.py 
