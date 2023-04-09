import os, sys
import json
import random
from random import seed, choice,randrange
import tkinter as tk
from tkinter import ttk
from tkinter import *

import customtkinter as ctk

from pathlib import Path
from functools import partial

ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green
special_char_map = {ord('ä'):'a', ord('ü'):'u', ord('ö'):'o', ord('ß'):'s'}

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath("./word_list")
    return os.path.join(base_path, relative_path)

frozen = 'not'
if getattr(sys, 'frozen', False):
        # we are running in a bundle
        frozen = 'ever so'
        bundle_dir = sys._MEIPASS
else:
        # we are running in a normal Python environment
        bundle_dir = os.path.dirname(os.path.abspath(__file__))


file_names = ["SportundFreizeit",
              "VerbenNiveauA2-B1",
              "Die90haeufigstenVerbenA1",
              "HaeufigkeitundReihenfolge",
              "KoerperlicheTaetigkeiten",
              "AeusseresErscheinungsbild",
              "CharakterAndTemperament"
              ]

files = {}
files_known = {}
for f in file_names:
    files[f] = resource_path(f+".json")
    files_known[f] = resource_path(f+"-known.json")

class word:
    def __init__(self, eng="", ger="", sent="", word="",known="", correct=0, wrong=0):
        self.eng = eng
        self.ger = ger
        self.sent = sent
        self.word = word
        self.known = known
        self.correct = correct
        self.wrong = wrong
    def set_known(self):
        self.correct += 1
        if self.correct > self.wrong and self.correct > 0:
            self.known = "True"
    def set_wrong(self):
        self.wrong += 1
    
def get_new_word_list():
    global filename, filename_known
    print("selected no, open ",filename)

    with open(filename,"r") as f: 
        data = json.load(f)
        for i in data["table"]:
            for k, v in i.items():        
                if len(v) > 3:
                    word_list.append(word(v[1], v[0], v[2], v[3],"", 0,0))
                else:
                    word_list.append(word(v[1], v[0], v[2], "","", 0,0))

    run()
def get_word_list():
    print(filename,filename_known)
    if not os.path.exists(filename_known):
        print("no progress found, start with full list")
        with open(filename,"r") as f:
            print("loading ",f)
            data = json.load(f)
            for i in data["table"]:
                for k, v in i.items():        
                    if len(v) > 3:
                        word_list.append(word(v[1], v[0], v[2], v[3],"", 0,0))
                    else:
                        word_list.append(word(v[1], v[0], v[2], "","", 0,0))
    else:
        with open(filename_known,"r") as f: 
            data = json.load(f)
            for v in data["table"]:
                word_list.append(word(v[0], v[1], v[2], v[3], v[4],v[5],v[6]))

    run()

    
def run():
    global root
    global w
    global frame

    set_frame()
    
    label = ctk.CTkLabel(frame)
    label.grid(row=0, column =0, columnspan=5, padx=10, pady=10)

    entry = ctk.CTkEntry(frame,width=250)
    entry.focus_set()
    x = entry.get()        
    i = 0    
    new_list = list(filter(lambda x :  x.known == "", word_list))
    if len(new_list) > 1:
        i = randrange(1,len(new_list))

    if len(new_list) > 0:
        w = new_list[i]
        label.configure(text=w.eng)
        print(w.eng, w.known, w.correct, w.wrong)
        
        check = ctk.CTkButton(frame, text= "Check",width= 100, command=lambda : compare(None,entry.get(),label ))
        cont = ctk.CTkButton(frame, text= "Continue",width= 100,  command=run)
        done = ctk.CTkButton(frame, text= "Exit",width= 100,  command=ask_save)
        example = ctk.CTkButton(frame, text= "Example",width= 100, command=lambda : get_sentence(None,entry,label ))
        
        entry.grid(column=0,columnspan=5, row=3, padx=10, pady=10)
        check.grid(column=1, row=4, padx=10, pady=10)
        example.grid(column=2, row=4, padx=10, pady=10)
        cont.grid(column=3, row=4, padx=10, pady=10)
        done.grid(column=4, row=4, padx=10, pady=10)

        root.bind('<Right>', lambda event=None: cont.invoke())
        root.bind('<Return>', lambda event=None: check.invoke())
        root.bind('<Escape>', lambda event=None: done.invoke())
        root.bind('<Shift Return>', lambda event=None: example.invoke())
    else:
        select_file()
        

def ask_save():
    global frame
    set_frame()

    label = ctk.CTkLabel(frame, width=100,
                               fg_color=("white", "gray75"),
                               corner_radius=8)
    label.grid(row=0, column = 0, sticky ="ew", columnspan=5, padx=10, pady=10)
    label.configure(text="Save progress?")
    
    yes_but=ctk.CTkButton(
        frame,
        text='yes',
        command=save_progress)


    no_but =ctk.CTkButton(
        frame,
        text='no',
        command=exit)

    yes_but.grid(column=1,   sticky ="ew",padx=10, pady=10, row=1)
    no_but.grid(column=3,   sticky ="ew",padx=10, pady=10,row=1)

    yes_but.focus_set()
    root.bind('<Right>', lambda event=None: no_but.invoke())
    root.bind('<Left>', lambda event=None: yes_but.invoke())
    root.bind('<Right>', lambda event=None: yes_but.invoke())
    
def save_progress():
    global word_list,filename_known

    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(os.path.realpath(sys.executable))
        running_mode = 'Frozen/executable'
    else:
        try:
            app_full_path = os.path.realpath(__file__)
            application_path = os.path.dirname(app_full_path)
            running_mode = "Non-interactive (e.g. 'python myapp.py')"
        except NameError:
            application_path = os.getcwd()
            running_mode = 'Interactive'
        
    #filename_known = os.path.join(application_path, filename_known)
    print(filename_known)
    table = {"table":[]}
    for s in word_list:
        table["table"].append([s.eng,s.ger,s.sent,s.word,s.known,s.correct,s.wrong])
        with open(filename_known, 'w') as outfile:
            json.dump(table, outfile)
    exit()

def exit():
    global root
    global frame
    frame.destroy()
    root.destroy()
    
def compare(event=None, x=None,label=None):
    global w
    
    print(w.ger, w.ger.lower().translate(special_char_map).replace(" ",""))
    if x == "":
        label.configure(text=" {}".format(w.ger))
    elif x.replace(" ","").lower()  == w.ger.replace(" ","").lower(): 
        w.set_known()
        run()
    elif x.lower()  in w.ger.lower():
        label.configure(text="Almost there, try again")
    elif x.lower().translate(special_char_map).replace(" ","") ==  w.ger.lower().translate(special_char_map).replace(" ",""):
        label.configure(text="Missing an umlaut probably, try again")
    else:
        label.configure(text="{}".format(w.ger))
        w.set_wrong()

def compare2(event=None, x=None,label=None):
    global w

    if x.replace(" ","").lower()  == w.word.replace(" ","").lower():        
        label.configure(text=w.sent, text_color=("midnight blue","dark-blue"))
    elif x.lower()  in w.word.lower():
        label.configure(text="Almost there, try again")
    elif x.lower().translate(special_char_map).replace(" ","") ==  w.word.lower().translate(special_char_map).replace(" ",""):
        label.configure(text="Missing an umlaut probably, try again")
    else:
        label.configure(text=w.sent, text_color=("red","red"))
    

def get_sentence(event=None, entry=None,label=None):
    global w

    entry.delete(0,END)
    x = entry.get()

    sent = w.sent 
    if w.word != "":
        sent = w.sent.replace(w.word, "__________")
   
    label.configure(text="{} ({})".format(sent, w.eng))

    check = ctk.CTkButton(frame, text= "Check",width= 100, command=lambda : compare2(None,entry.get(),label ))
    root.bind('<Return>', lambda event=None: check.invoke())
        
        
def ask_progress():
    global frame,filename, filename_known

    set_frame()
    
    label = ctk.CTkLabel(frame, width=600,
                               height=25,
                               fg_color=("white", "gray75"),
                               corner_radius=8)
    label.grid(row=0, column = 0, sticky ="ew", columnspan=4, padx=10, pady=10)
    label.configure( text="Continue from last practice?")
    
    yes_but=ctk.CTkButton(
        frame,
        text='yes',
        command= get_word_list)


    no_but =ctk.CTkButton(
        frame,
        text='no',
        command=get_new_word_list)

    yes_but.grid(column=1,   sticky ="ew",padx=10, pady=10, row=1)
    no_but.grid(column=2,   sticky ="ew",padx=10, pady=10,row=1)

    yes_but.focus_set()
    root.bind('<Right>', lambda event=None: no_but.invoke())
    root.bind('<Return>', lambda event=None: yes_but.invoke())
    
def select_file() :
    global frame, label
  
    set_frame()
    
    label = ctk.CTkLabel(frame, width=120,
                               height=25,
                               fg_color=("white", "gray75"),
                               corner_radius=8)
    label.grid(row=0, column =0, sticky="ew",columnspan=3, padx=10, pady=10)

    label.configure(text="Select word list to practice")

    buttons = []

    x = 0
    y = 0
    n = 0
    for k,i in files.items():
        print(i)
        i_known = files_known[k]
        def set_filename(fname=i,fname_known=i_known):
            global filename,filename_known
            filename = fname
            filename_known = fname_known
            ask_progress()

        buttons.append(ctk.CTkButton(frame, text = k, command = set_filename ))
        buttons[n].grid(row = 4+y, column = x,sticky="ew", padx=10, pady = 10)
        n += 1
        x += 1
        if x > 2:
            x = 0
            y += 1 

    return frame

def set_frame():
    global frame
    frame.destroy()
    frame = ctk.CTkFrame(root, width=630, height=250, bg_color=("midnight blue","dark-blue"))
    frame.grid(column = 0, row=0, padx=10, pady=10)
    #frame.grid(sticky='wse')
    for i in range(6):
        frame.columnconfigure(i, {'minsize': 100})
    frame.grid_propagate(0)
    #frame.grid(sticky='nswe')

# main sequence
w = word()
word_list = []

# create the root window
root = ctk.CTk(fg_color=("midnight blue"," midnight blue"))
root.wm_title('new  practice')
root.geometry('650x270')
root.resizable(0, 0)

frame = ctk.CTkFrame(root, bg_color=("midnight blue","dark-blue"))
set_frame()

label = ctk.CTkLabel(frame)

filename = ""
filename_known = ""
select_file()

# start the app
if __name__ == '__main__':
    root.mainloop()
