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
from statistics import mean

import pager

class Adc:

    val_array = []
    voltage_array = []
    num_samples = 10

    full_value = 65535   # Value returned when the tank is ready to burst

    def __init__(self):
        """Initialize the spi bus and chip select and create the mcp object."""
        self.spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
        self.cs = digitalio.DigitalInOut(board.D8)  # GPIO8 == CE0
        self.mcp = MCP.MCP3008(self.spi, self.cs)
        self.channel()

    def channel(self, pin=MCP.P0):
        """Create a single-ended analog input channel on pin."""
        self.chan = AnalogIn(self.mcp, pin)

    def differentailChannel(self, pin1=MCP.P0, pin2=MCP.P1):
        """Create a differential analgon input channel between pins1 and pins2.
           Note that not all combinations are possible; see MCP3008 documentation."""
        self.chan = AnalogIn(mcp, pin1, pin2)

    def abs_value(self):
        return(self.chan.value)

    def abs_voltage(self):
        return(self.chan.voltage)

    def average(self, array, sample):
        """Prepend new sample to the array, turncate at num_samples, and return the average."""
        array.insert(0, sample)     # TODO: Should probably do something to ignore crazy outliers
        del(array[self.num_samples:])
        return(round(mean(array)))

    def get_value(self):
        """Return the average value over the last <num_samples>."""
        return(self.average(self.val_array, self.abs_value()))

    def get_voltage(self):
        """Return the average voltage over the last <num_samples>."""
        return(self.average(self.voltage_array, self.abs_voltage()))

    def get_percent(self):
        """Return the percentage full using averaged <value> as index."""
        return(self.get_value() / self.full_value * 100)