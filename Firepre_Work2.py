"""
Eng
2021.11.19 Firepre Work2

reference link
https://towardsdatascience.com/micropython-on-esp-using-jupyter-6f366ff5ed9

Step 1. Install MicroPython Firmware on ESP8266
Step 2. Configure the circuit on the ESP8266 using the sensors to be used
Step 3. Check the operation of each sensor through ESP8266 using MicroPython code 

----------------
Kor
2021.11.19 Firepre Work2

참고 링크
https://towardsdatascience.com/micropython-on-esp-using-jupyter-6f366ff5ed9

Step 1. ESP8266에 마이크로파이썬 펌웨어 설치하기
Step 2. 사용할 센서들을 이용하여 ESP8266에 회로 구성하기
Step 3. MicroPython 코드를 이용하여 ESP8266을 통해 각 센서들의 동작 확인하기


"""

from machine import Pin
import time
# LED
led = Pin(0, Pin.OUT)
# DHT
from dht import DHT22
dht22 = DHT22(Pin(12))
def readDht():
    dht22.measure()
    return dht22.temperature(), dht22.humidity()
# DS18B20
import onewire, ds18x20
dat = Pin(2)
ds = ds18x20.DS18X20(onewire.OneWire(dat))
sensors = ds.scan()
def readDs():
    ds.convert_temp()
    time.sleep_ms(750)
    return round(ds.read_temp(sensors[0]), 1)
# LDR
from machine import ADC
adc = ADC(0)
def readLdr():
    lumPerct = (adc.read()-40)*(10/86)
    return round(lumPerct)
# Push Button
button = Pin(13, Pin.IN, Pin.PULL_UP)
def readBut():
    return button.value()
# Read all data:
def colectData():
    temp, hum, = readDht()
    extTemp = readDs()
    lum = readLdr()
    butSts = readBut()
    return temp, hum, extTemp, lum, butSts
# I2C / OLED
from machine import I2C
import ssd1306
i2c = I2C(scl=Pin(5), sda=Pin(4))
oled = ssd1306.SSD1306_I2C(128, 64, i2c, 0x3c)
def displayData(temp, hum, extTemp, lum, butSts):
    oled.fill(0)
    oled.text("Temp:    " + str(temp) + "oC", 0, 4)
    oled.text("Hum:     " + str(hum) + "%",0, 16)
    oled.text("ExtTemp: " + str(extTemp) + "oC", 0, 29)
    oled.text("Lumin:   " + str(lum) + "%", 0, 43)
    oled.text("Button:  " + str(butSts), 0, 57)
    oled.show()
# Main function
def main():
    led.on()
    temp, hum, extTemp, lum, butSts = colectData()
    displayData(temp, hum, extTemp, lum, butSts)
    led.off()
'''------ run main function --------'''
main()
