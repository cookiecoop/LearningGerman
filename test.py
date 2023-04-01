import os, sys
import json
import random
from random import seed, choice,randrange
import tkinter as tk
from tkinter import ttk
from tkinter import *
from pathlib import Path


class word:
    def __init__(self, eng, ger, sent, known, correct):
        self.eng = eng
        self.ger = ger.replace(" ","")
        self.sent = sent
        self.known = known
        self.correct = correct
    def set_known(self):
        self.correct += 1
        if self.correct > 1:
            self.known = "True"

    
def get_new_word_list():
    print("selected no")
    global filename    
    with open(filename,"r") as f: 
        data = json.load(f)
        for i in data["table"]:
            for k, v in i.items():        
                word_list.append(word(v[1], v[0], v[2], "", 0))

    run()
def get_word_list():
    global filename
    global filename_known
    if not os.path.exists(filename_known):
        print("no progress found, start with full list")
        with open(filename,"r") as f: 
            data = json.load(f)
            for i in data["table"]:
                for k, v in i.items():        
                    word_list.append(word(v[1], v[0], v[2], "", 0))
    else:
        with open(filename_known,"r") as f: 
            data = json.load(f)
            for v in data["table"]:
                word_list.append(word(v[0], v[1], v[2], v[3], v[4]))


    run()

    
def run():
    global root
    global w
    global frame

    frame.destroy()
    frame = Frame(root)
    frame.grid(column = 0, columnspan=10, row=0, padx=10, pady=10)
    
    label = Label(frame, text="Continue from last practice?")
    label.grid(column = 0, columnspan=10, row=0, padx=10, pady=10)

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
        print(w.eng)
        
        check = ttk.Button(frame, text= "Check",width= 20, command=lambda : compare(None,entry.get() ))
        cont = ttk.Button(frame, text= "Continue",width= 20, command= end)    

        entry.grid(column=3,columnspan=10, row=3, padx=10, pady=10)        
        check.grid(column=7, row=4, padx=10, pady=10)        
        cont.grid(column=8, row=4, padx=10, pady=10)

        root.bind('<Right>', lambda event=None: cont.invoke())
        root.bind('<Left>', lambda event=None: check.invoke())
        root.bind('<Return>', lambda event=None: check.invoke())
        
        
def end():
    run()

    
def save_progress():
    global word_list
    global filename_known
    table = {"table":[]}
    for s in word_list:
        table["table"].append([s.eng,s.ger,s.sent,s.known,s.correct])
        with open(filename_known, 'w') as outfile:
            json.dump(table, outfile)
    exit()

def exit():
    global root
    global frame
    frame.destroy()
    root.destroy()
    
def compare(event=None, x=None):
    global w
    global frame

    label = Label(frame)
    label.grid(column = 0, columnspan=10, row=0, padx=10, pady=10)

    if x == "":
        label.configure(text="answer is {} \n {}".format(w.ger, w.sent))
    elif x == "exit":
        frame.destroy()
        frame = Frame(root)
        frame.grid(column = 0, columnspan=10, row=0, padx=10, pady=10)

        label = Label(frame)
        label.grid(column = 0, columnspan=10, row=0, padx=10, pady=10)
        
        label.configure(text="Save progress?")
        yes_but=ttk.Button(
            frame,
            text='yes',
            command=save_progress)


        no_but =ttk.Button(
            frame,
            text='no',
            command=exit)
        

        yes_but.grid(column=7,  padx=0, pady=0, row=1)
        no_but.grid(column=8,  padx=0, pady=0,row=1)
        root.bind('<Right>', lambda event=None: no_but.invoke())
        root.bind('<Left>', lambda event=None: yes_but.invoke())

    elif x  == w.ger:        
        w.set_known()
        end()
    elif x  in w.ger:
        label = Label(frame)
        label.grid(column = 0, columnspan=10, row=0, padx=10, pady=10)
        label.configure(text="irregular werb, try again ")
    else:
        label.configure(text="{} \n {}".format(w.ger, w.sent))
    

def set_filename(event=None, file=None):
    global filename
    global filename_known
    filename = file
    filename_known = filename.replace('.json',"")+"-known.json"

    print(filename, filename_known)
    ask_progress()
    

def ask_progress():
    global frame
    frame.destroy()
    frame = Frame(root)
    label = Label(frame)
    label.configure( text="Continue from last practice?")

    frame.grid(column = 0, columnspan=10, row=0, padx=10, pady=10)
    label.grid(column = 0, columnspan=10, row=0, padx=10, pady=10)
    
    yes_but=ttk.Button(
        frame,
        text='yes',
        command=get_word_list)


    no_but =ttk.Button(
        frame,
        text='no',
        command=get_new_word_list)

    yes_but.grid(column=7,  padx=0, pady=0, row=1)
    no_but.grid(column=8,  padx=0, pady=0,row=1)
    
    root.bind('<Right>', lambda event=None: no_but.invoke())
    root.bind('<Left>', lambda event=None: yes_but.invoke())
    
def select_file() :
    global frame, label
    frame.destroy()
    frame = Frame(root)

    label = Label(frame)
    label.grid(column = 0, columnspan=10, row=0, padx=10, pady=10)
    
    label.configure(text="Select words to practice")
    frame.grid(column = 0, columnspan=10, row=0, padx=10, pady=10)
    label.grid(column = 0, columnspan=10, row=0, padx=10, pady=10)

    files = []
    buttons = []
    for file in os.listdir("."):
        if ".json" in file and "known" not in file:
            files.append( file)
            buttons.append(0)

    print(files)
    n = 0
    for i in files:        
        buttons[n]= Button(frame, text = i, command = lambda: set_filename(None, i))
        buttons[n].grid(row = 4, column = n, sticky = W, pady = 4)
        n += 1

    return frame


# main sequence
w = word("","","","",0)
word_list = []

# create the root window
root = tk.Tk()
root.wm_title('new  practice')
root.geometry('1000x300')
root.resizable(0, 0)

frame = Frame(root)
frame.grid(column = 0, columnspan=10, row=0, padx=10, pady=10)

label = Label(frame, text="Welcome")
label.grid(column = 0, columnspan=10, row=0, padx=10, pady=10)

select_file()

# start the app
root.mainloop()

