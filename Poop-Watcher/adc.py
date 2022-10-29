#
# adc.py -- Class to read the poop meter via SPI from the ADC (MCP3008)
#
# Uses CircuitPython mcp3xxx library (which includes Blinka):
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
        self.cs = digitalio.DigitalInOut(board.D8)  # GPIO8 == CE0
        self.mcp = MCP.MCP3008(self.spi, self.cs)

    def channel(pin=MCP.P0):
        """Create a single-ended analog input channel on pin."""
        self.chan = AnalogIn(self.mcp, pin)

    def differentailChannel(pin1=MCP.P0, pin2=MCP.P1):
        """Create a differential analgon input channel between pins1 and pins2.
           Note that not all combinations are possible; see MCP3008 documentation."""
        self.chan = AnalogIn(mcp, pin1, pin2)

    def value(self):
        return(self.chan.value)

    def voltage(self):
        return(self.chan.voltage)
