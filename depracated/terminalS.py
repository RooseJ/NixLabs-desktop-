from imports import *
import tkinter as tk
from switch import Switch

class ConsoleTextS(tk.Text, Switch):
    cmdline = ">"
    
    def __init__(self,master=None, name=None):
        # self.name = object.name
        self.comlist = {
        "enable":self.enable,
        "hostname":0,
        "copy":["running-config", "startup-config"],
        "show":{"version":self.version},
        "":0,
        "":0,
        "":0,
        "":0,
        "":0,
        "":0,
        "":0,
        "":0,
        "":0
        }
        self.name = name
        self.commandlist = self.comlist
        tk.Text.__init__(self, master, bg='black', fg='white', insertbackground='white',padx=0,pady=0)
        self.insert('1.0', self.name + 
                    ' is now available \n\n\nPress RETURN to get started\n\n\n') # first prompt
        # create input mark
        self.mark_set('input', 'insert')
        self.mark_gravity('input', 'left')
        # create proxy
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)
        # binding to Enter key
        self.bind("<Return>", self.enter)
        self.bind("<Control-Key-z>", self.exit)

    def _proxy(self, *args):
        largs = list(args)

        if args[0] == 'insert':
            if self.compare('insert', '<', 'input'):
                # move insertion cursor to the editable part
                self.mark_set('insert', 'end')  # you can change 'end' with 'input'
        elif args[0] == "delete":
            if self.compare(largs[1], '<', 'input'):
                if len(largs) == 2:
                    return # don't delete anything
                largs[1] = 'input'  # move deletion start at 'input'
        result = self.tk.call((self._orig,) + tuple(largs))
        return result

    def enter(self, event):
        command = self.get('input', 'end').split()

        # execute code
        print("This is the command ",command)
        print("This is the command ",self.name)
        self.checkcomm(command)

            
        # display next prompt
        self.insert('end', '\n\n' 
                    + self.name + self.cmdline+' ')
        self.see('end')
        # move input mark
        self.mark_set('input', 'insert')
        return "break" # don't execute class method that inserts a newline
    
    def exit(self, event):
        
        if self.cmdline == self.downgrade[self.cmdline]:
            self.insert('end', '')
        
        self.insert('end', '\n<Command result>\n\n' 
                    + self.name + self.cmdline+' ')
        self.see('end')
        # move input mark
        self.mark_set('input', 'insert')
        
        return "break"
    
    ############################################################
    ################ The Commands Section ######################
    ############################################################
    # '>' for user mode, '#' for priviledged, '(config)#' for config mode
    
    def checkcomm(self, command):
        temp = self.commandlist
        if command != []:
            for x in command:
                if x in temp.keys():
                    if type(temp[x]) == dict:
                        temp = temp[x]
                        continue
                    else:
                        print("command is valid")
                        temp[x]()
                        print(self.cmdline)
                        break
                    
                else:
                    self.invalid()
                
    def enable(self):
        if self.cmdline == ">":
            self.cmdline = "#"
            
    def invalid(self):
        print("command is invalid")
        self.insert('end', '\n\nUnknown command\n')
        self.see('end')
        # move input mark
        self.mark_set('input', 'insert')
        
        return "break"
        
    def version(self):
        self.insert('end', '\n'+Switch.version+'\n')
    
    