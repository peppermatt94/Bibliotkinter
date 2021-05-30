
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
import tkinter.tix as tix

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
    global SpecialVar
    global StringOfRestitution
    global variableString
    global LabelField
    SpecialVar={}
    dataframe=None
    dataframeLoan=None
    window = None
    variableString={}
    LabelField = {}
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
        header={}
        with open(filenameREPO, "w", encoding = "latin1" ) as f:
            #header = {"Title": [], "Author": [], "Position" : [], "Editorial" : [], "Year": [], "Available": []}
            for key, values in variableString.items():
                header[key]= [] 
            header["Available"] = []
            header = pd.DataFrame(header)
            header.to_csv(f, sep = ";", index = False) 
            
        with open(filenameLOAN, "w", encoding = "latin1" ) as f:
            header = {"Keeper": [], "Adress": [], "Title": [], "Author": [], "Position" : [],"Contact" :[], "Date of loan" : [], "Date of restitution":[]}
            header = pd.DataFrame(header)
            header.to_csv(f, sep=";", index = False) 
        try:
            dataframe=pd.read_csv(filenameREPO, sep = ";",encoding = "latin1")    
            dataframe =dataframe.replace(np.nan, '', regex=True)
            dataframe = dataframe.astype(str)
            dataframeLoan = pd.read_csv(filenameLOAN, sep = ";", encoding = "latin1")
            dataframeLoan = dataframeLoan.replace(np.nan, '', regex=True)
            dataframeLoan = dataframeLoan.astype(str)
        except:
            print("I didn't manage to load the dataframe")
        init.dataframe = dataframe
        init.dataframeLoan = dataframeLoan
        parameter( win,Workdir, newWin)

def parameter( win, Workdir,newWin): 
             
        if not os.path.exists(Workdir+".setup"): 
            os.makedirs(Workdir +".setup")
            ctypes.windll.kernel32.SetFileAttributesW(".setup", 2)
        with open(Workdir + ".setup\\parameter.txt", "w") as f:
            f.write(filenameREPO + "," +filenameLOAN +","+SpecialVar["Title"].get()+"," +SpecialVar["Author"].get()+","+SpecialVar["Position"].get()+"\n")        
        
        SpecialVar["Title"] = SpecialVar["Title"].get()
        SpecialVar["Author"] = SpecialVar["Author"].get()
        SpecialVar["Position"] = SpecialVar["Position"].get()
        win.destroy()
        newWin(dataframe, dataframeLoan, filenameREPO, credentials, variableString, window)
    
def initializerREPO(filenameREPO, filenameLOAN, newWin):
    global dataframe
    global dataframeLoan  
    
   
    initRP = tk.Tk()
    access = tk.Label(initRP, text = "Create a repository or choose one from your computer.").grid(row=0, column=1,sticky = "WE", padx=10, pady=10)
    
    NameRP =tk.StringVar(initRP)
    NameLN =tk.StringVar(initRP)
    
    accessRP = tk.Label(initRP, text = "Book repository").grid(row=1, column=0,sticky = "WE", padx=10, pady=10)
    accessLN = tk.Label(initRP, text = "Loan repository").grid(row=2, column=0,sticky = "WE", padx=10, pady=10)
    
    nameF = tk.Entry(initRP, textvariable = NameRP).grid(row=1, column=1, sticky = "WE", padx=10)
    roomF = tk.Entry(initRP, textvariable = NameLN).grid(row=2, column=1, sticky = "WE", padx=10)

    chooseRP = tk.Button(initRP, text = "Choose files in your computer", command =lambda: browse(initRP,newWin)).grid(row=1,column=2, padx=10, pady = 10)
    CreateRP = tk.Button(initRP, text = "Create a repository for book", command =lambda: format_repository(initRP,NameRP, NameLN, newWin)).grid(row=2,column=2, padx=10, pady = 10)
    
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
    global variableString
    filenameREPO =  filedialog.askopenfilename(initialdir = "/",title = "Select file for your repository",filetypes = (("csv files","*.csv"),("all files","*.*")))
    filenameLOAN = filedialog.askopenfilename(initialdir = "/",title = "Select file for your loan",filetypes = (("csv files","*.csv"),("all files","*.*")))
    
    
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
            dataframeLoan = pd.read_csv(filenameLOAN, sep = ";", encoding = "latin1")    
            dataframeLoan = dataframeLoan.replace(np.nan, '', regex=True)
            dataframeLoan = dataframeLoan.astype(str) 
            
        except:
            pass
        try:
            with open(filenameREPO, "w", encoding = "latin1" ) as f:
                dataframe.to_csv(f, sep =";", index = False)
        except:
            filenameREPO=filenameREPO[:-4] + "NEW.csv" #it is necessary for problem of permission create a new file. I didn't manage to do otherwise
            with open(filenameREPO, "w", encoding = "latin1" ) as f:
                dataframe.to_csv(f, sep =";", index = False)
        with open(filenameLOAN, "w", encoding = "latin1" ) as f:
            dataframeLoan.to_csv(f, sep =";", index = False)
        
        init.filenameREPO = filenameREPO
        init.filenameLOAN = filenameLOAN
        init.dataframeLoan = dataframeLoan
        init.dataframe=dataframe
        variableString={}
        for i in dataframe.columns:
            variableString[i] = tk.StringVar()
            variableString[i].set(i)
        
        select_Special_columns(initRP, parameter, Workdir, newWin)
        
        # #create a setup folder to record the setup
        # if not os.path.exists(Workdir +".setup"): os.makedirs(Workdir +".setup")
        # with open(Workdir+".setup//parameter.txt", "w") as f:
        #     f.write(filenameREPO + "," +filenameLOAN + "\n")
        # #breakpoint()
        
        # #newWin(init.dataframe, init.dataframeLoan, init.filenameREPO, credentials, variableString,initRP)
        
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
    if not os.path.exists(Workdir +".setup"): 
        os.makedirs(Workdir +".setup")
        ctypes.windll.kernel32.SetFileAttributesW(".setup", 2)
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
    
def format_repository(win,NameRP, NameLN, NewWin):
    global variableString
    win.destroy()
    formatWin = tk.Tk()
    variableString={}
    
    explain=tk.Label(formatWin,text = "Choose the name and the number of the columns").grid(row=0, column=0, columnspan =12)
    plusButton = tk.Button(formatWin, text="Add column",height =1, width=10, command = lambda: Add_Entry_in_format_win(formatWin)).grid(row = 1, column = 0, columnspan=2 )
    subtractButton = tk.Button(formatWin, text="Del column", height =1, width=10,command = lambda: subtract_entry_in_format_win(formatWin)).grid(row = 1, column = 2, columnspan=2 )
    applyButton = tk.Button(formatWin, text="Apply",height =1, width=10, command = lambda: select_Special_columns(formatWin, add_repository, NameRP, NameLN, NewWin)).grid(row = 1, column = 4, columnspan=2 )
    info =tk.Label(formatWin,text = "*An 'Available' field is alreeady present in reposotory").grid(row=2, column=0, columnspan =12)
    formatWin.mainloop()
    
def Add_Entry_in_format_win(win):
    
    global variableString
    number= len(variableString)
    variableString[f"{number+1}"] = tk.StringVar(win)
    LabelField[f"{number+1}"] = tk.Label(win, text = f"{number+1}^st col. name").grid(row = number+3, column = 0, columnspan = 1, padx = 5)
    RequestsFields[f"{number+1}_entry"] = tk.Entry(win, textvariable= variableString[f"{number+1}"]).grid(row = number+3, column = 2, columnspan = 6)
    
    
def subtract_entry_in_format_win(win):
    global variableString
    number = len(variableString)
    
    try:
        del variableString[f"{number}"]
        win.grid_slaves()[0].destroy()
        win.grid_slaves()[0].destroy()
    except:
        pass
    
def select_Special_columns(win,  function, *args):
    global window
    if not win == window:
        win.destroy()
    
    global variableString
    message = "You are loading a database with the following fields:\n"
    for key, values in variableString.items():
        message = message + f"{values.get()}\t"
    tmpDict = variableString
    variableString = {}
    for key, values in tmpDict.items():
        variableString[values.get()] = tmpDict[key]
    message = message+ "\nYou must pick up among the given fields the special fields of Title, Author and Position"
    message2="*Please be precise and rewritten the field perfectly in the same way, also in the case and special characters"
    specialFieldsWin = tk.Tk() 
    tk.Label(specialFieldsWin, text = message).pack()
    for i in ["Title", "Author", "Position"]:
        SpecialVar[i] = tk.StringVar(specialFieldsWin)
        tk.Label(specialFieldsWin, text = f"pick the {i} field:").pack()
        tk.Entry(specialFieldsWin, textvariable = SpecialVar[i]).pack() 
    tk.Label(specialFieldsWin, text=message2).pack()
    applyButton = tk.Button(specialFieldsWin, text="apply", command = lambda: function(specialFieldsWin,*args)).pack()
    specialFieldsWin.mainloop()
    
def trial():
    for key,value in SpecialVar.items():
        print(key,value.get())
# init()    
# format_repository()



