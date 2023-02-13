import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkinter.filedialog import asksaveasfilename
from filetrade import *

# create the root window
root = tk.Tk()
root.title('Tkinter Open File Dialog')
root.resizable(False, False)
root.geometry('300x150')


def import_file():
    """
    Asks the user which file to import and imports said file to be used
    """
    filetypes = (
        ('All Files', '*.*'),
        ('Config Files', '*.json')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)

    #Importing the file
    importjson(filename)
    
    if filename:
        showinfo(
            title='Selected File',
            message=filename
        )
    
def save_file():
    """
    Asks the user for where to export a file to
    """
    file = fd.asksaveasfilename(
        defaultextension='.json', 
        filetypes=[("Config Files", '*.json')],
        title="Choose filename")
    
    #exporting the file
    exportjson(file)
    
    if file:
        showinfo(
            title='Save File',
            message="File has been saved"
        )

#import button
open_button = ttk.Button(
    root,
    text='Import',
    command=import_file
)

#export button
save_button = ttk.Button(
    root,
    text='Export',
    command=save_file
)

open_button.pack(expand=True)
save_button.pack(expand=True)


# run the application
root.mainloop()