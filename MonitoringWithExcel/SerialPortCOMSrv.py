# -*- coding: utf-8 -*-

"""

"""
import serial
import pythoncom


class SerialPortCOMServer:
    _public_methods_=["Open","get_data","Close"]
    _reg_progid_ = "SerialPortCOMServer.data"
    _reg_clsid_ = pythoncom.CreateGuid()

    def __init__(self):
        self.port ='COM4'
        self.baud=9600
        self.ser = None
        self.connok=1
        self.humidity =0
        self.temperature=0
        self.heat_index=0
        self.line=""

    def Open(self,port,baud):
        self.port = port # you shoule change to your board port 
        self.baud = baud
        try:
            if self.ser:
                self.ser.close()
            self.ser = serial.Serial(self.port, self.baud)
        except (serial.SerialException, e):
            self.connok=0
        return self.connok

    def get_data(self):
        self.line = self.ser.readline().decode()
        return self.line 

    def Close(self):
        try:
            if self.ser:
                self.ser.close()
            self.ser = serial.Serial(self.port, self.baud)
        except (serial.SerialException, e):
            return 0
      

if __name__ == "__main__":
    # Run "python dht11sensor_com.py"
    #   to register the COM server.
    # Run "python dht11sensor_com.py --unregister"
    #   to unregister it.
    print("Registering COM server...")
    import win32com.server.register
    win32com.server.register.UseCommandLine(SerialPortCOMServer)
