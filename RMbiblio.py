# -*- coding: utf-8 -*-
"""
Created on Sat May  1 22:20:17 2021

@author: pepermatt94
"""

import tkinter as tk
import pandas as pd
from PIL import Image, ImageTk
from tkinter.font import Font
from tabulate import tabulate
import tkinter.scrolledtext as tkscrolled
import webbrowser
import io
from time import sleep
import os
import glob
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from tkinter import filedialog
from tkinter.ttk import Progressbar

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


def about():
    aboutWin = tk.Toplevel()
    aboutWin.iconbitmap('Seminario_RM.ico')
    label2 = tk.Label(aboutWin, text = ABOUT).pack()

def initializerPWD():
    global tip
    global dataframe
    global dataframeLoan  
    global window
    global Title
    global Author
    global Year
    global Editorial
    global Position
    global filenameREPO
    global filenameLOAN 
    global USER
    global PASSWORD 
    global RepositorySelected
    tip =False
    initializeWin = tk.Toplevel()
    initializeWin.attributes("-topmost", True)
    initializeWin.title("Create an Administrator account")
    #initializeWin.geometry("200x200")
    access = tk.Label(initializeWin, text = "Insert username and password").grid(row=0, column=1,sticky = "WE", padx=10, pady=10)
    user = tk.Label(initializeWin, text = "username").grid(row=1, column=0,sticky = "WE", padx=10)
    get_user = tk.Entry(initializeWin, textvariable = USER).grid(row=1, column=1, sticky = "WE", padx=10)
    pwd = tk.Label(initializeWin, text = "password").grid(row=2, column=0, padx=10)
    get_pwd = tk.Entry(initializeWin, textvariable = PASSWORD, show = "*").grid(row=2, column=1, sticky = "WE", padx=10)
    account = tk.Button(initializeWin, text = "create account", command =lambda: createAccount(USER,PASSWORD, initializeWin)).grid(row=3,column=2, padx=10, pady = 10)
 


def add_repository(win , NameRP, nameln):
    global dataframe
    global dataframeLoan  
    global window
    global Title
    global Author
    global Year
    global Editorial
    global Position
    global filenameREPO
    global filenameLOAN 
    global USER
    global PASSWORD 
    global RepositorySelected
    name=NameRP.get()
    nameLN = nameln.get()
    filenameREPO = os.getcwd() + "\\" + name + ".txt"
    filenameLOAN = os.getcwd() + "\\" + nameLN + ".txt"
    
    NameRP.set("")
    nameln.set("")
    
    if name=="" or nameLN =="":
        warn = tk.Toplevel()
        warn.title("WARNING")
        warn.iconbitmap('warn.ico')
        warn.geometry("300x100")
        label = tk.Label(warn, text="You must fullfilled both the fields \n for book and loan").pack()
        ok = tk.Button(warn, text = "ok", command = warn.destroy).pack()
        return None
    else:
        with open(filenameREPO, "w") as f:
            header = {"Title": [], "Author": [], "Position" : [], "Editorial" : [], "Year": [], "Available": []}
            header = pd.DataFrame(header)
            header.to_csv(f, sep = "\t", index = False) 
            
        with open(filenameLOAN, "w") as f:
            header = {"Keeper": [], "Adress": [], "Title": [], "Author": [], "Position" : [], "Editorial" : [], "Year": []}
            header = pd.DataFrame(header)
            header.to_csv(f, sep="\t", index = False) 
        with open("parameter.txt", "a") as f:
            f.write(filenameREPO + "," +filenameLOAN +"\n")
        
        try:
            dataframe=pd.read_csv(filenameREPO, sep = "\t",encoding = "latin1")     
            dataframe = dataframe.astype(str)
            dataframeLoan = pd.read_csv(filenameLOAN, sep = "\t", encoding = "latin1")    
            dataframeLoan = dataframeLoan.astype(str)
        except:
            pass
        win.destroy()
    
def initializerREPO():
    global dataframe
    global dataframeLoan  
    global window
    global Title
    global Author
    global Year
    global Editorial
    global Position
    global filenameREPO
    global filenameLOAN 
    global USER
    global PASSWORD 
    global RepositorySelected
    initRP = tk.Toplevel()
    
    access = tk.Label(initRP, text = "Create a repository or choose one from your computer.").grid(row=0, column=1,sticky = "WE", padx=10, pady=10)
    
    accessRP = tk.Label(initRP, text = "Book repository").grid(row=1, column=0,sticky = "WE", padx=10, pady=10)
    accessLN = tk.Label(initRP, text = "Loan repository").grid(row=2, column=0,sticky = "WE", padx=10, pady=10)
    
    
    chooseRP = tk.Button(initRP, text = "Choose files in your computer", command = browse).grid(row=1,column=2, padx=10, pady = 10)
    #chooseLN = tk.Button(initRP, text = "Choose file for loan", command = browse).grid(row=3,column=2, padx=10, pady = 10)
    
    CreateRP = tk.Button(initRP, text = "Create a repository for book", command =lambda: add_repository(initRP, NameRP,NameLN)).grid(row=2,column=2, padx=10, pady = 10)

    NameRP =tk.StringVar()
    NameLN =tk.StringVar()
    
    nameF = tk.Entry(initRP, textvariable = NameRP).grid(row=1, column=1, sticky = "WE", padx=10)
    roomF = tk.Entry(initRP, textvariable = NameLN).grid(row=2, column=1, sticky = "WE", padx=10)
        
def newRep():
    if os.path.exists("parameter.txt"):
        os.remove("parameter.txt")
        initializerREPO()
    else:
        initializerREPO()

def openRep():
    if os.path.exists("parameter.txt"):
        os.remove("parameter.txt")
        browse()
    else:
        browse()
    
    
def newCredential():
    openPWDrequest2()
    
    
def browse():
    global dataframe
    global dataframeLoan  
    global window
    global Title
    global Author
    global Year
    global Editorial
    global Position
    global filenameREPO
    global filenameLOAN 
    global USER
    global PASSWORD 
    global RepositorySelected
    filenameREPO =  filedialog.askopenfilename(initialdir = "/",title = "Select file for your repository",filetypes = (("txt files","*.txt"),("csv files","*.csv"),("all files","*.*")))
    filenameLOAN = filedialog.askopenfilename(initialdir = "/",title = "Select file for your loan",filetypes = (("txt files","*.txt"),("csv files","*.csv"),("all files","*.*")))
    
    if filenameREPO=="" or filenameLOAN=="":
        warn = tk.Toplevel()
        warn.title("WARNING")
        warn.iconbitmap('warn.ico')
        warn.geometry("300x100")
        label = tk.Label(warn, text="You must fullfilled both the fields \n for book and loan").pack()
        ok = tk.Button(warn, text = "ok", command = warn.destroy).pack()
        return None
    else:
        with open("parameter.txt", "a") as f:
            f.write(filenameREPO + "," +filenameLOAN + "\n")
        
        try:
            dataframe=pd.read_csv(filenameREPO, sep = "\t", encoding = "latin1")     
            dataframe = dataframe.astype(str)
            dataframeLoan = pd.read_csv(filenameLOAN, sep = "\t", encoding = "latin1")    
            dataframeLoan = dataframeLoan.astype(str) 
        except:
            pass
        
        
def make_password(password, salt):    #PBKDFHMAC generate a good password froma a password we pass, generating an hashing with salt(random hash) and then enctrypted in base64
	kdf = PBKDF2HMAC(
		algorithm=hashes.SHA256(),
		length=32,
		salt=salt,
		iterations=100000,
		backend=default_backend()
	)
	return base64.urlsafe_b64encode(kdf.derive(password))
    
def createAccount(get_user,get_pwd, win):
    global dataframe
    global dataframeLoan  
    global window
    global Title
    global Author
    global Year
    global Editorial
    global Position
    global filenameREPO
    global filenameLOAN 
    global USER
    global PASSWORD 
    global RepositorySelected
    salt = os.urandom(16)     #salt need for introduce a random process in hashing file
    key = make_password(InternalPassword, salt)   #we are creating the key to decode our encrypted file in future. we have generated it with PBKDFHMAC method (see above)
    cipher_suite = Fernet(key)

    
    
    username=get_user.get()
    password=get_pwd.get()
    get_user.set("")
    get_pwd.set("")
    stringa = username+","+password  #the message to encrypt
    
    cipher_text = cipher_suite.encrypt(stringa.encode("utf-8"))#here the strina encoded in a cipher text, This text is needed for encoding and decodign
    cipher_text_utf8 = base64.b64encode(salt).decode('utf-8') + cipher_text.decode('utf-8')#we place the key at the beginning of the encrypted message
    
    with open("credentials.txt", "w") as cred:
         cred.write(cipher_text_utf8)
    win.destroy()
 

#functions executed by the buttons

def merging_search(field, strfield):
    global dataframe
    global dataframeLoan  
    global window
    global Title
    global Author
    global Year
    global Editorial
    global Position
    global filenameREPO
    global filenameLOAN 
    global USER
    global PASSWORD 
    global RepositorySelected
    #breakpoint()
    name = field.get()
    if name=="":
        return dataframe
    else:
        position = dataframe[strfield].str.contains(name, case = False)
        field.set("")
        rank = dataframe[position]
        return rank
    
def merging_search2(field, strfield):
    global dataframe
    global dataframeLoan  
    global window
    global Title
    global Author
    global Year
    global Editorial
    global Position
    global filenameREPO
    global filenameLOAN 
    global USER
    global PASSWORD 
    global RepositorySelected
    name = field.get()
    if name=="":
        return dataframeLoan
    else:
        position = dataframeLoan[strfield].str.contains(name, case = False)
        field.set("")
        rank = dataframeLoan[position]
        return rank


def to_string(df, strfield):
    global dataframe
    global dataframeLoan  
    global window
    global Title
    global Author
    global Year
    global Editorial
    global Position
    global filenameREPO
    global filenameLOAN 
    global USER
    global PASSWORD 
    global RepositorySelected
    if df.equals(dataframe)==True:
        return f"No search for {strfield}"
    else:
        #rank = df.to_string(index=False)
        rank = tabulate(df, headers = 'keys', tablefmt = 'simple')
        answer = f"The search for {strfield} field has found this match:\n" + rank
        return answer
    

def search():
    global dataframe
    global dataframeLoan  
    global window
    global Title
    global Author
    global Year
    global Editorial
    global Position
    global filenameREPO
    global filenameLOAN 
    global USER
    global PASSWORD 
    global RepositorySelected
    
    dfTitle = merging_search(Title, "Title")
    dfAuthor = merging_search(Author, "Author")
    dfYear = merging_search(Year, "Year")
    dfEdit = merging_search(Editorial, "Editorial")
    dfPosition = merging_search(Position, "Position")
    
    Resultsdf = dfTitle.merge(dfAuthor.merge(dfYear.merge(dfEdit.merge(dfPosition))))
    
    Resultsdf = dfTitle[dfTitle.isin(dfAuthor)].dropna()
    Resultsdf = Resultsdf[Resultsdf.isin(dfPosition)].dropna()
    Resultsdf = Resultsdf[Resultsdf.isin(dfYear)].dropna()
    Resultsdf = Resultsdf[Resultsdf.isin(dfEdit)].dropna()
    
    GeneralAnswer = to_string(Resultsdf, "all")
    answerTitle = to_string(dfTitle, "Title")
    answerAuthor = to_string(dfAuthor, "Author")
    answerYear = to_string(dfYear, "Year")
    answerEdit = to_string(dfEdit, "Editorial")
    answerPosition = to_string(dfPosition, "Position")
    
    answer = GeneralAnswer+ "\n\n\n" +answerTitle + "\n\n\n" + answerAuthor+"\n\n\n"+answerYear+"\n\n\n"+ answerEdit + "\n\n\n" + answerPosition
    text = tkscrolled.ScrolledText(window)
    text.insert(tk.END, answer)
    text.grid(row=6, column=1, columnspan= 1, sticky= "WE")
    #scroll = tk.Scrollbar(window, borderwidth=1,command=text.yview).grid(row=6, column=2, columnspan =1, sticky = "WE")
    #text['yscrollcommand'] = scroll
    myFont = Font(family="Times New Roman", size=12)
    text.configure(font=myFont)
    
def add_book():
    global dataframe
    global dataframeLoan  
    global window
    global Title
    global Author
    global Year
    global Editorial
    global Position
    global filenameREPO
    global filenameLOAN 
    global USER
    global PASSWORD 
    global RepositorySelected
    #openPWDrequest() 
    title=Title.get()
    author=Author.get()
    year=Year.get()
    position=Position.get()
    edit=Editorial.get()
    if title == "" and author == "" and year == "" and position == "" and edit == "":
        Warn = tk.Toplevel()
        
        Warn.title("WARNING")
        access = tk.Label(Warn, text = "The fields cannot be all empty.\n Please, add at least one field and a position").grid(row=0, column=0,sticky = "WE", padx=10)
        ok = tk.Button(Warn, text = "ok", command = Warn.destroy).grid(row=1,column=0, padx = 10, pady=30)
    else:
        if position == "":
            Warn = tk.Toplevel()
            
            Warn.title("WARNING")
            access = tk.Label(Warn, text = "The field position must be fullfilled\n A book cannot be wherever").grid(row=0, column=0,sticky = "WE", padx=10)
            ok = tk.Button(Warn, text = "ok", command = Warn.destroy).grid(row=1,column=0, padx = 10, pady=30)
        with open(filenameREPO, 'w') as f:
            book_to_append = {"Title": [title], "Author": [author], "Position" : [position], "Editorial" : [edit], "Year": [year], "Available": ["Yes"]}
            book_to_append = pd.DataFrame(book_to_append)
            dataframe = dataframe.append(book_to_append)
            #dataframe = dataframe.sort("Title")
            dataframe.to_csv(f, sep = "\t", index = False)
            
        with open(filenameREPO, 'r') as f:
             dataframe=pd.read_csv(filenameREPO, sep = "\t", encoding = "latin1")
             dataframe = dataframe.astype(str)
            
        
def explore_repository():
    global dataframe
    global dataframeLoan  
    global window
    global Title
    global Author
    global Year
    global Editorial
    global Position
    global filenameREPO
    global filenameLOAN 
    global USER
    global PASSWORD 
    global RepositorySelected
    Repository = tabulate(dataframe, headers = 'keys', tablefmt = 'simple')
    TextWin = tk.Toplevel()
    TextWin.title("REPOSITORY RM MEXICO")
    text = tkscrolled.ScrolledText(TextWin)
    text.insert(tk.END, Repository)
    text.grid(row=0, column=0, columnspan= 1, sticky= "WE", padx=10, pady = 10)
    myFont = Font(family="Times New Roman", size=12)
    text.configure(font=myFont)

def explore_loan_repository():
    global dataframe
    global dataframeLoan  
    global window
    global Title
    global Author
    global Year
    global Editorial
    global Position
    global filenameREPO
    global filenameLOAN 
    global USER
    global PASSWORD 
    global RepositorySelected
    
    Repository = tabulate(dataframeLoan, headers = 'keys', tablefmt = 'simple')
    TextWin = tk.Toplevel()
    TextWin.title("REPOSITORY RM MEXICO")
    text = tkscrolled.ScrolledText(TextWin)
    text.insert(tk.END, Repository)
    text.grid(row=0, column=0, columnspan= 1, sticky= "WE", padx=10, pady = 10)
    myFont = Font(family="Times New Roman", size=12)
    text.configure(font=myFont)
    
def online_search():
    global dataframe
    global dataframeLoan  
    global window
    global Title
    global Author
    global Year
    global Editorial
    global Position
    global filenameREPO
    global filenameLOAN 
    global USER
    global PASSWORD 
    global RepositorySelected
    
    title=Title.get()
    author=Author.get()
    year=Year.get()
    edit=Editorial.get()
    request = f"{title} {author} {edit} {year}"
    webbrowser.open(f"https://www.google.com/search?q={request}&oq={request}&aqs=edge..69i57j69i60l3.478j0j4&sourceid=chrome&ie=UTF-8")
    
#functions for password requests 

  

def openPWDrequest():
    global dataframe
    global dataframeLoan  
    global window
    global Title
    global Author
    global Year
    global Editorial
    global Position
    global filenameREPO
    global filenameLOAN 
    global USER
    global PASSWORD 
    global RepositorySelected
    pwdWindow = tk.Toplevel()
    pwdWindow.iconbitmap('Seminario_RM.ico')
    pwdWindow.title("Credentials required")
    #pwdWindow.geometry("100x200")
    access = tk.Label(pwdWindow, text = "Insert password").grid(row=0, column=1,sticky = "WE", padx=10)
    user = tk.Label(pwdWindow, text = "Username").grid(row=1, column=0,sticky = "WE", padx=10)
    get_user = tk.Entry(pwdWindow, textvariable = USER).grid(row=1, column=1, sticky = "WE", padx=10)
    pwd = tk.Label(pwdWindow, text = "Password").grid(row=2, column=0,sticky = "WE", padx=10)
    get_pwd = tk.Entry(pwdWindow, textvariable = PASSWORD, show="*").grid(row=2, column=1, sticky = "WE", padx=10, pady=10)
    done = tk.Button(pwdWindow, text = "done", command = lambda: controlPWD(USER, PASSWORD, pwdWindow)).grid(row=3,column=2, padx = 10, pady=30)

def openPWDrequest2():
    global dataframe
    global dataframeLoan  
    global window
    global Title
    global Author
    global Year
    global Editorial
    global Position
    global filenameREPO
    global filenameLOAN 
    global USER
    global PASSWORD 
    global RepositorySelected
    pwdWindow = tk.Toplevel()
    pwdWindow.iconbitmap('Seminario_RM.ico')
    pwdWindow.title("Credentials required")
    #pwdWindow.geometry("100x200")
    access = tk.Label(pwdWindow, text = "Insert password").grid(row=0, column=1,sticky = "WE", padx=10)
    user = tk.Label(pwdWindow, text = "Username").grid(row=1, column=0,sticky = "WE", padx=10)
    get_user = tk.Entry(pwdWindow, textvariable = USER).grid(row=1, column=1, sticky = "WE", padx=10)
    pwd = tk.Label(pwdWindow, text = "Password").grid(row=2, column=0,sticky = "WE", padx=10)
    get_pwd = tk.Entry(pwdWindow, textvariable = PASSWORD, show="*").grid(row=2, column=1, sticky = "WE", padx=10, pady=10)
    done = tk.Button(pwdWindow, text = "done", command = lambda: controlPWD2(USER, PASSWORD, pwdWindow)).grid(row=3,column=2, padx = 10, pady=30)

def controlPWD2(get_user, get_pwd, pwd):
    global dataframe
    global dataframeLoan  
    global window
    global Title
    global Author
    global Year
    global Editorial
    global Position
    global filenameREPO
    global filenameLOAN 
    global USER
    global PASSWORD 
    global RepositorySelected
    
    username=get_user.get()
    password=get_pwd.get()
    get_user.set("")
    get_pwd.set("")
    
    InsertedCredentials = [username,password]
    with open("credentials.txt", "r") as cred:
        credentials = cred.read()
    
    
    salt = base64.b64decode(credentials[:24].encode("utf-8"))
    cipher_suite = Fernet(make_password(InternalPassword, salt))
    plain_text = cipher_suite.decrypt(credentials[24:].encode("utf-8"))
    credentials = plain_text.decode("utf-8")
    credentials = io.StringIO(credentials)
    credentials = credentials.read().splitlines()
    
    for i in range(len(credentials)):
        credentials[i] = credentials[i].split(",")
    
    if credentials[0] == InsertedCredentials:
        access = tk.Label(pwd, text = "correct credentials").grid(row=3, column=1,sticky = "WE", padx=10, pady=30)
        if os.path.exists("credentials.txt"):
            os.remove("credentials.txt")
            initializerPWD()
        else:
            initializerPWD()
        pwd.destroy()   
    else: 
        control = False
        access = tk.Label(pwd, text = "Access denied").grid(row=3, column=1,sticky = "WE", padx=10, pady=30)
        return None
    
    #access = tk.Label(pwd, text = "correct credentials").grid(row=2, column=1,sticky = "WE", padx=10, pady=30)
    
    pwd.destroy()


def controlPWD(get_user, get_pwd, pwd):
    global dataframe
    global dataframeLoan  
    global window
    global Title
    global Author
    global Year
    global Editorial
    global Position
    global filenameREPO
    global filenameLOAN 
    global USER
    global PASSWORD 
    global RepositorySelected
    
    username=get_user.get()
    password=get_pwd.get()
    get_user.set("")
    get_pwd.set("")
    
    InsertedCredentials = [username,password]
    with open("credentials.txt", "r") as cred:
        credentials = cred.read()
    
    
    salt = base64.b64decode(credentials[:24].encode("utf-8"))
    cipher_suite = Fernet(make_password(InternalPassword, salt))
    plain_text = cipher_suite.decrypt(credentials[24:].encode("utf-8"))
    credentials = plain_text.decode("utf-8")
    credentials = io.StringIO(credentials)
    credentials = credentials.read().splitlines()
    
    for i in range(len(credentials)):
        credentials[i] = credentials[i].split(",")
    
    if credentials[0] == InsertedCredentials:
        access = tk.Label(pwd, text = "correct credentials").grid(row=3, column=1,sticky = "WE", padx=10, pady=30)
        add_book()
        pwd.destroy()   
    else: 
        control = False
        access = tk.Label(pwd, text = "Access denied").grid(row=3, column=1,sticky = "WE", padx=10, pady=30)
        
        return None
    
    #access = tk.Label(pwd, text = "correct credentials").grid(row=2, column=1,sticky = "WE", padx=10, pady=30)
    #add_book()
    #control=True
    #pwd.destroy()
     
def search_book():
    global dataframe
    global dataframeLoan  
    global window
    global Title
    global Author
    global Year
    global Editorial
    global Position
    global filenameREPO
    global filenameLOAN 
    global USER
    global PASSWORD 
    global RepositorySelected
    searchWin = tk.Toplevel()
    searchWin.iconbitmap('Seminario_RM.ico')
    searchWin.title("Edit repository")   
    access = tk.Label(searchWin, text = "write the position of the book you want to edit").grid(row=0, column=0,sticky = "WE", padx=10)
    book = tk.Entry(searchWin, textvariable = Position).grid(row=1, column=0, sticky = "WE", padx=10)
    
    Explore = tk.Button(searchWin, text = "Explore catalogue", command = explore_repository).grid(row=0,column=1, padx = 10, pady=30)
    hint = tk.Label(searchWin, text = "or\n search it in the home window").grid(row=1, column=1,sticky = "WE", padx=10)
    delete = tk.Button(searchWin, text = "delete", command = lambda: warning(Position)).grid(row=2,column=1, padx = 10, pady=30)
    Loan = tk.Button(searchWin, text = "Loan", command =lambda: loan(Position)).grid(row=2,column=0, padx = 10, pady=30)
    


def warning(position):
    global dataframe
    global dataframeLoan  
    global window
    global Title
    global Author
    global Year
    global Editorial
    global Position
    global filenameREPO
    global filenameLOAN 
    global USER
    global PASSWORD 
    global RepositorySelected
    
    pos = position.get()
    found =  dataframe[dataframe["Position"]==pos]
    warn = found.to_string(index=False)
    Warn = tk.Toplevel()
    Warn.iconbitmap('warn.ico')
    Warn.title("WARNING") 
    access = tk.Label(Warn, text = f"Are you sure to delete the following book?\n{warn}").grid(row=0, column=0,sticky = "WE", padx=10)
    ok = tk.Button(Warn, text = "I'm sure", command =lambda: eliminateBook(Warn,found)).grid(row=1,column=0, padx = 10, pady=30)
    No = tk.Button(Warn, text = "Cancel", command = Warn.destroy).grid(row=1,column=1, padx = 10, pady=30)
    
    
def eliminateBook(Warn,found):
    global dataframe
    global dataframeLoan  
    global window
    global Title
    global Author
    global Year
    global Editorial
    global Position
    global filenameREPO
    global filenameLOAN 
    global USER
    global PASSWORD 
    global RepositorySelected
    Warn.destroy()
    dataframe = dataframe.drop(labels=found.index, axis=0)
    with open(filenameREPO, 'w') as f:
            dataframe.to_csv(f, sep = "\t", index = False)
    

def loan(position):
    global dataframe
    global dataframeLoan  
    global window
    global Title
    global Author
    global Year
    global Editorial
    global Position
    global filenameREPO
    global filenameLOAN 
    global USER
    global PASSWORD 
    global RepositorySelected
    
    pos = position.get()
    found =  dataframe[dataframe["Position"]==pos]
    warn = found.to_string(index=False)
    loanWin = tk.Toplevel()
    loanWin.title("Loan")
    info = tk.Label(loanWin, text = f"you are loaning the book:\n{warn}\n Insert the Id of receving").grid(row=0, column=0,sticky = "WE", padx=10)
    
    Name = tk.StringVar()
    Room = tk.StringVar()
    
    name = tk.Label(loanWin, text = "name and surname").grid(row=0, column=1)
    nameF = tk.Entry(loanWin, textvariable = Name).grid(row=0, column=2, sticky = "WE", padx=100)

    room = tk.Label(loanWin, text = "room/adress").grid(row=1, column=1)
    roomF = tk.Entry(loanWin, textvariable = Room).grid(row=1, column=2, sticky = "WE", padx=100)
    
    take = tk.Button(loanWin, text = "insert", command=lambda: load(found,Name, Room,loanWin)).grid(row = 2,column=1, padx = 10, pady=30)
   
def load(found, Name, Room,win):
    global dataframe
    global dataframeLoan  
    global window
    global Title
    global Author
    global Year
    global Editorial
    global Position
    global filenameREPO
    global filenameLOAN 
    global USER
    global PASSWORD 
    global RepositorySelected
    nome = Name.get() 
    adress = Room.get()
    Name.set("")
    Room.set("")
    book_to_append = {"Keeper": [nome], "Adress": [adress], "Title": found["Title"], "Author": found["Author"], "Position" : found["Position"], "Editorial" : found["Editorial"], "Year": found["Year"]}
    
    book_to_append = pd.DataFrame(book_to_append)
    dataframeLoan = dataframeLoan.append(book_to_append)
    
    with open(filenameLOAN, 'w') as f:
            
            # book_to_append = {"Keeper": [nome], "Adress": [adress], "Title": found["Title"], "Author": found["Author"], "Position" : found["Position"], "Editorial" : found["Editorial"], "Year": found["Year"]}
                       
            # book_to_append = pd.DataFrame(book_to_append)
            # dataframeLoan = dataframeLoan.append(book_to_append)
            #dataframe = dataframe.sort("Title")
            dataframeLoan.to_csv(f, sep = "\t", index = False)
            
    
    dataframe["Available"][found.index] = "No"
    with open(filenameREPO, 'w') as f:
        dataframe.to_csv(f, sep = "\t", index = False, encoding = "utf8")
    
    with open(filenameLOAN, 'r') as f:
            dataframeLoan = pd.read_csv(f, sep = "\t",  encoding = "latin1")
    
    win.destroy()      

def restitution():
    global dataframeLoan
    global window
    global Title
    global Author
    global Year
    global Editorial
    global Position
    global filenameREPO
    global filenameLOAN 
    global USER
    global PASSWORD 
    global RepositorySelected
    nome = tk.StringVar()
    rome = tk.StringVar()
    titolo = tk.StringVar()
    posi = tk.StringVar()
    
    restWin = tk.Toplevel()
    restWin.iconbitmap('Seminario_RM.ico')
    name = tk.Label(restWin, text = "name and surname").grid(row=1, column=0)
    nameF = tk.Entry(restWin, textvariable = nome).grid(row=1, column=1, sticky = "WE", padx=100)

    room = tk.Label(restWin, text = "room/adress").grid(row=2, column=0)
    roomF = tk.Entry(restWin, textvariable = rome).grid(row=2, column=1, sticky = "WE", padx=100)
        
    pos = tk.Label(restWin, text = "Position").grid(row=3, column=0)
    search_field_position = tk.Entry(restWin, textvariable =pos).grid(row=3, column=1, sticky = "WE", padx=100)

    title = tk.Label(restWin, text = "Title").grid(row=4, column=0)
    search_field_Title = tk.Entry(restWin, textvariable = titolo).grid(row=4, column=1, sticky = "WE", padx=100)
    
    
    
    take = tk.Button(restWin, text = "restitute", command=lambda: resa(titolo, nome, rome, posi,restWin)).grid(row = 1,column=2)

def resa(titolo, nome, rome, pos,win):
    global dataframeLoan
    global window
    global Title
    global Author
    global Year
    global Editorial
    global Position
    global filenameREPO
    global filenameLOAN 
    global USER
    global PASSWORD 
    global RepositorySelected
    dfname = merging_search2(nome, "Keeper")
    dfroom = merging_search2(rome, "Adress")
    dfposition = merging_search2(pos, "Position")
    dfTitle = merging_search2(titolo, "Title")
    
    Resultsdf = dfTitle[dfTitle.isin(dfroom)].dropna()
    Resultsdf = Resultsdf[Resultsdf.isin(dfposition)].dropna()
    Resultsdf = Resultsdf[Resultsdf.isin(dfname)].dropna()
    
    
    dataframeLoan = dataframeLoan.drop(labels=Resultsdf.index, axis=0)
   
    with open(filenameLOAN, 'w') as f:
            dataframeLoan.to_csv(f, sep = "\t", index = False)
     
    with open(filenameLOAN, 'r') as f:
            dataframeLoan = pd.read_csv(f, sep = "\t",  encoding = "latin1")    
        
    dataframe["Available"][Resultsdf.index] = "Yes"
    with open(filenameREPO, 'w') as f:
        dataframe.to_csv(f, sep = "\t", index = False)
       
    win.destroy()
 
def new_win(): 
    global dataframe
    global dataframeLoan
    global window
    global Title
    global Author
    global Year
    global Editorial
    global Position
    global filenameREPO
    global filenameLOAN 
    global USER
    global PASSWORD 
    global RepositorySelected
    window = tk.Tk()
    window.title("RMbiblio0.1")
    window.iconbitmap('Seminario_RM.ico')
    #window.geometry("1000x100")
    window.grid_columnconfigure(0,weight=1)
    Volto_di_Cristo= Image.open("Volto.jpg")
    Volto_di_Cristo = ImageTk.PhotoImage(Volto_di_Cristo)
    VoltoImage = tk.Label(image=Volto_di_Cristo).grid(row=0, column=3, columnspan =2, rowspan = 10)
    
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_coordinate = (screen_width/2)-(width_of_window/2)
    y_coordinate = (screen_height/2)-(height_of_window/2)
    
    
    Title = tk.StringVar()
    Author = tk.StringVar()
    Position = tk.StringVar()
    Editorial = tk.StringVar()
    Year = tk.StringVar()
     
   
    #initialization of credentials
        
    InternalPassword= b"RM.MEXICO" #password to initialize the encrypter
    
    #user and password variable
    USER = tk.StringVar()
    PASSWORD = tk.StringVar()
    RepositorySelected = 0
    
    if glob.glob("credentials.txt") == []:  
        initializerPWD()
    
    if glob.glob("parameter.txt") == []:
        initializerREPO()
    else:
        with open("parameter.txt", "r") as f:
            files = f.read()
            
            files = files.splitlines()
            if len(files)==1:
                
                
                files[0] = files[0].split(",")
                files = files[0]
            else:
                
                selector = RepositorySelected
                for i in range(len(files)):
                    
                    files[i]= files[i].split(",")
                    files = files[RepositorySelected]
                    
        filenameREPO =  files[0]
        filenameLOAN = files[1]
        
        try:
            
            dataframe=pd.read_csv(filenameREPO, sep = "\t", encoding = "latin1")
            dataframe = dataframe.astype(str)
            dataframeLoan=pd.read_csv(filenameLOAN, sep = "\t", encoding = "latin1")
            dataframeLoan = dataframeLoan.astype(str)
            
        except:
            pass
    
    
    #requests fields of the GUI
    title = tk.Label(window, text = "Title").grid(row=1, column=0)
    search_field_Title = tk.Entry( textvariable = Title).grid(row=1, column=1, sticky = "WE", padx=100)
    
    author = tk.Label(window, text = "author").grid(row=2, column=0)
    search_field_author = tk.Entry( textvariable = Author).grid(row=2, column=1, sticky = "WE", padx=100)
    
    pos = tk.Label(window, text = "Position").grid(row=3, column=0)
    search_field_position = tk.Entry( textvariable = Position).grid(row=3, column=1, sticky = "WE", padx=100)
    
    Edit = tk.Label(window, text = "Editorial home").grid(row=4, column=0)
    search_field_Edit = tk.Entry( textvariable = Editorial).grid(row=4, column=1, sticky = "WE", padx=100)
    
    Years = tk.Label(window, text = "Year").grid(row=5, column=0)
    search_field_Year = tk.Entry( textvariable = Year).grid(row=5, column=1, sticky = "WE", padx=100)
    
    #button of the gui
    
    searchButton = tk.Button( text = "Search", command=search, height = 2, width = 15).grid(row = 1,column=2)
    Addbutton = tk.Button(text = "Add to repository", command = openPWDrequest, height = 2, width = 15).grid(row=2,column=2)
    exploreButton = tk.Button(text = "Explore Repository", command = explore_repository, height = 2, width = 15).grid(row=3,column=2)
    exploreButton = tk.Button(text = "Explore Loan \nRepository", command = explore_loan_repository, height = 2, width = 15).grid(row=4,column=2)
    onlineButton = tk.Button(text = "Search online", command = online_search, height = 2, width = 15).grid(row=5,column=2)
    #eliminateButton = tk.Button(text = "Delete Book", command = search_book).grid(row=5,column=2)
    #loanButton= tk.Button(text = "Loan", command = search_book).grid(row=6,column=2)
    
    #fileMenu
    
    menu = tk.Menu(window)
    window.config(menu=menu)
    fileMenu = tk.Menu(menu)
    menu.add_cascade(label="File", menu=fileMenu)
    fileMenu.add_command(label="New Repository", command = newRep)
    fileMenu.add_command(label = "Open Repository", command = openRep)
    fileMenu.add_command(label = "New Credentials", command = newCredential)
    
    editMenu = tk.Menu(menu)
    menu.add_cascade(label="Option", menu=editMenu)
    editMenu.add_command(label="Delete a Book", command = search_book)
    editMenu.add_command(label="Loan book",command = search_book)
    editMenu.add_command(label="Restitution", command =restitution)
    editMenu.add_command(label="Explore repository", command =explore_repository)
    editMenu.add_command(label="Explore loan repository", command =explore_loan_repository)
    
    
    aboutMenu = tk.Menu(menu)
    menu.add_cascade(label="?", menu=aboutMenu)
    aboutMenu.add_command(label = "About", command = about)
    window.mainloop()






def bar():

    l4=tk.Label(w,text='Loading...',fg='white',bg=a)
    lst4=('Calibri (Body)',10)
    l4.config(font=lst4)
    l4.place(x=18,y=210)
    
    import time
    r=0
    for i in range(100):
        progress['value']=r
        w.update_idletasks()
        time.sleep(0.03)
        r=r+1
    
    w.destroy()
    new_win()
        
filenameREPO =  None
filenameLOAN = None
dataframe = None
dataframeLoan = None
window=None    
Title = None
Author = None
Position = None
Editorial = None
Year = None
#initialization of credentials   
InternalPassword= b"RM.MEXICO" #password to initialize the encrypter
#user and password variable
USER = None
PASSWORD = None
RepositorySelected = 0

w=tk.Tk()


width_of_window = 427
height_of_window = 250
screen_width = w.winfo_screenwidth()
screen_height = w.winfo_screenheight()
x_coordinate = (screen_width/2)-(width_of_window/2)
y_coordinate = (screen_height/2)-(height_of_window/2)
w.geometry("%dx%d+%d+%d" %(width_of_window,height_of_window,x_coordinate,y_coordinate))



w.overrideredirect(1)


s = tk.ttk.Style()
s.theme_use('clam')
s.configure("red.Horizontal.TProgressbar", foreground='red', background='#4f4f4f')
progress=Progressbar(w,style="red.Horizontal.TProgressbar",orient=tk.HORIZONTAL,length=500,mode='determinate',)

#############progressbar          33333333333333333333333333333

progress.place(x=-10,y=235)



'''

def rgb(r):
    return "#%02x%02x%02x" % r
#Frame(w,width=432,height=241,bg=rgb((100,100,100))).
'''
a='#249794'
tk.Frame(w,width=427,height=241,bg=a).place(x=0,y=0)  #249794
b1=tk.Button(w,width=10,height=1,text='Get Started',command=bar,border=0,fg=a,bg='white')
b1.place(x=170,y=200)


######## Label

l1=tk.Label(w,text='RMbiblio',fg='white',bg=a)
lst1=('Calibri (Body)',18,'bold')
l1.config(font=lst1)
l1.place(x=50,y=80)

l2=tk.Label(w,text='0.1',fg='white',bg=a)
lst2=('Calibri (Body)',18)
l2.config(font=lst2)
l2.place(x=155,y=82)

l3=tk.Label(w,text='Library of Ciudad de Mexico',fg='white',bg=a)
lst3=('Calibri (Body)',13)
l3.config(font=lst3)
l3.place(x=50,y=110)

w.mainloop()
  

