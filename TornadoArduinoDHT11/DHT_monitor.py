# -*- coding: utf-8 -*-

"""
A web monitor with Tornado web server enables real time plotting of DHT11 signals in the browser(support websocket)

License: this code is in the public domain

Author:   Cheng Tianshi
Email:    chengts95@163.com

Last modified: 2016.7.28
"""
import serial
import time

global ser
global t0
t0 = time.time()


def getvalue(line, itemname, unitstr):
    index = line.find(itemname)
    value = ''
    itemnamelen = len(itemname)
    if index > -1:
        startIndex = index + itemnamelen
        index = line.find(unitstr, startIndex + 1)
        value = line[startIndex: index]
    return float(value)


def openSerial():
    global ser
    port = 'COM4'  # you shoule change to your board port
    baudrate = 9600
    try:
        print("Trying...", port)
        ser = serial.Serial(port, baudrate)
        print("Connected on ", port)
        # Arduino is reset when opening port so wait before communicating
        time.sleep(1.5)
    except:
        print("Failed to connect on ", port, " change COM4 to your board port")


def getTHD():
    global ser
    humidity = 0
    temperature = 0
    heat_index = 0

    line = ser.readline().decode()
    # print(line)
    humidity = getvalue(line, " Humidity: ", '%')
    temperature = getvalue(line, " Temperature: ", '*C')
    heat_index = getvalue(line, " Heat index: ", '*C')

    print(' Humidity=', humidity, 'Temperatur=',
          temperature, 'Heat index=', heat_index)

    global t0
    t = time.time() - t0

    return t, {"t": temperature, "h": humidity, "a": heat_index}
