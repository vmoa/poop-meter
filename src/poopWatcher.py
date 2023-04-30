#!/usr/bin/python
#
# Manage the poop meter and water main vavle
#   Reads analog voltage from poop probe via the ADC connected to the SPI bus and operates the remote valve
#   to shut off the water main before the holding take is full.  Also sends SMS satatus notifications.
#
# Requires SPI for reading from the MCP3008 analog/digital converter
# Requires I2C for updating status on the the Grove LCD (https://wiki.seeedstudio.com/Grove-LCD_RGB_Backlight/)
#   raspi-config --> interfacing --> {spi,i2c}
#
# We also use:
#   gpiozero (https://gpiozero.readthedocs.io/en/stable/) sudo pip3 install gpiozero rpi.gpio
#   pySerial (https://pyserial.readthedocs.io/en/latest/) sudo pip3 install pyserial
#   Twilio helper (https://www.twilio.com/docs/libraries/python) sudo pip3 install twilio
#   MCP library (https://github.com/adafruit/Adafruit_CircuitPython_MCP3xxx/) sudo pip3 install adafruit-circuitpython-mcp3xxx
#   i2c smbus bindings (https://pypi.org/project/smbus/) sudo pip3 install smbus
#
#  sudo apt-get install python3-pigpio
#
# Running user needs to be a member of groups: i2c, spi, gpio

import argparse
import datetime
import errno
import fcntl
import glob
import logging
import os
import serial
import signal
import sys
import threading
from time import sleep

import device
import grove
import override
import pager
import poop
import valve


# Pull version from first line of VERSION file
version = os.popen('head -1 VERSION').read()[0:-1]

lockfile = 0            # Global so when we lock we keep it
lockfilename = '/tmp/poop.lock'

def initialize():
    # Parse command line args
    default_logfile = '/var/log/poop.log'   # TODO: change this to daily rotation
    parser = argparse.ArgumentParser(description='RFO Poop Tank (septic) controller.')
    parser.add_argument('--debug', dest='module', action='append', help='log debugging messages for module')
    parser.add_argument('--test-mode', dest='test_mode', action='store_true', help='enter test mode')
    parser.add_argument('--simulate', dest='simulate', action='store_true', help='simulate (do not send) pages')
    parser.add_argument('--log-file', '-L', dest='logfile', action='store', help='log filename (default {})'.format(default_logfile))
    args = parser.parse_args()

    # Acquire an exclusive lock
    global lockfile
    try:
        lockfile = open(lockfilename, "a+")
        if (lockfile):
            fcntl.lockf(lockfile, fcntl.LOCK_EX|fcntl.LOCK_NB)
    except OSError as e:
        if (e.errno == errno.EACCES or e.errno == errno.EAGAIN):
            sys.exit("ABORT! poopWatcher is already running!")

    # Annotate the lock file with our pid
    lockfile.seek(0)
    lockfile.truncate()
    lockfile.write("{}\n".format(os.getpid()))
    lockfile.flush()

    print ("Logfile: {}".format(args.logfile))
    # Set up logging
    loggingConfig = dict(
        format = "%(asctime)s [%(levelname)s] %(message)s",
        datefmt = "%Y-%m-%d %H:%M:%S",
        level = logging.DEBUG if (args.module) else logging.INFO)
    if (sys.stdin.isatty() and not args.logfile):
        print("TTY detected; logging to stderr")
    else:
        loggingConfig['filename'] = args.logfile if args.logfile else default_logfile;
    print(loggingConfig)
    logging.basicConfig(**loggingConfig)
    logging.info("Initializing poopWatcher Version {}".format(version))
    logging.info("Working directory: {}".format(os.popen('pwd').read()[0:-1]))

    # Enable module specific debugging
    if (args.module):
        for mod in args.module:
            if (mod == 'grove'):
                grove.Grove.setDebug()
            elif (mod == 'override'):
                override.Override.setDebug()
            else:
                logging.error("Debug module {} unknown; ignored".format(mod))

    # Initialize the Grove LCD
    lcd = grove.Grove()
    lcd.setRGB(0, 255, 255)  # cyan
    lcd.latentMessage("RFO Poop Meter\n  {}".format(version), 2)

    # Initialize devices
    gpio = device.Gpio(lcd = lcd)
    poop.Poop.simulateMode(args.simulate)
    override.Override.simulateMode(args.simulate)
    logging.info(poop.Poop.printStatus())

    # Initialize pager
    mypager = pager.Pager(simulate = args.simulate)
    mypager.set_default_recip('dave')

    return(args)



if __name__ == '__main__':
    """Set up interrupts and a per-second callback, the pause forever"""
    args = initialize()
    poop.Poop.syscheck()
    poop.Poop.perSecond()
    threading.Timer(3.0, poop.Poop.printStatus).start()  # Update the display in a few seconds

    if (args.test_mode):
        logging.info("Entering test mode")
        pager.Pager.send('Test mode starting')
        valve = valve.Valve()
        while (1):
            valve.command('Open')
            sleep(60)
            valve.command('Close')
            sleep(60)
        exit

    signal.pause()
