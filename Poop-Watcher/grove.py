#!/usr/bin/env python
#
# Initially based on GrovePi Example for using the Grove - LCD RGB Backlight (http://www.seeedstudio.com/wiki/Grove_-_LCD_RGB_Backlight)
# but pruned and extended to be more flexibibile for the poop meter by dkensiski

import logging
import time
import smbus
import sys
import threading

class Grove:

    # Device definition
    bus = smbus.SMBus(1)
    DISPLAY_RGB_ADDR = 0x62
    DISPLAY_TEXT_ADDR = 0x3e

    # Ensure we only run one command at a time
    grove_lock = threading.Lock()

    # Bitmasks for cursor positioning
    LINE0 = 0x80
    LINE1 = 0xC0

    def __init(self, version='v?'):
        logging.debug("grove.init()")

        if sys.platform == 'uwp':
            import winrt_smbus as smbus
            self.bus = smbus.SMBus(1)
        else:
            import smbus
            import RPi.GPIO as GPIO
            rev = GPIO.RPI_REVISION
            if rev == 2 or rev == 3:
                self.bus = smbus.SMBus(1)
            else:
                self.bus = smbus.SMBus(0)

        self.sendCommand(0x08 | 0x04)    # display on, no cursor
        self.sendCommand(0x28)           # 2 lines
        time.sleep(.05)
        self.setText("Poop Meter {}\nLet's Poop!".format(version))

    @classmethod
    def setRGB(self, r, g, b):
        """Set backlight color (values from 0..255 for each)."""
        with self.grove_lock:
            logging.debug("grove.setRGB({},{},{})".format(r,g,b))
            self.bus.write_byte_data(self.DISPLAY_RGB_ADDR, 0, 0)
            self.bus.write_byte_data(self.DISPLAY_RGB_ADDR, 1, 0)
            self.bus.write_byte_data(self.DISPLAY_RGB_ADDR, 0x08, 0xaa)
            self.bus.write_byte_data(self.DISPLAY_RGB_ADDR, 4, r)
            self.bus.write_byte_data(self.DISPLAY_RGB_ADDR, 3, g)
            self.bus.write_byte_data(self.DISPLAY_RGB_ADDR, 2, b)

    @classmethod
    def setColor(self, color):
        """Set the backlight to a common color."""
        if (color == 'red'):
            self.setRGB(255,0,0)
        elif (color == 'green'):
            self.setRGB(0,255,0);
        elif (color == 'blue'):
            self.setRGB(0,0,255)
        elif (color == 'cyan'):
            self.setRGB(0,255,255)
        elif (color == 'indigo'):
            self.setRGB(255,0,255)
        elif (color == 'yellow'):
            self.setRGB(255,255,0)
        elif (color == 'orange'):
            self.setRGB(255,64,0)
        else:
            logging.error("grove.setColor: {} unknown".format(color))

    @classmethod
    def sendCommand(self, cmd):
        """Send command to display."""
        with self.grove_lock:
            logging.debug("grove.sendCommand({})".format(cmd))
            self.bus.write_byte_data(self.DISPLAY_TEXT_ADDR, 0x80, cmd)

    @classmethod
    def setText(self, text):
        """Set display text with wrapping and \n support."""
        logging.debug("grove.setText({})".format(text))
        self.sendCommand(0x01) # clear display
        time.sleep(.05)
        self.setText_norefresh(text)

    @classmethod
    def setText_norefresh(self, text):
        """Update the display without erasing the display."""
        logging.debug("grove.setText_norefresh({})".format(text))
        self.sendCommand(0x02) # return home
        time.sleep(.05)
        while len(text) < 32: #clears the rest of the screen
            text += ' '
        count = 0
        row = 0
        for c in text:
            if c == '\n' or count == 16:
                count = 0
                row += 1
                if row == 2:
                    break
                self.sendCommand(0xc0)
                if c == '\n':
                    continue
            count += 1
            self.printChar(c)

    @classmethod
    def selectLine(self, line):
        """Select which line to update next."""
        logging.debug("grove.selectLine({})".format(line))
        if (line == 0):
            self.sendCommand(0x80)
        else:
            self.sendCommand(0xc0)
        pass

    @classmethod
    def setCursor(self, row, col):
        logging.debug("grove.setCursor({},{})".format(row,col))
        if (col < 0):
            col = 0
        if (col > 15):
            col = 15
        if (row == 0):
            data = col | self.LINE0
        else:
            data = col | self.LINE1
        self.sendCommand(data)

    @classmethod
    def clearLine(self, line=0):
        """Clear the current (or specified) line."""
        logging.debug("grove.clearLine({})".format(line))
        if (line > 0):
            self.selectLine(line)
        self.setText(' '*16)

    @classmethod
    def printChar(self, c):
        with self.grove_lock:
            self.bus.write_byte_data(self.DISPLAY_TEXT_ADDR, 0x40, ord(c))

    @classmethod
    def printLine(self, text, line=0):
        """Set text on current (or specified) line and truncate to EOL."""
        logging.debug("grove.printLine({},{})".format(text,line))
        if (line > 0):
            self.selectLine(line)
        text += ' '*16      # Space pad at end
        text = text[:16]    # And truncate
        for c in text:
            self.printChar(c)


# Unit test
if (__name__ == "__main__"):
    loggingConfig = dict(
        format = "%(asctime)s [%(levelname)s] %(message)s",
        datefmt = "%Y-%m-%d %H:%M:%S",
        level = logging.DEBUG)
    logging.basicConfig(**loggingConfig)
    logging.info("Grove unit test")

    lcd = Grove()
    lcd.setRGB(0,128,64)
    lcd.setText("Hello world\nLCD Unit Test......")
    time.sleep(2)
    lcd.selectLine(0)
    lcd.printLine("This is line 0")
    lcd.selectLine(1)
    lcd.printLine("This is line 1")
    time.sleep(1)

    for color in [ 'red', 'green', 'blue', 'cyan', 'purple', 'yellow', 'orange' ]:
        lcd.printLine(color, line=1)
        lcd.setColor(color)
        print(color)
        time.sleep(2)

    direction = -1
    while (True):
        direction = -direction
        columns = range(0,15,1) if (direction > 0) else range(15,0,-1)
        for col in columns:
            lcd.setRGB(255-16*col, 16*col, 128)
            lcd.setCursor(1, col-direction)
            lcd.printChar(' ')
            lcd.setCursor(1, col)
            lcd.printChar('x')
            time.sleep(0.08)
