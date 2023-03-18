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

interval = {
    'sample': 1,
    'heart': 2,
    'status': 6,
}

overrideNotifySecs1 = 10     # Seconds before sending first page about manual override (5 minutes grace)
overrideNotifySecs2 = 300    # Seconds between subsequent pages about manual override (daily)

# Valve control thresholds
threshold = {
    "panic_value": pager.Pager.get_panic(),
    "empty_value": pager.Pager.get_nominal(),
}

class Gpio:

    def __init__(self):
        """Connect all our devices. Set `simulator` to increase timings so a human can respond."""
        Gpio.is_opened = self.Sensor(pin=22, name='opened')
        Gpio.is_closed = self.Sensor(pin=23, name='closed')
        Gpio.is_override = self.Sensor(pin=24, name='override')

        Gpio.do_enable = self.Control(pin=25, name='enable')
        Gpio.set_direction = self.Control(pin=26, name='open_close')
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

def printStatus():
    """Return a string with the formatted status."""
    status = ''
    ### print(util.timestamp(), threading.get_ident(), end=' ')
    poopLevel, poopVolts, poopPercent = Gpio.adc.get_values()
    #poopVolts = Gpio.adc.get_voltage()
    #poopPercent = Gpio.adc.get_percent()
    status += "POOP:{pct:3.1f}%-{val}-{volt:3.2f}v ".format(pct=poopPercent, val=poopLevel, volt=poopVolts)
    grove.Grove.updatePoop(poopPercent, poopLevel, poopVolts)

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
            if ((op == 'close' and Gpio.is_closed.isOn()) or (op == 'open' and Gpio.is_opened.isOn())):
                return   # Valve is already in the state we want
            msg = "{}ing water main valve".format(op[0:4])
            logging.info("Valve.operate(): {}".format(msg))
            pager.Pager.send("NOTICE: {}".format(msg))
            if (op == 'close'):
                Gpio.set_direction.setClose()
            else:
                Gpio.set_direction.setOpen()
            Gpio.do_enable.turnOn()
            cls.valveStartTime = now
            cls.operation = op

        else:
            # Operation in progress
            elapsed = now - cls.valveStartTime
            if ((op == 'close' and Gpio.is_closed.isOn()) or (op == 'open' and Gpio.is_opened.isOn())):
                logging.info("Valve.operate(): valve {}ed after {} seconds".format(op[0:4], elapsed))
                Gpio.do_enable.turnOff()
                cls.valveStartTime = 0
                cls.operation = None
            else:
                if (elapsed > cls.valveTimeExceeded):
                    msg = "valve failed to {} after {} seconds; giving up".format(op, elapsed)
                    logging.error("Valve.operate(): {}".format(msg))
                    pager.Pager.send("WARNING: {}".format(msg))
                    Gpio.do_enable.turnOff()
                    cls.valveStartTime = 0
                    cls.operation = None

    @classmethod
    def maybeOperate(cls, value):
        """Open or close the valve if threshold conditions are met."""
        if (cls.operation):
            # Operation in progress
            cls.operate(cls.operation)  # Operation in progress
        if (Gpio.is_closed.isOff()):
            if (value >= threshold["panic_value"]):
                cls.operate('close')
        elif (Gpio.is_opened.isOff()):
            if (value <= threshold["empty_value"]):
                cls.operate('open')

def checkPoop():
    """Read the ADC and Do The Right Thing(tm) as regards the poop level."""
    value, voltage, percent = Gpio.adc.get_values()
    pager.Pager.poop_notify(value, voltage, percent)
    Valve.maybeOperate(value)


perSecond_lock = threading.Lock()  # Ensure we run perSecond only one at a time

def perSecond():
    """Callback that runs every second to perform housekeeping duties"""
    with perSecond_lock:
        threading.Timer(1.0, perSecond).start()  # Predispatch next self

        now = int(time.time())
        if (now % interval['sample'] == 0):
            Gpio.adc.do_sample()
        if (now % interval['heart'] == 0):
            beatHeart(Gpio.heart.device)
        if (now % interval['status'] == 0):
            logging.info(printStatus())

        checkPoop()
        checkOverride()

