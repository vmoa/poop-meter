#
# Manage the poop meter and water main vavle
#   Reads serial data from Arduino, but also reads analog data from poop probe via SPI
#   In this version, the Arduino data is canonical and SPI data is recorded for comparison
#   Once we get corellation between Arduino and SPI data we switch to SPI and retire Arduino
#
# Requires SPI for reading from the MCP3009 analog/digital converter
# Requires I2C for updating status on the the Grove LCD (https://wiki.seeedstudio.com/Grove-LCD_RGB_Backlight/)
#   raspi-config --> interfacing --> {spi,i2c}
#
# The running user must be a member of groups gpio and spi
#
# We also use:
#   gpiozero (https://gpiozero.readthedocs.io/en/stable/) pip3 install gpiozero rpi.gpio
#   pySerial (https://pyserial.readthedocs.io/en/latest/) pip3 install pyserial
#   Twilio helper (https://www.twilio.com/docs/libraries/python) pip3 install twilio
#   MCP library (https://github.com/adafruit/Adafruit_CircuitPython_MCP3xxx/) pip3 install adafruit-circuitpython-mcp3xxx
#   i2c smbus bindings (https://pypi.org/project/smbus/) pip3 install smbus
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
import pager
import valve


version = 'v0.9.1'      # Poop Watcher version
statusInterval = 60     # Seconds between status updates without input changes
lockfile = 0            # Global so when we lock we keep it
lockfilename = '/tmp/poop.lock'

def initialize():
    # Parse command line args
    default_logfile = '/var/log/poop.log'   # TODO: change this to daily rotation from perl code
    parser = argparse.ArgumentParser(description='RFO Poop Tank (septic) controller.')
    parser.add_argument('--debug', dest='debug', action='store_true', help='include DEBUG messages in logs')
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

    # Set up logging
    loggingConfig = dict(
        format = "%(asctime)s [%(levelname)s] %(message)s",
        datefmt = "%Y-%m-%d %H:%M:%S",
        level = logging.DEBUG if (args.debug) else logging.INFO)
    if (sys.stdin.isatty() and not args.logfile):
        print("TTY detected; logging to stderr")
    else:
        loggingConfig['filename'] = args.logfile if args.logfile else default_logfile;
    logging.basicConfig(**loggingConfig)
    logging.info("Initializing poopWatcher {}".format(version))

    # Initialize the Grove LCD
    lcd = grove.Grove()
    lcd.setRGB(0, 255, 255)  # cyan
    lcd.setText("RFO Poop Meter\nVersion {}".format(version))
    sleep(2)  # This should be an LCD freeze display option intead of a sleep

    # Initialize devices
    gpio = device.Gpio(simulate = args.simulate)
    logging.info(device.printStatus())

    # Initialize pager
    mypager = pager.Pager(simulate = args.simulate)
    mypager.set_default_recip('dave')

    return(args)



if __name__ == '__main__':
    """Set up interrupts and a per-second callback, the pause forever"""
    args = initialize()
    device.perSecond()

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
