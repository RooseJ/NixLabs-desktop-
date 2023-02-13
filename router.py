from filetrade import get_router_attributes
from filetrade import push_router_attributes

class Router:
    version = """  
    Xisco IOS Software, Version 2.6(1b), RELEASE SOFTWARE (mc2)
                        
    Xisco 2008 (revision 6.0) with 233472K/28672K bytes of memory.
    Processor board ID FTX1048W1XD
    2 FastEthernet interfaces
    4 Serial(sync/async) interfaces
    1 Virtual Private Network (VPN) Module
    
    DRAM configuration is 64 bits wide with parity disabled.
    191K bytes of NVRAM.
    62720K bytes of ATA CompactFlash (Read/Write)"""
    
    def __init__(self, name) -> None:
        self.name = name
        self.hostname = "Xicso XP2v3"
        self.os = "IOS 3.4"
        self.ip4 = "192.168.1.0"
        self.ip6 = "2001:0db8:85a3:0000:0000:8a2e:0370:7334"
        self.subnet = "192.168.2.x"
        self.username = "admin"
        self.password = "password"
        self.mask = ""
        self.mac = ""
        self.ipdefault = ""
        self.links = []
        
        self.download()

    def attr(self, dict: dict):
        for k, v in dict.items():
            setattr(self, k, v)
            
    def upload(self):
        temp = self.__dict__
        push_router_attributes(temp)
    
    def download(self):
        temp = get_router_attributes(self.name)
        self.attr(temp)
        

    def addlink(self, link):
        self.links.append(link)

    def login(self, username, password):
        self.download()
        if self.username == username and self.password == password:
            return True
        return False
        
    def change_attr (self, key,value):
        self.download()
        temp = self.__dict__[key]
        self.__dict__[key] = value
        
        print(key+" changed from "+temp+" to "+ self.__dict__[key])
        print(self.__dict__)
        self.upload()

    
    def show(self,key:str):
        self.download()
        key = key.lower()
        if key == "version":
            return self.version
        if key == "ip":
            return self.ip4
        if key == "ipv6":
            return self.ip6
        
        output = self.__dict__.get(key)
        print(output)
        if type(output) == list:
            output = '\n'.join(output)
        if output:
            return self.__dict__.get(key)
        else:
            return ' '