import tkinter as tk
from tkinter import Grid, Misc
from tkinter import filedialog as fd
import json

class Item(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(master=parent, *args, **kwargs)
        
        topFrame = tk.Frame(self, width=3200, height=32, bg='lightblue')
        topFrame.pack(side=tk.TOP)
        
        middleFrame = tk.Frame(self, width=3200, height=200, bg='blue')
        middleFrame.pack()

class Main:
    def __init__(self):
        # GUI Setup
        self.canvasHolder = tk.Frame(root, width=100, height=100, highlightbackground='black', highlightthickness=2, relief=tk.SUNKEN, border=3)
        self.canvasHolder.grid(sticky='nesw', row=0, column=0)
        
        self.buttonFrame = tk.Frame(root, bg='lightgray', width=000, height=1000, highlightbackground='black', highlightthickness=1)
        self.buttonFrame.grid(sticky='nesw', row=1, column=0)
        
        self.listFrame = tk.Frame(root, width=100, height=100, highlightbackground='black', highlightthickness=1)
        self.listFrame.grid(sticky='nesw', row=0, column=1, rowspan=2)
        
        operatorCanvas = tk.Canvas(self.canvasHolder, width=600, height=940)
        operatorCanvas.pack(side=tk.LEFT)
        
        scrollbar = tk.Scrollbar(self.canvasHolder, command=operatorCanvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=(60, 10), padx=(0, 2), before=operatorCanvas)
        
        self.mainFrame = tk.Frame(operatorCanvas, width=1000, height=940)
        self.mainFrame.bind('<Configure>', lambda e: operatorCanvas.configure(scrollregion=operatorCanvas.bbox('all')))
        
        operatorCanvas.create_window((0, 0), window=self.mainFrame, anchor=tk.N)
        operatorCanvas.configure(yscrollcommand=scrollbar.set)
        
        
        # Add the buttons to the button frame
        addButton = tk.Button(self.buttonFrame,text="Add New...").grid(row=0, column=0, padx=8, pady=8, ipadx=20)
        
        test = Item(self.mainFrame, width=600, height=180, bg='black', border=2, relief=tk.GROOVE)
        test.pack()
        
        
        
        
       




root = tk.Tk()
root.title("Data-Gen")
root.geometry('720x960')

root.update()

root.resizable(False, True)

Grid.rowconfigure(root,0,weight=3)
Grid.columnconfigure(root,0,weight=3)
Grid.rowconfigure(root,1,weight=0)
Grid.columnconfigure(root,1,weight=1)

Main()

root.mainloop()