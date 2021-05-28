# -*- coding: utf-8 -*-
"""
Created on Sat May  1 22:20:17 2021

@author: pepermatt94
"""

import tkinter as tk
import pandas as pd
from PIL import Image, ImageTk
from tkinter.font import Font
import tkinter.scrolledtext as tkscrolled
import webbrowser
import os
import glob
from tkinter import filedialog
from tkinter.ttk import Progressbar
from tkscrolledframe import ScrolledFrame
from treview import treview
import initizializers as init
import SearchInRepo as search
import ActOnRepo as act
import tkinter.ttk as ttk
import numpy as np
ABOUT = """

This is a proptotype program for library management. 

The author and the developer of the program claims only 
an honest regard on his own for his work and his time. 

Each develop, modification or, even more, saling or 
distribution of this product is free in a 
gentle agreement with the author and the law.

The program is completely open source, 
and the source code of the program can be found on github at page 
https://github.com/peppermatt94/Bibliotkinter .

There is no lucrative or secondary aim in this project, 
but only the hope that the knowledge
of God and the Gospel expands. 

signature of the author:
pepermatt94
pep.94@libero.it .
"""
init.init()

def bar():
    global OpenWindow
    l4=tk.Label(OpenWindow,text='Loading...',fg='white',bg=a)
    lst4=('Calibri (Body)',10)
    l4.config(font=lst4)
    l4.place(x=18,y=210)
    
    import time
    
    r=0
    for i in range(100):
        progress['value']=r
        OpenWindow.update_idletasks()
        time.sleep(0.03)
        r=r+1
    
    OpenWindow.destroy()
    
    Start_init(init.filenameREPO, init.filenameLOAN, init.variableString, init.credentials, REMOTE = init.REMOTE)
    
 
def about():
    aboutWin = tk.Toplevel()
    aboutWin.iconbitmap('Seminario_RM.ico')
    label2 = tk.Label(aboutWin, text = ABOUT).pack()

    

def Start_init(filenameREPO, filenameLOAN, variableString, credentials, REMOTE ="No"): 
    global dataframe
    global dataframeLoan
    global window
   
    
        
    if REMOTE == "Yes":
        if os.path.exist("Z:\\RMbiblio"): os.makedirs("Z:\\RMbiblio")
        Workdir = "Z:\\RMbiblio\\"
    else:
        Workdir = os.getcwd() +"\\"
    if not os.path.exists(Workdir+".setup\\credentials.txt"):  
        init.initializerPWD(credentials,init.initializerREPO, new_win)
    
    #if not os.path.exists(Workdir+".setup\\parameter.txt"):
    #    init.initializerREPO(filenameREPO, filenameLOAN)
    else:
        with open(Workdir+".setup\\parameter.txt", "r") as f:
            files = f.read()
            
            files = files.splitlines()
            if len(files)==1:
                
                
                files[0] = files[0].split(",")
                files = files[0]
            else:
                RepositorySelected = 0
                selector = RepositorySelected
                for i in range(len(files)):
                    
                    files[i]= files[i].split(",")
                    files = files[RepositorySelected]
                    
        init.filenameREPO =  files[0]
        init.filenameLOAN = files[1]
        #New variables
            
        try:
            
            init.dataframe=pd.read_csv(init.filenameREPO, sep = ",", encoding = "latin1")
            init.dataframe = init.dataframe.replace(np.nan, '', regex=True)
            init.dataframe = init.dataframe.astype(str)
            init.dataframeLoan = pd.read_csv(init.filenameLOAN, sep = ",", encoding = "latin1")
            init.dataframeLoan = init.dataframeLoan.replace(np.nan, '', regex=True)
            init.dataframeLoan = init.dataframeLoan.astype(str)  
        except:
            pass

        
        new_win(init.dataframe, init.dataframeLoan, init.filenameREPO, init.credentials, init.variableString, init.window)


    
def new_win(dataframe, dataframeLoan, filenameREPO, credentials, variableString, PrecedentWindow):
    
    global window
    if PrecedentWindow != None:
        PrecedentWindow.destroy()
    window = tk.Tk()
    #New variables
    #breakpoint()
    init.window=window
    for i in dataframe.columns:
        variableString[f"{i}"] = tk.StringVar()
     #user and password variables
    credentials["USER"] = tk.StringVar()
    credentials["PASSWORD"] = tk.StringVar()
    window.title("RMbiblio0.1")
    window.iconbitmap('Seminario_RM.ico')
    #window.geometry("1000x100")
    window.grid_columnconfigure(0,weight=1)
    Volto_di_Cristo= Image.open("Volto.jpg")
    Volto_di_Cristo = ImageTk.PhotoImage(Volto_di_Cristo)
    VoltoImage = tk.Label(image=Volto_di_Cristo).grid(row=0, column=4, columnspan =2, rowspan = 6)
    
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_coordinate = (screen_width/2)-(width_of_window/2)
    y_coordinate = (screen_height/2)-(height_of_window/2)  
    
   #let's make the window responsive
    n_rows =10
    n_columns =6
    for i in range(n_rows):
        window.grid_rowconfigure(i,  weight =1)
        for i in range(n_columns):
            window.grid_columnconfigure(i,  weight =1)
    #requests fields of the GUI
    LabelField={}
    RequestsFields={}
    
    for i in range(len(dataframe.columns)):
        if dataframe.columns[i] != "Available":
            if i < 5:
                LabelField[f"{dataframe.columns[i]}"] = tk.Label(window, text = f"{dataframe.columns[i]}").grid(row=i, column=0) 
                RequestsFields[f"{dataframe.columns[i]}_entry"] = tk.Entry( textvariable = variableString[f"{dataframe.columns[i]}"]).grid(row=i, column=1, sticky = 'WE', padx=10, pady=0)
            if i>4 and i<10:
                LabelField[f"{dataframe.columns[i]}"] = tk.Label(window, text = f"{dataframe.columns[i]}").grid(row=i-5, column=2) 
                RequestsFields[f"{dataframe.columns[i]}_entry"] = tk.Entry( textvariable = variableString[f"{dataframe.columns[i]}"]).grid(row=i-5, column=3, sticky = 'WE', padx=10, pady=0)
    
    
    container = ttk.Frame(window)
    canvas = tk.Canvas(container, width=1200)
    scrollbar = ttk.Scrollbar(container,orient="vertical")#.grid(row=0, column=20, rowspan = 20, sticky=tk.S + tk.E + tk.N)
    scrollbar.config( command = canvas.yview )
    #scrollbar.grid(row=0, column=20, rowspan = 20, sticky=tk.S + tk.E + tk.N)
    
    scrollable_frame = ttk.Frame(canvas)
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
            )
            )   

    canvas.create_window((10, 10), window=scrollable_frame, anchor="nw")

    canvas.configure(yscrollcommand=scrollbar.set)

    #for i in range(50):
    #    tk.Label(scrollable_frame, text="Sample scrolling label").grid(row = i, column=10)
    
    # container.grid(row = 8, column=0)
    # canvas.grid(row = 8, column=0)
    # scrollbar.grid(row=0, column=20, rowspan = 20, sticky=tk.S + tk.E + tk.N)

    
    #button of the gui
    
    searchButton = tk.Button( text = "Search", command=lambda: search.search(dataframe, dataframeLoan, scrollable_frame, container, canvas, scrollbar), height = 2, width = 15).grid(row = 6,column=0)
    Addbutton = tk.Button(text = "Add to repository", command = lambda: init.openPWDrequest(act.add_book, credentials, init.dataframe, dataframeLoan, variableString, filenameREPO), height = 2, width = 15).grid(row=6,column=1)
    exploreButton = tk.Button(text = "Explore Repository", command =lambda : act.explore_repository(init.dataframe, variableString), height = 2, width = 15).grid(row=6,column=2)
    exploreButton = tk.Button(text = "Explore Loan \nRepository", command =lambda: act.explore_loan_repository(init.dataframeLoan, init.StringOfRestitution), height = 2, width = 15).grid(row=6,column=3)
    onlineButton = tk.Button(text = "Search online", command =lambda: search.online_search(variableString), height = 2, width = 15).grid(row=6,column=4)
    #eliminateButton = tk.Button(text = "Delete Book", command = search_book).grid(row=5,column=2)
    #loanButton= tk.Button(text = "Loan", command = search_book).grid(row=6,column=2)
    
    #fileMenu
    
    menu = tk.Menu(window)
    window.config(menu=menu)
    fileMenu = tk.Menu(menu)
    menu.add_cascade(label="File", menu=fileMenu)
    fileMenu.add_command(label="New Repository", command =lambda: init.newRep(init.filenameREPO, init.filenameLOAN, new_win))
    fileMenu.add_command(label = "Open Repository", command = lambda: init.openRep(window, new_win))
    fileMenu.add_command(label = "New Credentials", command = init.newCredential)
    
    editMenu = tk.Menu(menu)
    menu.add_cascade(label="Option", menu=editMenu)
    editMenu.add_command(label="Delete Book", command =lambda: act.eliminateBook(init.dataframe,filenameREPO, variableString))
    editMenu.add_command(label="Loan book",command = lambda: act.loan_id_insert(init.dataframe, init.dataframeLoan, variableString,filenameREPO, init.filenameLOAN))
    editMenu.add_command(label="Restitution", command =lambda: act.restitution_win(dataframeLoan, dataframe, filenameREPO, init.filenameLOAN, init.StringOfRestitution))
    editMenu.add_command(label="Explore repository", command =lambda: act.explore_repository(dataframe, variableString))
    editMenu.add_command(label="Explore loan repository", command =lambda: act.explore_loan_repository(dataframeLoan, variableString))
    
    
    aboutMenu = tk.Menu(menu)
    menu.add_cascade(label="?", menu=aboutMenu)
    aboutMenu.add_command(label = "About", command = about)
    
    
    
    window.mainloop()



#Starting window: 
OpenWindow=tk.Tk()
width_of_window = 427
height_of_window = 250
screen_width = OpenWindow.winfo_screenwidth()
screen_height = OpenWindow.winfo_screenheight()
x_coordinate = (screen_width/2)-(width_of_window/2)
y_coordinate = (screen_height/2)-(height_of_window/2)
OpenWindow.geometry("%dx%d+%d+%d" %(width_of_window,height_of_window,x_coordinate,y_coordinate))
Volto_di_Cristo= Image.open("Seminario_RM.ico")
Volto_di_Cristo = ImageTk.PhotoImage(Volto_di_Cristo)
VoltoImage = tk.Label(OpenWindow,image=Volto_di_Cristo).pack()

OpenWindow.overrideredirect(1)
s = tk.ttk.Style()
s.theme_use('clam')
s.configure("red.Horizontal.TProgressbar", foreground='red', background='#4f4f4f')
progress=Progressbar(OpenWindow,style="red.Horizontal.TProgressbar",orient=tk.HORIZONTAL,length=500,mode='determinate',)

#############progressbar          33333333333333333333333333333

progress.place(x=-10,y=235)

a='#249794'
tk.Frame(OpenWindow,width=427,height=241,bg=a).place(x=0,y=0)  #249794
Start=tk.Button(OpenWindow,width=10,height=1,text='Get Started',command= bar ,border=0,fg=a,bg='white')
Start.place(x=170,y=200)


######## Label

l1=tk.Label(OpenWindow,text='RMbiblio',fg='white',bg=a)
lst1=('Calibri (Body)',18,'bold')
l1.config(font=lst1)
l1.place(x=50,y=80)

l2=tk.Label(OpenWindow,text='0.1',fg='white',bg=a)
lst2=('Calibri (Body)',18)
l2.config(font=lst2)
l2.place(x=155,y=82)

l3=tk.Label(OpenWindow,text='Library de Ciudad de Mexico',fg='white',bg=a)
lst3=('Calibri (Body)',13)
l3.config(font=lst3)
l3.place(x=50,y=110)

OpenWindow.mainloop()
               
