#
# page.py -- Send SMS pages
#

import configparser
import logging
import twilio.rest

class Pager:

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('twilio.conf')
        self.config.read('/usr/local/etc/twilio.conf')
        if ('twilio' not in self.config):
            logging.error("Pager: no Twilio config found; pages will not be sent")
            return
        self.client = twilio.rest.Client(
            self.config['twilio']['account_sid'],
            self.config['twilio']['auth_token'])

    def send(self, recip, message):
        """Send sms <message> to <recip>"""
        if ('twilio' in self.config):
            if (recip in self.config['recipient']):
                msg = self.client.messages.create(
                    to    = self.config['recipient'][recip],
                    from_ = self.config['twilio']['from_phone'],
                    body  = message)
                logging.info('Page sent to {} ({})'.format(recip, msg.sid))
            else:
                logging.error('Pager: recipient {} unknown')
        else:
            logging.error('Pager: cannot send to {}: no Twilio config found'.format(recip))
