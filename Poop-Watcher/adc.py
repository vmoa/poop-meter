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
    voltage = -1
    percent = -1

    # Value returned when the tank is ready to burst
    full_value = 65535

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
        testprint("abs_value(): {}".format(self.chan.value))
        return(self.chan.value)

    def abs_voltage(self):
        testprint("abs_voltage(): {}".format(self.chan.voltage))
        return(self.chan.voltage)

    def average(self, array, sample):
        """Prepend new sample to the array, turncate at num_samples, and return the average."""
        array.insert(0, sample)     # TODO: Should probably do something to ignore crazy outliers
        del(array[self.num_samples:])
        return(round(mean(array)))

    def do_sample(self):
        """Collect and average new samples, storing them in class variables for later retrieval.
           This should be called at a regular interval by device.per_second()."""
        self.value = self.average(self.val_array, self.abs_value())
        self.voltage = self.average(self.voltage_array, self.abs_voltage())
        self.percent = self.value / self.full_value * 100

    def get_value(self):
        """Return the average value over the last <num_samples>."""
        return(self.value)

    def get_voltage(self):
        """Return the average voltage over the last <num_samples>."""
        return(self.voltage)

    def get_percent(self):
        """Return the percentage full using averaged <value> as index."""
        return(self.percent)

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
        print("ABS: {} {}v --- AVG: {} {}v {}%".format(
            adc.abs_value(), adc.abs_voltage(),
            adc.get_value(), adc.get_voltage(), adc.get_percent()))
        sleep(1)
        
    #poopLevel, poopVolts, poopPercent = Gpio.adc.get_values()
