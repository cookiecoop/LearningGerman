import os, sys
import json
import random
from random import seed, choice,randrange
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.messagebox import askyesno

page =sys.argv[1]
colors = ('red', 'yellow', 'green', 'cyan', 'blue', 'magenta')
word_list = []
filename = page+".json"
filename_known = page+"-known.json"


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
    global yes_but
    global no_but
    with open(filename,"r") as f: 
        data = json.load(f)
        for i in data["table"]:
            for k, v in i.items():        
                word_list.append(word(v[1], v[0], v[2], "", 0))

    yes_but.grid_remove()
    no_but.grid_remove()
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

    yes_but.grid_remove()
    no_but.grid_remove()
    run()
                
def run():
    global root
    global w
    i = 0
    
    new_list = list(filter(lambda x :  x.known == "", word_list))
    if len(new_list) > 1:
        i = randrange(1,len(new_list))

    if len(new_list) > 0:
        w = new_list[i]
        label.configure(text=w.eng)
        label.grid(columnspan=10, row=0, padx=10, pady=10)
        
        entry.grid(columnspan=10, row=1, padx=10, pady=10)        
        check.grid(column=5, row=3, padx=10, pady=10)        
        cont.grid(column=6, row=3, padx=10, pady=10)

        root.bind('<Right>', lambda event=None: cont.invoke())
        root.bind('<Left>', lambda event=None: check.invoke())
        root.bind('<Return>', lambda event=None: check.invoke())

        
def end():
    entry.delete(0,'end')
    run()

    
def save_progress():
    global word_list

    table = {"table":[]}
    for s in word_list:
        table["table"].append([s.eng,s.ger,s.sent,s.known,s.correct])
        with open(filename_known, 'w') as outfile:
            json.dump(table, outfile)
    exit()

def exit():
    root.destroy()
def compare():
    global entry
    global label
    global check
    global cont
    global w

    x = entry.get()        
    if x == "":
        label.configure(text="answer is {} \n {}".format(w.ger, w.sent))
    elif x == "exit":
        label.configure(text='Save progress?')
        entry.grid_remove()
        check.grid_remove()
        cont.grid_remove()
        yes_but.grid(column=5,  padx=0, pady=0, row=1)
        no_but.grid(column=6,  padx=0, pady=0,row=1)
        yes_but.configure(command=save_progress)
        no_but.configure(command=exit)
        root.bind('<Right>', lambda event=None: no_but.invoke())
        root.bind('<Left>', lambda event=None: yes_but.invoke())

    elif x  == w.ger:        
        w.set_known()
        end()
    elif x  in w.ger:
        label.configure(text="irregular werb, try again ")
    else:
        label.configure(text="correct answer is {} \n {}".format(w.ger, w.sent))
    
# create the root window
root = tk.Tk()
root.title('Page 1 practice')
root.geometry('1000x300')
root.resizable(0, 0)

entry = Entry(root)
entry.focus_set()
check = ttk.Button(root, text= "Check",width= 20, command=compare)
cont = ttk.Button(root, text= "Continue",width= 20, command= end)

w = word("","","","",0)
#Initialize a Label to display the User Input
label = Label(root, text="", font=("Courier 22 bold"))
label.grid(columnspan=10, row=0, padx=10, pady=10)

label.configure(text="Continue from last practice?")

yes_but=ttk.Button(
    root,
    text='yes',
    command=get_word_list)


no_but =ttk.Button(
    root,
    text='no',
    command=get_new_word_list)
yes_but.grid(column=5,  padx=0, pady=0, row=1)
no_but.grid(column=6,  padx=0, pady=0,row=1)

root.bind('<Right>', lambda event=None: no_but.invoke())
root.bind('<Left>', lambda event=None: yes_but.invoke())


# start the app
root.mainloop()
