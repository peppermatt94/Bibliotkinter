# -*- coding: utf-8 -*-
"""
Created on Sat May  1 22:20:17 2021

@author: pepermatt94
"""

import tkinter as tk
import pandas as pd
from PIL import Image, ImageTk

# biblio = {"Title": ["harry potter", "Il codice da vinci","il Signore degli anelli"], "Author": ["Rowling", "Brown", "Tolkien"], "Position" : ["a55", "b2","d3"], "Editorial" : ["la fenice", "Erudita", "Oxford Express"], "Year": [1990, 2002, 1997]}
# dataframe = pd.DataFrame(biblio)
# with open("C:\\Users\\pepermatt94\\OneDrive\\Libri Magistrale\\SOFTWARE and COMPUTING\\biblio.txt", 'w') as f:
#         f.write(dataframe.to_string(index=False))


dataframe=pd.read_csv("biblio.txt", sep = "\t")
dataframe = dataframe.astype(str)

window = tk.Tk()
window.title("Biblio")
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
    
def merging_search(field, strfield):
    name = field.get()
    if name=="":
        return dataframe
    else:
        position = dataframe[strfield].str.contains(name, case = False)
        field.set("")
        rank = dataframe[position]
        return rank

def to_string(df, strfield):
    if df.equals(dataframe)==True:
        return f"No search for {strfield}"
    else:
        rank = df.to_string(index=False)
        answer = f"the search for {strfield} field has found this match:\n" + rank
        return answer
    

def search():
    dfTitle = merging_search(Title, "Title")
    dfAuthor = merging_search(Author, "Author")
    dfYear = merging_search(Year, "Year")
    dfEdit = merging_search(Editorial, "Editorial")
    Resultsdf = dfTitle.merge(dfAuthor.merge(dfYear.merge(dfEdit)))
    
    GeneralAnswer = to_string(Resultsdf, "all")
    answerTitle = to_string(dfTitle, "Title")
    answerAuthor = to_string(dfAuthor, "Author")
    answerYear = to_string(dfYear, "Year")
    answerEdit = to_string(dfEdit, "Editorial")
    
    
    answer = GeneralAnswer+ "\n\n\n" +answerTitle + "\n\n\n" + answerAuthor+"\n\n\n"+answerYear+"\n\n\n"+ answerEdit
    text = tk.Text(window)
    text.insert(tk.END, answer)
    text.grid(row=6, column=1, columnspan= 1, sticky= "WE")
    scroll = tk.Scrollbar(text)
    
def add_book():
    global dataframe
    title=Title.get()
    author=Author.get()
    year=Year.get()
    position=Position.get()
    edit=Editorial.get()
    with open("C:\\Users\\pepermatt94\\OneDrive\\Libri Magistrale\\SOFTWARE and COMPUTING\\RMbiblio\\Biblio.txt", 'w') as f:
        book_to_append = {"Title": [title], "Author": [author], "Position" : [position], "Editorial" : [edit], "Year": [year]}
        book_to_append = pd.DataFrame(book_to_append)
        dataframe = dataframe.append(book_to_append)
        #dataframe = dataframe.sort("Title")
        dataframe.to_csv(f, sep = "\t", index = False)

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

button = tk.Button( text = "Search", command=search).grid(row = 3,column=2)
button2 = tk.Button(text = "Add to repository", command = add_book).grid(row=4,column=2)


#if __name__ == '__main__':
window.mainloop()
