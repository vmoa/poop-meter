#
# Class Gpio with subclasses Sensor and Control (extends Digital{Input,Output}Device) for Poop Watcher
#

import datetime
from gpiozero import DigitalInputDevice, DigitalOutputDevice
import logging
import threading
import time

import adc
import grove
import override
import pager
import poop

class Gpio:

    def __init__(self, lcd):
        """Connect all our devices."""
        Gpio.is_opened = self.Sensor(pin=22, name='opened')
        Gpio.is_closed = self.Sensor(pin=23, name='closed')
        Gpio.is_override = self.Sensor(pin=24, name='override')

        Gpio.do_enable = self.Control(pin=25, name='enable')
        Gpio.set_direction = self.Control(pin=26, name='open_close')
        Gpio.heart = self.Control(pin=27, name='heart')    # heartLed

        Gpio.adc = adc.Adc()
        Gpio.lcd = lcd;


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
            logging.debug('when_activated:{}, when_deactivated{}'.format(self.device.when_activated, self.device.when_deactivated))
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
            logging.info(poop.Poop.printStatus() + ' HIGH:' + self.name)
            if (self.name == 'override'):
                override.Override.check()

        def deactivated(self):
            logging.info(poop.Poop.printStatus() + ' LOW:' + self.name)
            if (self.name == 'override'):
                override.Override.check()


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
            logging.info(poop.Poop.printStatus() + ' ON:' + self.name)

        def turnOff(self):
            self.device.off()
            logging.info(poop.Poop.printStatus() + ' OFF:' + self.name)

        def setOpen(self):
            """Alias for turnOn() for set_direction control."""
            self.turnOn()

        def setClose(self):
            """Alias for turnOff() for set_direction control."""
            self.turnOff()

        def is_active(self):
            return(self.device.value == 1)

        def isOn(self):
            return(self.device.value == 1)

        def isOff(self):
            return(self.device.value == 0)

    @classmethod
    def beatHeart(cls, output=0, step=0):
        if (step == 0):
            output.on()
            grove.Grove.setCursor(1,15)
            grove.Grove.printChar('*')
            threading.Timer(0.1, cls.beatHeart, [output,1]).start()
        elif (step == 1):
            output.off()
            threading.Timer(0.05, cls.beatHeart, [output,2]).start()
        elif (step == 2):
            output.on()
            threading.Timer(0.1, cls.beatHeart, [output,3]).start()
        elif (step == 3):
            output.off()
            grove.Grove.setCursor(1,15)
            grove.Grove.printChar(' ')
        else:
            logging.error("WTF? beatHeart() called with step %".format(step))

