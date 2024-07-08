import tkinter as tk
from tkinter import Grid
from tkinter import filedialog as fd
import json

class Item(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(master=parent, *args, **kwargs)
        
        WIDTH = 580
        
        topFrame = tk.Frame(self, width=WIDTH, height=40, bg='lightblue', highlightbackground='black', highlightthickness=2)
        topFrame.pack(side=tk.TOP)
        topFrame.pack_propagate(False)
        
        middleFrame = tk.Frame(self, width=WIDTH, height=200, bg='blue')
        middleFrame.pack()
        
        deleteButton = tk.Button(topFrame, text='⛝', font=('Cascadia Code', 12), width=3, height=1, fg='red').pack(side=tk.LEFT, anchor=tk.W, padx=5, pady=2)

class Main:
    def __init__(self):
        # GUI Setup
        self.canvasHolder = tk.Frame(root, width=100, height=100, highlightbackground='black', highlightthickness=2, relief=tk.SUNKEN, border=3)
        self.canvasHolder.grid(sticky='nesw', row=0, column=0)
        
        self.buttonFrame = tk.Frame(root, bg='lightgray', width=400, height=200, highlightbackground='black', highlightthickness=1)
        self.buttonFrame.grid(sticky='nesw', row=1, column=0)
        
        self.listFrame = tk.Frame(root, width=400, height=100, highlightbackground='black', highlightthickness=1)
        self.listFrame.grid(sticky='nesw', row=0, column=1, rowspan=2)
        
        operatorCanvas = tk.Canvas(self.canvasHolder, width=600, height=940)
        operatorCanvas.pack(side=tk.LEFT, fill=tk.Y, expand=True)
        
        scrollbar = tk.Scrollbar(self.canvasHolder, command=operatorCanvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=(60, 10), padx=(0, 2), before=operatorCanvas)
        
        self.mainFrame = tk.Frame(operatorCanvas, width=1000, height=940)
        self.mainFrame.bind('<Configure>', lambda e: operatorCanvas.configure(scrollregion=operatorCanvas.bbox('all')))
        
        operatorCanvas.create_window((0, 0), window=self.mainFrame, anchor=tk.N)
        operatorCanvas.configure(yscrollcommand=scrollbar.set)
        
        
        # Add the buttons to the button frame
        addButton = tk.Button(self.buttonFrame,text="Add New...").grid(row=0, column=0, padx=8, pady=8, ipadx=20)
        
        test = Item(self.mainFrame, height=180, bg='black', border=2, relief=tk.GROOVE)
        test.pack()
        
        tk.Label(self.mainFrame, text="This program is still\n in development!", font=("idk", 32)).pack()




root = tk.Tk()
root.title("Data-Gen")
root.geometry('1000x1080')

root.update()

Grid.rowconfigure(root,0,weight=10)
Grid.columnconfigure(root,0,weight=10)
Grid.rowconfigure(root,1,weight=3)
Grid.columnconfigure(root,1,weight=3)

Main()

root.resizable(False, True)
root.mainloop()