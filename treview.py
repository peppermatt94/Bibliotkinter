# -*- coding: utf-8 -*-
"""
Created on Tue May 25 00:01:25 2021

@author: pepermatt94
"""
import tkinter as tk
import pandas as pd
from tkinter.font import Font
from tkinter import ttk
from tkscrolledframe import ScrolledFrame


enter = None
my_tree = None
def treview(root, dataframe, Entry, ROW, COLUMN, COLS, ROWS):
    global enter
    global my_tree
    enter = Entry
    style = ttk.Style()
    #breakpoint()
# Pick A Theme
    style.theme_use('default')

# Configure the Treeview Colors
    style.configure("Treeview",
                    kground="#D3D3D3",
                    eground="black",
                    height=25,
                    ldbackground="#D3D3D3")

    # Change Selected Color
    style.map('Treeview',
    	background=[('selected', "#347083")])
    
    
    
    tree_frame = tk.Frame(root)
    tree_frame.grid(row=ROW,column=COLUMN, columnspan= COLS, rowspan = ROWS)
    
    # Create a Treeview Scrollbar
    tree_scroll = tk.Scrollbar(tree_frame)
    tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    
    
    # Create The Treeview
    my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
    my_tree.pack()
    
    
    # Configure the Scrollbar
    tree_scroll.config(command=my_tree.yview)
    
    # Define Our Columns
    lista = []
    for i in dataframe.columns:
        lista.append(i)
    my_tree['columns'] = (lista)
    my_tree.column("#0", width=0, stretch=tk.NO)
    for i in dataframe.columns:
        exec(f"my_tree.column(i, anchor=tk.W, width = 100)")    
    # Create Headings
        exec(f"my_tree.heading(i, text = i, anchor=tk.W)")
    my_tree.heading("#0", text="", anchor=tk.W)
    
    # Create Striped Row Tags
    my_tree.tag_configure('oddrow', background="white")
    my_tree.tag_configure('evenrow', background="lightblue")
    query_database(dataframe, my_tree)
    my_tree.bind("<Double-1>", select_record)
   
def select_record(e):
    # Clear entry boxes
    for key, entry in enter.items():
        entry.set("")

    # Grab record Number
    selected = my_tree.focus()
    # Grab record values
    values = my_tree.item(selected, 'values')
    
    # outpus to entry boxes
    count = 0
    for key, entry in enter.items():
        entry.set(values[count])
        count+=1

    
def query_database(dataframe, my_tree):

    # Add our data to the screen
    global count
    count = 0
    record =0
    
    lista = []
    for record in dataframe.index:
        for i in dataframe.columns:
            lista.append(dataframe[i][record])
        if count % 2 == 0:
            my_tree.insert(parent='', index='end', iid=count, text='', values=(lista), tags=('evenrow',))
        else:
            my_tree.insert(parent='', index='end', iid=count, text='', values=(lista), tags=('oddrow',))
        lista =[]
        # increment counter
        count += 1

    



