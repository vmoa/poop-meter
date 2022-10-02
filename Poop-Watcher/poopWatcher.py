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
# We also use:
#   pySerial (https://pyserial.readthedocs.io/en/latest/) pip3 install pyserial
#   Twilio helper (https://www.twilio.com/docs/libraries/python) pip3 install twilio

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

import arduino
import pager

arduino = new Arduino

	while 1 :
		out = ''
		# let's not overwhelm our CPU with a tight loop (of course a better way would be a timed wait serial read...l timed wait serial read...))
		time.sleep(1)
		while ser.inWaiting() > 0:
			out += ser.read(1)
		if out != '':
			sys.stdout.write('>> ' + out)


