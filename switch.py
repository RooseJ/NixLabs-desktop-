from filetrade import get_switch_attributes
from filetrade import push_switch_attributes

class Switch:
    type = "switch"
    name = "switch1"
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

    def attr(self, dict: dict):
        for k, v in dict.items():
            setattr(self, k, v)

    def addlink(self, link):
        self.links.append(link)

    def changeusername(self, name):
        self.username = name

    def changepassword(self, password):
        self.username = password

    def login(self, username, password):
        if self.username == username and self.password == password:
            return True
        return False
