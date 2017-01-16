# Thermometer With Python and VBA 

* The projects of Thermometer were made as little tutorials/examples to show the basic technologies :

  * The development of GUI/Web Real-Time Serial Port  Monitor with Python.

  * Monitoring serial port devices with the MS Excel

* If you have any comments, please tell me: chengts95@seu.edu.cn

## HardWare
  
* Board:  [Arduino uno](http://www.arduino.cc/) 

![Arduino](./doc/arduino.jpg)

* Sensor: [DHT11](http://playground.arduino.cc/Main/DHT11Lib)

![DHT11](./doc/dht11-4pin.jpg)

## Layout: Arduino UNO + DHT11  
 ```  
   Connect DHT11 pin 1(VCC,left,power)   ->  Arduino +5V

   Connect DHT11 pin 2(DATA,signal)      ->  your DHTPIN in Arduino UNO,for example pin 3

   Connect DHT11 pin 4(GND,right)        ->  Arduino GROUND

   Connect DHT11 pin 2(DATA,signal)      -> a 10K resistor  ->  DHT11 pin 1 (VCC) 
```
![ArduinoDHT11](./doc/arduino-DHT11-layout.jpg)

## Arduino sketch  

* Open **ArduinoDHTSensor.ino**, build and upload to Arduino 

## Python and Packages

*  Python3.5 

*  PyQt4, PySerial, PythonQwt, Thread, Tornado

## PyQtArduinoDHT11

* A threaded GUI Monitor with Python and PyQt4 plots live data using PythonQwt

 * Key Points：Python3.5,PyQt4, PySerial, PythonQwt, Thread

* Launching the app
```
    >python DHT_monitor.py
``` 
![DesktopDHT11](./doc/DesktopDHT11.jpg)

* The GUI application is modified from: mba7  https://github.com/mba7/SerialPort-RealTime-Data-Plotter,

## TornadoArduinoDHT11

* A web monitor with Tornado web server enables real time plotting of DHT11 signals in the browser(support websocket)

 * Key Points： tornado server + websocket + flotr2 

*  Enjoying live data

```
  1) Launching the web server

      >python app.py

  2) Open a web browser and go to :

   http://localhost:8000  

  You should see the graph and be able to select the curves to display.
```
![WebDHT11](./doc/WebDHT11.jpg)

## MS Excel： MonitoingDHT11SerialPortByFile.xlsm

 * The Workbook provides an easy way to monitor serial port devices with the MS Excel
   
  * Key Points： serial port communication in the VBA through file

    The advantage of this method, which uses file functions to call the serial port directly,
    is that you do not really need to install anything on your PC, apart from the Excel itself

![ExcelDHT11](./doc/ExcelDHT11.jpg)

## Reference

1. Arduino: http://www.arduino.cc/

2. Arduino and Python: http://playground.arduino.cc/Interfacing/Python

3. DHT11：http://playground.arduino.cc/Main/DHT11Lib

5. PyQt: https://riverbankcomputing.com/software/pyqt/intro

6. PythonQwt： https://github.com/PierreRaybaut/PythonQwt

7. Tornado Web Server: http://www.tornadoweb.org/en/stable/

8. Noah Gift. Practical threaded programming with Python. http://www.ibm.com/developerworks/aix/library/au-threadingpython/index.html

9. mba7. SerialPort-RealTime-Data-Plotter. https://github.com/mba7/SerialPort-RealTime-Data-Plotter

10. John Walkenbach. Excel 2013 Power Programming with VBA. John Wiley & Sons, Inc. USA. s2013

10. Read from Serial port to Excel. http://stackoverflow.com/questions/14792502/read-from-serial-port-to-excel

## License

MIT 
