#
# adc.py -- Class to read the poop meter via SPI from the ADC (MCP3008)
#
# https://learn.adafruit.com/mcp3008-spi-adc/python-circuitpython
#

import logging
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

import pager

class Adc:

    def __init__(self):
        """Initialize the spi bus and chip select and create the mcp object."""
        self.spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
        self.cs = digitalio.DigitalInOut(board.D5)
        self.mcp = MCP.MCP3008(self.spi, self.cs)

    def channel(pin=MCP.P0):
        # create an analog input channel
        self.chan = AnalogIn(self.mcp, pin)

    def value(self):
        return(self.chan.value)

    def voltage(self):
        return(self.chan.voltage)

