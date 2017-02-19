# -*- coding: utf-8 -*-

"""
A threaded GUI Monitor with Python and PyQt4 plots live data using PythonQwt

Code modified from mba7 (monta.bha@gmail.com)
 
License: this code is in the public domain

Author:   Cheng Tianshi
Email:    chengts95@seu.edu.cn

Last modified: 2016.7.28

"""
import queue
import threading
import time
import serial

from DHT_globals import *


def getvalue(line, itemname, unitstr):
    index = line.find(itemname)
    value = ''
    itemnamelen = len(itemname)
    if index > -1:
        startIndex = index + itemnamelen
        index = line.find(unitstr, startIndex + 1)
        value = line[startIndex: index]
    return float(value)


class ComMonitorThread(threading.Thread):
    """ A thread for monitoring a COM port.
        The COM port is opened when the thread is started.

        data_q:
            Queue for received data. Items in the queue are
            (data, timestamp) pairs, where data is a binary 
            string representing the received data, and timestamp
            is the time elapsed from the thread's start (in 
            seconds).

        error_q:
            Queue for error messages. In particular, if the 
            serial port fails to open for some reason, an error
            is placed into this queue.

        port:
            The COM port to open. Must be recognized by the 
            system.

        port_baud/stopbits/parity: 
            Serial communication parameters

        port_timeout:
            The timeout used for reading the COM port. If this
            value is low, the thread will return data in finer
            grained chunks, with more accurate timestamps, but
            it will also consume more CPU.
    """

    def __init__(self,
                 data_q, error_q,
                 port_num,
                 port_baud):

        threading.Thread.__init__(self)

        self.serial_port = None
        self.port = port_num
        self.baud = port_baud

        self.data_q = data_q
        self.error_q = error_q

        self.alive = threading.Event()
        # Start Thread
        self.alive.set()

    def getTHD(self):

        humidity = 0
        temperature = 0
        heat_index = 0

        line = self.serial_port.readline().decode()
        print(line)
        humidity = getvalue(line, " Humidity: ", '%')
        temperature = getvalue(line, " Temperature: ", '*C')
        heat_index = getvalue(line, " Heat index: ", '*C')

        print('humidity=', humidity, 'temperature=',
              temperature, 'Heat index=', heat_index)

        return {"t": temperature, "h": humidity, "a": heat_index}

    def run(self):
        try:
            if self.serial_port:
                self.serial_port.close()

            self.serial_port = serial.Serial(self.port, self.baud)
            print(self.serial_port)

        except (serial.SerialException, e):
            self.error_q.put(e.message)
            return

        # Restart the clock
        startTime = time.time()

        while self.alive.isSet():
            qdata = [0, 0, 0]

            thd = self.getTHD()

            qdata[0] = thd['t']
            qdata[1] = thd['h']
            qdata[2] = thd['a']

            print("qdata :", qdata)
            timestamp = time.time()
            self.data_q.put((qdata, timestamp))

        # clean up
        if self.serial_port:
            self.serial_port.close()

    def join(self, timeout=None):
        self.alive.clear()
        threading.Thread.join(self, timeout)
