#
# Class Override with manual override verification and notification logic
#

import datetime
import logging
import threading
import time

import adc
import device
import grove
import pager


class Override:

    initialNotifySec = 300      # Seconds before sending first page about manual override (5 minutes grace)
    repeatNotifySec = 86400     # Seconds between subsequent pages about manual override (daily)

    startTime = 0           # Time override detected
    notifyNext = 0          # Time for next notification
    notifySent = False      # Whether we sent a notification or not

    def __init__(self, simulate=False):
        pass

    @classmethod
    def simulateMode(cls):
        logging.info("Override in simulate mode -- notifications sent every 10 seconds")
        cls.initialNotifySec = 10
        cls.repeatNotifySec = 10

    @classmethod
    def notifyMaybe(cls):
        """Send override notification if it's time."""
        now = time.time()
        if (cls.notifyNext > 0 and now >= cls.notifyNext):
            pager.Pager.send("WARNING: manual override has been enabled for {}; poop valve operation suspended"
                       .format(datetime.timedelta(seconds=int(now - cls.startTime))))
            cls.notifySent = True
            cls.notifyNext = now + cls.repeatNotifySec

    @classmethod
    def check(cls):
        """Check if manual override is set and, after a grace period, notify at regular intervals."""
        now = time.time()
        if (device.Gpio.is_override.isOn()):
            if (cls.startTime > 0):
                cls.notifyMaybe()
            else:
                logging.warning("Manual override is enabled; will notify in {} seconds if still set".format(cls.initialNotifySec))
                cls.startTime = now
                cls.notifyNext = now + cls.initialNotifySec
            return True

        else:   # Gpio.is_override is off
            if (cls.startTime > 0):
                msg = "manual override disabled after {}".format(datetime.timedelta(seconds=int(now - cls.startTime)))
                logging.warning(msg)
                cls.startTime = 0
                if (cls.notifySent):
                    pager.Pager.send(msg)
                    cls.notifyNext = 0
                    cls.notifySent = False
            return False


