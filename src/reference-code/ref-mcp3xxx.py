# Lifted from https://github.com/adafruit/Adafruit_CircuitPython_MCP3xxx

import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

from time import sleep

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
#cs = digitalio.DigitalInOut(board.D5)
cs = digitalio.DigitalInOut(board.CE0)
cs.switch_to_output(True)
cs.value = 0
print(cs)
print("value: {}".format(cs.value))

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create an analog input channel on pin 0
chan = AnalogIn(mcp, MCP.P0)

while (1):
    print('Raw ADC Value: ', chan.value)
    print('ADC Voltage: ' + str(chan.voltage) + 'V')
    sleep(2)
