#!/usr/bin/python3

import http.client
import json
import time

while True:
    #rfid = input("My RFID: ") 
    rfid = "Test5"
    print(rfid)
    connection = http.client.HTTPConnection("192.168.1.101:3030")
    #connection = http.client.HTTPConnection("192.168.111.19:3030")
    headers = {'Content-type':'application/json'}
    scandata = {'TagNo':rfid,'StationId':1}
    json_scandata = json.dumps(scandata)
    connection.request("POST", "/scandata",json_scandata,headers)
    response = connection.getresponse()
    print(response.read().decode())
    time.sleep(5)
    #rfid = input("My RFID: ") 

connection.close()
