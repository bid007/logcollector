#Author : Bidhya Nandan Sharma
#Date 12/18/2017

import sys
import time
from config_reader import XmlToDict
import os
from tasks import *

#Read emailconfig.ini and get 
#HOST, PORT, USER, PWD, FROM, SUBJECT
def get_econfig_dict(econfig_file):
    #open the file and make list of all contents
    with open(econfig_file) as f:
        contents = f.readlines()
    contents = [x.strip() for x in contents]
    #save the config in dict 
    econfig_dict = {}
    #all the fields we look for
    all_fields = set(('HOST', 'PORT', 'USER', 'PWD', 'FROM', 'SUBJECT'))
    #iterate through the lines to find fields we want
    for content in contents:
        temp = content.split('=')
        key = temp[0].rstrip() #remove spaces
        value = temp[1].rstrip() #remove spaces 
        #need int port so special case
        if key == 'PORT':
            econfig_dict['PORT'] = int(value)
            all_fields.remove('PORT')
        else:
            econfig_dict[key] = value
            all_fields.remove(key)
    #return ecofig dict if we found all the fields else raise exception 
    if len(all_fields) == 0:
        return econfig_dict
    else:
        raise Exception("Invalid email config file")

#Takes xmlfile as input and uses XmlToDict to get dicts of clients
#For each clients creates task to be handled by celery
def create_task(clients, econfig_dict):
    for k, v in clients.items():
        execute_client.delay(v, econfig_dict)

#requires command line input
#Number of times server should execute clients scripts 
#Exampe -n 80 would execute of 80 times -n 0 will execute continously
#Time interval between each calls -t 100 (100 s)
#config file -cli clients.xml
def main():
    argument_list = sys.argv
    try:
        t_index = argument_list.index('-t')
        n_index = argument_list.index('-n')
        f_index = argument_list.index('-cli')
        econfig_index = argument_list.index('-econf')
    except:
        #Raising exception if some arguments are missing
        raise Exception("Insufficient arguments")

    t = int(argument_list[t_index+1])
    n = int(argument_list[n_index+1])  
    if n == 0 : n = float('inf')
    xmlfile = argument_list[f_index+1]
    econfig_file = argument_list[econfig_index+1]
    clients = XmlToDict(xmlfile)
    #recording last modified time
    last_modified_time = os.stat(xmlfile).st_mtime
    #get the email config dict 
    econfig_dict = get_econfig_dict(econfig_file)
    count = 1
    while n > 0:
        print('Monitor # %s at interval of %s sec'%(count, t))
        #if modified time changes, the config file is reread
        if last_modified_time != os.stat(xmlfile).st_mtime:
            clients = XmlToDict(xmlfile)
        create_task(clients.get_clients(), econfig_dict)
        time.sleep(t)
        n -= 1
        count += 1

if __name__ == '__main__':
    main()