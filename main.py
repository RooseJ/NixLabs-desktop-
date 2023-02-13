from imports import *
from terminal import *
from PIL import ImageTk, Image

#Dimensions
w = 400
h = 400
x = w/2
y = h/2

class simpledialog(object): #Container for the terminal
    def __init__(self, parent):
        # The "return value" of the dialog,
        # entered by user in self.entry Entry box.
        self.data = None

        self.root=Toplevel(parent)
        # self.root.geometry('300x300')
        name = clicked.get()
        self.root.title('Terminal ('+name+')')

        self.tfield = ConsoleText(self.root,name)
        self.tfield.pack(expand=True, fill=BOTH)
        # if name in devicenames['routers']: #Check if device is a router or switch
        #     self.tfield = ConsoleText(self.root,name)
        #     self.tfield.pack(expand=True, fill=BOTH)
        # else:
        #     self.tfield = ConsoleText(self.root, name)
        #     self.tfield.pack(expand=True, fill=BOTH)
        # Modal window.
        # Wait for visibility or grab_set doesn't seem to work.
        self.root.wait_visibility()   # <<< NOTE
        # self.root.grab_set()          # <<< NOTE
        self.root.transient(parent)   # <<< NOTE
        
        # self.parent = parent

    def ok(self): #depracated?
        self.data = self.entry.get()
        self.root.grab_release()      # <<< NOTE
        self.root.destroy()


class MainWindow:
    def __init__(self, window):
        window.geometry('800x650')
        window.title('Phoenix Lab Sim')
        
        #************************************************
        # Setting icon of master window
        self.p1 = PhotoImage(file = "assets/logo.png")
        window.iconphoto(True, self.p1)

        Button(window, text='Quit', command=self.closeme).pack(anchor=NE,padx=3,pady=3)
        
        self.window = window
        window.bind('<Key>', self.handle_key)
        
        self.entry_frame()
        self.entry.pack()
        
        
    def main_frame(self):
        self.entry.pack_forget()
        self.top.destroy()
        startup(1) #Starts up the sim. Copies startup files to running folder
        
        #***********************************************
        #Add image to window
        self.imgpath = "assets/nodes.png"
        self.img = ImageTk.PhotoImage(Image.open(self.imgpath))

        self.main = Frame(self.window, width=600, height=600)
        self.main.pack(pady=10)
        # self.entry.pack()
        # self.main.place(anchor=CENTER, relx=0.5, rely=0.5)

        # Create a Label Widget to display the Image
        label = Label(self.main, image = self.img)
        label.pack()
               
        #**********************************************
        #Adding bottom panel
        self.bottom_panel = PanedWindow(self.main, bd=4) 
        self.bottom_panel.pack(fill=BOTH, side=BOTTOM)
        
        #create device names
        global devicenames
        devicenames = find_device_names()
        
        #create dropdown menu
        options = devicenames["routers"] + devicenames["switches"]
        
        global clicked
        # datatype of menu text
        clicked = StringVar()
        
        # initial menu text
        clicked.set(options[0])
        
        # Create Dropdown menu
        drop = OptionMenu(self.bottom_panel , clicked , *options )
        drop.pack(pady=5)
        Button(self.bottom_panel, text='Open Terminal', command=self.popup).pack(pady=5)
        Button(self.bottom_panel, text='Compare Solution', command=self.compare).pack(pady=5)
        # self.main.pack()

        
    
    def entry_frame(self):
        """
        The first frame users see
        """
        self.entry = Frame(self.window, width=800, height=650)
        Label(self.entry, text= "Welcome to\nPhoenix Lab Sim", 
              font=('Mistral 18 bold')).pack(pady=30)
        Label(self.entry, image = self.p1).pack(pady=10)
        Label(self.entry, text= "Please select an option", 
              font=('Mistral 18 bold')).pack(pady=5)
        
        Button(self.entry, text='Open Simulation', 
               command=self.askimport).pack(pady=5)
        Button(self.entry, text='Create Simulation', 
               command=self.asknumber).pack(pady=5)

    def handle_key(self, event):
        k = event.keysym
        print(f"got k: {k}")

    def popup(self):
        d = simpledialog(self.window)
        print('opened login window, about to wait')
        self.window.wait_window(d.root)   # <<< NOTE
        print('end wait_window, back in MainWindow code')
        print(f'got data: {d.data}')
        
    def compare(self):
        compare()
        
        
    def askimport(self):
        """
        Asks the user if they want to import sim document or not
        """
        self.top= Toplevel(self.window)
        self.top.geometry("200x200")
        self.top.title("Import?")
        Label(self.top, text= "Import config file\nor use existing?").pack(pady=5)
        Button(self.top, text='Import file', command = self.importfiles).pack(pady=5)
        Button(self.top, text='Use existing', command = self.main_frame).pack(pady=5)

    def importfiles(self):
        import_file()
        self.main_frame()
        
    def closeme(self):
        root.destroy()
        
    #************************************************************
    #                 Frames for create sims
    
    def create_sim(self):
        """
        Function that initializes the frame when a new simulation is being created
        """
        self.entry.pack_forget()
        self.ask.destroy()
        
        self.create = Frame(self.window, width=800, height=700)
        self.create.pack()
        initjson(int(self.no_routers.get()[0]),int(self.no_switches.get()[0]))
        plot()
        self.imgpath = "assets/nodes.png"
        self.img = ImageTk.PhotoImage(Image.open(self.imgpath))
        self.label = Label(self.create, image = self.img)
        self.label.pack()
        
        Button(self.create, text='Add', command = self.addedge).pack(side=LEFT, pady=5, padx=5)
        
        
        #**********************************************
        #Adding bottom panel
        self.bottom_panel2 = PanedWindow(self.create, bd=4) 
        self.bottom_panel2.pack(fill=BOTH, side=BOTTOM)
        
        #create device names
        global devicenames
        devicenames = find_device_names()
        
        #create text field for adding sim instructions
        self.instructions = "Please add the instructions for the simulation"
        
        #create dropdown menu
        options = devicenames["routers"] + devicenames["switches"]
        
        # datatype of menu text
        self.clickedfrom = StringVar()
        self.clickedto = StringVar()
        self.editobj = StringVar()
        
        # initial menu text
        self.clickedfrom.set(options[0])
        self.clickedto.set(options[1])
        self.editobj.set(options[0])
        
        subframe0 = Frame(self.bottom_panel2)
        subframe1 = Frame(self.bottom_panel2)
        subframe2 = Frame(self.bottom_panel2)
        
        # Create Dropdown menu to add link from and to
        addlinklabel = Label(subframe0, text= "Add Links")
        addlinklabel.pack(side= LEFT, padx=5)
        
        fromlabel = Label(subframe0, text= "From:")
        fromlabel.pack(side=LEFT, padx=5)
        drop = OptionMenu(subframe0 , self.clickedfrom , *options )
        drop.pack(side=LEFT, pady=5, padx=5)

        tolabel = Label(subframe0, text= "To:")
        tolabel.pack(side=LEFT, padx=5)
        drop = OptionMenu(subframe0 , self.clickedto , *options )
        drop.pack(side=LEFT, pady=5, padx=5)

        Button(subframe0, text='Add', command = self.addedge).pack(side=LEFT, pady=5, padx=5)
        subframe0.pack()
        
        #Create dropdown to edit files
        editlabel = Label(subframe1, text= "Edit Device")
        editlabel.pack(pady=5, fill = BOTH, side=LEFT)
        drop = OptionMenu(subframe1 , self.editobj , *options )
        drop.pack(pady=5, padx=5, side=LEFT)

        Button(subframe1, text='Edit', command = self.editwindow).pack(pady=5, padx=5, side=LEFT)
        subframe1.pack()
        
        Button(subframe2, text='Export', command = save_file).pack(pady=5, padx=5)
        subframe2.pack()
        
        
    def editwindow(self):
        """
        The edit device pop up when creating a sim
        """
        self.top= Toplevel(self.window)
        self.top.geometry("600x300")
        temp = self.editobj.get()
        self.top.title("Editing "+temp)
        
        self.device = get_dict(temp)
        
        self.editatr_s = {}
        self.editatr_u = {}
        #LEFT SIDE
        x = "startup"
        subframe0 = Frame(self.top)
        subframe1 = Frame(self.top)
        
        atrlist=["hostname","ip4","ip6","subnet","username","password","mask","mac","ipdefault"]
        
        for atr in atrlist:
            self.editatr_s[atr] = StringVar()
            self.editatr_s[atr].set(self.device[x][atr])
            Label(subframe0, text = atr.capitalize()).pack(pady=3)
            Entry(subframe1, textvariable=self.editatr_s[atr]).pack()

        # subject.place(relx=0.5, rely=0.5,anchor=CENTER)
        subframe0.pack(expand = True, fill = BOTH, side=LEFT)
        subframe1.pack(expand = True, fill = BOTH, side=LEFT)
 
        #RIGHT SIDE
        x = "ultimate"
        subframe2 = Frame(self.top)

        for atr in atrlist:
            self.editatr_u[atr] = StringVar()
            self.editatr_u[atr].set(self.device[x][atr])
            Entry(subframe2, textvariable=self.editatr_u[atr]).pack()
        # message = Label(subframe2, text= "Message")
        # message.place(relx=0.5, rely=0.5,anchor=CENTER)
        subframe2.pack(expand=True, fill=BOTH, side=LEFT)
        
        Button(self.top, text=' Save ', command = self.save_edit).pack(pady=5, padx=5, side=BOTTOM)        
    
    def save_edit(self):
        atrlist=["hostname","ip4","ip6","subnet","username","password","mask","mac","ipdefault"]
        startup_atr = {}
        ultimate_atr = {}
        for x in atrlist:
            startup_atr[x]=self.editatr_s[x].get().strip()
            ultimate_atr[x]=self.editatr_u[x].get().strip()

        save_edit_to_file(self.device["startup"]["name"],startup_atr,ultimate_atr)       
        self.top.destroy()

    
    def addedge(self):
        """
        Add link to graph
        """
        print("adding link from main")
        add_edge(self.clickedfrom.get(),self.clickedto.get())
        self.label.pack_forget()
        self.img = ImageTk.PhotoImage(Image.open(self.imgpath))
        self.label = Label(self.create, image = self.img)
        self.label.pack()
        
        
    def asknumber(self):
        """
        Asks the user for total number of routers and switches the want to create
        """
        self.ask = Toplevel(self.window)
        self.ask.geometry("300x300")
        self.ask.title("Number of Devices")
        Label(self.ask, text= "How many routers and switches \ndo you want to create?").pack(pady=15)
        
        #Creating dropdowns to select number of routers and switches
        self.no_routers = StringVar()
        self.no_switches = StringVar()
        
        #dropdown options
        roptions = [
            "1 Router",
            "2 Routers",
            "3 Routers",
            "4 Routers",
            "5 Routers"
        ]
        soptions = [
            "1 Switch",
            "2 Switches",
            "3 Switches",
            "4 Switches",
            "5 Switches"
        ]
        
        # initial menu text
        self.no_routers.set(roptions[0])
        self.no_switches.set(soptions[0])
        
        # Create Dropdown menu
        rdrop = OptionMenu(self.ask , self.no_routers , *roptions )
        sdrop = OptionMenu(self.ask , self.no_switches , *soptions )
        rdrop.pack(pady=5)
        sdrop.pack(pady=5)

        Button(self.ask, text='Back', command = self.ask.destroy).pack(pady=5)
        Button(self.ask, text='Create', command = self.create_sim).pack(pady=5)
        
    def textfield(self, option):
        self.text = Toplevel(self.window)
        self.text.geometry("600x300")
        self.text.title ("Simulation Instructions")
        
        subframe0 = Frame(self.text)
        subframe1 = Frame(self.text)
        
        Text(subframe0).pack(pady=5,padx=5)
        subframe0.insert('end',self.instructions)
        
        Button(subframe1, text=' Save ', command = self.savetext).pack(pady=5, padx=5, side=BOTTOM)
        pass
     
    def savetext(self):
        self.text.destroy()
           
    def showgraph(self):
        self.img = ImageTk.PhotoImage(Image.open(self.imgpath))
        imglabel = Label(self.create, image = self.img)
        imglabel.pack()

root = Tk()
app = MainWindow(root)
root.mainloop()
print('exit main loop')