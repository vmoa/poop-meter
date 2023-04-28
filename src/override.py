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


"""
# Thoughts on Hard / Soft Override Mode

## Soft Override Mode
    Enter by holding momentary button for XX seconds and then releasing
    Exit by pressing momentary for XX seconds then releasing
    Restart/reboot restores normal operation
    PANIC level will restore normal operation
## Hard Override Mode
    Enter by toggling Emergency Override inside box; detect by Override low
    Can only be exitied by user restoring Emergency Override switch
    Restart/reboot RETAINS Hard Override because it's a hardware switch

Mode    Switch  Elapsed         Action
none    no      d/c             -
none    yes     <soft           -
none    yes     <hard           => soft
none    yes     >hard           => HARD
soft    no      d/c             => SOFT
soft    yes     <hard           -
soft    yes     >hard           => HARD
SOFT    no      -               -
SOFT    yes     <soft           -
SOFT    yes     >soft           => none
HARD    no      d/c             => none
HARD    yes     d/c             -

"""


class Override:

    mode = 'none'           # The state of manual override (none, soft, SOFT, HARD)
    manualOverrideStartTime = None # The time the button or switch was pressed

    interval = {            # The length of time the override switch is 'on' to detect mode
        'soft': 10,         # Triggers mode=`soft`, which will become `SOFT` if released before interval[hard]
        'hard': 120,        # This is long enough that we assume the internal switch has been thrown
    }                       # Note that interval[soft] is also used to cancel SOFT override

    initialNotifySec = 300      # Seconds before sending first page about manual override (5 minutes grace)
    repeatNotifySec = 86400     # Seconds between subsequent pages about manual override (daily)

    startTime = 0           # Time override detected
    notifyNext = 0          # Time for next notification
    notifySent = False      # Whether we sent a notification or not

    debug = False


    def __init__(self):
        pass

    @classmethod
    def simulateMode(cls, simulate):
        if (simulate):
            logging.info("Override in simulate mode -- notifications sent every 10 seconds")
            cls.initialNotifySec = 10
            cls.repeatNotifySec = 10

    @classmethod
    def setDebug(cls):
        logging.debug("DEBUG: Enabling override debugging")
        cls.debug = True

    @classmethod
    def detectMode(cls):
        """Figure out which overrideMode we're in."""

        # Mode    Switch  Elapsed         Action
        # none    no      -               -
        # none    yes     <soft           -
        # none    yes     <hard           => soft
        # none    yes     >hard           => HARD
        # soft    no      -               => SOFT
        # soft    yes     <hard           -
        # soft    yes     >hard           => HARD
        # SOFT    no      -               -
        # SOFT    yes     <soft           -
        # SOFT    yes     >soft           => none
        # HARD    no      -               => none
        # HARD    yes     -               -

        if (device.Gpio.is_override.isOn()):
            now = time.time()
            if (cls.manualOverrideStartTime == None):
                cls.manualOverrideStartTime = now
            elapsed = cls.manualOverrideStartTime - now

            # Boo: match/case comes with Python 3.10 and we're stuck with 3.5
            if (cls.mode == 'none'):
                if (elapsed < cls.modeTime["soft"]):
                    pass
                elif (elapsed < cls.modeTime["hard"]):
                    cls.mode = 'soft'
                    cls.debug and logging.debug("override.detectMode() ==> soft after {} seconds".format(elapsed))
                else:
                    cls.mode = 'HARD'
                    cls.debug and logging.debug("override.detectMode() ==> HARD* after {} seconds".format(elapsed))

            elif (cls.mode == 'soft'):
                if (elapsed < cls.modeTime["hard"]):
                    pass
                else:
                    cls.mode = 'HARD'
                    cls.debug and logging.debug("override.detectMode() ==> HARD after {} seconds".format(elapsed))

            elif (cls.mode == 'SOFT'):
                pass

            elif (cls.mode == 'HARD'):
                pass

        else:  # device.Gpio.is_override.isOff()
            if (cls.overrideStartTime):
                elapsed = cls.manualOverrideStartTime - time.time()
                if (cls.mode == 'soft'):
                    cls.mode = 'SOFT'
                    cls.debug and logging.debug("override.detectMode() ==> SOFT after {} seconds".format(elapsed))
                elif (cls.mode == 'HARD' or cls.mode == 'SOFT'):
                    cls.mode = 'none'
                    cls.debug and logging.debug("override.detectMode() ==> none after {} seconds".format(elapsed))
                cls.manualOverrideStartTime = None


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
                cls.detectMode()
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


