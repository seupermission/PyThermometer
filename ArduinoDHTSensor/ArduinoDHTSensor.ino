//  DHT11 temperature/humidity sensors
//  Board: Arduino Uno
//       Written by Cheng Tianshi, public domain

#include "DHT.h"

// the digital pin of Arduino which DHT11 is connected to，
//  DHT11 is connected to  pin 3 of GoKit 
#define DHTPIN 3     
#define DHTTYPE DHT11   // DHT 11

// ------------------------------------   LAYLOUT   --------------------------
//  Connect DHT11 pin 1(VCC,on the left,power)   ->  Arduino +5V
//  Connect DHT11 pin 2(data)                    ->  your DHTPIN in Arduino,for example pin 3
//  Connect DHT11 pin 4(GND,on the right)        ->  Arduino GROUND
//  Connect DHT11 pin 2(data) -> a 10K resistor  ->  DHT11 pin 1 (power) 

// Initialize DHT sensor.
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  // Wait a few seconds between measurements.
  delay(2000);

  // Reading temperature or humidity takes about 250 milliseconds!
  float h = dht.readHumidity();
  // Read temperature as Celsius (the default)
  float t = dht.readTemperature();
 
  // Check if any reads failed and exit early (to try again).
  if (isnan(h) || isnan(t) ) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }
  // Compute heat index in Celsius (isFahreheit = false)
  float hic = dht.computeHeatIndex(t, h, false);

  Serial.print(" Humidity: ");
  Serial.print(h);
  Serial.print("%");
  Serial.print(" Temperature: ");
  Serial.print(t);
  Serial.print("*C");
  Serial.print(" Heat index: ");
  Serial.print(hic);
  Serial.println("*C");
}
