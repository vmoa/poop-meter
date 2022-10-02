#
# Manage the poop meter and water main vavle
#   Reads serial data from Arduino, but also reads analog data from poop probe via SPI
#   In this version, the Arduino data is canonical and SPI data is recorded for comparison
#   Once we get corellation between Arduino and SPI data we switch to SPI and retire Arduino
#
# Requires SPI for reading from the MCP3009 analog/digital converter
# Requires I2C for updating status on the the Grove LCD
#   raspi-config --> interfacing --> {spi,i2c}
#
# The running user must be a member of group 'gpio'
#
# We also use:
#   gpiozero (https://gpiozero.readthedocs.io/en/stable/) pip3 install gpiozero rpi.gpio
#   pySerial (https://pyserial.readthedocs.io/en/latest/) pip3 install pyserial
#   Twilio helper (https://www.twilio.com/docs/libraries/python) pip3 install twilio
#
#  sudo apt-get install python3-pigpio

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

import arduino
import device
import pager
import valve


version = 'v0.9.0'      # Poop Watcher version
statusInterval = 60     # Seconds between status updates without input changes
lockfile = 0            # Global so when we lock we keep it
lockfilename = '/tmp/poop.lock'

def initialize():
    # Parse command line args
    default_logfile = '/var/log/poop.log'   # TODO: change this to daily rotation from perl code
    parser = argparse.ArgumentParser(description='RFO Poop Tank (septic) controller.')
    parser.add_argument('--debug', dest='debug', action='store_true', help='include DEBUG messages in logs')
    parser.add_argument('--test-mode', dest='test_mode', action='store_true', help='enter test mode')
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

    # Initialize devices
    gpio = device.Gpio()
    logging.info(device.printStatus())

    return(args)



if __name__ == '__main__':
    """Set up interrupts and a per-second callback, the pause forever"""
    args = initialize()
    device.perSecond()

    if (args.test_mode):
        logging.info("Entering test mode")
        valve = valve.Valve()
        while (1):
            valve.command('Open')
            sleep(60)
            valve.command('Close')
            sleep(60)
        exit

    signal.pause()
