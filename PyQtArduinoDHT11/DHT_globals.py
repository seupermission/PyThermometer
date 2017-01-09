
# -*- coding: utf-8 -*-

"""
A threaded GUI Monitor with Python and PyQt4 plots live data using PythonQwt

Code modified from mba7 (monta.bha@gmail.com)

License: this code is in the public domain

Author:   Cheng Tianshi
Email:    chengts95@163.com

Last modified: 2016.7.28

"""
import random
import sys
import queue
import serial
import glob
import os
import csv
import time

ktrace = 0

LeftYMAX = 80.000
LeftYMIN = 0.000

RightYMAX = 60.000
RightYMIN = 0.000

savedsamples = 100


class LiveDataFeed(object):
    """ A simple "live data feed" abstraction that allows a reader 
        to read the most recent data and find out whether it was 
        updated since the last read. 

        Interface to data writer:

        add_data(data):
            Add new data to the feed.

        Interface to reader:

        read_data():
            Returns the most recent data.

        has_new_data:
            A boolean attribute telling the reader whether the
            data was updated since the last read.    
    """

    def __init__(self):
        self.cur_data = None
        self.has_new_data = False

    def add_data(self, data):
        self.cur_data = data
        self.has_new_data = True

    def read_data(self):
        self.has_new_data = False
        return self.cur_data


def debug(message1, message2=None, message3=None):
    if ktrace:
        print(message1, message2, message3)

if sys.version_info[:2] < (2, 5):
    def partial(func, arg):
        def callme():
            return func(arg)
        return callme
else:
    from functools import partial


def get_all_from_queue(Q):
    """ Generator to yield one after the others all items 
        currently in the queue Q, without any waiting.
    """
    try:
        while True:
            yield Q.get_nowait()
    except queue.Empty:
        raise StopIteration


def get_item_from_queue(Q, timeout=0.01):
    """ Attempts to retrieve an item from the queue Q. If Q is
        empty, None is returned.

        Blocks for 'timeout' seconds in case the queue is empty,
        so don't use this method for speedy retrieval of multiple
        items (use get_all_from_queue for that).
    """
    try:
        item = Q.get(True, 0.01)
    except queue.Empty:
        return None
    return item


def enumerate_serial_ports():
    """ 
    Purpose:        scan for available serial ports
    Return:         return a list of of the availables ports names
    """
    if os.name == 'nt':
        outAvailablePorts = []
        for i in range(256):
            try:
                s = serial.Serial('com'+str(i))
                outAvailablePorts.append(s.portstr)
                s.close()
            except serial.SerialException:
                pass
        return outAvailablePorts
    else:
        return glob.glob('/dev/tty*')
