import tkinter as tk
import os
from treview import treview
import initizializers as init
from tabulate import tabulate
from tkscrolledframe import ScrolledFrame
import tkinter.scrolledtext as tkscrolled
import tkinter.ttk as ttk
import requests
import webbrowser
import ActOnRepo as act
from treviewClass import treview as tw
#import initizializer as init
#functions executed by the buttons

def merging_search(field, strfield, df):
    
  
    name = field.get()
    if name=="":
        return df
    else:
        name = str(name)
      
        position = df[strfield].str.contains(name, case = False)
        field.set("")
        rank = df[position]
        return rank
    

def to_string(df, strfield):
    global dataframe
    global dataframeLoan  
    global window
    
    if df.equals(init.dataframe)==True:
        return f"No search for {strfield}"
    else:
        
        rank = tabulate(df, headers = 'keys', tablefmt = 'simple')
        answer = f"The search for {strfield} field has found this match:\n" + rank
        return answer
    

def search(dataframe, dataframeLoan, window,container, canvas, scrollbar):
    
    
    dfReturns={}
    
    for key, val in init.variableString.items():
        dfReturns[f"df{key}"] = merging_search(val, key, init.dataframe)
    
     
    Resultsdf = dfReturns[f"df{dataframe.columns[0]}"]
    for val in list(dfReturns.values())[1:]:
        Resultsdf = Resultsdf[Resultsdf.isin(val)].dropna()
    
    positionINcanvasRow = 7
    GeneralAnswer = Resultsdf
    for key, val in init.variableString.items():
        if key == init.SpecialVar["Title"]:
            Title = dfReturns[f"df{key}"]
            if not Title.equals(init.dataframe)==True:
                LabelTitle = ttk.Label(window, text = f"The search for {key} has found this match:").grid(row=positionINcanvasRow, column=0, columnspan= 20, sticky= "WE")
                treview(window, Title, init.variableString, positionINcanvasRow+1,0, 10,2)
                positionINcanvasRow=positionINcanvasRow+4
            else:
                LabelTitle = ttk.Label(window, text = f"No search for {key}.").grid(row=positionINcanvasRow, column=0, columnspan= 20, sticky= "WE") 
                positionINcanvasRow=positionINcanvasRow+1
        if key == init.SpecialVar["Author"]:
            Author = dfReturns[f"df{key}"]
            if not Author.equals(init.dataframe)==True:
                LabelAuthor = ttk.Label(window, text = f"The search for {key} has found this match:").grid(row=positionINcanvasRow, column=0, columnspan= 1, sticky= "WE")
                treview(window, Author, init.variableString,positionINcanvasRow+1,0,10,2)
                positionINcanvasRow=positionINcanvasRow+4
            else:
                LabelAuthor = ttk.Label(window, text = f"No search for {key}.").grid(row=positionINcanvasRow, column=0, columnspan= 1, sticky= "WE")
                positionINcanvasRow=positionINcanvasRow+1
                
    if not GeneralAnswer.equals(init.dataframe) == True:           
        LabelGeneral = tk.Label(window, text = "The search for All Fields has found this match:").grid(row=positionINcanvasRow, column=0, columnspan= 1, sticky= "WE")
        
        treview(window, GeneralAnswer, init.variableString, positionINcanvasRow +1,0,10,4)
    else:
        LabelGeneral = tk.Label(window, text = "Are you sure you are searching something?").grid(row=positionINcanvasRow, column=0, columnspan= 1, sticky= "WE")
        
    
    container.grid(row = 8, column=0, columnspan = 6)
    canvas.grid(row = 8, column=2, columnspan =10)
    scrollbar.grid(row=8, column=20, rowspan = 20, sticky=tk.S + tk.E + tk.N)

def online_search(variableString):
    request = ""
    for value in variableString.values():
        request += f"{value} "
    webbrowser.open(f"https://www.google.com/search?q={request}&oq={request}&aqs=edge..69i57j69i60l3.478j0j4&sourceid=chrome&ie=UTF-8")



    