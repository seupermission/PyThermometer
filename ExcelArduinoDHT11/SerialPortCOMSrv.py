# -*- coding: utf-8 -*-

"""
    Serial Port COM Server for MS Excel

       Polled data I/O: A nonblocking call will return immediately， avoid an I/O hang.

 License: this code is in the public domain

 Author:   Cheng Tianshi
 Email:    chengts95@seu.edu.cn

"""
import time
import serial
import pythoncom


class SerialPortCOMServer:
    _public_methods_ = ["Open", "get_data", "Close"]
    _reg_progid_ = "SerialPortCOMServer.data"
    _reg_clsid_ = pythoncom.CreateGuid()

    def __init__(self):
        self.port = 'COM4'
        self.baud = 9600
        self.ser = None
        self.connok = 1
        self.humidity = 0
        self.temperature = 0
        self.heat_index = 0
        self.line = ""

    def Open(self, port, baud):
        self.port = port  # you shoule change to your board port
        self.baud = baud
        try:
            if self.ser:
                self.ser.close()
            self.ser = serial.Serial(self.port, self.baud)
            # non-block read
            self.ser.timeout = 0
        except (serial.SerialException, e):
            self.connok = 0
        return self.connok

    def get_data(self):
        """
         Polled data I/O： A nonblocking call will return immediately， avoid an I/O hang.
        """
        tmax = 20.0
        checking = True
        tstart = time.time()
        while checking:
            # self.ser.timeout = 0 ，non-block read
            self.line = self.ser.readline().decode()
            if self.line != "" or time.time() - tstart > tmax:
                checking = False
            else:
                time.sleep(0.5)  # wait 500 ms between checks
        return self.line

    def Close(self):
        try:
            if self.ser:
                self.ser.close()
            self.ser = serial.Serial(self.port, self.baud)
        except (serial.SerialException, e):
            return 0


if __name__ == "__main__":
    # Run "python SerialPortCOMSrv.py"
    #   to register the COM server.
    # Run "python SerialPortCOMSrv.py --unregister"
    #   to unregister it.
    print("Registering COM server...")
    import win32com.server.register
    win32com.server.register.UseCommandLine(SerialPortCOMServer)
