import tkinter as tk
import pandas as pd
import os
from treview import treview
import initizializers as init
import SearchInRepo as search
import datetime
import numpy as np
#from initizializers import dataframe

def add_book(dataframe, dataframeLoan, variableString, filenameREPO):
    
    book_to_append = {}
    for key, value in variableString.items():
        book_to_append[key] = [value.get()]
        if key == init.SpecialVar["Title"]:
            SpecialVarTitle = value.get()
        if key == init.SpecialVar["Author"]: 
            SpecialVarAuthor = value.get()
        if key == init.SpecialVar["Position"]:
             SpecialVarPos = value.get()
        if key == "Available":
            book_to_append[key] = "Yes"
    
           
    if not init.dataframe[init.dataframe[init.SpecialVar["Position"]].isin([SpecialVarPos])].empty :
        init.warning("There is already a book in that position.\nIt's impossible that two book are in the same place.\nMaybe you missed something?")
        return None
    voidTesT = [values == [""] for values in book_to_append.values()]
    if all(voidTesT):
        message = "The fields cannot be all empty!!!"
        init.warning(message)
    else:
        if SpecialVarTitle == "" and SpecialVarAuthor == "" and SpecialVarPos == "":
            message = "You must add at least Title, Author and Position!!!"
            init.warning(message)
            return None
       
        with open(filenameREPO, 'w',  encoding = "latin1" ) as f:
            book_to_append = pd.DataFrame(book_to_append).dropna()
            dataframe = dataframe.append(book_to_append)
            dataframe = dataframe.astype(str)
            dataframe.to_csv(f, sep = ";", index = False)
            
        with open(filenameREPO, 'r') as f:
             dataframe=pd.read_csv(filenameREPO, sep = ";", encoding = "latin1")
             dataframe = dataframe.replace(np.nan, '', regex=True)
             dataframe = dataframe.astype(str)
             dataframe = dataframe.replace(np.nan, '', regex=True)
       
        init.dataframe = dataframe   
def explore_repository(dataframe, variableString):
    
    TextWin = tk.Toplevel()
    TextWin.title("REPOSITORY RM MEXICO")
    n_rows =1
    n_columns =1
    for i in range(n_rows):
        TextWin.grid_rowconfigure(i,  weight =1)
        for i in range(n_columns):
            TextWin.grid_columnconfigure(i,  weight =1)
    treview(TextWin, dataframe, variableString, 0,0,20,20)

def explore_loan_repository(dataframeLoan, StringOfRestitution):
   
   TextWin = tk.Toplevel()
   TextWin.title("REPOSITORY RM MEXICO")
   treview(TextWin, dataframeLoan, StringOfRestitution,0,0,20,20)


def eliminateBook(dataframe, filenameREPO,variableString):
    
    for key, value in variableString.items():
        if key == init.SpecialVar["Position"]:
            position = value.get()
            found_book =  init.dataframe[init.dataframe[key]==position]
          
    init.dataframe = init.dataframe.drop(labels=found_book.index, axis=0)
    with open(filenameREPO, 'w',  encoding = "latin1" ) as f:
            init.dataframe.to_csv(f, sep = ";", index = False)
    

def loan_id_insert(dataframe, dataframeLoan, variableString,filenameREPO, filenameLOAN):  
    
    for key, value in variableString.items():
        if key == init.SpecialVar["Position"]:
            position = value.get()
            found_book =  dataframe[dataframe[key]==position]
    message =""
    for i in [init.SpecialVar["Title"], init.SpecialVar["Author"], init.SpecialVar["Position"]]:
        message += str(dataframe[i].iloc[0]) + " "
    #message = found_book.to_string(index=False)
    loanWin = tk.Toplevel()
    loanWin.title("Loan")
    info = tk.Label(loanWin, text = f"you are loaning the book:\n{message}\n Insert the Id of receving").grid(row=0, column=2,columnspan = 5, sticky = "WE", padx=10)
    
    Name = tk.StringVar()
    Room = tk.StringVar()
    Contact = tk.StringVar()
    Day = tk.StringVar()
    Month = tk.StringVar()
    Year = tk.StringVar()
    Day.set("DD")
    Month.set("MM")
    Year.set(datetime.date.today().year)
    n_rows =10
    n_columns =20
    for i in range(n_rows):
        loanWin.grid_rowconfigure(i,  weight =1)
        for i in range(n_columns):
            loanWin.grid_columnconfigure(i,  weight =1)
            
    name = tk.Label(loanWin, text = "name and surname").grid(row=1, column=0,columnspan=2)
    nameF = tk.Entry(loanWin, textvariable = Name).grid(row=1, column=2, columnspan=5, sticky = "WE", padx=10)

    room = tk.Label(loanWin, text = "room/adress").grid(row=2, column=0, columnspan =2)
    roomF = tk.Entry(loanWin, textvariable = Room).grid(row=2, column=2, columnspan=5, sticky = "WE", padx=10)
    
    room = tk.Label(loanWin, text = "Contact").grid(row=3, column=0, columnspan =2)
    roomF = tk.Entry(loanWin, textvariable = Contact).grid(row=3, column=2, columnspan=5, sticky = "WE", padx=10)
    
    dateLab = tk.Label(loanWin, text = "Date\nrestitution").grid(row=4, column=0, columnspan=1, padx=1)
    dateEntry1= tk.Entry(loanWin, textvariable = Day, width=5).grid(row=4, column=2, columnspan =1, sticky = "WE", padx=1)
    
    dateLab = tk.Label(loanWin, text = "-").grid(row=4, column=4, columnspan = 1,padx=1)
    dateEntry1= tk.Entry(loanWin, textvariable = Month, width=5).grid(row=4, column=4, columnspan = 1, sticky = "WE", padx=1)
   
    dateLab = tk.Label(loanWin, text = "-").grid(row=4, column=5, columnspan=1, padx=1)
    dateEntry1= tk.Entry(loanWin, textvariable = Year, width=5).grid(row=4, column=6, columnspan=1, sticky = "WE", padx=1)
    
    
    take = tk.Button(loanWin, text = "insert", command=lambda: loan_the_book(found_book,Name, Room,Contact,Day, Month, Year,loanWin,dataframe, dataframeLoan, variableString, filenameREPO, filenameLOAN)).grid(row = 5,column=1, padx = 10, pady=30, columnspan = 3)
   
def loan_the_book(found, Name, Room,Contact, Day, Month, Year,win, dataframe, dataframeLoan, variableString, filenameREPO, filenameLOAN):
        
    nome = Name.get() 
    adress = Room.get()
    contact = Contact.get()
    day = Day.get()
    month = Month.get()
    year = Year.get()
    Name.set("")
    Room.set("")
    Day.set("DD")
    Month.set("MM")
    Year.set("")
    today = datetime.date.today()
                 
    for column in found.columns:
        if column == init.SpecialVar["Title"]:
            SpecialVarTitle = found[column][found.index]
        if column == init.SpecialVar["Author"]: 
            SpecialVarAuthor = found[column][found.index]
        if column == init.SpecialVar["Position"]:
             SpecialVarPos = found[column][found.index]
    today = f"{today.day}-{today.month}-{today.year}"
    book_to_append = {"Keeper": [nome], "Adress": [adress], "Title": SpecialVarTitle, "Author": SpecialVarAuthor, "Position" : SpecialVarPos, "Contact": [contact], "Date of loan" : [today], "Date of restitution" : [day+"-"+month+"-"+year]}
    
    book_to_append = pd.DataFrame(book_to_append)
    dataframeLoan = dataframeLoan.append(book_to_append)
    dataframeLoan["Date of restitution" ] =pd.to_datetime(dataframeLoan["Date of restitution" ])
    dataframeLoan=dataframeLoan.sort_values(by="Date of restitution", ascending = False) 
    with open(filenameLOAN, 'w', encoding = "latin1" ) as f:
            dataframeLoan.to_csv(f, sep = ";", index = False)
            
    
    dataframe["Available"][found.index] = "No"
    with open(filenameREPO, 'w', encoding = "latin1" ) as f:
        dataframe.to_csv(f, sep = ";", index = False, encoding = "latin1")
    
    with open(filenameLOAN, 'r') as f:
            dataframeLoan = pd.read_csv(f, sep = ";",  encoding = "latin1")
            dataframeLoan = dataframeLoan.replace(np.nan, '', regex=True)
            dataframeLoan = dataframeLoan.astype(str)  
    
    init.dataframeLoan = dataframeLoan
    win.destroy()      

def restitution_win(dataframeLoan, dataframe, filenameREPO, filenameLOAN, StringOfRestitution):    
    
    StringOfRestitution["Name"] = tk.StringVar()
    StringOfRestitution["Adress"]= tk.StringVar()
    StringOfRestitution["Title"]= tk.StringVar()
    StringOfRestitution["Author"] = tk.StringVar()
    StringOfRestitution["Position"]= tk.StringVar()
    
    restWin = tk.Toplevel()
    restWin.iconbitmap('Seminario_RM.ico')
    name = tk.Label(restWin, text = "name and surname").grid(row=1, column=0)
    nameF = tk.Entry(restWin, textvariable = StringOfRestitution["Name"] ).grid(row=1, column=1, sticky = "WE", padx=10)

    room = tk.Label(restWin, text = "room/adress").grid(row=2, column=0)
    roomF = tk.Entry(restWin, textvariable = StringOfRestitution["Adress"]).grid(row=2, column=1, sticky = "WE", padx=10)
        
    pos = tk.Label(restWin, text = "Position").grid(row=3, column=0)
    search_field_position = tk.Entry(restWin, textvariable =StringOfRestitution["Position"]).grid(row=3, column=1, sticky = "WE", padx=10)

    pos = tk.Label(restWin, text = "Author").grid(row=4, column=0)
    search_field_position = tk.Entry(restWin, textvariable =StringOfRestitution["Author"]).grid(row=4, column=1, sticky = "WE", padx=10)    

    title = tk.Label(restWin, text = "Title").grid(row=5, column=0)
    search_field_Title = tk.Entry(restWin, textvariable = StringOfRestitution["Title"]).grid(row=5, column=1, sticky = "WE", padx=10)

    take = tk.Button(restWin, text = "restitute", command=lambda: resa(StringOfRestitution,restWin,dataframeLoan,dataframe, filenameREPO, filenameLOAN)).grid(row = 1,column=2)

def resa(StringOfRestitution,win, dataframeLoan, dataframe, filenameREPO, filenameLOAN, REMOTE = "No"):
  
    dfname = search.merging_search(StringOfRestitution["Name"], "Keeper", init.dataframeLoan)
    dfroom = search.merging_search(StringOfRestitution["Adress"], "Adress", init.dataframeLoan)
    dfposition = search.merging_search(StringOfRestitution["Position"], "Position", init.dataframeLoan)
    dfTitle = search.merging_search(StringOfRestitution["Title"], "Title", init.dataframeLoan)
    dfAuthor = search.merging_search(StringOfRestitution["Author"], "Title", init.dataframeLoan)
    
    Resultsdf = dfTitle[dfTitle.isin(dfroom)].dropna()
    Resultsdf = Resultsdf[Resultsdf.isin(dfposition)].dropna()
    Resultsdf = Resultsdf[Resultsdf.isin(dfname)].dropna()
    
    init.dataframeLoan = init.dataframeLoan.drop(labels=Resultsdf.index, axis=0)
    
    with open(filenameLOAN, 'w', encoding = "latin1" ) as f:
            init.dataframeLoan.to_csv(f, sep = ";", index = False)
    with open(filenameLOAN, 'r') as f:
            dataframeLoan = pd.read_csv(f, sep = ";",  encoding = "latin1") 
            dataframeLoan = dataframeLoan.replace(np.nan, '', regex=True)
            dataframeLoan = dataframeLoan.astype(str)  
    for key, values in init.variableString.items():
        if key == init.SpecialVar["Title"]:
            indexes = dataframe[key]
           
    Index = indexes[indexes == Resultsdf["Title"][Resultsdf.index[0]]].index.tolist()    
    dataframe["Available"][Index] = "Yes"
    with open(filenameREPO, 'w', encoding = "latin1" ) as f:
        dataframe.to_csv(f, sep = ";", index = False)
        
    init.dataframe = dataframe
    init.dataframeLoan = dataframeLoan
    win.destroy()
 