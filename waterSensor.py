# import the necessary modules
import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)
mcp = MCP.MCP3008(spi, cs)

# analog input channel from the water sensor (channel 0 i.e. P0)
channel = AnalogIn(mcp, MCP.P0)

# printing values from the sensor (water level, and voltage) every second
try: 
    print('Raw ADC Value: ', channel.value)
    print('ADC Voltage: ' + str(channel.voltage) + 'V')
    print ("")
    time.sleep (1)
except:
    print ("Something is wrong.")