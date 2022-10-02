#
#  Interface with the poop meter via serial port
#
# easy_install -U pyserial

import sys
import time
import serial
import glob

for device in glob.glob("/dev/tty.usbmodem*"):
	print 'Opening ', device
	ser = serial.Serial(device, 115200)
	ser.isOpen()

	while 1 :
		out = ''
		# let's not overwhelm our CPU with a tight loop (of course a better way would be a timed wait serial read...l timed wait serial read...))
		time.sleep(1)
		while ser.inWaiting() > 0:
			out += ser.read(1)
		if out != '':
			sys.stdout.write('>> ' + out)

