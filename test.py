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

class word:
    """
    This defines the class to use for the words to practice
    eng: english word
    ger: german word
    sent: An example sentence in german
    word: the word in german used in the example sentence (it could be part of the original word for seperable german words)
    known: status of learning. True if correctly answered at least twice and more often correct than wrong.
    correct: number of correct answers
    wrong: number of wrong answers
    """
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
        if self.correct > self.wrong and self.correct > 1:
            self.known = "True"
    def set_wrong(self):
        self.wrong += 1

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


# create a global word (english,german,example sentence in german)
w = word()
# create an empty word list, it will be filled when a practice is selected
word_list = []
    
file_names = ["Die90haeufigstenVerbenA1",
              "VerbenNiveauA2-B1",
              "SportundFreizeit",
              "HaeufigkeitundReihenfolge",
              "KoerperlicheTaetigkeiten",
              "AeusseresErscheinungsbild",
              "CharakterAndTemperament",
              "Zeitangaben"
              ]

files = {}
files_known = {}
files_progress = {}
count_progress=0
count=0
word_lists ={}
known_lists = {}

def get_progress():
    global file_names, files, files_known, files_progress
    global count, count_progress
    for f in file_names:
        files[f] = resource_path(f+".json")
        files_known[f] = resource_path(f+"-known.json")
        word_lists[f]= []
        known_lists[f]= []

        if not os.path.exists(files_known[f]):
            with open(files[f],"r") as fl:
                data = json.load(fl)
                for i in data["table"]:
                    for k, v in i.items():
                        if len(v) > 3:
                            word_lists[f].append(word(v[1], v[0], v[2], v[3],""))
                        else:
                            word_lists[f].append(word(v[1], v[0], v[2], "",""))
        else:
            with open(files_known[f],"r") as fl:
                data = json.load(fl)
                for v in  data["table"]:
                    word_lists[f].append(word(v[0], v[1], v[2], v[3], v[4],v[5],v[6]))
    
        known_lists[f] = list(filter(lambda x :  x.known == "True", word_lists[f]))
        progress = 1./len(word_lists[f])
        files_progress[f]= int(len(known_lists[f])*progress*100)
        print(f,files_progress[f])
        count += len(word_lists[f])
        count_progress += len(known_lists[f])
        
        print("count ",count_progress/count)
        
def select_file() :
    global frame, label,root
    root.wm_title("Learning German new practice")
    get_progress()
    set_frame()
    label = ctk.CTkLabel(frame, width=120,
                               height=25,
                               fg_color=("white", "gray75"),
                               corner_radius=8)
    label.grid(row=0, column =0, sticky="ew",columnspan=2, padx=10, pady=10)
    label.configure(text="Select word list to practice")

    # set the buttons for selecting word list
    buttons = []
    
    frame.columnconfigure(0, {'minsize': 310})
    frame.columnconfigure(1, {'minsize': 310})

    x = 0
    y = 0
    n = 0
    for k,i in files.items():
        print(k,i)
        i_known = files_known[k]
        i_progress = files_progress[k]
        print(k, i_progress)
        def set_filename(fname=i,fname_known=i_known,title=k, p= i_progress):
            global filename,filename_known
            filename = fname
            filename_known = fname_known
            root.wm_title(title)
            ask_progress()

        buttons.append(ctk.CTkButton(frame, text = "{}  ({}%)".format(k,str(i_progress)), command = set_filename ))
        buttons[n].grid(row = 4+y, column = x,sticky="ew", padx=10, pady = 10)
        n += 1
        x += 1
        if x > 1:
            x = 0
            y += 1

    return frame
    
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

def get_new_word_list():
    global filename, filename_known
    global pb,progress
    print("selected no, open ",filename)

    with open(filename,"r") as f: 
        data = json.load(f)
        for i in data["table"]:
            for k, v in i.items():        
                if len(v) > 3:
                    word_list.append(word(v[1], v[0], v[2], v[3],"", 0,0))
                else:
                    word_list.append(word(v[1], v[0], v[2], "","", 0,0))

    known_list = list(filter(lambda x :  x.known == "True", word_list))
    progress = 1./len(word_list)
    pb.set(len(known_list)*progress )
    print(len(known_list), len(word_list), progress)
    print( pb.get())

    run()
def get_word_list():
    global filename, filename_known
    global pb,progress
    print(filename,filename_known)
    if not os.path.exists(filename_known):
        print("no progress found, start with full list")
        get_new_word_list()
    else:
        with open(filename_known,"r") as f: 
            data = json.load(f)
            for v in data["table"]:
                word_list.append(word(v[0], v[1], v[2], v[3], v[4],v[5],v[6]))

    known_list = list(filter(lambda x :  x.known == "True", word_list))
    progress = 1./len(word_list)
    pb.set(len(known_list)*progress )
    print(len(known_list), len(word_list), progress)
    print( pb.get())
    run()

def run():
    global root
    global w
    global frame
    global pb, progress
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
        ask_save("Well done, all words in the list learned!")
        
def compare(event=None, x=None,label=None):
    global w, pb,progress
    
    print(w.ger, w.ger.lower().translate(special_char_map).replace(" ",""))
    if x == "":
        label.configure(text=" {}".format(w.ger))
    elif x.replace(" ","").lower()  == w.ger.replace(" ","").lower():
        w.set_known()
        if(w.known == "True"):
            pb.set(pb.get()+progress)
        print( pb.get())
        run()
    elif x.lower()  in w.ger.lower():
        if "/" in w.ger.lower():
            label.configure(text="There are alternatives, try again")
        elif "," in w.ger.lower():
            label.configure(text="Irregular verb, try again")
        else:
            label.configure(text="Almost there, try again")
    elif x.lower().translate(special_char_map).replace(" ","") ==  w.ger.lower().translate(special_char_map).replace(" ",""):
        label.configure(text="Missing or extra umlaut, try again")
    else:
        label.configure(text="{}".format(w.ger))
        w.set_wrong()

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
    

def ask_save(mes=""):
    global frame
    set_frame()

    label = ctk.CTkLabel(frame, width=100,
                               fg_color=("white", "gray75"),
                               corner_radius=8)
    label.grid(row=0, column = 0, sticky ="ew", columnspan=5, padx=10, pady=10)
    label.configure(text=mes+ " Save progress?")
    
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
    root.bind('<Returb>', lambda event=None: yes_but.invoke())
    
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
    ask_new_practice()

def ask_new_practice():
    global frame
    set_frame()

    label = ctk.CTkLabel(frame, width=100,
                               fg_color=("white", "gray75"),
                               corner_radius=8)
    label.grid(row=0, column = 0, sticky ="ew", columnspan=5, padx=10, pady=10)
    label.configure(text="Try another word list?")
    
    yes_but=ctk.CTkButton(
        frame,
        text='yes',
        command=select_file)


    no_but =ctk.CTkButton(
        frame,
        text='no',
        command=exit)

    yes_but.grid(column=1,   sticky ="ew",padx=10, pady=10, row=1)
    no_but.grid(column=3,   sticky ="ew",padx=10, pady=10,row=1)

    yes_but.focus_set()
    root.bind('<Right>', lambda event=None: no_but.invoke())
    root.bind('<Return>', lambda event=None: yes_but.invoke())

def exit():
    global root
    global frame
    frame.destroy()
    root.destroy()

def set_frame():
    global frame
    frame.destroy()
    frame = ctk.CTkFrame(root, width=630, height=620, bg_color=("midnight blue","dark-blue"))
    frame.grid(column = 0, row=1, padx=10, pady=10)
    #frame.grid(sticky='wse')
    for i in range(6):
        frame.columnconfigure(i, {'minsize': 100})
    frame.grid_propagate(0)
    #frame.grid(sticky='nswe')
    

def welcome():
    global frame,filename, filename_known

    set_frame()
    
    label = ctk.CTkLabel(frame, width=600,
                               height=25,
                               fg_color=("white", "gray75"),
                               corner_radius=8)
    label.grid(row=0, column = 0, sticky ="ew", columnspan=4, padx=10, pady=10)
    label.configure( text="Welcome to learning german practice.")
    
    info_but=ctk.CTkButton(
        frame,
        text='See instructions',
        command=instructions)


    practice_but =ctk.CTkButton(
        frame,
        text='Select words to practice',
        command=select_file)

    practice_but.grid(column=1,   sticky ="ew",padx=10, pady=10, row=1)
    info_but.grid(column=2,   sticky ="ew",padx=10, pady=10,row=1)

    practice_but.focus_set()
    root.bind('<Right>', lambda event=None: info_but.invoke())
    root.bind('<Return>', lambda event=None: practice_but.invoke())

def instructions():
    global frame,filename, filename_known

    set_frame()
    
    label = ctk.CTkLabel(frame, width=600,
                               #height=325,
                               fg_color=("white", "gray75"),
                               corner_radius=8,
                               justify="left",
                               wraplength=550)
    label.grid(row=0, column = 0, sticky ="ew", columnspan=4, padx=10, pady=10)
    label.configure( text="\n Start by selecting a word list to practice. \n Select if you want to start a new practice or continue from where you left. In case this is your first practice, it doesn't matter what you select here.  \n Type your answer and check. Pressing enter will check your answer.  \n Sometimes there will be alternative answers. They are seperated by '/'. For some verb, you are asked to give past and perfect versions seperated by a comma. \n You can use Example button (or shift-enter) to see an example sentence in German. Sometimes the word you are practicing will be blank. In that case, type the missing word and check your answer. For seperable German words, this might be second part of the word only. \n Use Continue button to go to next word. You can use Right arrow for this. \n Use Exit to end your practice. You will have a chance to save your progress before closing the program.\n")
    
    label2 = ctk.CTkLabel(frame, width=600,
                               #height=225,
                               fg_color=("white", "gray75"),
                               corner_radius=8,
                               justify="left",
                               wraplength=550)
    label2.grid(row=1, column = 0, sticky ="ew", columnspan=4, padx=10, pady=10)
    label2.configure( text="\n Learning measure: \n To mark a word as learned, you need to have at least two correct answers and answer correctly more than incorrectly. If you answer incorrectly for 5 times, you need to answer 6 times correctly before the word is marked as 'learned'. Answers to example sentences do not count neither as correct nor as wrong. They are only meant to give context.\n \n Top progress bar shows your progress in all practices. Once you start a new practice, it will show the progress in current practice. \n")
    
    exit_but=ctk.CTkButton(
        frame,
        text='Exit',
        command= exit)


    practice_but =ctk.CTkButton(
        frame,
        text='Select words to practice',
        command=select_file)

    practice_but.grid(column=1,   sticky ="ew",padx=10, pady=10, row=2)
    exit_but.grid(column=2,   sticky ="ew",padx=10, pady=10,row=2)

    practice_but.focus_set()
    root.bind('<Right>', lambda event=None: exit_but.invoke())
    root.bind('<Return>', lambda event=None: practice_but.invoke())

# start the app
if __name__ == '__main__':
    
    # create the root window
    root = ctk.CTk(fg_color=("midnight blue"," midnight blue"))
    root.wm_title("Learning German new practice")

    root.geometry('650x700')
    root.resizable(0, 0)
    
    # create a dummy global frame and label, they will be recreated with every change
    frame = ctk.CTkFrame(root, bg_color=("midnight blue","dark-blue"))
    set_frame()
    label = ctk.CTkLabel(frame)
    
    pb = ctk.CTkProgressBar(root, width= 600)
    get_progress()
    pb.set(count_progress/count)
    pb.grid(column=0, row=0, padx=10, pady=20)
    progress = 0
    
    # The files to be used are selected when practice is chosen, file names are global
    filename = ""
    filename_known = ""
    welcome()

    # start the loop
    root.mainloop()
