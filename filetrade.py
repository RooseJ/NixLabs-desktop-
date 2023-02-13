#This file handles everything that has to do with file manipulation
#It boots up the system too

import json
# from router import *
# from switch import *
import filecmp
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import plot

def startup(opt:int): #Copies files from base folder to startup folder
    """
    Copies files from one folder to the other (starts up the sim)
    opt:
    0 - copies from base to startup
    1 - copies from startup to running
    2 - copies from startup to ultimate
    3 - copies from running to startup
    """ 
    
    if opt == 0:
        filepathb = "assets/base/"
        filepaths = "assets/startup/"
    elif opt == 1:
        filepathb = "assets/startup/"
        filepaths = "assets/running/"
    elif opt == 2:
        filepathb = "assets/startup/"
        filepaths = "assets/ultimate/"
    elif opt == 3:
        filepathb = "assets/running/"
        filepaths = "assets/startup/"
    
    r = "routers.json"
    s = "switches.json"
    
    with open(filepathb+r, 'r') as openfile:
    # Reading from json file
        json_object = json.load(openfile)
        with open(filepaths+r, 'w') as outfile:
            json.dump(json_object, outfile, indent= 4)
            
    with open(filepathb+s, 'r') as openfile:
    # Reading from json file
        json_object = json.load(openfile)
        with open(filepaths+s, 'w') as outfile:
            json.dump(json_object, outfile, indent= 4)
            

    # print(json_object["name"])
    

def initjson(R:int,S:int):
    """
    To create new instances of Routers and Switches into startup
    
    R: number of Routers
    S: number of Switches
    """
 
    #For Routers
    path = "assets/base/routers.json"

    with open(path, 'r') as openfile:
        json_object = json.load(openfile)
    temp = json_object[0:R]

    path = "assets/startup/routers.json"
    with open(path, "w") as outfile:
        json.dump(temp, outfile, indent= 4)
    
    #For Switches
    path = "assets/base/switches.json"

    with open(path, 'r') as openfile:
        json_object = json.load(openfile)
    temp = json_object[0:S]

    path = "assets/startup/switches.json"
    with open(path, "w") as outfile:
        json.dump(temp, outfile, indent= 4)
    
    #For config
    temp = []
    
    for x in range(R):
        no = x+1
        temp.append("Router "+str(no))
        
    for x in range(S):
        no = x+1
        temp.append("Switch "+str(no))
        
    path = "assets/startup/config.json"

    config = {
        "R" : R,
        "S" : S,
        "links" : {
            "nodes": temp,
            "edges": []
        }
    }    
    
    with open(path, "w") as outfile:
        json.dump(config, outfile, indent= 4)
        
    startup(2)
        
    print("Initialized",R," routers and ",S," switches from base folder")


#Compare files
def compare():
    """
    Compares the files. Makes sure the simulation is complete
    """
    
    exp1 = filecmp.cmp('assets/ultimate/routers.json',
                       'assets/startup/routers.json')
    exp2 = filecmp.cmp('assets/ultimate/switches.json',
                       'assets/startup/switches.json')
    exp3 = filecmp.cmp('assets/running/routers.json',
                       'assets/ultimate/routers.json')
    exp4 = filecmp.cmp('assets/running/switches.json',
                       'assets/ultimate/switches.json')
    
    if exp1 and exp2:
        showinfo(
            title='Congratulations!',
            message="Sim has been\ncompleted!"
        )
    else:
        print("Ultimate files and Startup files are NOT the same")
        
        if exp3 and exp4:
            showinfo(
                title='Incorrect Solution!',
                message="Did you forget to copy running config\nto startup config?"
            )
        else:
            showinfo(
                title='Incorrect Solution!',
                message="Maybe you missed a couple of things?"
            )
        
# compare()

def package(folder:str):
    """
    Packages an entire folder directory and returns a json file format
    folder: startup/ultimate
    """ 
    #Packaging an entire folder and output it as a json
    output = {}
    path = "assets/"+folder+"/"
    if folder =="startup":
        files = ["config","routers","switches"]
    else:
        files = ["routers","switches"]
    
    for x in files:
        with open(path+x+".json", 'r') as openfile:
            json_object = json.load(openfile)
            output[x] = json_object

    return output
    

def exportjson(file):
    """
    Exports the startup and ultimate folders in a document
    file: the file path to where the exported document should go
    """
    #exporting startup and ultimate
    export = {}
    exporting = ["startup","ultimate"]
    
    update_edges()
    
    for x in exporting:
        # temp = {}        
        # temp[x] = package(x)
        export[x] = package(x)
    
    with open(file, "w") as outfile:
        json.dump(export, outfile, indent= 4)

def update_edges():
    """
    Updates the links for the routers and switches
    """
    folders = ["startup",'ultimate']
    files = ["routers","switches"]
    
    # plot.plot()
    
    for folder in folders:
        for file in files:
            path = "assets/"+folder+"/"+file+".json"
            
            with open(path, 'r') as openfile:
                json_object = json.load(openfile)

            for index,device in enumerate(json_object):
                edges = plot.neighbors(device["name"])
                json_object[index]["links"] = edges
                
            with open(path, "w") as outfile:
                json.dump(json_object, outfile, indent= 4)
                         

def importjson(path:str):
    """
    Imports a json file to initialize the startup and ultimate folders
    path: the path to the importing file (.json)
    """
    files = ["routers","switches"]
    folders = ["ultimate","startup"]
    
    with open(path, 'r') as openfile:
        json_object = json.load(openfile)
        
    path = "assets/startup/config.json"
    temp = json_object['startup']['config']
    with open(path, "w") as outfile:
        json.dump(temp, outfile, indent= 4)   
    
    for f in folders:    
        for x in files:
            path = "assets/"+f+"/"+x+".json"
            temp = json_object[f][x]

            with open(path, "w") as outfile:
                json.dump(temp, outfile, indent= 4)
   
            
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
            message="Import Successful"
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
            message="Sim has been saved"
        )


def find_device_names():
    """
    Finds and returns the names of all the devices
    """
    output = {
        "routers": [],
        "switches": []
    }
    rpath = "assets/startup/routers.json"
    spath = "assets/startup/switches.json"
    
    #For routers
    with open(rpath, 'r') as openfile:
        json_object = json.load(openfile)
    
    for name in json_object:
        output["routers"].append(name["name"])
    
    #For switches
    with open(spath, 'r') as openfile:
        json_object = json.load(openfile)
    
    for name in json_object:
        output["switches"].append(name["name"])
        
    return output

def get_dict(name):
    """
    Gets the attributes of a device for both start and running and outputs it
    """
    output = {
        "startup":{},
        "ultimate":{}
    }
    folders= ["startup","ultimate"]
    
    for path in folders:
        rpath = "assets/"+path+"/routers.json"
        spath = "assets/"+path+"/switches.json"
        
        #For routers
        with open(rpath, 'r') as openfile:
            json_object = json.load(openfile)
        
        for device in json_object:
            if device["name"] == name:
                output[path] = device
                break
        
        #For switches
        with open(spath, 'r') as openfile:
            json_object = json.load(openfile)
        
        for device in json_object:
            if device["name"] == name:
                output[path] = device
                break
    return output

def save_edit_to_file(name,start_atr,ulti_atr):
    """
    Saves the edit to file from creating simulation
    """
    folders= ["startup","ultimate"]
    
    new_atr = {
        "startup": start_atr,
        "ultimate": ulti_atr  
    }
    
    for path in folders:
        rpath = "assets/"+path+"/routers.json"
        spath = "assets/"+path+"/switches.json"
        
        #For routers
        with open(rpath, 'r') as openfile:
            json_object = json.load(openfile)
        
        for device in json_object:
            if device["name"] == name:
                for atr in new_atr[path]:
                    device[atr] = new_atr[path][atr]
                break
        
        with open(rpath, "w") as outfile:
            json.dump(json_object, outfile, indent= 4)
            
        #For switches
        with open(spath, 'r') as openfile:
            json_object = json.load(openfile)
        
        for device in json_object:
            if device["name"] == name:
                for atr in new_atr[path]:
                    device[atr] = new_atr[path][atr]
                break
            
        with open(spath, "w") as outfile:
            json.dump(json_object, outfile, indent= 4)
            

#########################################################
#            Running Config functions
########################################################
def get_router_attributes(name):
    """
    Gets the attributes for the router
    name: name of the router
    """
    path = "assets/running/routers.json"
    
    with open(path, 'r') as openfile:
        json_object = json.load(openfile)
        
    for device in json_object:
        if device["name"] == name:
            return device
    return


def get_switch_attributes(name):
    """
    Gets the attributes for the switch
    name: name of the switch
    """
    path = "assets/running/switches.json"
    
    with open(path, 'r') as openfile:
        json_object = json.load(openfile)
        
    for device in json_object:
        if device["name"] == name:
            return device
    return
        
def push_router_attributes(attr:dict):
    """
    Pushes the attributes for the router
    attr: dictionary of the device attributes to push
    """
    path = "assets/running/routers.json"
    name = attr["name"]
    
    with open(path, 'r') as openfile:
        json_object = json.load(openfile)
        
    for index,device in enumerate(json_object):
        if device["name"] == name:
            json_object[index] = attr

    with open(path, "w") as outfile:
        json.dump(json_object, outfile, indent= 4)   
        
        
def push_switch_attributes(attr:dict):
    """
    Pushes the attributes for the switch
    attr: dictionary of the device attributes to push
    """
    path = "assets/running/switch.json"
    name = attr["name"]
    
    with open(path, 'r') as openfile:
        json_object = json.load(openfile)
        
        
    for index,device in enumerate(json_object):
        if device["name"] == name:
            json_object[index] = attr
    
    
    with open(path, "w") as outfile:
        json.dump(json_object, outfile, indent= 4)    