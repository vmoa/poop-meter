#
# page.py -- Send SMS pages
#

import configparser
import logging
import time
import twilio.rest

import device

class Pager:

    # Class variables so they can be accessed without an instance, eg: pager.Pager.send()
    config = configparser.ConfigParser()    # Configuration from file
    recip = None                            # Default recipient
    #client                                 # Twilio client; created in __init__()
    simulate = False                        # If set, simulate sending pages but don't actually send

    # Based on bench testing an inch equates to about 8 ticks on the ADC
    # https://docs.google.com/document/d/1y9-7Vs1QebsVzuF8hXrv6W9YnSJAdl80ODEjWZSmrM8/
    # This should be tuned after some real-world testing
    hour = 3600
    poopmap = [
        {
            'severity': 'empty',
            'threshold': -1,            # Tune `nominal` so this only happens after a pump-out
            'frequency': 7 * 24 * hour,
        }, {
            'severity': 'nominal',
            'threshold': 320,           # 60 inches below 'PANIC' (5 feet) -- to be tuned
            'frequency': 7 * 24 * hour,
        }, {
            'severity': 'High',
            'threshold': 700,           # Should match the Classroom Red Light turning on
            'frequency': 24 * hour,     # Wholly arbitrary before real-world tuning
        }, {
            'severity': 'URGENT',
            'threshold': 800,           # 20 inches below sensor
            'frequency': 4 * hour,      # Or maybe this should be the Red Light?
        }, {
            'severity': 'PANIC',        # This will trigger shutting off the water main valve
            'threshold': 880,           # 10 inches below sensor
            'frequency': 1 * hour,
        }, {
            'severity': 'placeholder9', # place holder to make the math easier
            'threshold': 99999,         # should never be returned
            'frequency': 1 * hour,      # but just in case...
        }
    ]

    def __init__(self, simulate=False):
        self.simulate_mode(simulate)
        self.config.read('twilio.conf')
        self.config.read('/usr/local/etc/twilio.conf')
        if ('twilio' not in self.config):
            logging.error("Pager: no Twilio config found; pages will not be sent")
            return
        # Twilio requires credentials to create a class instance so we cannot create it until now
        __class__.client = twilio.rest.Client(
            self.config['twilio']['account_sid'],
            self.config['twilio']['auth_token'])

    @classmethod
    def simulate_mode(cls, simulate):
        """Enable or disable simulate mode and sending of actual pages."""
        cls.simulate = simulate
        for entry in cls.poopmap:
            entry["frequency"] = 10  # Override all alerts to 10 seconds
        if (simulate):
            logging.info("Pager in simulate mode -- pages will NOT be sent")

    @classmethod
    def set_default_recip(cls, recip=recip):
        """Set recipient for when none is specified in send()"""
        if (recip in cls.config['recipient']):
            cls.recip = recip
        else:
            logging.error("Pager.set_default_recip(): recipient {} not known; pages will not be sent".format(recip))

    @classmethod
    def send(cls, msg, recip=None):
        """Send sms <msg> to <recip>"""
        if (recip not in locals()):
            recip = cls.recip  # Use default
        if ('twilio' in cls.config):
            if (recip in cls.config['recipient']):
                if (cls.simulate):
                    prefix = 'Simulated page'
                else:
                    prefix = 'Page'
                    sent = cls.client.messages.create(
                        to    = cls.config['recipient'][recip],
                        from_ = cls.config['twilio']['from_phone'],
                        body  = msg)
                logging.info('{} sent to {} ({})'.format(prefix, recip, msg))
            else:
                logging.error('Pager.send(): recipient {} unknown'.format(recip))
        else:
            logging.error('Pager.send(): cannot send to {}: no Twilio config found'.format(recip))

    #
    # Generic-ish Twilio stuff above; poopy stuff below
    #

    # Message categories
    lastSend = {}

    @classmethod
    def notify_maybe(cls, cat, msg, recip=None):
        """Send a categorical message <cat> with protection to prevent rapid duplication."""
        now = int(time.time())
        if (cat in lastSend):
            elapsed = now - lastSend[cat]
            if (elapsed > 10 * min):
                cls.send(msg, recip)
                lastSend[cat] = now
        else:
            cls.send(msg, recip)
            lastSend[cat] = now

    @classmethod
    def get_panic(cls):
        for a in cls.poopmap:
            if (a["severity"] == 'PANIC'):
                return(a["threshold"])
        logging.error("pager.get_panic(): cannot find panic!")

    @classmethod
    def get_nominal(cls):
        for a in cls.poopmap:
            if (a["severity"] == 'nominal'):
                return(a["threshold"])
        logging.error("pager.get_nominal(): cannot find nominal!")

    poopmessage = "Poop level {}: {:1.0f}% ({:d}, {:3.2}v)"  # Poop level PANIC|URGENT|High|nominal: 93% (128, 4.12v)
    last_poopalert = poopmap[0]
    last_pooptime = 0

    @classmethod
    def poop_notify(cls, value, voltage, percent, recip=None):
        """Format and send poop message, throttled according to `frequency` defined in poopmap."""
        now = int(time.time())

        # Find approprate stanza
        for p in range(len(cls.poopmap)):
            if (value < cls.poopmap[p]["threshold"]):
                alert = cls.poopmap[p-1]
                break

        elapsed = now - cls.last_pooptime

        if ((p != cls.last_poopalert) or (elapsed > alert["frequency"])):
            cls.send(cls.poopmessage.format(alert["severity"], percent, value, voltage))
            cls.last_poopalert = p
            cls.last_pooptime = now



