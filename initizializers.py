
import tkinter as tk
import pandas as pd
import os
import glob
import io
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from tkinter import filedialog
import numpy as np
from os.path import abspath
from pathlib import Path
import ctypes

#Global variables
def init():
    global dataframe
    global dataframeLoan
    global window
    global RequestsFields
    global credentials
    global filenameREPO
    global filenameLOAN
    global REMOTE
    global variableString
    global StringOfRestitution
    dataframe=None
    dataframeLoan=None
    window = None
    variableString={}
    RequestsFields = {}
    credentials = {}  
    filenameREPO = ""
    filenameLOAN = ""
    REMOTE = "No"
    StringOfRestitution = {}
InternalPassword= b"RM.MEXICO" #password to initialize the encrypter



def initializerPWD(credentials, initREPO, newWin):
    #Win for the initialization of password
    #user and password variables
    
    initializeWin = tk.Tk()
    credentials["USER"] = tk.StringVar()
    credentials["PASSWORD"] = tk.StringVar()
    initializeWin.attributes("-topmost", True)
    initializeWin.title("Create an Administrator account")
    access = tk.Label(initializeWin, text = "Insert username and password").grid(row=0, column=1,sticky = "WE", padx=10, pady=10)
    user = tk.Label(initializeWin, text = "username").grid(row=1, column=0,sticky = "WE", padx=10)
    get_user = tk.Entry(initializeWin, textvariable = credentials["USER"]).grid(row=1, column=1, sticky = "WE", padx=10)
    pwd = tk.Label(initializeWin, text = "password").grid(row=2, column=0, padx=10)
    get_pwd = tk.Entry(initializeWin, textvariable = credentials["PASSWORD"], show = "*").grid(row=2, column=1, sticky = "WE", padx=10)
    account = tk.Button(initializeWin, text = "create account", command =lambda: createAccount(credentials["USER"],credentials["PASSWORD"], initializeWin,  initREPO, newWin)).grid(row=3,column=2, padx=10, pady = 10)
    initializeWin.mainloop()


def add_repository(win , NameRP, nameln, newWin, REMOTE ="No"):
    global dataframe
    global dataframeLoan 
    global filenameREPO
    global filenameLOAN
    global credentials
    
    name=NameRP.get()
    nameLN = nameln.get()
   
    if REMOTE == "Yes":
        if not os.path.exists("Z:\\RMbiblio") : os.makedirs("Z:\\RMbiblio")
        filenameREPO = "Z:\\RMbiblio\\+"+name+".csv"
        filenameLOAN = "Z:\\RMbiblio\\"+nameLN+".csv"
        Workdir = "Z:\\RMbiblio\\"
    else:
        filenameREPO = os.getcwd() + "\\" + name + ".csv"
        filenameLOAN = os.getcwd() + "\\" + nameLN + ".csv"
        Workdir = os.getcwd() +"\\"
    
    NameRP.set("")
    nameln.set("")
    
    if name=="" or nameLN =="":
       warning("You must fullfilled both the repository and loan repository fields")
       return None
    else:
        with open(filenameREPO, "w", encoding = "latin1" ) as f:
            header = {"Title": [], "Author": [], "Position" : [], "Editorial" : [], "Year": [], "Available": []}
            header = pd.DataFrame(header)
            header.to_csv(f, sep = ",", index = False) 
            
        with open(filenameLOAN, "w", encoding = "latin1" ) as f:
            header = {"Keeper": [], "Adress": [], "Title": [], "Author": [], "Position" : [], "Date of loan" : [], "Date of restitution":[]}
            header = pd.DataFrame(header)
            header.to_csv(f, sep=",", index = False) 
        
        if not os.path.exists(Workdir+".setup"): os.makedirs(Workdir +".setup")
        with open(Workdir + ".setup\\parameter.txt", "w") as f:
            f.write(filenameREPO + "," +filenameLOAN +"\n")        
        try:
            dataframe=pd.read_csv(filenameREPO, sep = ",",encoding = "latin1")    
            dataframe =dataframe.replace(np.nan, '', regex=True)
            dataframe = dataframe.astype(str)
            dataframeLoan = pd.read_csv(filenameLOAN, sep = ",", encoding = "latin1")
            dataframeLoan = dataframeLoan.replace(np.nan, '', regex=True)
            dataframeLoan = dataframeLoan.astype(str)
        except:
            pass
        
        init.dataframe = dataframe
        init.dataframeLoan = dataframeLoan
        win.destroy()
        newWin(dataframe, dataframeLoan, filenameREPO, credentials, variableString, init.window)
    
def initializerREPO(filenameREPO, filenameLOAN, newWin):
    global dataframe
    global dataframeLoan  

    initRP = tk.Tk()
    access = tk.Label(initRP, text = "Create a repository or choose one from your computer.").grid(row=0, column=1,sticky = "WE", padx=10, pady=10)
    
    NameP =tk.StringVar(initRP)
    NameN =tk.StringVar(initRP)
    NameP.set("sono io")
    accessRP = tk.Label(initRP, text = "Book repository").grid(row=1, column=0,sticky = "WE", padx=10, pady=10)
    accessLN = tk.Label(initRP, text = "Loan repository").grid(row=2, column=0,sticky = "WE", padx=10, pady=10)
    
    nameF = tk.Entry(initRP, textvariable = NameP).grid(row=1, column=1, sticky = "WE", padx=10)
    roomF = tk.Entry(initRP, textvariable = NameN).grid(row=2, column=1, sticky = "WE", padx=10)

    chooseRP = tk.Button(initRP, text = "Choose files in your computer", command =lambda: browse(initRP,newWin)).grid(row=1,column=2, padx=10, pady = 10)
    CreateRP = tk.Button(initRP, text = "Create a repository for book", command =lambda: add_repository(initRP, NameP,NameN, newWin)).grid(row=2,column=2, padx=10, pady = 10)
    
    # nameF = tk.Entry(initRP, textvariable = NameRP).grid(row=1, column=1, sticky = "WE", padx=10)
    # roomF = tk.Entry(initRP, textvariable = NameLN).grid(row=2, column=1, sticky = "WE", padx=10)
    #breakpoint()
    initRP.mainloop()
        
def newRep(filenameLOAN, filenameREPO, newWin,REMOTE = "No"):
    if REMOTE =="Yes":
        Workdir = "Z:\\RMbiblio\\"
    else:
        Workdir = os.getcwd()
    if os.path.exists(Workdir +".setup\\parameter.txt"):
        os.remove(Workdir+".setup\\parameter.txt")
        initializerREPO(filenameREPO, filenameLOAN, newWin)
    else:
        initializerREPO(filenameREPO, filenameLOAN, newWin)

def openRep(win, newWin):
    if REMOTE =="Yes":
        Workdir = "Z:\\RMbiblio\\"
    else:
        Workdir = os.getcwd()
    if os.path.exists(Workdir +".setup\\parameter.txt"):
        os.remove(Workdir +".setup\\parameter.txt")
        browse(win, newWin)
    else:
        browse(win, newWin)
    
    
def newCredential():
    openPWDrequest(initializerPWD(variableString))
    
    
def browse(initRP,newWin, REMOTE ="No"):
    global dataframe
    global dataframeLoan  
    global window
    global filenameREPO
    global filenameLOAN
    
    filenameREPO =  filedialog.askopenfilename(initialdir = "/",title = "Select file for your repository",filetypes = (("txt files","*.txt"),("csv files","*.csv"),("all files","*.*")))
    filenameLOAN = filedialog.askopenfilename(initialdir = "/",title = "Select file for your loan",filetypes = (("txt files","*.txt"),("csv files","*.csv"),("all files","*.*")))
    
    
    if filenameREPO=="" or filenameLOAN=="":
        warning("You must fullfilled both the field for repository and loan repository")
        return None
    else:
        if REMOTE =="yes":
            if not os.path.exists("Z:/RMbiblio"): os.makedirs("Z:/RMbiblio")
            Workdir = "Z:/RMbiblio/"  
        else:
            Workdir = os.getcwd() + "/"
        nameRP = filenameREPO.split("/")[-1]
        nameLN = filenameLOAN.split("/")[-1]
        #breakpoint()
        import shutil
        #breakpoint()
        if  abspath((Workdir+nameRP).lower()) == abspath((filenameREPO).lower()):
            pass
        else:       
            shutil.copyfile(filenameREPO, Workdir+nameRP)
        if  abspath((Workdir+nameLN).lower()) == abspath((filenameLOAN).lower()):
            pass
        else:
            shutil.copyfile(filenameLOAN, Workdir+nameLN)
        
        
        # os.popen(f"cp {filenameREPO} {Workdir}{nameRP}")
        # os.popen(f"cp {filenameLOAN} {Workdir}{nameLN}")
        
       
        filenameREPO = abspath(Workdir+ nameRP)
        filenameLOAN = abspath(Workdir+ nameLN)
        
        try:
            dataframe=pd.read_csv(filenameREPO, sep = ";", encoding = "latin1")  
            if "Available" not in dataframe.columns:
                dataframe["Available"] = ["Yes" for i in dataframe.index]
            dataframe = dataframe.replace(np.nan, '', regex=True)
            dataframe = dataframe.astype(str)
            dataframeLoan = pd.read_csv(filenameLOAN, sep = ",", encoding = "latin1")    
            dataframeLoan = dataframeLoan.replace(np.nan, '', regex=True)
            dataframeLoan = dataframeLoan.astype(str) 
            
        except:
            pass
        filenameREPO=filenameREPO[:-4] + "NEW.csv" #it is necessary for problem of permission create a new file. I didn't manage to do otherwise
        #breakpoint()
        with open(filenameREPO, "w", encoding = "latin1" ) as f:
            dataframe.to_csv(f, sep =",", index = False)
            
        with open(filenameLOAN, "w", encoding = "latin1" ) as f:
            dataframeLoan.to_csv(f, sep =",", index = False)
        
        init.filenameREPO = filenameREPO
        init.filenameLOAN = filenameLOAN
        init.dataframeLoan = dataframeLoan
        init.dataframe=dataframe
        
        #create a setup folder to record the setup
        if not os.path.exists(Workdir +".setup"): os.makedirs(Workdir +".setup")
        with open(Workdir+".setup//parameter.txt", "w") as f:
            f.write(filenameREPO + "," +filenameLOAN + "\n")
        #breakpoint()
        
        newWin(init.dataframe, init.dataframeLoan, init.filenameREPO, credentials, variableString,initRP)
        
def make_password(password, salt):    #PBKDFHMAC generate a good password froma a password we pass, generating an hashing with salt(random hash) and then enctrypted in base64
	kdf = PBKDF2HMAC(
		algorithm=hashes.SHA256(),
		length=32,
		salt=salt,
		iterations=100000,
		backend=default_backend()
	)
	return base64.urlsafe_b64encode(kdf.derive(password))
    
def createAccount(get_user,get_pwd, win, initRepo, newWin, REMOTE ="No",):  
    global credentials
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
    if REMOTE =="yes":
        if not os.path.exists("Z:\\RMbiblio"): os.makedirs("Z:\\RMbiblio")
        WorkDir = "Z:\\RMbiblio\\"  
    else:
        Workdir = os.getcwd() + "\\"
    if not os.path.exists(Workdir +".setup"): os.makedirs(Workdir +".setup")
    with open(Workdir+".setup\\credentials.txt", "w") as cred:
         cred.write(cipher_text_utf8)
    win.destroy()
    initRepo(filenameREPO, filenameLOAN, newWin)
   

def openPWDrequest(functionForTheRequests, credentials, *args):
    

    pwdWindow = tk.Toplevel()
    pwdWindow.iconbitmap('Seminario_RM.ico')
    pwdWindow.title("Credentials required")
    #pwdWindow.geometry("100x200")
    access = tk.Label(pwdWindow, text = "Insert password").grid(row=0, column=1,sticky = "WE", padx=10)
    user = tk.Label(pwdWindow, text = "Username").grid(row=1, column=0,sticky = "WE", padx=10)
    get_user = tk.Entry(pwdWindow, textvariable = credentials["USER"]).grid(row=1, column=1, sticky = "WE", padx=10)
    pwd = tk.Label(pwdWindow, text = "Password").grid(row=2, column=0,sticky = "WE", padx=10)
    get_pwd = tk.Entry(pwdWindow, textvariable = credentials["PASSWORD"], show="*").grid(row=2, column=1, sticky = "WE", padx=10, pady=10)
    done = tk.Button(pwdWindow, text = "done", command = lambda: controlPWD(credentials["USER"], credentials["PASSWORD"], pwdWindow,functionForTheRequests, *args)).grid(row=3,column=2, padx = 10, pady=30)

def controlPWD(get_user, get_pwd, pwd, functionForTheRequests, *args, REMOTE = "No"):
    global credentials
    
    username=get_user.get()
    password=get_pwd.get()
    get_user.set("")
    get_pwd.set("")
    
    InsertedCredentials = [username,password]
    if REMOTE =="yes":
        if not os.path.exists("Z:\\RMbiblio"): os.makedirs("Z:\\RMbiblio")
        WorkDir = "Z:\\RMbiblio\\"  
    else:
        Workdir = os.getcwd() + "\\"
        
    Workdir = Workdir +".setup\\"
    with open(Workdir +"credentials.txt", "r") as cred:
        Credentials = cred.read()
    
    
    salt = base64.b64decode(Credentials[:24].encode("utf-8"))
    cipher_suite = Fernet(make_password(InternalPassword, salt))
    plain_text = cipher_suite.decrypt(Credentials[24:].encode("utf-8"))
    Credentials = plain_text.decode("utf-8")
    Credentials = io.StringIO(Credentials)
    Credentials = Credentials.read().splitlines()
    
    for i in range(len(Credentials)):
        Credentials[i] = Credentials[i].split(",")
    
    if Credentials[0] == InsertedCredentials:
        access = tk.Label(pwd, text = "correct credentials").grid(row=3, column=1,sticky = "WE", padx=10, pady=30)
        functionForTheRequests(*args)
        pwd.destroy()   
    else: 
        control = False
        access = tk.Label(pwd, text = "Access denied").grid(row=3, column=1,sticky = "WE", padx=10, pady=30)
        
        return None
  
    #initiializing warning message
    
def warning(message, function = None, Continue ="No"):
    
    Warn = tk.Toplevel()
    Warn.iconbitmap('warn.ico')
    Warn.title("WARNING") 
    access = tk.Label(Warn, text = message).grid(row=0, column=0,sticky = "WE", padx=10)
    if Continue == "Yes":    
        ok = tk.Button(Warn, text = "Continue", command =lambda: [function, Warn.destroy]).grid(row=1,column=0, padx = 10, pady=30)
    No = tk.Button(Warn, text = "Canceal", command = Warn.destroy).grid(row=1,column=1, padx = 10, pady=30)
    