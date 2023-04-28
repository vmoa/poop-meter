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
    Enter by holding momentary button for XX seconds
    Exit by pressing momentary for XX seconds
    Restart/reboot restores normal operation
    PANIC level will restore normal operation
## Hard Override Mode
    Enter by toggling Emergency Override inside box; detect by Override low for > YY seconds
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

    interval = {
        'soft': 30,
        'hard': 120,
    }

    initialNotifySec = 300      # Seconds before sending first page about manual override (5 minutes grace)
    repeatNotifySec = 86400     # Seconds between subsequent pages about manual override (daily)

    startTime = 0           # Time override detected
    notifyNext = 0          # Time for next notification
    notifySent = False      # Whether we sent a notification or not

    def __init__(self):
        pass

    @classmethod
    def simulateMode(cls, simulate):
        if (simulate):
            logging.info("Override in simulate mode -- notifications sent every 10 seconds")
            cls.initialNotifySec = 10
            cls.repeatNotifySec = 10

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
            if (!cls.overrideStartTime):
                cls.overrideStartTime = now
            elapsed = cls.overrideStartTime - now

            match cls.mode:
                case "none":
                    if (elapsed < cls.modeTime["soft"]):
                        pass
                    elif (elapsed < cls.modeTime["hard"]):
                        cls.mode = 'soft'
                        logging.debug("override.detectMode() ==> soft after {} seconds".format(elapsed))
                    else:
                        cls.mode = 'HARD'
                        logging.debug("override.detectMode() ==> HARD* after {} seconds".format(elapsed))

                case "soft":
                    if (elapsed < cls.modeTime["hard"]):
                        pass
                    else:
                        cls.mode = 'HARD'
                        logging.debug("override.detectMode() ==> HARD after {} seconds".format(elapsed))

                case "SOFT":
                    pass

                case "HARD":
                    pass

        else  # device.Gpio.is_override.isOff()
            if (cls.overrideStartTime):
                elapsed = cls.overrideStartTime - time.time()
                if (cls.mode = 'soft'):
                    cls.mode = 'SOFT'
                    logging.debug("override.detectMode() ==> SOFT after {} seconds".format(elapsed))
                elif (cls.mode = 'HARD' or cls.mode = 'SOFT'):
                    cls.mode = 'none'
                    logging.debug("override.detectMode() ==> none after {} seconds".format(elapsed))
                cls.overrideStartTime = None


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


