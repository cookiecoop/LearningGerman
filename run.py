import os, sys
import json
import random
from random import seed, choice,randrange
import tkinter as tk
from tkinter import ttk
from tkinter import *

import customtkinter as ctk

from pathlib import Path
from functools import partial, reduce

class tk:
    """
    Define the main frame and files
    """
    def __init__(self, file_names):
        self.root = ctk.CTk(fg_color=("midnight blue"," midnight blue"))
        self.root.wm_title("Learning German new practice")
        self.root.geometry('650x700')
        self.root.resizable(0, 0)

        # create a dummy global frame and label
        self.frame = ctk.CTkFrame(self.root, bg_color=("midnight blue","dark-blue"))
        self.label = ctk.CTkLabel(self.frame)

        #current word and word lists
        self.word = None
        self.tfiles = tfiles(file_names)

        #setup progress bar
        self.pb = ctk.CTkProgressBar(self.root, width= 600)
        self.pb.set(self.get_progress())
        self.pb.grid(column=0, row=0, padx=10, pady=20)

    def get_progress(self):
        
        count = reduce(lambda x, y: x+y, [len(l) for l in self.tfiles.word_lists.values()], 0 )
        count_progress = reduce(lambda x, y: x+y, [len(l) for l in self.tfiles.known_lists.values()], 0 )
        
        return count_progress/count

class tfiles:
    """
    Define files and keep track of progres
    """
    def __init__(self, file_names):
        self.file_names = file_names
        self.files = {f: resource_path(f+".json") for f in file_names}
        self.files_known = {f: resource_path(f+"-known.json") for f in file_names}
        self.word_lists = {f: self.get_words(f) for f in file_names}
        self.known_lists = self.get_known_words(self.word_lists)

        self.files_progress = {f: int(len(self.known_lists[f])*100/len(self.word_lists[f])) for f in file_names}

        self.filename = file_names[0]

    def get_words(self, f, new_list=False):
        word_list = []
        if new_list or not os.path.exists(self.files_known[f]):
            with open(self.files[f],"r") as fl:
                data = json.load(fl)
                for i in data["table"]:
                    for k, v in i.items():
                        if len(v) > 3:
                            word_list.append(word(v[1], v[0], v[2], v[3],""))
                        else:
                            word_list.append(word(v[1], v[0], v[2], "",""))
        else:
            with open(self.files_known[f],"r") as fl:
                data = json.load(fl)
                for v in  data["table"]:
                    word_list.append(word(v[0], v[1], v[2], v[3], v[4],v[5],v[6]))
        return word_list

    def get_known_words(self, adict):
        return {k: list(filter(lambda x :  x.known == True, v)) for k,v in adict.items()}

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



        
def select_file(mtk):

    mtk.root.wm_title("Learning German new practice")

    set_frame(mtk)
    mtk.label = ctk.CTkLabel(mtk.frame, width=120,
                               height=25,
                               fg_color=("white", "gray75"),
                               corner_radius=8)
    mtk.label.grid(row=0, column =0, sticky="ew",columnspan=2, padx=10, pady=10)
    mtk.label.configure(text='Select word list to practice')

    # set the buttons for selecting word list
    buttons = []
    
    mtk.frame.columnconfigure(0, {'minsize': 310})
    mtk.frame.columnconfigure(1, {'minsize': 310})

    x = 0
    y = 0
    n = 0
    for i in mtk.tfiles.file_names:

        i_known = i
        i_progress = mtk.tfiles.files_progress[i]

        def set_filename(fname=i,title=i):

            mtk.tfiles.filename = fname
            mtk.root.wm_title(title)
            ask_progress(mtk)

        buttons.append(ctk.CTkButton(mtk.frame, text = "{}  ({}%)".format(i,str(i_progress)), hover_color="white",  command = set_filename ))
        buttons[n].grid(row = 4+y, column = x,sticky="ew", padx=10, pady = 10)

        n += 1
        x += 1
        if x > 1:
            x = 0
            y += 1
    
    exit_but=ctk.CTkButton(
        mtk.frame,
        text='Exit',
        command= lambda: exit(mtk))
    exit_but.grid(column=0, columnspan=2,   sticky ="ew",padx=10, pady=10,row=4+y)



def ask_progress(mtk):

    set_frame(mtk)    
    mtk.label = ctk.CTkLabel(mtk.frame, width=600,
                               height=25,
                               fg_color=("white", "gray75"),
                               corner_radius=8)
    mtk.label.grid(row=0, column = 0, sticky ="ew", columnspan=4, padx=10, pady=10)
    mtk.label.configure( text="Continue from last practice?")
    
    yes_but=ctk.CTkButton(
        mtk.frame,
        text='yes',
        command= lambda: get_word_list(mtk))


    no_but =ctk.CTkButton(
        mtk.frame,
        text='no',
        command= lambda: get_new_word_list(mtk))

    yes_but.grid(column=1,   sticky ="ew",padx=10, pady=10, row=1)
    no_but.grid(column=2,   sticky ="ew",padx=10, pady=10,row=1)

def get_new_word_list(mtk):

    mtk.tfiles.word_lists[mtk.tfiles.filename] = mtk.tfiles.get_words(mtk.tfiles.filename, True)
    run(mtk)
def get_word_list(mtk):
    run(mtk)

def run(mtk):
    set_frame(mtk)

    label = ctk.CTkLabel(mtk.frame)
    label.grid(row=0, column =0, columnspan=5, padx=10, pady=10)

    entry = ctk.CTkEntry(mtk.frame,width=250)
    entry.focus_set()
    x = entry.get()        
    i = 0
    new_list = list(filter(lambda x :  x.known == "", mtk.tfiles.word_lists[mtk.tfiles.filename]))

    if len(new_list) > 1:
        i = randrange(1,len(new_list))

    if len(new_list) > 0:
        mtk.word = new_list[i]
        label.configure(text=mtk.word.eng)
        print(mtk.word.eng, mtk.word.known, mtk.word.correct, mtk.word.wrong)
        
        check = ctk.CTkButton(mtk.frame, text= "Check",width= 100, command=lambda : compare(None,entry.get(),label, mtk ))
        cont = ctk.CTkButton(mtk.frame, text= "Continue",width= 100,  command=lambda: run(mtk))
        done = ctk.CTkButton(mtk.frame, text= "Exit",width= 100,  command=lambda: ask_save(mtk))
        example = ctk.CTkButton(mtk.frame, text= "Example",width= 100, command=lambda : get_sentence(None,entry,label, mtk ))
        
        entry.grid(column=0,columnspan=5, row=3, padx=10, pady=10)
        check.grid(column=1, row=4, padx=10, pady=10)
        example.grid(column=2, row=4, padx=10, pady=10)
        cont.grid(column=3, row=4, padx=10, pady=10)
        done.grid(column=4, row=4, padx=10, pady=10)

    else:
        ask_save(mtk, "Well done, all words in the list learned!")
        
def compare(event=None, x=None,label=None, mtk=None):

    print(mtk.word.ger, mtk.word.ger.lower().translate(special_char_map).replace(" ",""))
    if x == "":
        label.configure(text=" {}".format(mtk.word.ger))
    elif x.replace(" ","").lower()  == mtk.word.ger.replace(" ","").lower():
        mtk.word.set_known()
        if(mtk.word.known == "True"):
            mtk.pb.set(mtk.pb.get()+progress)
        print( mtk.pb.get())
        run(mtk)
    elif x.lower()  in mtk.word.ger.lower():
        if "/" in mtk.word.ger.lower():
            label.configure(text="There are alternatives, try again")
        elif "," in mtk.word.ger.lower():
            label.configure(text="Irregular verb, try again")
        elif "der " in mtk.word.ger.lower() or "das " in mtk.word.ger.lower() or "die " in mtk.word.ger.lower():
            label.configure(text="missing definite artikel")
        else:
            label.configure(text="Almost there, try again")
    elif x.lower().translate(special_char_map).replace(" ","") ==  mtk.word.ger.lower().translate(special_char_map).replace(" ",""):
        label.configure(text="Missing or extra umlaut, try again")
    else:
        label.configure(text="{}".format(mtk.word.ger))
        mtk.word.set_wrong()

def get_sentence(event=None, entry=None,label=None, mtk=None):

    entry.delete(0,END)
    x = entry.get()

    sent = mtk.word.sent
    if mtk.word.word != "":
        sent = mtk.word.sent.replace(mtk.word.word, "__________")
   
    label.configure(text="{} ({})".format(sent, mtk.word.eng))

    check = ctk.CTkButton(mtk.frame, text= "Check",width= 100, command=lambda : compare2(None,entry.get(), label ))

def compare2(event=None, x=None,label=None, mtk=None):

    if x.replace(" ","").lower()  == mtk.word.replace(" ","").lower():
        label.configure(text=mtk.word.sent, text_color=("midnight blue","dark-blue"))
    elif x.lower()  in mtk.word.word.lower():
        label.configure(text="Almost there, try again")
    elif x.lower().translate(special_char_map).replace(" ","") ==  mtk.word.word.lower().translate(special_char_map).replace(" ",""):
        label.configure(text="Missing an umlaut probably, try again")
    else:
        label.configure(text=mtk.word.sent, text_color=("red","red"))
    

def ask_save(mtk, mes=""):
    set_frame(mtk)

    mtk.label = ctk.CTkLabel(mtk.frame, width=100,
                               fg_color=("white", "gray75"),
                               corner_radius=8)
    mtk.label.grid(row=0, column = 0, sticky ="ew", columnspan=5, padx=10, pady=10)
    mtk.label.configure(text=mes+ " Save progress?")
    
    yes_but=ctk.CTkButton(
        mtk.frame,
        text='yes',
        command=lambda: save_progress(mtk))


    no_but =ctk.CTkButton(
        mtk.frame,
        text='no',
        command=lambda: exit(mtk))

    yes_but.grid(column=1,   sticky ="ew",padx=10, pady=10, row=1)
    no_but.grid(column=3,   sticky ="ew",padx=10, pady=10,row=1)
    
def save_progress(mtk):

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
        

    table = {"table":[]}
    for s in mtk.tfiles.word_lists[mtk.tfiles.filename]:
        table["table"].append([s.eng,s.ger,s.sent,s.word,s.known,s.correct,s.wrong])
        with open(mtk.tfiles.files_known[mtk.tfiles.filename], 'w') as outfile:
            json.dump(table, outfile)
    ask_new_practice(mtk)

def ask_new_practice(mtk):
    set_frame(mtk)

    mtk.label = ctk.CTkLabel(mtk.frame, width=100,
                               fg_color=("white", "gray75"),
                               corner_radius=8)
    mtk.label.grid(row=0, column = 0, sticky ="ew", columnspan=5, padx=10, pady=10)
    mtk.label.configure(text="Try another word list?")
    
    yes_but=ctk.CTkButton(
        mtk.frame,
        text='yes',
        command=lambda: select_file(mtk))


    no_but =ctk.CTkButton(
        mtk.frame,
        text='no',
        command=lambda: exit(mtk))

    yes_but.grid(column=1,   sticky ="ew",padx=10, pady=10, row=1)
    no_but.grid(column=3,   sticky ="ew",padx=10, pady=10,row=1)

def exit(mtk):
    mtk.frame.destroy()
    mtk.root.destroy()

def set_frame(mtk):
    mtk.frame.destroy()
    mtk.frame = ctk.CTkFrame(mtk.root, width=630, height=620, bg_color=("midnight blue","dark-blue"))
    mtk.frame.grid(column = 0, row=1, padx=10, pady=10)

    for i in range(6):
        mtk.frame.columnconfigure(i, {'minsize': 100})
    mtk.frame.grid_propagate(0)
    
def welcome(mtk):

    set_frame(mtk)
    
    mtk.label = ctk.CTkLabel(mtk.frame, width=600,
                               #height=325,
                               fg_color=("white", "gray75"),
                               corner_radius=8,
                               justify="left",
                               wraplength=550)
    mtk.label.grid(row=0, column = 0, sticky ="ew", columnspan=4, padx=10, pady=10)
    mtk.label.configure( text="\n If you have issues clicking a button, click on the title bar first (https://github.com/python/cpython/issues/110218). \n Start by selecting a word list to practice. \n Select if you want to start a new practice or continue from where you left. In case this is your first practice, it doesn't matter what you select here.  \n Type your answer and check. Sometimes there will be alternative answers. They are seperated by '/'. For some verb, you are asked to give past and perfect versions seperated by a comma. \n You can use Example button to see an example sentence in German. Sometimes the word you are practicing will be blank. In that case, type the missing word and check your answer. For seperable German words, this might be second part of the word only. \n  You will have a chance to save your progress before closing the program. \n")
    
    label2 = ctk.CTkLabel(mtk.frame, width=600,
                               #height=225,
                               fg_color=("white", "gray75"),
                               corner_radius=8,
                               justify="left",
                               wraplength=550)
    label2.grid(row=1, column = 0, sticky ="ew", columnspan=4, padx=10, pady=10)
    label2.configure( text="\n Learning measure: \n To mark a word as learned, you need to have at least two correct answers and answer correctly more than incorrectly. If you answer incorrectly for 5 times, you need to answer 6 times correctly before the word is marked as 'learned'. Answers to example sentences do not count neither as correct nor as wrong. They are only meant to give context.\n \n Top progress bar shows your progress in all practices. Once you start a new practice, it will show the progress in current practice. \n")

    exit_but=ctk.CTkButton(
        mtk.frame,
        text='Exit',
        command= lambda: exit(mtk))


    practice_but =ctk.CTkButton(
        mtk.frame,
        text='Select word list to practice',
        command=lambda: select_file(mtk))

    practice_but.grid(column=1,   sticky ="ew",padx=10, pady=10, row=2)
    exit_but.grid(column=2,   sticky ="ew",padx=10, pady=10,row=2)

def instructions(mtk):

    set_frame(mtk)
    
    mtk.label = ctk.CTkLabel(mtk.frame, width=600,
                               #height=325,
                               fg_color=("white", "gray75"),
                               corner_radius=8,
                               justify="left",
                               wraplength=550)
    mtk.label.grid(row=0, column = 0, sticky ="ew", columnspan=4, padx=10, pady=10)
    mtk.label.configure( text="\n If you have issues clicking a button, click on the title bar first (https://github.com/python/cpython/issues/110218). \n Start by selecting a word list to practice. \n Select if you want to start a new practice or continue from where you left. In case this is your first practice, it doesn't matter what you select here.  \n Type your answer and check. Sometimes there will be alternative answers. They are seperated by '/'. For some verb, you are asked to give past and perfect versions seperated by a comma. \n You can use Example button to see an example sentence in German. Sometimes the word you are practicing will be blank. In that case, type the missing word and check your answer. For seperable German words, this might be second part of the word only. \n  You will have a chance to save your progress before closing the program. \n You can discover the shortcuts on your own.")
    
    label2 = ctk.CTkLabel(mtk.frame, width=600,
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
        command= lambda: exit(mtk))


    practice_but =ctk.CTkButton(
        mtk.frame,
        text='Select word list to practice',
        command=lambda: select_file(mtk))

    practice_but.grid(column=1,   sticky ="ew",padx=10, pady=10, row=2)
    exit_but.grid(column=2,   sticky ="ew",padx=10, pady=10,row=2)

# start the app
if __name__ == '__main__':
    
    # available files to practice
    file_names = ["Die90haeufigstenVerbenA1",
              "VerbenNiveauA2-B1",
              "SportundFreizeit",
              "HaeufigkeitundReihenfolge",
              "KoerperlicheTaetigkeiten",
              "AeusseresErscheinungsbild",
              "CharakterAndTemperament",
              "Zeitangaben"
              ]
    # create the root window
    mtk = tk(file_names)
    
    #setup files
    welcome(mtk)

    # start the loop
    mtk.root.mainloop()
