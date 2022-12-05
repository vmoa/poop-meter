#
# Class Sensor to extend Digital{Input,Output}Device for Poop Watcher
#

import datetime
from gpiozero import DigitalInputDevice, DigitalOutputDevice
import logging
import threading
import time

import adc
import grove
import pager

statusInterval = 6     # Seconds between status updates without input changes
overrideNotifySecs1 = 10     # Seconds before sending first page about manual override (5 minutes grace)
overrideNotifySecs2 = 300    # Seconds between subsequent pages about manual override (daily)

toggle=False           # To swap between abs and volts display

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
            logging.debug('when_activated:{}, when_deactivated{}'.format(self.device.when_activated, self.device.when_deactivated))
            Gpio.Sensor.sensors.append(self)
            Gpio.Sensor.by_name[name] = self
            Gpio.Sensor.by_pin[pin] = self
            Gpio.Sensor.names.append(name)

            # Initialize override timers
            if (name == 'override'):
                if (self.isOn()):
                    logging.warning("Manual override is enabled; will notify in {} if still set".format(datetime.timedelta(seconds=overrideNotifySecs1)))
                    now = time.time()
                    self.activated_ts = now
                    self.notify_ts = now + overrideNotifySecs1
                else:
                    self.activated_ts = -1
                    self.notify_ts = -1

        def is_active(self):
            return(self.device.is_active)

        def isOn(self):
            return(self.device.value == 1)

        def isOff(self):
            return(self.device.value == 0)

        # Default callbacks; override at instance creation or by setting <var>.device.when_[de]activated
        def activated(self):
            logging.info(printStatus() + ' HIGH:' + self.name)
            if (self.name == 'override'):
                logging.warning("Manual override is enabled; will notify in {} if still set".format(datetime.timedelta(seconds=overrideNotifySecs1)))
                now = time.time()
                self.activated_ts = now
                self.notify_ts = now + overrideNotifySecs1

        def deactivated(self):
            logging.info(printStatus() + ' LOW:' + self.name)
            if (self.name == 'override'):
                logging.warning("Manual override cleared")
                checkOverride()
                self.activated_ts = -1
                self.notify_ts = -1


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
            logging.info(printStatus() + ' ON:' + self.name)

        def turnOff(self):
            self.device.off()
            logging.info(printStatus() + ' OFF:' + self.name)

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
    poopLevel = Gpio.adc.get_value()
    poopVolts = Gpio.adc.get_voltage()
    poopPercent = Gpio.adc.get_percent()
    status += "POOP:{}%-{}-{}v ".format(poopPercent, poopLevel, poopVolts)

    try:
        printStatus.toggle
    except AttributeError:
        printStatus.toggle = False
    printStatus.toggle = not(printStatus.toggle)
    print("DEBUG: ", printStatus.toggle)
    grove.Grove.selectLine(1)
    grove.Grove.printLine("{}% ({}a)".format(poopPercent, poopLevel) if (printStatus.toggle == False) else "{}% ({}v)".format(poopPercent, poopVolts))

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
        grove.Grove.setCursor(1,15)
        grove.Grove.printChar('*')
        threading.Timer(0.1, beatHeart, [output,1]).start()
    elif (step == 1):
        output.off()
        threading.Timer(0.05, beatHeart, [output,2]).start()
    elif (step == 2):
        output.on()
        threading.Timer(0.1, beatHeart, [output,3]).start()
    elif (step == 3):
        output.off()
        grove.Grove.setCursor(1,15)
        grove.Grove.printChar(' ')
    else:
        logging.error("WTF? beatHeart() called with step %".format(step))

def checkOverride():
    """Check if manual override is set and notify at regular intervals."""
    if (Gpio.is_override.isOn()):
        now = time.time()
        # print("{} > {}".format(int(now), int(Gpio.is_override.notify_ts)))
        if (Gpio.is_override.notify_ts > 0 and now > Gpio.is_override.notify_ts):
            pager.Pager.send("WARNING: manual override has been enabled for {}; poop valve operation suspended"
                       .format(datetime.timedelta(seconds=int(now-Gpio.is_override.activated_ts))))
            Gpio.is_override.notify_ts = now + overrideNotifySecs2
    else:
        if (Gpio.is_override.notify_ts > 0):
            now = time.time()
            pager.Pager.send("INFO: manual override disabled after {}"
                       .format(datetime.timedelta(seconds=int(now-Gpio.is_override.activated_ts))))
            Gpio.is_override.notify_ts = -1
            Gpio.is_override.activated_ts = -1


def samplePoop():
    """Read the ADC and Do The Right Thing(tm) with respect to poop level."""
    # Should this live in adc.py?
    pass


sampleInterval = 1  # Rate at which we sample poop level

def perSecond():
    """Callback that runs every second to perform housekeeping duties"""
    now = int(time.time())
    if (int(datetime.datetime.now().second) % sampleInterval == 0):
        samplePoop()
    if (int(datetime.datetime.now().second) % 2 == 0):
        beatHeart(Gpio.heart.device)
    if (now % statusInterval == 0):
        logging.info(printStatus())
    checkOverride()
    threading.Timer(1.0, perSecond).start()  # Redispatch self

