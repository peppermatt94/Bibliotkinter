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


# biblio = {"Title": ["harry potter", "Il codice da vinci","il Signore degli anelli"], "Author": ["Rowling", "Brown", "Tolkien"], "Position" : ["a55", "b2","d3"], "Editorial" : ["la fenice", "Erudita", "Oxford Express"], "Year": [1990, 2002, 1997]}
# dataframe = pd.DataFrame(biblio)
# with open("C:\\Users\\pepermatt94\\OneDrive\\Libri Magistrale\\SOFTWARE and COMPUTING\\biblio.txt", 'w') as f:
#         f.write(dataframe.to_string(index=False))


#variable and initialization


dataframe=pd.read_csv("biblio.txt", sep = "\t")
dataframe = dataframe.astype(str)

dataframeLoan = pd.read_csv("biblioLend.txt")
dataframeLoan = dataframeLoan.astype(str)

window = tk.Tk()
window.title("Biblio")
window.iconbitmap('Seminario_RM.ico')
#window.geometry("1000x100")
window.grid_columnconfigure(0,weight=1)
Volto_di_Cristo= Image.open("Volto.jpg")
Volto_di_Cristo = ImageTk.PhotoImage(Volto_di_Cristo)
VoltoImage = tk.Label(image=Volto_di_Cristo).grid(row=0, column=3, columnspan =2, rowspan = 10)

Title = tk.StringVar()
Author = tk.StringVar()
Position = tk.StringVar()
Editorial = tk.StringVar()
Year = tk.StringVar()

#initialization of credentials
    
InternalPassword= b"RM.MEXICO" #password to initialize the encypter

#user and password variable
USER = tk.StringVar()
PASSWORD = tk.StringVar()

#intializing function

def initializerPWD():
    global tip
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
    
#def initializerREPO():
#    window.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("txt files","*.txt"),("all files","*.*")))
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
 
if glob.glob("credentials.txt") == []:  
    initializerPWD()

       
#functions executed by the buttons

def merging_search(field, strfield):
    name = field.get()
    if name=="":
        return dataframe
    else:
        position = dataframe[strfield].str.contains(name, case = False)
        field.set("")
        rank = dataframe[position]
        return rank
def merging_search2(field, strfield):
    name = field.get()
    if name=="":
        return dataframeLoan
    else:
        position = dataframeLoan[strfield].str.contains(name, case = False)
        field.set("")
        rank = dataframeLoan[position]
        return rank


def to_string(df, strfield):
    if df.equals(dataframe)==True:
        return f"No search for {strfield}"
    else:
        #rank = df.to_string(index=False)
        rank = tabulate(df, headers = 'keys', tablefmt = 'simple')
        answer = f"The search for {strfield} field has found this match:\n" + rank
        return answer
    

def search():
    dfTitle = merging_search(Title, "Title")
    dfAuthor = merging_search(Author, "Author")
    dfYear = merging_search(Year, "Year")
    dfEdit = merging_search(Editorial, "Editorial")
    dfPosition = merging_search(Position, "Position")
    Resultsdf = dfTitle.merge(dfAuthor.merge(dfYear.merge(dfEdit.merge(dfPosition))))
    
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
        with open("biblio.txt", 'w') as f:
            book_to_append = {"Title": [title], "Author": [author], "Position" : [position], "Editorial" : [edit], "Year": [year], "Available": ["Yes"]}
            book_to_append = pd.DataFrame(book_to_append)
            dataframe = dataframe.append(book_to_append)
            #dataframe = dataframe.sort("Title")
            dataframe.to_csv(f, sep = "\t", index = False)
        
def explore_repository():
    Repository = tabulate(dataframe, headers = 'keys', tablefmt = 'simple')
    TextWin = tk.Toplevel()
    TextWin.title("REPOSITORY RM MEXICO")
    text = tkscrolled.ScrolledText(TextWin)
    text.insert(tk.END, Repository)
    text.grid(row=0, column=0, columnspan= 1, sticky= "WE", padx=10, pady = 10)
    myFont = Font(family="Times New Roman", size=12)
    text.configure(font=myFont)

def online_search():
    title=Title.get()
    author=Author.get()
    year=Year.get()
    edit=Editorial.get()
    request = f"{title} {author} {edit} {year}"
    webbrowser.open(f"https://www.google.com/search?q={request}&oq={request}&aqs=edge..69i57j69i60l3.478j0j4&sourceid=chrome&ie=UTF-8")
    
#functions for password requests 
    
def openPWDrequest():
    pwdWindow = tk.Toplevel()
    pwdWindow.title("Credentials required")
    #pwdWindow.geometry("100x200")
    access = tk.Label(pwdWindow, text = "Insert password").grid(row=0, column=1,sticky = "WE", padx=10)
    user = tk.Label(pwdWindow, text = "Username").grid(row=1, column=0,sticky = "WE", padx=10)
    get_user = tk.Entry(pwdWindow, textvariable = USER).grid(row=1, column=1, sticky = "WE", padx=10)
    pwd = tk.Label(pwdWindow, text = "Password").grid(row=2, column=0,sticky = "WE", padx=10)
    get_pwd = tk.Entry(pwdWindow, textvariable = PASSWORD, show="*").grid(row=2, column=1, sticky = "WE", padx=10, pady=10)
    done = tk.Button(pwdWindow, text = "done", command = lambda: controlPWD(USER, PASSWORD, pwdWindow)).grid(row=3,column=2, padx = 10, pady=30)


def controlPWD(get_user, get_pwd, pwd):
    
    
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
        sleep(5)
        return None
    
    access = tk.Label(pwd, text = "correct credentials").grid(row=2, column=1,sticky = "WE", padx=10, pady=30)
    add_book()
    control=True
    pwd.destroy()
     
def search_book():
    searchWin = tk.Toplevel()
    searchWin.title("Edit repository")   
    access = tk.Label(searchWin, text = "write the position of the book you want to edit").grid(row=0, column=0,sticky = "WE", padx=10)
    book = tk.Entry(searchWin, textvariable = Position).grid(row=1, column=0, sticky = "WE", padx=10)
    
    Explore = tk.Button(searchWin, text = "Explore catalogue", command = explore_repository).grid(row=0,column=1, padx = 10, pady=30)
    hint = tk.Label(searchWin, text = "or\n search it in the home window").grid(row=1, column=1,sticky = "WE", padx=10)
    delete = tk.Button(searchWin, text = "delete", command = lambda: warning(Position)).grid(row=2,column=1, padx = 10, pady=30)
    Loan = tk.Button(searchWin, text = "Loan", command =lambda: loan(Position)).grid(row=2,column=0, padx = 10, pady=30)
    


def warning(Position):
    found =  merging_search(Position, "Position")
    warn = found.to_string(index=False)
    Warn = tk.Toplevel()
    Warn.title("WARNING") 
    access = tk.Label(Warn, text = f"Are you sure to delete the following book?\n{warn}").grid(row=0, column=0,sticky = "WE", padx=10)
    ok = tk.Button(Warn, text = "I'm sure", command =lambda: eliminateBook(Warn,found)).grid(row=1,column=0, padx = 10, pady=30)
    No = tk.Button(Warn, text = "Cancel", command = Warn.destroy).grid(row=1,column=1, padx = 10, pady=30)
    
    
def eliminateBook(Warn,found):
    global dataframe
    Warn.destroy()
    dataframe = dataframe.drop(labels=found.index, axis=0)
    with open("biblio.txt", 'w') as f:
            dataframe.to_csv(f, sep = "\t", index = False)
    

def loan(Position):
    found =  merging_search(Position, "Position")
    warn = found.to_string(index=False)
    loanWin = tk.Toplevel()
    loanWin.title("Edit repository")
    info = tk.Label(loanWin, text = f"you are loaning the book:\n{warn}\n Insert the Id of receving").grid(row=0, column=0,sticky = "WE", padx=10)
    
    name = tk.Label(loanWin, text = "name and surname").grid(row=0, column=1)
    nameF = tk.Entry(loanWin, textvariable = Title).grid(row=0, column=2, sticky = "WE", padx=100)

    room = tk.Label(loanWin, text = "room/adress").grid(row=1, column=1)
    roomF = tk.Entry(loanWin, textvariable = Author).grid(row=1, column=2, sticky = "WE", padx=100)
    
    take = tk.Button(loanWin, text = "insert", command=lambda: load(found,Title, Author,loanWin)).grid(row = 2,column=1, padx = 10, pady=30)

def load(found, Title, Author,win):
    global dataframe
    global dataframeLoan  
   
    nome = Title.get() 
    adress = Author.get()
    Title.set("")
    Author.set("")
    with open("biblioLend.txt", 'w') as f:
            book_to_append = {"Keeper": [nome], "Adress": [adress], "Title": found["Title"], "Author": found["Author"], "Position" : found["Position"], "Editorial" : found["Editorial"], "Year": found["Year"]}
            book_to_append = pd.DataFrame(book_to_append)
            dataframeLoan = dataframeLoan.append(book_to_append)
            #dataframe = dataframe.sort("Title")
            dataframeLoan.to_csv(f, sep = "\t", index = False)
    dataframe["Available"][found.index] = "No"
    with open("biblio.txt", 'w') as f:
        dataframe.to_csv(f, sep = "\t", index = False)
    
    win.destroy()      

def restitution():
    global dataframeLoan
    restWin = tk.Toplevel()
    
    name = tk.Label(restWin, text = "name and surname").grid(row=1, column=0)
    nameF = tk.Entry(restWin, textvariable = Title).grid(row=1, column=1, sticky = "WE", padx=100)

    room = tk.Label(restWin, text = "room/adress").grid(row=2, column=0)
    roomF = tk.Entry(restWin, textvariable = Author).grid(row=2, column=1, sticky = "WE", padx=100)
        
    pos = tk.Label(restWin, text = "Position").grid(row=3, column=0)
    search_field_position = tk.Entry(restWin, textvariable = Position).grid(row=3, column=1, sticky = "WE", padx=100)

    title = tk.Label(restWin, text = "Title").grid(row=1, column=0)
    search_field_Title = tk.Entry(restWin, textvariable = Editorial).grid(row=1, column=1, sticky = "WE", padx=100)
    
    dfname = merging_search(Title, "keeper")
    dfroom = merging_search(Author, "Adress")
    dfposition = merging_search(Position, "Position")
    dfTitle = merging_search(Editorial, "Title")
    
    Resultsdf = dfname.merge(dfroom.merge(dfposition.merge(dfTitle)))
    
    take = tk.Button( text = "restitute", command=lambda: resa(Resultsdf,restWin)).grid(row = 1,column=2)

def resa(found,win):
    global dataframeLoan
    dataframeLoan = dataframeLoan.drop(labels=found.index, axis=0)
    with open("biblioLend.txt", 'w') as f:
            dataframeLoan.to_csv(f, sep = "\t", index = False)
            
    dataframe["Available"][found.index] = "Yes"
    with open("biblio.txt", 'w') as f:
        dataframe.to_csv(f, sep = "\t", index = False)
       
    win.destroy()
    

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

searchButton = tk.Button( text = "Search", command=search).grid(row = 1,column=2)
Addbutton = tk.Button(text = "Add to repository", command = openPWDrequest).grid(row=2,column=2)
exploreButton = tk.Button(text = "Explore Repository", command = explore_repository).grid(row=3,column=2)
onlineButton = tk.Button(text = "Search online", command = online_search).grid(row=4,column=2)
eliminateButton = tk.Button(text = "Delete Book", command = search_book).grid(row=5,column=2)
loanButton= tk.Button(text = "Loan", command = search_book).grid(row=6,column=2)
window.mainloop()
