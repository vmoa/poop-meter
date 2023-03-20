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
    reboot = True                           # Cleared after we send the first page

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
                if (cls.reboot):
                    msg = 'Poop meter rebooted; ' + msg
                    cls.reboot = False
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
