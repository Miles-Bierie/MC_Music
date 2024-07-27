import tkinter as tk
from tkinter import ttk
from tkinter import Grid
from tkinter import filedialog as fd
import tkinter.simpledialog as sd
import json
import pprint


class Prompt(tk.Label):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(master=parent, *args, **kwargs)
        
        self.format = tk.StringVar(self, ' ... ')
        
        self.config(textvariable=self.format)
        self.bind('<Button-1>', lambda e: self.get_format())

    def get_format(self):
        format = sd.askinteger('Pack Format', "Please enter pack format:")
        if format != None:
            self.format.set(format)

class Item(tk.Frame):
    _count = 0 # Stores how many items there are
    _incrament = 1
    _items = [] # Holds all items
    def __init__(self, parent, *args, **kwargs):
        super().__init__(master=parent, *args, **kwargs)
        
        WIDTH = 580
        
        topFrame = tk.Frame(self, width=WIDTH, height=40, bg='lightblue', highlightbackground='black', highlightthickness=2)
        topFrame.pack(side=tk.TOP)
        topFrame.pack_propagate(False)
        
        middleFrame = tk.Frame(self, width=WIDTH, height=200)
        middleFrame.pack()
        middleFrame.pack_propagate(False)
        
        middleLeftFrame = tk.Frame(middleFrame, height=200, width=200)
        middleLeftFrame.pack(side=tk.LEFT)
        middleLeftFrame.pack_propagate(False)
        
        middleRightFrame = tk.Frame(middleFrame, height=200, width=378)
        middleRightFrame.pack(side=tk.LEFT, anchor=tk.N)
        middleRightFrame.pack_propagate(False)
        
        self.songNameVar = tk.StringVar(self, "Item_" + str(Item._incrament))
        
        
        # Top frame
        tk.Button(topFrame, text='⛝', font=('Cascadia Code', 12), width=3, height=1, fg='red', command=self.try_delete).pack(side=tk.LEFT, anchor=tk.W, padx=5, pady=2) # Delete Button
        tk.Entry(topFrame, width=64, font=('Calibri', 14), textvariable=self.songNameVar, fg='blue').pack(side=tk.LEFT, padx=10)
        
        # Middle frame
        self.image = tk.PhotoImage(file='./icons/blank.png')
        
        self.imageButton = tk.Button(middleLeftFrame, image=self.image, height=100, width=100, command=self.image.get, relief=tk.FLAT, disabledforeground='white', highlightbackground='black', borderwidth=0)
        self.imageButton.pack(side=tk.TOP, anchor=tk.NW, padx=(50, 50), pady=(20, 0))
        self.imageButton.bind('<Button-1>', lambda e: self.open_image())

        self.modelDataVar = tk.StringVar() # Store the model data the user inputs
        
        tk.Label(middleLeftFrame, text="Custom model data:", font=('Calibri', 13)).pack(side=tk.LEFT, anchor=tk.SE, padx=2, pady=2)
        
        self.modelDataEntry = tk.Entry(middleLeftFrame, state=tk.NORMAL, width=8, font=('Calibri', 14), textvariable=self.modelDataVar)
        self.modelDataEntry.pack(side=tk.RIGHT, anchor=tk.SW, padx=2, pady=2)
        
        ttk.Separator(middleRightFrame, orient=tk.VERTICAL).pack(ipady=100, anchor=tk.NW)
        
        powerValues = list(range(16)) # 1 - 15
        self.powerValue = tk.StringVar()
        self.powerValue.set('0')
        
        self.audioVar = tk.StringVar()
        
        # Power row
        tk.Label(middleRightFrame, text='Power: ', font=('Calibri', 14)).grid(row=0, column=0, sticky=tk.W, padx=2)
        powerMenu = ttk.OptionMenu(middleRightFrame, self.powerValue, *powerValues)
        powerMenu.grid(row=0, column=1, sticky=tk.W)
        
        # Audio row
        dir = None
        tk.Label(middleRightFrame, text='Audio: ', font=('Calibri', 14)).grid(row=1, column=0, sticky=tk.W, padx=2)
        audioFileEntry = tk.Entry(middleRightFrame, width=18, font=('Calibri', 14), textvariable=self.audioVar)
        audioFileEntry.grid(row=1, column=1, sticky=tk.W)
        tk.Button(middleRightFrame, text='open...', font=('Calibri', 11), command= self.open_audio).grid(row=1, column=2, padx=4)
        
        # Description row
        tk.Label(middleRightFrame, text='Description: ', font=('Calibri', 14)).grid(row=2, column=0, sticky=tk.W, padx=2)
        self.descriptionText = tk.Text(middleRightFrame, width=18, font=('Calibri', 14))
        self.descriptionText.grid(row=3, column=0, sticky=tk.W, columnspan=3)
        
        Item._items.append(self)
        Item._incrament += 1
        Item._count += 1
        
    def open_audio(self):
        dir = fd.askopenfilename(
            title='Open audio file',
            filetypes=(('Ogg Vorbis', '*.ogg'),
                       ('Ogg Vorbis', '*.ogg'))
        )
        
        self.audioVar.set(dir if dir != '' else self.audioVar.get())
    
    def try_delete(self): # Delete item only if it is not the only one
        if Item._count > 1:
            Item._items.remove(self)
            self.destroy()
            
            Item._items[0].pack_configure(pady=(2, 4))
            
            Item._count -= 1
        
    def open_image(self):
        image = fd.askopenfilename(title="Open image file", filetypes=(('PNG Files', '*.png'),('PNG Files', '*.png')))
        
        if image == '':
            return
        
        self.image = tk.PhotoImage(file=image)
        if self.image.width() == 16:
            self.image = self.image.zoom(5)
        self.imageButton.configure(image=self.image)
        
    def get_name(self) -> str:
        return self.songNameVar.get()
        
    def compile(self) -> dict:
        return {
            'power': int(self.powerValue.get()),
            'audio': self.audioVar.get(),
            'description': self.descriptionText.get('0.0', tk.END).strip(),
            "texture": self.image.cget('file'),
            "model": int(self.modelDataVar.get())
        }
        
        # TODO: Make description jsonable


class Main:
    _count = 0
    def __init__(self):
        # GUI Setup
        self.dataFrame = tk.Frame(root, height=32).grid(row=4, column=0, sticky=tk.S)

        self.canvasHolder = tk.Frame(root, width=100, height=100, highlightbackground='black', highlightthickness=2, relief=tk.SUNKEN, border=3)
        self.canvasHolder.grid(sticky='nesw', row=0, column=0)
        
        self.buttonFrame = tk.Frame(root, bg='lightgray', width=400, height=300, highlightbackground='black', highlightthickness=1)
        self.buttonFrame.grid(sticky='nesw', row=1, column=0)
             
        self.listFrame = tk.Frame(root, width=400, height=100, highlightbackground='black', highlightthickness=1)
        self.listFrame.grid(sticky='nesw', row=0, column=1, rowspan=2)
        
        self.operatorCanvas = tk.Canvas(self.canvasHolder, width=600, height=940)
        self.operatorCanvas.pack(side=tk.LEFT, fill=tk.Y, expand=True)
        
        scrollbar = tk.Scrollbar(self.canvasHolder, command=self.operatorCanvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=(60, 10), padx=(0, 2), before=self.operatorCanvas)
        
        self.mainFrame = tk.Frame(self.operatorCanvas, width=1000)
        self.mainFrame.bind('<Configure>', lambda e: self.operatorCanvas.configure(scrollregion=self.operatorCanvas.bbox('all')))
        
        self.operatorCanvas.create_window((0, 0), window=self.mainFrame, anchor=tk.N)
        self.operatorCanvas.configure(yscrollcommand=scrollbar.set)
        
        
        # Add the buttons to the button frame
        addButton = tk.Button(self.buttonFrame,text="Add New...", command=self.add_new)
        addButton.grid(row=0, column=0, padx=8, pady=8, ipadx=20)
        
        clearButton = tk.Button(self.buttonFrame,text="Clear All", command=self.clear)
        clearButton.grid(row=0, column=1, padx=8, pady=8, ipadx=20)
        
        compileButton = tk.Button(self.buttonFrame,text="Compile", command=self.compile)
        compileButton.grid(row=0, column=2, padx=8, pady=8, ipadx=20)
        
        initialItem = Item(self.mainFrame, height=180, bg='black', border=2, relief=tk.GROOVE)
        initialItem.pack(padx=(2, 0), pady=(2, 4))

        
        # tk.Label(self.mainFrame, text="This program is still\n in development!", font=("idk", 32)).pack()
        
        # Data frame
        self.descriptionVar = tk.StringVar()
        self.itemVar = tk.StringVar()

        tk.Label(self.dataFrame, text="Datapack Format: ").grid(row=4, column=0)
        self.datapackFormatPrompt = Prompt(self.dataFrame, bg='lightgray', highlightbackground='black', highlightthickness=1)
        self.datapackFormatPrompt.grid(row=4, column=0, padx=(120, 0))
        
        tk.Label(self.dataFrame, text="Resourcepack Format: ").grid(row=4, column=1)
        self.resourcepackFormatPrompt = Prompt(self.dataFrame, bg='lightgray', highlightbackground='black', highlightthickness=1)
        self.resourcepackFormatPrompt.grid(row=4, column=1, padx=(145, 0))
        
        tk.Label(self.dataFrame, text="Description: ").grid(row=5, column=0)
        tk.Entry(self.dataFrame, width=64, font=('Calibri', 12), textvariable=self.descriptionVar).grid(row=6, column=0, pady=(0, 8))
        
        tk.Label(self.dataFrame, text="Item: ").grid(row=5, column=1)
        tk.Entry(self.dataFrame, textvariable=self.itemVar, width=32, font=('Calibri', 12)).grid(row=6, column=1, pady=(0, 8))
        
        
    def add_new(self) -> None:
        item = Item(self.mainFrame, height=180, bg='black', border=2, relief=tk.GROOVE)
        item.pack(padx=(2, 0), pady=4)
        
          
    def clear(self) -> None:
        for i in self.mainFrame.winfo_children():
            i.destroy()
        
        Item._count = 0
        Item._incrament = 1
        Item._items.clear()
        
        self.add_new()
        self.operatorCanvas.yview_moveto(0)
        
    def compile(self) -> None:
        file = fd.asksaveasfilename(title="Save file", filetypes=(("Json", '*.json'),("Json", '*.json')))
        
        # TODO: Check if all fields are filled out!
        
        if file != '':
            jsonDict = {
                "songs": {},
                "data": {}
            }
            
            jsonDict['data']["datapack_format"] = self.datapackFormatPrompt.cget('text')
            jsonDict['data']["resourcepack_format"] = self.resourcepackFormatPrompt.cget('text')
            
            if self.descriptionVar.get() != "":
                jsonDict['data']["description"] = self.descriptionVar.get()
            if self.itemVar.get() != "":
                jsonDict['data']["item"] = self.itemVar.get()
                
            for i in self.mainFrame.winfo_children():
                jsonDict['songs'][i.get_name()] = i.compile()
            
            pprint.pprint(file)
            with open(file, 'w') as f:
                f.write(str(jsonDict).replace("'", '"'))

root = tk.Tk()
root.title("Data-Gen")
root.geometry('1020x960')



Grid.rowconfigure(root,0,weight=10)
Grid.columnconfigure(root,0,weight=10)
Grid.rowconfigure(root,1,weight=0)
Grid.columnconfigure(root,1,weight=3)
Grid.rowconfigure(root,2,weight=0)

Main()

root.resizable(False, True)
root.mainloop()