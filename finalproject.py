from threading import Thread

# Import Raspberry Pi GPIO library
import RPi.GPIO as GPIO

import Adafruit_DHT as DHT

import os

# Import time module
import time


# Ignore warning for now
GPIO.setwarnings(False) 
# Use physical pin numbering

GPIO.setmode(GPIO.BOARD)

dht_pin = 4
water_pin = 5

rgb_red_pin = 38
rgb_green_pin = 36
rgb_blue_pin = 35

ldr_pin = 8
button_pin = 37

wait_time = 2

# Setting input sensors
GPIO.setup(ldr_pin, GPIO.IN)
GPIO.setup(button_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

dht_sensor = DHT.DHT11


# Class for RGB LED control
class RGB_LED(object):
    def __init__(self, red_pin, blue_pin, green_pin):
        self.red_pin = red_pin
        self.blue_pin = blue_pin
        self.green_pin = green_pin
        # Setting up RGB LED pins

        self.pins = {"red": self.red_pin, "blue": self.blue_pin, "green": self.green_pin}
        self.setup()
        self.commands = {"on": GPIO.HIGH, "off": GPIO.LOW}
    def setup(self):
        for pin in self.pins.values():
            GPIO.setup (pin, GPIO.OUT)
    def output(self, pin, command):
        GPIO.output(self.pins[pin], self.commands[command])

# class weather_sensors(object):
#     def __init__(self,dht_pin, ldr_pin, water_pin):
#         self.running = True
#         self.dht_pin = dht_pin
#         self.ldr_pin = ldr_pin
#         self.water_pin = water_pin
    
#     def dht_sensor(self):
#         sensor = DHT.DHT11
#         while True:
#             humidity,temperature = DHT.read_retry(sensor, self.dht_pin)
#             if humidity is not None and temperature is not None:
#                 print (f'Humidity: {humidity}%, Temperature: {temperature}*C')
#             else:
#                 print ("Reading failed.")
#             time.sleep(wait_time)

#     def ldr_sensor(self):
#         while True:
#             print (GPIO.input(self.ldr_pin))
#             print ("")
#             time.sleep(wait_time)
#     def water_sensor(self):
#         pass
    
class weather_reporter(object):
    def __init__(self):
        self.running = True
    def terminate(self):
        self.running = False
    def log_reading(self):
        while self.running:
            humidity,temperature = DHT.read_retry(dht_sensor, dht_pin)
            if humidity is not None and temperature is not None:
                print (f'Humidity: {humidity}%, Temperature: {temperature}*C')
            else:
                print ("Reading failed.")
            print (GPIO.input(ldr_pin))
            print ("")
            # try: 
            #     print('Raw ADC Value: ', channel.value)
            #     print('ADC Voltage: ' + str(channel.voltage) + 'V')
            #     print ("")
            # except:
            #     print ("Something is wrong.")
            
            #os.system("raspistill -o test.jpg -n")
            time.sleep(wait_time)


# 1. everything is off, led is blue (standby)
# 2. button press? pressed: goes to 3; else: 1
# 3. runs all functions, error? yes: led turns red, goes to 9; no: led turns on green, goes to 4
# 4. get reading from all sensor and camera
# 5. save in log files
# 6. read log file to make data file
# 7. send data to server
# 8. repeat from 4
# 9. shows error on screen, exit
global running
running = False



def switch():
    ON = True
    OFF = False
    state = OFF
    rgb_led = RGB_LED(rgb_red_pin, rgb_blue_pin, rgb_green_pin)
    rgb_led.output("blue", "on")
    while True:
        button_state = GPIO.input(button_pin)
        print(button_state)
        if button_state == 0:
            time.sleep(0.5)
            if state == OFF:
                state = ON
            else:
                state = OFF

        if state == ON:
            try:
                reporter  = weather_reporter()
                reporterThread = Thread(target = reporter.log_reading)
                reporterThread.start();
                rgb_led.output("red", "off")
                rgb_led.output("blue", "off")
                rgb_led.output("green", "on")
            except:
                rgb_led.output("red", "on")
                rgb_led.output("blue", "off")
                rgb_led.output("green", "off")
        else:
            try:
                reporter.terminate()
                rgb_led.output("red", "off")
                rgb_led.output("blue", "on")
                rgb_led.output("green", "off")
            except:
                rgb_led.output("red", "on")
                rgb_led.output("blue", "off")
                rgb_led.output("green", "off")
           

#switch_thread = Thread (target = switch)

#switch_thread.start()
global off
off = True
def on(button_pin):
    global off
    if off:
        print (1)
        rgb_led.output("green", "on")
        off = False
        time.sleep(2)
    else:
        rgb_led.output("green", "off")
        off = True
        time.sleep(2)
        
def off():
    rgb_led("green", "off")
    
#GPIO.add_event_detect(button_pin, GPIO.RISING, callback = on)


rgb_led = RGB_LED(rgb_red_pin, rgb_blue_pin, rgb_green_pin)
rgb_led.output("blue", "on")
ON = True
OFF = False
state = OFF
    
while True:
    button_state = GPIO.input(button_pin)
    print(button_state)
    if button_state == 0:
        time.sleep(1)
        if state == OFF:
            state = ON
        else:
            state = OFF

    if state == ON:
        try:
            rgb_led.output("red", "off")
            rgb_led.output("blue", "off")
            rgb_led.output("green", "on")
            humidity,temperature = DHT.read_retry(dht_sensor, dht_pin)
            if humidity is not None and temperature is not None:
                print (f'Humidity: {humidity}%, Temperature: {temperature}*C')
            else:
                print ("Reading failed.")
            print (GPIO.input(ldr_pin))
            print ("")
            # try: 
            #     print('Raw ADC Value: ', channel.value)
            #     print('ADC Voltage: ' + str(channel.voltage) + 'V')
            #     print ("")
            # except:
            #     print ("Something is wrong.")
            
            #os.system("raspistill -o test.jpg -n")
            time.sleep(wait_time)

            
        except:
            rgb_led.output("red", "on")
            rgb_led.output("blue", "off")
            rgb_led.output("green", "off")
    else:
        try:
            rgb_led.output("red", "off")
            rgb_led.output("blue", "on")
            rgb_led.output("green", "off")
        except:
            rgb_led.output("red", "on")
            rgb_led.output("blue", "off")
            rgb_led.output("green", "off")
       


