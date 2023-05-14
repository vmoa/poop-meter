#
# adc.py -- Class to read the poop meter via SPI from the ADC (MCP3008)
#
# Uses CircuitPython mcp3xxx library (which includes Blinka):
# https://learn.adafruit.com/mcp3008-spi-adc/python-circuitpython
#

import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from statistics import mean
from time import sleep     # Only used in unit testing

unittest = False

class Adc:

    # Arrays to hold <num_samples> values for averaging
    val_array = []
    voltage_array = []
    num_samples = 10

    # Holding places for averaged values
    value = -1
    voltage = -1.0
    percent = -1.0

    # Values returned when the tank is empty and ready to burst
    # These should probably be scraped out of poop.py
    empty = 222
    full  = 888

    def __init__(self):
        """Initialize the spi bus and chip select and create the mcp object."""
        self.spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
        self.cs = digitalio.DigitalInOut(board.D8)  # GPIO8 == CE0
        testprint(self.cs)
        self.mcp = MCP.MCP3008(self.spi, self.cs)
        testprint(self.mcp)
        self.channel()

    def channel(self, pin=MCP.P0):
        """Create a single-ended analog input channel on pin."""
        testprint("channel({})".format(pin))
        self.chan = AnalogIn(self.mcp, pin)

    def differentailChannel(self, pin1=MCP.P0, pin2=MCP.P1):
        """Create a differential analgon input channel between pins1 and pins2.
           Note that not all combinations are possible; see MCP3008 documentation."""
        testprint("differentialChannel({},{})".format(pin1,pin2))
        self.chan = AnalogIn(mcp, pin1, pin2)

    def abs_value(self):
        v = int(self.chan.value / 63)  # Restore scale; why do I have to do this???
        testprint("abs_value(): {}".format(v))
        return(v)

    def abs_voltage(self):
        testprint("abs_voltage(): {}".format(self.chan.voltage))
        return(float(self.chan.voltage))

    def average(self, array, sample):
        """Prepend new sample to the array, turncate at num_samples, and return the average."""
        array.insert(0, sample)     # TODO: Should probably do something to ignore crazy outliers
        del(array[self.num_samples:])
        testprint("average() array: {}".format(array))
        return(float(mean(array)))

    def do_sample(self):
        """Collect and average new samples, storing them in class variables for later retrieval.
           This should be called at a regular interval by device.per_second()."""
        self.value = int(self.average(self.val_array, self.abs_value()))
        self.voltage = self.average(self.voltage_array, self.abs_voltage())
        self.percent = (self.value - self.empty) / (self.full - self.empty) * 100

    def get_value(self):
        """Return the average value over the last <num_samples>."""
        return(self.value)

    def get_voltage(self):
        """Return the average voltage over the last <num_samples>."""
        return(float(self.voltage))

    def get_percent(self):
        """Return the percentage full using averaged <value> as index."""
        return(float(self.percent))

    def get_values(self):
        """Return all three averaged values (value, voltabe, percentage)."""
        return(self.get_value(), self.get_voltage(), self.get_percent())


def testprint(arg):
    if (unittest):
        print(arg)

# Unit test
if (__name__ == "__main__"):
    unittest = True
    adc = Adc()

    while (1):
        adc.do_sample()
        print("ABS: {value} {volt:4.2f}v --- AVG: {avg_value} {avg_volt:3.2f}v {pct:2.1f}%".format(
            value=adc.abs_value(), volt=adc.abs_voltage(),
            avg_value=int(adc.get_value()), avg_volt=adc.get_voltage(), pct=adc.get_percent()))
        sleep(1)
        
    #poopLevel, poopVolts, poopPercent = Gpio.adc.get_values()
