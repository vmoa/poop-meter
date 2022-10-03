#
# valve.py -- Class to manipulate the water valve
#

import logging
import threading
from time import sleep

import device
import globalvar
import pager

class Valve:

    timeout = 30    # Seconds to wait for valve to open/close

    def __init__(self):
        return

    def command(self, action=''):
        """Open or close the valve."""
        if (action != 'Open' and action != 'Close'):
            logging.error("valve.commmand() called with invalid action: {}".format(action))
            return

        if (device.Gpio.is_override.isOn()):
            logging.warning("valve.commmand(): manual override in use")
            return

        if (action == 'Open' and device.Gpio.is_opened.isOn()):
            logging.warning("valve.command(Open): valve is already opened")
            return
        if (action == 'Close' and device.Gpio.is_closed.isOn()):
            logging.warning("valve.command(Close): valve is already closed")
            return

        logging.info("{}ing valve (timeout in {} seconds)".format(action, self.timeout))
        globalvar.Globalvar.pager.send('dave', 'PoopWatcher is {}ing the main water vavle'.format(action))
        if (action == 'Open'):
            device.Gpio.do_open_close.turnOff()  # Off == Open
            threading.Timer(self.timeout, self.when_open_timeout).start()
        else:
            device.Gpio.do_open_close.turnOn()   # On == Close
            threading.Timer(self.timeout, self.when_close_timeout).start()
        sleep(0.1)
        device.Gpio.do_enable.turnOn()       # Start action

    def when_opened():
        """Callback for when valve is being opened"""
        logging.info("Open complete")
        device.Gpio.do_enable.turnOff()
        device.printStatus()

    def when_closed():
        """Callback for when valve is being closed"""
        logging.info("Close complete")
        device.Gpio.do_enable.turnOff()
        device.printStatus()

    def when_open_timeout(self):
        if (device.Gpio.is_opened.isOff()):
            logging.error("Valve open not detected after {} seconds".format(self.timeout))
        device.Gpio.do_enable.turnOff()

    def when_close_timeout(self):
        if (device.Gpio.is_closed.isOff()):
            logging.error("Valve close not detected after {} seconds".format(self.timeout))
        device.Gpio.do_enable.turnOff()
