
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  dataLoggerTS.py
# import general libraries
from machine import Pin
import time
from time import sleep
import network
from umqtt.simple import MQTTClient

# ThingSpeak Credentials:
SERVER = "mqtt.thingspeak.com"
CHANNEL_ID = "1570037"
WRITE_API_KEY = "MGSW6L0R6WUNW878"
PUB_TIME_SEC = 10

# MQTT client object
client = MQTTClient("umqtt_client", SERVER)

# Create the MQTT topic string
topic = "channels/" + CHANNEL_ID + "/publish/" + WRITE_API_KEY

# WiFi Credentials 
WiFi_SSID = "firepre"
WiFi_PASS = "00000000"

# define pin 0 (LED) as output
led = Pin(0, Pin.OUT)

# DHT
from dht import DHT22
dht22 = DHT22(Pin(12))

# Function to read DHT
def readDht():
    dht22.measure()
    return dht22.temperature(), dht22.humidity()

# DS18B20 
import onewire, ds18x20

# Define which pin the 1-wire device will be connected ==> pin 2 (D4)
dat = Pin(2)

# Create the onewire object
ds = ds18x20.DS18X20(onewire.OneWire(dat))

# scan for devices on the bus
sensors = ds.scan()

# function to read DS18B20 
def readDs(): 
    ds.convert_temp()
    time.sleep_ms(750)
    return round(ds.read_temp(sensors[0]), 1)

# LDR
from machine import ADC

# Define object
adc = ADC(0)

#function to read luminosity
def readLdr():
    lumPerct = (adc.read()-40)*(10/86) # convert in percentage ("map")
    return round(lumPerct)

# define pin 13 as an input and activate an internal Pull-up resistor:
button = Pin(13, Pin.IN, Pin.PULL_UP)

# Function to read button state:
def readBut():
        return button.value()

# Function to read all data:
def colectData():
    temp, hum, = readDht()
    extTemp = readDs()
    lum = readLdr()
    butSts = readBut()
    return temp, hum, extTemp, lum, butSts


# Function to connect to local WiFi
def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(WiFi_SSID, WiFi_PASS)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())


#''' ------ general functions ----'''
# create a blink function
def blinkLed(num):
    for i in range(0, num):
        led.on()
        sleep(0.5)
        led.off()
        sleep(0.5)

#'''------ main function --------'''
def main():
    while button.value():
        led.on()
        temp, hum, extTemp, lum, butSts = colectData()
        led.off()
        payload = "field1="+str(temp)+"&field2="+str(hum)+"&field3="+str(extTemp)+"&field4="+str(lum)+"&field5="+str(butSts)
        client.connect()
        client.publish(topic, payload)
        client.disconnect()
        time.sleep(PUB_TIME_SEC)
    blinkLed(3)

#'''------ run main function --------'''
do_connect()
main()
