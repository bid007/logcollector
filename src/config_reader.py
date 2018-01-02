#Author : Bidhya Nandan Sharma
#Date 12/18/2017
import xml.etree.ElementTree as et 

class XmlToDict:
    """
    Class to convert xml to dict
    Input : Filename 
    Attributes : 
        root: XML parsed root of tree
        dict : dict form of the xml
    """
    def __init__(self,xmlfile):
        self.tree = et.parse(xmlfile)
        self.root = self.tree.getroot()
        try:
            self.parse()
        except KeyError as K:
            raise KeyError


    #Changes the xml file to the dictionary format
    def parse(self):
        self.clients = {}
        for client in self.root:
            temp = {}

            attr_list = ['ip', 'port', 'username', 'password', 'mail']
            for attr in attr_list:
                temp[attr] = client.attrib[attr]

            temp_alerts = []
            for alert in client:
                temp_alerts.append({'type':alert.attrib['type'], 
                                    'limit':alert.attrib['limit']
                                    })
            temp['alerts'] = temp_alerts
            self.clients[client.attrib['ip']] = temp

    #Returns the dict of ip:config clients 
    def get_clients(self):
        return self.clients

# x = XmlToDict("test/error.xml")
# print(x.get_clients())