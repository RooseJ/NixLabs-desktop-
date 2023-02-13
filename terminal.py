import tkinter as tk
from tkinter import *
from router import Router
from switch import Switch
import os
from sys import platform
from filetrade import startup, find_device_names


class ConsoleText(tk.Text, Router, Switch):
    def __init__(self,master=None,name=None):
        # self.name = clicked.get()
        self.cmdline = ">"
        self.command = []
        self.previouscmd = []
        self.commandlist = {
            "enable":self.enable,
            "hostname":self.change,
            "nslookup":self.show,
            "ping":self.ping,
            "copy":{"running-config": {"startup-config":self.copy}, 
                    "startup-config": {"running-config":self.copy}},
            "show":self.show,
            "ip":{"address":self.changeip},
        }
        # print(self)
        
        if name[0].lower() == 'r':
            self.device = Router(name)
        else:
            self.device = Switch(name)
        
        self.name = name

        tk.Text.__init__(self,master, bg='black', fg='white', insertbackground='white',padx=0,pady=0)
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
        # binding to CTRL+Z key
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
        self.command = self.get('input', 'end').strip().split()

        # execute code
        print("This is the command ",self.command)
        self.checkcomm(self.command)
 
        # display next prompt
        self.insert('end', '\n\n' 
                    + self.name + self.cmdline+' ')
        self.see('end')
        # move input mark
        self.mark_set('input', 'insert')
        return "break" # don't execute class method that inserts a newline
    
    def exit(self, event):
        
        if self.cmdline == "#(":
            self.cmdline = ">"
        else:
            self.invalid()
            

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
                        break
                    
                else:
                    self.invalid()
                
    def enable(self):
        if self.cmdline == ">":
            self.cmdline = "#"
            
    def invalid(self):
        print("command is invalid")
        self.insert('end', '\n\nUnknown command')
        self.see('end')
        # move input mark
        self.mark_set('input', 'insert')
        
        return "break"
        
    def show(self):
        showlist = ["name","version","ip","hostname","subnet","os","mask"]
        cmd = self.command[-1]
        print(cmd)
        if cmd == "neighbors":
            temp = self.device.show("links")
            self.insert('end', '\n\n'+temp)
            return
        
        if not(cmd in showlist):
            self.insert('end', '\n\nValue does not exist')
            return
               
        temp = self.device.show(cmd)
        self.insert('end', '\n\n'+temp)
        
    def ip(self):
        self.insert('end', '\n\n'+self.device.ip4+'\n')
        
    # def changehostname(self):
    #     if len(self.command) != 2:
    #         return self.invalid()
    #     temp = self.command[1]
    #     self.device.changehostname(temp)
        
    def changeip(self):
        if len(self.command) != 4:
            return self.invalid()
        new_ip = self.command[2]
        new_mask = self.command[3]
        self.device.change_attr("ip4",new_ip)
        self.device.change_attr("mask",new_mask)
        
    
    def ping(self):
        host = ''.join(self.command[1::])
        # host = self.command[-1]
        if platform == "win32":
            count = '-n'
        else:
            count = '-c'
            
        devicenames = find_device_names()
        if host.lower() in devicenames:
            host = "www.google.com"
        output = os.popen("ping "+count+" 3 "+host).read()
        self.insert('end', '\n\n'+output)
        
    
    def change(self):
        key = self.command[0]
        val = self.command[-1]
        self.device.change_attr(key,val)
        
    def copy(self):
        if self.command[-1][0] == 'r':
            opt = 1
        else:
            opt = 3
            
        startup(opt)
    

#For testing only terminal
class terminalwindow(object): #Container for the terminal
    def __init__(self, parent):
        # The "return value" of the dialog,
        # entered by user in self.entry Entry box.
        self.data = None

        self.root=parent
        # self.root.geometry('300x300')
        name = "Router 1"
        self.root.title('Terminal ('+name+')')

        self.tfield = ConsoleText(self.root,name)
        self.tfield.pack(expand=True, fill='both')


# root = Tk()
# app = terminalwindow(root)
# root.mainloop()