"""
D-Vitaminder

Tracks if D-vitamin has been used on the current day

Parts list:
Raspberry pi pico
DS3231 Real time clock
RGB LED
3 x 330 Ohm resistors
1 x 10k Ohm resistor
1 x photoresistor

Author: Hjalte Mann, TECOLOGY.xyz
"""

### IMPORT PACKAGES ###
from machine import I2C, Pin
from ds3231 import DS3231_I2C 
import utime

### Set DS I2C ID, SDA, SCL respective pins and uses default frequency (freq=400000) ###
ds_i2c = I2C(1,sda=Pin(6), scl=Pin(7))
ds = DS3231_I2C(ds_i2c)


### SET LIGHT THRESHOLD ###
lightThreshold = 15


### SET TIME ###
# Uncomment the lines below to set time
#current_time = b'\x00\x22\x17\x27\x17\x08\x21' # sec min hour week day month year
#ds.set_time(current_time)
### ###


### RGB LED & PHOTORESISTOR ###
led_red = Pin(10, Pin.OUT)
led_green = Pin(11, Pin.OUT)
led_blue = Pin(14, Pin.OUT)
photoPIN = 26


### DEFINE FUNCTIONS ###
def setLED(colour):
    if colour == "red":
        led_red.value(1)
        led_green.value(0)
        led_blue.value(0)
    if colour == "blue":
        led_red.value(0)
        led_green.value(0)
        led_blue.value(1)
    if colour == "green":
        led_red.value(0)
        led_green.value(1)
        led_blue.value(0)
    if colour == "off":
        led_red.value(0)
        led_green.value(0)
        led_blue.value(0)       


def readLight(photoGP):
    photoRes = machine.ADC(machine.Pin(26))
    light = photoRes.read_u16()
    light = round(light/65535*100,2)
    return light


### GIVE SOME TIME TO ASSEMBLE BOX AND PUT IN D-VITAMIN BEFORE MAIN LOOP STARTS ###
for i in range(0,5):
    setLED("red")
    utime.sleep(0.1)
    setLED("off")
    utime.sleep(0.1)

for i in range(0,10):
    setLED("red")
    utime.sleep(1)
    setLED("off")
    utime.sleep(1)

for i in range(0,5):
    setLED("green")
    utime.sleep(0.1)
    setLED("off")
    utime.sleep(0.1)

setLED("red")

### READ CURRENT DAY ###
t = ds.read_time()
day = "%02x" %(t[4]) # Clock returns time in hexadecimal format. Convert to string and then to int.
day = int(day)

### MAIN LOOP ###
while True:
    
    light = int(readLight(photoPIN))
    
    if light > lightThreshold: # If the light is above the threshold, that means the bottle has been removed.
        
        while True:
            led_red.value(1)
            led_green.value(0)
            led_blue.value(0)
            
            utime.sleep(1)
            
            led_red.value(0)
            led_green.value(0)
            led_blue.value(0)

            utime.sleep(1)

            light = int(readLight(photoPIN))
            
            if light < lightThreshold:
                setLED("green")
                break
    
    
    t = ds.read_time()
    day_now = "%02x" %(t[4])
    day_now = int(day_now)
    
    if day_now != day:
        day = day_now
        setLED("red")
     
"""
To get full date and time use the code below

date = ("Date: %02x/%02x/20%x" %(t[4],t[5],t[6]))
time = "%02x:%02x:%02x" %(t[2],t[1],t[0])
"""
