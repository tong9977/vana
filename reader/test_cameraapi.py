#!/usr/bin/python3

import http.client
import json
import time
import os
import string

def cameraIsTaken(station,scanUnixtime,connection):
    headers = {'Content-type':'application/json'}
    params = {'ScanUnixtime':scanUnixtime,'Station':station}
    json_params = json.dumps(params)
    connection.request("PATCH", "/camera/IsTaken",json_params,headers)
    response = connection.getresponse()
    resposeJson = response.read().decode()
    print(resposeJson)
    return False


def main():

    count = 0
    taken = False
    timeout = 10
    connection = http.client.HTTPConnection("localhost:3030")

    while (not taken) and (count < timeout)  :
        taken = cameraIsTaken('innertube2',1568104025,connection)
        time.sleep(1)
        count = count + 1
    
    if not taken :
        print('Time Out!!')
    
    if taken :
        print('Got Photo')


    



if __name__ == '__main__':

  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    pass