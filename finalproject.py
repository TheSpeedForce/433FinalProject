# 1. everything is off, led is blue (standby)
# 2. button press? pressed: goes to 3; else: 1
# 3. runs all functions, error? yes: led turns red, goes to 9; no: led turns on green, goes to 4
# 4. get reading from all sensor and camera
# 5. save in log files
# 6. read log file to make data file
# 7. send data to server
# 8. repeat from 4
# 9. shows error on screen, exit

from threading import Thread

# Import Raspberry Pi GPIO library
import RPi.GPIO as GPIO

import Adafruit_DHT as DHT

import os


# Ignore warning for now
GPIO.setwarnings(False) 

# Use physical pin numbering
GPIO.setmode(GPIO.BOARD)


# Set sensors pin
dht_pin = 4
ldr_pin = 8

# Set RGB LED pins
rgb_red_pin = 38
rgb_green_pin = 36
rgb_blue_pin = 35

# Set button pin
button_pin = 37

# Setting LDR sensors
GPIO.setup(ldr_pin, GPIO.IN)

# Setting button input
GPIO.setup(button_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

# Class for RGB LED control
class RGB_LED(object):
    commands = {"on": GPIO.HIGH, "off": GPIO.LOW}
    def __init__(self, red_pin, blue_pin, green_pin):
        self.red_pin = red_pin
        self.blue_pin = blue_pin
        self.green_pin = green_pin
        
        # Set dictionary for pins
        self.pins = {"red": self.red_pin, "blue": self.blue_pin, "green": self.green_pin}
        
        # Setting up RGB LED pins
        self.setup()

    # Function to set up RGB LED    
    def setup(self):
        # Set every pin from dictionary
        for pin in self.pins.values():
            GPIO.setup (pin, GPIO.OUT)

    # Function to output given command on given pin
    def output(self, pin, command):
        GPIO.output (self.pins[pin], self.commands[command])

class weather_reporter(object):
    # Constructor
    def __init__(self):
        self.keepGoing = False
    
    # Function to terminate execution
    def terminate(self):
        self.keepGoing = False
    def execute(self):
        self.keepGoing = True
    # Function to log sensor readings
    def log_reading(self):
        while self.keepGoing:

            # DHT Sensor
            dht_sensor = DHT.DHT11
            humidity,temperature = DHT.read_retry(dht_sensor, dht_pin)
            if humidity is not None and temperature is not None:
                print (f'Humidity: {humidity}%, Temperature: {temperature}*C')
            else:
                print ("Reading failed.")
            
            # LDR Sensor
            print (GPIO.input(ldr_pin))
            print ("")

            #Water Sensor
            try: 
                os.system("python3 waterSensor.py")    
            except:
                print ("Something is wrong.")
            
            # Camera module
            os.system("raspistill -o test.jpg -n --timeout 0")

def switch():

    # Set variables to manage running
    running = False

    # Create RGB LED object
    rgb_led = RGB_LED(rgb_red_pin, rgb_blue_pin, rgb_green_pin)
    rgb_led.output("blue", "on")

    # Create weather reporter object
    reporter  = weather_reporter()
    
    while True:

        # Wait for button press
        GPIO.wait_for_edge(button_pin, GPIO.RISING)

        # Change running if button pressed
        running = not running

        # Start log reading if running
        if running:
            try:

                # Change LED to green
                reporterThread = Thread(target = reporter.log_reading)
                reporter.execute()
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
           

switch_thread = Thread (target = switch)

switch_thread.start()