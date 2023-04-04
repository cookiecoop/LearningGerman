import os, sys
import json
import random
from random import seed, choice,randrange
import tkinter as tk
from tkinter import ttk
from tkinter import *
from pathlib import Path
from functools import partial

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath("./word_list")
    return os.path.join(base_path, relative_path)

file_names = ["SportundFreizeit",
              "VerbenNiveauA2-B1",
              "Die90haeufigstenVerbenA1",
              "HaeufigkeitundReihenfolge",
              "KoerperlicheTaetigkeiten"
              ]

files = {}
for f in file_names:
    files[f] = resource_path(f+".json")

class word:
    def __init__(self, eng="", ger="", sent="", known="", correct=0, wrong=0):
        self.eng = eng
        self.ger = ger.replace(" ","")
        self.sent = sent
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
                word_list.append(word(v[1], v[0], v[2], "", 0, 0))

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
                    word_list.append(word(v[1], v[0], v[2], "", 0,0))
    else:
        with open(filename_known,"r") as f: 
            data = json.load(f)
            for v in data["table"]:
                word_list.append(word(v[0], v[1], v[2], v[3], v[4],v[5]))
                if v[3] == "":
                    print(v[0], v[1], v[2], v[3], v[4],v[5])
    run()

    
def run():
    global root
    global w
    global frame

    frame.destroy()
    frame = Frame(root)
    set_frame()
    
    label = Label(frame)
    label.grid(row=0, column =0, columnspan=10, padx=10, pady=10)

    entry = Entry(frame)
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
        
        check = ttk.Button(frame, text= "Check",width= 20, command=lambda : compare(None,entry.get(),label ))
        cont = ttk.Button(frame, text= "Continue",width= 20, command=run)    
        done = ttk.Button(frame, text= "Exit",width= 20, command=ask_save)
        
        entry.grid(column=0,columnspan=10, row=3, padx=10, pady=10)        
        check.grid(column=3, row=4, padx=10, pady=10)        
        cont.grid(column=4, row=4, padx=10, pady=10)
        done.grid(column=5, row=4, padx=10, pady=10)

        root.bind('<Right>', lambda event=None: cont.invoke())
        root.bind('<Return>', lambda event=None: check.invoke())
        root.bind('<Escape>', lambda event=None: done.invoke())
    else:
        select_file()
        

def ask_save():
    global frame
    frame.destroy()
    frame = Frame(root)
    set_frame()

    label = Label(frame)
    label.grid(row=0, column =0, columnspan=10, padx=10, pady=10)
    label.configure(text="Save progress?")
    
    yes_but=ttk.Button(
        frame,
        text='yes',
        command=save_progress)


    no_but =ttk.Button(
        frame,
        text='no',
        command=exit)
    
    yes_but.grid(column=4,  padx=0, pady=0, row=1)
    no_but.grid(column=5,  padx=0, pady=0,row=1)

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
        
    filename_known = os.path.join(application_path, filename_known)
    print(filename_known)
    table = {"table":[]}
    for s in word_list:
        table["table"].append([s.eng,s.ger,s.sent,s.known,s.correct,s.wrong])
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
    global frame

    if x == "":
        label.configure(text=" {} \n {}".format(w.ger, w.sent))
    elif x  == w.ger:        
        w.set_known()
        run()
    elif x  in w.ger:
        label.configure(text="irregular werb, try again ")
    else:
        label.configure(text="{} \n {}".format(w.ger, w.sent))
        w.set_wrong()

    

def ask_progress():
    global frame,filename, filename_known
    frame.destroy()
    frame = Frame(root)
    set_frame()

    label = Label(frame)
    label.grid(row=0, column = 0, columnspan=10, padx=10, pady=10)
    label.configure( text="Continue from last practice?")
    
    yes_but=ttk.Button(
        frame,
        text='yes',
        command= get_word_list)


    no_but =ttk.Button(
        frame,
        text='no',
        command=get_new_word_list)

    yes_but.grid(column=4,  padx=10, pady=10, row=1)
    no_but.grid(column=5,  padx=10, pady=10,row=1)

    yes_but.focus_set()
    root.bind('<Right>', lambda event=None: no_but.invoke())
    root.bind('<Return>', lambda event=None: yes_but.invoke())
    
def select_file() :
    global frame, label
    frame.destroy()
    frame = Frame(root)
    set_frame()
    
    label = Label(frame)
    label.grid(row=0, column =0, columnspan=10, padx=10, pady=10)

    label.configure(text="Select words to practice")

    buttons = []

    x = 0
    y = 0
    n = 0
    for k,i in files.items():
        print(i)
        i_known = i.replace('.json',"")+"-known.json"
        def set_filename(fname=i,fname_known=i_known):
            global filename,filename_known
            filename = fname
            filename_known = fname_known
            ask_progress()

        buttons.append(Button(frame, text = k, command = set_filename ))
        buttons[n].grid(row = 4+y, column = x+1, padx=10, pady = 10)
        n += 1
        x += 1
        if x > 2:
            x = 0
            y += 1 

    return frame

def set_frame():
    global frame
    frame.grid(column = 0, row=0, padx=10, pady=10)
    for i in range(16):
        frame.columnconfigure(i, {'minsize': 50})
    
# main sequence
w = word()
word_list = []

# create the root window
root = tk.Tk()
root.wm_title('new  practice')
root.geometry('1000x300')
root.resizable(0, 0)

frame = Frame(root)
set_frame()

label = Label(frame)

filename = ""
filename_known = ""
select_file()

# start the app
if __name__ == '__main__':
    root.mainloop()
