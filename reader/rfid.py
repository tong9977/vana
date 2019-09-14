#!/usr/bin/python3

import http.client
import json
import time
import smbus
import os
import string

# Define some device parameters
I2C_ADDR  = 0x27 # I2C device address
#I2C_ADDR  = 0x3f# I2C device address
LCD_WIDTH = 16   # Maximum characters per line

# Define some device constants
LCD_CHR = 1 # Mode - Sending data
LCD_CMD = 0 # Mode - Sending command

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line

LCD_BACKLIGHT  = 0x08  # On
#LCD_BACKLIGHT = 0x00  # Off

ENABLE = 0b00000100 # Enable bit

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

#Open I2C interface
#bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
bus = smbus.SMBus(1) # Rev 2 Pi uses 1

def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off 
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  time.sleep(E_DELAY)

def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = the data
  # mode = 1 for data
  #        0 for command

  bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
  bits_low = mode | ((bits<<4) & 0xF0) | LCD_BACKLIGHT

  # High bits
  bus.write_byte(I2C_ADDR, bits_high)
  lcd_toggle_enable(bits_high)

  # Low bits
  bus.write_byte(I2C_ADDR, bits_low)
  lcd_toggle_enable(bits_low)

def lcd_toggle_enable(bits):
  # Toggle enable
  time.sleep(E_DELAY)
  bus.write_byte(I2C_ADDR, (bits | ENABLE))
  time.sleep(E_PULSE)
  bus.write_byte(I2C_ADDR,(bits & ~ENABLE))
  time.sleep(E_DELAY)

def lcd_string(message,line):
  # Send string to display

  message = message.ljust(LCD_WIDTH," ")

  lcd_byte(line, LCD_CMD)

  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)

def getIP():
  os.system("hostname -I>>ip.text")
  f = open('ip.text', 'r')
  myip = f.read()
  f.close()
  os.system('sudo rm ip.text')
  return myip

def checkIp():
  myip = ''
  count = 0
  while len(myip) < 5:
    myip = getIP()
    print('my-ip: ' + myip)
    count = count +1
    lcd_string('CheckIP: ' + str(count),LCD_LINE_1)
    lcd_string("",LCD_LINE_2)
    lcd_string("",LCD_LINE_4)
    lcd_string("",LCD_LINE_3)
    time.sleep(2)

  return myip.split()[0]

def displayReadyToScan(myip,station):
  lcd_string("READY TO SCAN",LCD_LINE_1)
  lcd_string("",LCD_LINE_2)
  lcd_string(station,LCD_LINE_3)
  lcd_string(myip,LCD_LINE_4)

def displayWaiting():
  lcd_string("WAIT !!!",LCD_LINE_1)
  lcd_string("",LCD_LINE_2)
  lcd_string("",LCD_LINE_3)
  lcd_string("",LCD_LINE_4)

def displayOK(tagno,scanno,maxscan,scan_time):
  lcd_string(tagno,LCD_LINE_1)
  lcd_string(str(scanno)+'/'+str(maxscan),LCD_LINE_2)
  lcd_string("",LCD_LINE_3)
  lcd_string(str(scan_time),LCD_LINE_4)
  print(tagno + ' ' + str(scanno) +'/'+ str(maxscan)  + ' '+ str(scan_time))

def cameraIsTaken(station,scanUnixtime,connection):
    headers = {'Content-type':'application/json'}
    params = {'ScanUnixtime':scanUnixtime,'Station':station}
    json_params = json.dumps(params)
    connection.request("PATCH", "/camera/IsTaken",json_params,headers)
    response = connection.getresponse()
    resposeJson = response.read().decode()
    dict = json.loads(resposeJson)
    print(dict)
    return dict['Taken']

def sendRFID(rfid,station,connection):
    headers = {'Content-type':'application/json'}
    scandata = {'TagNo':rfid,'Station':station}
    json_scandata = json.dumps(scandata)
    connection.request("POST", "/scandata",json_scandata,headers)
    response = connection.getresponse()
    resposeJson = response.read().decode()
    print(resposeJson)

    dict = json.loads(resposeJson)
    return dict['TagNo'],dict['Unixtime']


def waitForCamera(station,scan_time,connection):
    displayWaiting()
    lcd_string(str(scan_time),LCD_LINE_2)
    count = 0
    taken = False
    timeout = 10

    while (not taken) and (count < timeout)  :
        taken = cameraIsTaken(station,scan_time,connection)
        time.sleep(1)
        count = count + 1
        lcd_string(str(count),LCD_LINE_4)
    
    if taken :
        lcd_string('Got Photo',LCD_LINE_4)
        print('Got Photo')

    if not taken :
        lcd_string('Time Out!!',LCD_LINE_4)
        print('Time Out!!')
    
    time.sleep(2)


def RFIDWaitInQueue(station,connection):
    return 1


def main():
  # Main program block
  # Initialise display
  lcd_init()
  myip=checkIp()
  print(myip)
  station = "innertube"
  maxscan=2
  scanno=0
  while True: 

    #connection = http.client.HTTPConnection("192.168.1.102:3030")
    connection = http.client.HTTPConnection("192.168.111.19:3030")
    # scan 1
    displayReadyToScan(myip,station)
    rfid = input("SCAN RFID: ")
    scanno = scanno+1
    tagno,scan_time =sendRFID(rfid,station,connection)

    myqueue = RFIDWaitInQueue(station,connection) 

    if myqueue <= maxscan: 
      displayOK(tagno,scanno,maxscan,scan_time)


    if myqueue >= maxscan: 
      scanno = 0
      waitForCamera(station,scan_time,connection)

    connection.close()



if __name__ == '__main__':

  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    pass
    lcd_byte(0x01, LCD_CMD)