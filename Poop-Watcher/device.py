#
# Class Sensor to extend Digital{Input,Output}Device for Poop Watcher
#

import datetime
from gpiozero import DigitalInputDevice, DigitalOutputDevice
import logging
import threading
import time

import adc

statusInterval = 6     # Seconds between status updates without input changes

class Gpio:

    def __init__(self):
        """Connect all our devices. Set `simulator` to increase timings so a human can respond."""
        Gpio.is_opened = self.Sensor(pin=22, name='opened')
        Gpio.is_closed = self.Sensor(pin=23, name='closed')
        Gpio.is_override = self.Sensor(pin=24, name='override')

        Gpio.do_enable = self.Control(pin=25, name='enable')
        Gpio.do_open_close = self.Control(pin=26, name='open_close')
        Gpio.heart = self.Control(pin=27, name='heart')    # heartLed

        Gpio.adc = adc.Adc()


    class Sensor:
        sensors = []    # array of all sensor instances (in order of creation for status printout)
        by_name = {}    # dict of all sensors by name
        by_pin = {}     # dict of all sensors by pin
        names = []      # array of sensor names (in order of creation for status printout)

        def __init__(self, pin, name, pull_up=False, active_state=True, bounce_time=0.1, when_activated=0, when_deactivated=0):
            # TODO throw exception if pin not set
            self.name = name
            self.isSensor = True
            self.device = DigitalInputDevice(pin=pin, pull_up=pull_up, bounce_time=bounce_time)
            self.device.when_activated = when_activated if (when_activated) else self.activated
            self.device.when_deactivated = when_deactivated if (when_deactivated) else self.deactivated
            logging.info('Initialize sensor {} (pull_up={})'.format(name, self.device.pull_up))
            Gpio.Sensor.sensors.append(self)
            Gpio.Sensor.by_name[name] = self
            Gpio.Sensor.by_pin[pin] = self
            Gpio.Sensor.names.append(name)

        def is_active(self):
            return(self.device.is_active)

        def isOn(self):
            return(self.device.value == 1)

        def isOff(self):
            return(self.device.value == 0)

        # Default callbacks; override at instance creation or by setting <var>.device.when_[de]activated
        def activated(self):
            logging.info('UP ' + self.name + ' ' + printStatus())

        def deactivated(self):
            logging.info('DN ' + self.name + ' ' + printStatus())


    class Control:
        controls = []   # array of all sensor instances (in order of creation for status printout)
        by_name = {}    # dict of all controls by name
        by_pin = {}     # dict of all controls by pin
        names = []      # array of control names (in order of creation for status printout)

        def __init__(self, pin, name, active_high=True, initial_value=False, toggle_delay=0.5):
            # TODO throw exception if pin not set
            self.name = name
            self.isControl = True
            self.device = DigitalOutputDevice(pin=pin, active_high=active_high, initial_value=initial_value)
            self.toggle_delay = toggle_delay
            Gpio.Control.controls.append(self)
            Gpio.Control.by_name[name] = self
            Gpio.Control.by_pin[pin] = self
            Gpio.Control.names.append(name)

        def turnOn(self):
            self.device.on()
            logging.info('ON ' + printStatus())

        def turnOff(self):
            self.device.off()
            logging.info('OF ' + printStatus())

        def is_active(self):
            return(self.device.value == 1)

        def isOn(self):
            return(self.device.value == 1)

        def isOff(self):
            return(self.device.value == 0)


def printStatus():
    """Return a string with the formatted status."""
    status = ''
    ### print(util.timestamp(), threading.get_ident(), end=' ')
    print(Gpio.adc)
    poopLevel = Gpio.adc.get_value()
    poopVolts = Gpio.adc.get_voltage()
    poopPercent = Gpio.adc.get_percent()
    status += "POOP:{}%-{}-{}v ".format(poopPercent, poopLevel, poopVolts)
    for sensor in Gpio.Sensor.sensors:
        if (sensor.is_active()):
            status += "[{}] ".format(sensor.name.upper())
        else:
            status += "({}) ".format(sensor.name)
    for control in Gpio.Control.controls:
        if (control.is_active()):
            status += "[{}] ".format(control.name.upper())
        else:
            status += "({}) ".format(control.name)
    return(status)

def beatHeart(output=0, step=0):
    if (step == 0):
        output.on()
        threading.Timer(0.1, beatHeart, [output,1]).start()
    elif (step == 1):
        output.off()
        threading.Timer(0.05, beatHeart, [output,2]).start()
    elif (step == 2):
        output.on()
        threading.Timer(0.1, beatHeart, [output,3]).start()
    elif (step == 3):
        output.off()
    else:
        logging.error("WTF? beatHeart() called with step %".format(step))

def checkOverride():
    if (Gpio.is_override.isOn()):
        started = Gpio.is_override.started()
        warned = Gpio.is_override.warned()
        now = datetime.datetime.now().second
        if (now > warned + OVERRIDE_WARN_SECS):
            page("WARNING: manual override has been set for {} minutes; poop valve operation suspended".format((now - started)/60))
            OVERRIDE_WARN_SECS = now


def samplePoop():
    """Read the ADC and Do The Right Thing(tm) with respect to poop level."""
    # Should this live in adc.py?
    pass


sampleInterval = 1  # Rate at which we sample poop level

def perSecond():
    """Callback that runs every second to perform housekeeping duties"""
    if (int(datetime.datetime.now().second) % sampleInterval == 0):
        samplePoop()
    if (int(datetime.datetime.now().second) % 2 == 0):
        beatHeart(Gpio.heart.device)
    if (int(datetime.datetime.now().second) % statusInterval == 0):
        logging.info('-- ' + printStatus())
    checkOverride()
    threading.Timer(1.0, perSecond).start()  # Redispatch self

