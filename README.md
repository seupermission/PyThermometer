# Thermometer:  The GUI/Web Real-time Serial Port Monitor of DHT11
 
   These projects introduce some concepts and technologies to build robust and reliable monitoring software of serial port devices in the easy way.

## HardWare
  
* Board:  [Arduino UNO](http://www.arduino.cc/) 

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
![ArduinoDHT11](./doc/arduino-dht11-layout.jpg)

## Arduino sketch  

* Open **ArduinoDHTSensor.ino**, build and upload to Arduino 

## Python and Packages

*  Python3.5 

*  PyQt4, PySerial, PythonQwt, Tornado

## PyQtArduinoDHT11

* A threaded GUI Monitor with Python and PyQt4 plots live data using PythonQwt

 * Key Points：Python3.5,PyQt4, PySerial, PythonQwt, Thread

* Launching the app
```
    >python DHT_monitor.py
``` 
![DesktopDHT11](./doc/desktop-dht11.jpg)

* The GUI application is modified from: mba7  https://github.com/mba7/SerialPort-RealTime-Data-Plotter,

## TornadoArduinoDHT11

* A web monitor with Tornado web server enables real-time plotting of DHT11 signals in the browser(support websocket)

 * Key Points： tornado server + websocket + flotr2 

*  Enjoying live data on **COM4**

   * if your board serial port is not **COM4**, you may change:
    
      ```python
        def openSerial():
            
            port = 'COM4'  # you shoule change to your board port
       ```

```
  1) Launching the web server

      >python app.py

  2) Open a web browser and go to :

   http://localhost:8000  

  You should see the graph and be able to select the curves to display.
```
![WebDHT11](./doc/web-dht11.jpg)

## Reference

* Arduino
 
  * Arduino: http://www.arduino.cc/

  * Wiring: http://wiring.org.co/

  * DHT11：http://playground.arduino.cc/Main/DHT11Lib

  * Arduino and Python: http://playground.arduino.cc/Interfacing/Python

* Python

  * PyQt: https://riverbankcomputing.com/software/pyqt/intro

  * PythonQwt： https://github.com/PierreRaybaut/PythonQwt

  * Tornado Web Server: http://www.tornadoweb.org/en/stable/

  * Noah Gift. Practical threaded programming with Python. http://www.ibm.com/developerworks/aix/library/au-threadingpython/index.html

## License

MIT 
