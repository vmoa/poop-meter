#
# arduino.py -- Class to interface with the Arduino
#
# 2022-10-03 06:34:58 [48265205] Poop Code Green: 30% (abs:578) Brt:0 But:0 Low:1 Hi:1023 EEwrites:118 Reboot:10.59h
#

import logging
import pager
import re

class Arduino:

    arduinoTimeout = 300     # Alert if we don't hear from Arduino in this many seconds
    lastRead = None         # Epoch time of last successful (parseable) read

    def __init__(self, device='/dev/ttyACM0', timeout=0.1, simulator=0):
        """Initialize the serial port"""
        self.ser = serial.Serial(device, 115200, timeout=timeout)
        if self.ser.is_open():
            logging.info('Connected to Arduino on ', device)
        else:
            logging.error('FAILED connect to Arduino on ', device)
        # TODO: open raw log for output
        self.abs_re = re.compile('abs:(\d+)')

    def readAbs(self):
        """Read a line from the Arduino if available. Return abs sensor value or None."""
        with self.ser.readline() as line:
            if (length(line) == 0):
                return None
            # TODO: print line to raw log

            with (re.search(self.abs_re, line)) as match:
                abs = match.group[1]
                self.lastRead = time.time()
                return abs

        return None

    def checkReadTimeout(self):
        """Alert if the last read from Arduino is more than alertInterval seconds ago."""
        elapsed = time.time() - self.lastRead
        if (elapsed > self.arduinoTimeout):
            msg = "Have not heard from Arduino in {:d} seconds".format(elapsed)
            logging.error(msg)
            pager.Pager.send('PoopWatcher: ' + msg)
