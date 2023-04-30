#
# Class Poop with overall Poop Meter logic
#

import datetime
import logging
import os
import threading
import time

import adc
import device
import grove
import override
import pager
import valve


class Poop:

    # Intervals at which perSecond does work (modulo timestamp)
    interval = {
        'sample': 1,
        'heart': 2,
        'status': 60,
        'syscheck': 600,
    }

    # A map of poop levels and what to do for each.
    # Based on bench testing an inch equates to about 8 ticks on the ADC
    # https://docs.google.com/document/d/1y9-7Vs1QebsVzuF8hXrv6W9YnSJAdl80ODEjWZSmrM8/
    # This should be tuned after some real-world testing
    hour = 3600
    poopmap = [
        {
            'severity' : 'empty',
            'color'    : 'green',
            'threshold': -1,            # Tune `nominal` so this only happens after a pump-out
            'frequency': 7 * 24 * hour,
        }, {
            'severity' : 'nominal',
            'color'    : 'green',
            'threshold': 320,           # 60 inches below 'PANIC' (5 feet) -- to be tuned
            'frequency': 7 * 24 * hour,
        }, {
            'severity' : 'High',
            'color'    : 'orange',
            'threshold': 700,           # Should match the Classroom Red Light turning on
            'frequency': 24 * hour,     # Wholly arbitrary before real-world tuning
        }, {
            'severity' : 'URGENT',
            'color'    : 'red',
            'threshold': 800,           # 20 inches below sensor
            'frequency': 4 * hour,      # Or maybe this should be the Red Light?
        }, {
            'severity' : 'PANIC',        # This will trigger shutting off the water main valve
            'color'    : 'red',
            'threshold': 880,           # 10 inches below sensor
            'frequency': 1 * hour,
        }, {
            'severity' : 'placeholder9', # place holder to make the math easier
            'color'    : 'blue',
            'threshold': 99999,         # should never be returned
            'frequency': 1 * hour,      # but just in case...
        }
    ]

    # Build a dictionary indexed by threshold
    # This is a public dictionary accessed directly (eg in valve.py)
    threshold = dict()
    for poop in poopmap:
        threshold[poop["severity"]] = poop["threshold"]

    # Build a list of poopmap entries indexed by poop level
    # This trades off memory (1024 element list) for perfomance, since we look this up every second
    # And requires that poopmap entries are sorted in increasing threshold order
    mapidx = 0
    poopmapArray = []
    for thresh in range(0,1024):
        if (thresh >= poopmap[mapidx+1]['threshold']):
            mapidx += 1
        poopmapArray.append(poopmap[mapidx])

    # Poop level PANIC|URGENT|High|nominal: 93% (128, 4.12v) Valve:open|closed Override:none|soft|SOFT|HARD
    poopmessage = "Poop level {}: {:1.0f}% ({:d}, {:3.2}v) Valve:{} Override:{}"
    last_poopalert = poopmap[0]
    last_pooptime = 0

    # This ensures we run perSecond() only one at a time
    # Introduces the possibility that we miss seconds here and there if perSecond() blocks or takes longer than a second
    perSecond_lock = threading.Lock()

    def __init__(self):
        pass

    @classmethod
    def simulateMode(cls, simulate):
        """Override all alert frequencies and set to 10 seconds."""
        if (simulate):
            logging.info("Poop in simulate mode -- notifications sent every 10 seconds")
            for entry in cls.poopmap:
                entry["frequency"] = 10
            cls.interval["status"] = 1  # and update status every sample

    @classmethod
    def poop_notify(cls, value, voltage, percent, valve, recip=None):
        """Format and send poop message, throttled according to `frequency` defined in poopmap."""
        now = int(time.time())
        elapsed = now - cls.last_pooptime

        # Is it time to alert?
        if ((p != cls.last_poopalert) or (elapsed > alert["frequency"])):

            # Find approprate stanza
            for p in range(len(cls.poopmap)):
                if (value < cls.poopmap[p]["threshold"]):
                    alert = cls.poopmap[p-1]
                    break

            # Poop level PANIC|URGENT|High|nominal: 93% (128, 4.12v) Valve:open|closed Override:none|soft|SOFT|HARD
            pager.Pager.send("Poop level {}: {:1.0f}% ({:d}, {:3.2}v) Valve:{} Override:{}"
                .format(cls.poopmessage.format(alert["severity"], percent, value, voltage, valve, override.Override.getMode())))
            cls.last_poopalert = p
            cls.last_pooptime = now

    @classmethod
    def check(cls):
        """Read the poop level from the ADC and Do The Right Thing(tm)."""
        value, voltage, percent = device.Gpio.adc.get_values()
        if (device.Gpio.is_opened.isOn()):
            valve_state = 'open'
        elif (device.Gpio.is_closed.isOn()):
            valve_state = 'closed'
        else:
            valve_state = 'midway'
        cls.poop_notify(value, voltage, percent, valve_state)
        valve.Valve.maybeOperate(value)

    colorIterator = 0;
    overrideColors = [ 'indigo', 'red' ]

    @classmethod
    def printStatus(cls):
        """Update display and return a string with the formatted status."""
        poopLevel, poopVolts, poopPercent = device.Gpio.adc.get_values()

        poopEntry = cls.poopmapArray[int(poopLevel)]
        poopColor = poopEntry["color"]

        overrideMode = override.Override.getMode()
        if (overrideMode == 'none'):
            pass
        elif (poopColor == 'red'):
            poopColor = cls.overrideColors[cls.colorIterator]
            cls.colorIterator = not cls.colorIterator
        else:
            poopColor = cls.overrideColors[0]

        device.Gpio.lcd.setColor(poopColor)
        device.Gpio.lcd.printLine("Poop level {:d}%".format(int(poopPercent)), line=0)              # Poop level 100%
        device.Gpio.lcd.printLine("  {:4.2f}v {:4d}".format(poopVolts, int(poopLevel)), line=1)     #   3.45v 1024   *

        # 2023-04-28 07:32:00 [INFO] POOP:8.6%-88-0.28v Mode:OVR(HARD) -- [OPENED] (closed) (override) (enable) (open_close) [HEART]
        status = "POOP:{pct:3.1f}%-{val}-{volt:3.2f}v ".format(pct=poopPercent, val=poopLevel, volt=poopVolts)
        status += " Mode:{}({})".format('OVR' if (override.Override.isOverride()) else 'run', overrideMode)
        status += " -- "
        for sensor in device.Gpio.Sensor.sensors:
            if (sensor.is_active()):
                status += "[{}] ".format(sensor.name.upper())
            else:
                status += "({}) ".format(sensor.name)
        for control in device.Gpio.Control.controls:
            if (control.is_active()):
                status += "[{}] ".format(control.name.upper())
            else:
                status += "({}) ".format(control.name)
        return(status)

    @classmethod
    def syscheck(cls):
        """Check system stuff infrequently."""
        if (os.path.exists("nopage")):
            logging.warning("Sentinel file 'nopage' file found -- pages are NOT being sent!")

    @classmethod
    def perSecond(cls):
        """Callback that runs every second to perform housekeeping duties"""
        with cls.perSecond_lock:
            threading.Timer(1.0, cls.perSecond).start()  # Predispatch next self

            now = int(time.time())
            if (now % cls.interval['sample'] == 0):
                device.Gpio.adc.do_sample()
            if (now % cls.interval['heart'] == 0):
                device.Gpio.beatHeart(device.Gpio.heart.device)
            if (now % cls.interval['status'] == 0):
                logging.info(Poop.printStatus())
            if (now % cls.interval['syscheck'] == 0):
                cls.syscheck()

            cls.check()

