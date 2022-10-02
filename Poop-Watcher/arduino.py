#
# arduino.py -- Class to interface with the Arduino
#

Class arduino:

    def __init__(self, device='/dev/ttyACM0', timeout=0.1, simulator=0):
        """Initialize the serial port"""
        self.ser = serial.Serial(device, 115200, timeout=timeout)
        if self.ser.is_open():
            print 'Connected to Arduino on ', device
        else:
            print 'FAILED connect to Arduino on ', device

    def read(self):
        """Read a line from the Arduino if available."""
        return self.ser.readline()

