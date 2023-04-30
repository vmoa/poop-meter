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
import poop


"""
# Thoughts on Hard / Soft Override Mode

## Soft Override Mode
    Enter by holding momentary button for XX seconds and then releasing
    Exit by pressing and releasing momentary
    Restart/reboot restores normal operation
    PANIC level will restore normal operation

## Hard Override Mode
    Enter by toggling Emergency Override inside box; detect by Override low
    Can only be exitied by user restoring Emergency Override switch
    Restart/reboot RETAINS Hard Override because it's a hardware switch

## State transitions
    Mode    Switch  Elapsed         Action
    ====    ======  =======         ======
    none    no      -               -
    none    yes     <soft           -
    none    yes     <hard           => soft
    none    yes     >hard           => HARD
    soft    no      -               => SOFT
    soft    yes     <hard           -
    soft    yes     >hard           => HARD
    SOFT    no      -               -
    SOFT    yes     <soft           -
    SOFT    yes     >soft           => none
    HARD    no      -               => none
    HARD    yes     -               -

"""


class Override:

    mode = 'none'           # The state of manual override (none, soft, SOFT, HARD)
    startTime = None        # The time the button or switch was pressed
    modeStartTime = None    # The time we entered the particular mode (for alerting purposes)
    notifyNext = None       # Time for next notification

    interval = {            # The length of time the override switch is 'on' to detect mode
        'soft': 2,          # Triggers mode=`soft`, which will become `SOFT` if released before interval[hard]
        'hard': 120,        # This is long enough that we assume the internal switch has been thrown
        'notify1': 300,     # Seconds before sending first page about manual override (5 minutes grace)
        'notifyN': 86400,   # Seconds between subsequent pages about manual override (daily)
    }

    debug = False


    def __init__(self):
        pass

    @classmethod
    def simulateMode(cls, simulate):
        if (simulate):
            logging.info("Override in simulate mode -- notifications sent every 10 seconds")
            cls.interval['notify1'] = 10
            cls.interval['notifyN'] = 10

    @classmethod
    def setDebug(cls):
        cls.debug = True
        cls.debug and logging.debug("Enabling override debugging")

    @classmethod
    def isOverride(cls):
        if (cls.mode == 'none'):
            return(False)
        else:
            return(True)

    @classmethod
    def getMode(cls):
        return(cls.mode)

    @classmethod
    def cancelMode(cls, message):
        """Forcibly cancel override mode. Will only work for soft modes."""
        if (cls.mode in {'HARD', 'none'}):
            logging.warning("Attempt to cancel {} override ignored".format(cls.mode))
        else:
            msg = "Forcibly cancelling {} override: {}".format(cls.mode, message)
            logging.warning(msg)
            pager.Pager.send(msg)
            cls.mode = 'none'
            cls.startTime = None
            cls.modeStartTime = None
            cls.notifyNext = None

    @classmethod
    def logIt(cls, mode, elapsed):
        cls.debug and logging.debug("Override mode ==> {} after {} seconds".format(mode, int(elapsed)))

        if (mode == 'none'):
            msg = "Manual override disabled after {}".format(datetime.timedelta(seconds=int(time.time() - cls.modeStartTime)))
            logging.warning(msg)
            pager.Pager.send(msg)
        elif (mode == 'soft'):
            pass
        else:
            msg = "Manual override enabled ({}); will notify in {} seconds if still set".format(mode, cls.interval['notify1'])
            logging.warning(msg)
            cls.notifyNext = time.time() + cls.interval['notify1']

        logging.info(poop.Poop.printStatus())

    @classmethod
    def check(cls):
        """Determine override `mode` and notify when appropriate."""
        now = time.time()

        if (device.Gpio.is_override.isOn()):
            if (cls.startTime == None):
                cls.startTime = now
            if (cls.modeStartTime == None):
                cls.modeStartTime = now
            elapsed = now - cls.startTime

            False and cls.debug and logging.debug("check(): mode:{} elapsed:{} startTime:{}".
                format(cls.mode, int(elapsed), int(cls.startTime)))

            if (cls.mode == 'none'):
                if (elapsed < cls.interval["soft"]):
                    pass
                elif (elapsed < cls.interval["hard"]):
                    cls.mode = 'soft'
                    cls.logIt(cls.mode, elapsed)
                else:
                    cls.mode = 'HARD'
                    cls.logIt('HARD*', elapsed)

            elif (cls.mode == 'soft'):
                if (elapsed < cls.interval["hard"]):
                    pass
                else:
                    cls.mode = 'HARD'
                    cls.logIt(cls.mode, elapsed)

            elif (cls.mode == 'SOFT'):
                pass

            elif (cls.mode == 'HARD'):
                pass

        else:  # device.Gpio.is_override.isOff()
            if (cls.startTime):
                elapsed = now - cls.modeStartTime
                False and cls.debug and logging.debug("check(): mode:{} elapsed:{} startTime:{}".
                    format(cls.mode, int(elapsed), int(cls.startTime)))
                if (cls.mode == 'soft'):
                    cls.mode = 'SOFT'
                    cls.logIt(cls.mode, elapsed)
                elif (cls.mode in {'HARD', 'SOFT'}):
                    cls.mode = 'none'
                    cls.logIt(cls.mode, elapsed)
                    cls.notifyNext = None
                    cls.modeStartTime = None
                cls.startTime = None

        # Send override notification if it's time
        if (cls.notifyNext and now >= cls.notifyNext):
            suspendNotice = ""
            if (cls.mode == 'HARD'):
                suspendNotice = "; poop valve operation suspended"
            pager.Pager.send("WARNING: manual override ({}) has been enabled for {}{}"
                       .format(cls.mode, datetime.timedelta(seconds=int(now - cls.modeStartTime)), suspendNotice))
            cls.notifyNext = now + cls.interval['notifyN']

