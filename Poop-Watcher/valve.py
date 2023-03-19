#
# Class Valve with Poop Meter valve twiddling logic
#

import datetime
import logging
import threading
import time

import adc
import device
import grove
import override
import pager
import poop

class Valve:

    valveTimeExceeded = 30  # Seconds inside of which the operation should succeeed
    valveStartTime = 0      # Time we started the valve operation
    operation = None        # Operation in progress

    def __init__(self):
        pass

    @classmethod
    def operate(cls, op):
        """Open or Close the valve; keep checking back to ensure operation completes."""
        now = int(time.time())
        if (cls.valveStartTime == 0):
            # No operation is going on right now
            if ((op == 'close' and device.Gpio.is_closed.isOn()) or (op == 'open' and device.Gpio.is_opened.isOn())):
                return   # Valve is already in the state we want
            msg = "{}ing water main valve".format(op[0:4])
            logging.info("Valve.operate(): {}".format(msg))
            pager.Pager.send("NOTICE: {}".format(msg))
            if (op == 'close'):
                device.Gpio.set_direction.setClose()
            else:
                device.Gpio.set_direction.setOpen()
            device.Gpio.do_enable.turnOn()
            cls.valveStartTime = now
            cls.operation = op

        else:
            # Operation in progress
            elapsed = now - cls.valveStartTime
            if ((op == 'close' and device.Gpio.is_closed.isOn()) or (op == 'open' and device.Gpio.is_opened.isOn())):
                logging.info("Valve.operate(): valve {}ed after {} seconds".format(op[0:4], elapsed))
                device.Gpio.do_enable.turnOff()
                cls.valveStartTime = 0
                cls.operation = None
            else:
                if (elapsed > cls.valveTimeExceeded):
                    msg = "valve failed to {} after {} seconds; giving up".format(op, elapsed)
                    logging.error("Valve.operate(): {}".format(msg))
                    pager.Pager.send("WARNING: {}".format(msg))
                    device.Gpio.do_enable.turnOff()
                    cls.valveStartTime = 0
                    cls.operation = None

    @classmethod
    def maybeOperate(cls, value):
        """Open or close the valve if threshold conditions are met."""

        # We can't do anything if manual override is set
        if (override.Override.check()):
            if (cls.operation):
                logging.warning("Manual override interrupted valve {}! Cancelling operation.".format(cls.operation))
                cls.operation = False
                cls.valveStartTime = 0
            return

        if (cls.operation):
            # Operation in progress
            cls.operate(cls.operation)
        if (device.Gpio.is_closed.isOff()):
            if (value >= poop.Poop.threshold["PANIC"]):
                cls.operate('close')
        elif (device.Gpio.is_opened.isOff()):
            if (value <= poop.Poop.threshold["nominal"]):
                cls.operate('open')

