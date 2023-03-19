#
# Class Poop with overall Poop Meter logic
#

import datetime
import logging
import threading
import time

import adc
import device
import grove
import pager
import valve


class Poop:

    # Intervals at which perSecond does work (modulo timestamp)
    interval = {
        'sample': 1,
        'heart': 2,
        'status': 6,
    }

    # This ensures we run perSecond() only one at a time
    # Introduces the possibility that we miss seconds here and there if perSecond() blocks or takes longer than a second
    perSecond_lock = threading.Lock()

    def __init__(self):
        pass

    @classmethod
    def check(cls):
        """Read the ADC and Do The Right Thing(tm) as regards the poop level."""
        value, voltage, percent = device.Gpio.adc.get_values()
        if (device.Gpio.is_opened.isOn()):
            valve_state = 'open'
        elif (device.Gpio.is_closed.isOn()):
            valve_state = 'closed'
        else:
            valve_state = 'midway'
        pager.Pager.poop_notify(value, voltage, percent, valve_state)
        valve.Valve.maybeOperate(value)

    @classmethod
    def printStatus(cls):
        """Return a string with the formatted status."""
        poopLevel, poopVolts, poopPercent = device.Gpio.adc.get_values()
        device.Gpio.lcd.printLine("{:3d}% {:4.2f}v {:4d}".format(int(poopPercent), poopVolts, int(poopLevel)), line=1)   # 100% 3.45v 1024

        status = "POOP:{pct:3.1f}%-{val}-{volt:3.2f}v ".format(pct=poopPercent, val=poopLevel, volt=poopVolts)
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

            cls.check()

