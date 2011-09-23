#!/usr/bin/env python

# YELLING
# http://github.com/mastbaum/yelling
#
# A tiny module for logging and notifications
#
# A. Mastbaum (amastbaum@gmail.com)
#

import re
import types
import getpass
import socket
import smtplib
import datetime
import urllib
import settings

# Log to file
def log(filename, message, service_name=None, hoststamp=True, timestamp=True, console=True):
    '''writes a message to a log file. optionally, write a time and hostname
    stamp like syslog. if you want to customize that, just put it in message.
    '''
    m = ''
    if timestamp:
        t = datetime.datetime.strftime(datetime.datetime.now(),'%b %d %H:%M:%S')
        m = m + t + ' '
    if hoststamp:
        m = m + socket.gethostname() + ' '
    if service_name:
        m = m + service_name + ' '
    if timestamp or hoststamp or service_name:
        m = m + ': '
    m = m + message
    with open(filename, 'a') as f:
        f.write(m + '\n')
    if console:
        print m

# Logging class so we can store some state for frequent logging
class Log:
    '''stores all the options for yelling.log, useful for frequent logging
    without the boatload of options
    '''
    def __init__(self, filename, service_name=None, hoststamp=True, timestamp=True, console=True):
        self.filename = filename
        self.service_name = service_name
        self.hoststamp = hoststamp
        self.timestamp = timestamp
        self.console = console
    def write(self, message):
        '''write to log file'''
        log(self.filename, message, self.service_name, self.hoststamp, self.timestamp, self.console)
    def __str__(self):
        return '<yelling.Log, %s' % filename

# Email
def email(recipients, subject, message, sender=None):
    '''sends a good, old-fashioned email via smtp'''
    if settings.smtp_server == '':
        print 'No SMTP server defined, unable to send email'
        return
    if type(recipients) is not types.ListType:
        recipients = [recipients]
    if not sender:
        username = getpass.getuser()
        hostname = socket.gethostname()
        sender = '%s@%s' % (username, hostname)
    message = ('Subject: %s' % subject) + '\n\n' + message
    try:
        smtp = smtplib.SMTP(setting.smtp_server)
        smtp.sendmail(sender, recipients, message)
    except smtplib.SMTPException:
        print 'yelling: email: Failed to send message'
        raise

# SMS messaging
sms_domain = {'tmobile': 'tmomail.net',
    'virgin': 'vmobl.com',
    'cingular': 'cingularme.com',
    'sprint': 'messaging.sprintpcs.com',
    'verizon': 'vtext.com',
    'nextel': 'messaging.nextel.com',
    'uscellular': 'email.uscc.net',
    'suncom': 'tms.suncom.com',
    'powertel': 'ptel.net',
    'att': 'txt.att.net',
    'att_mms': 'MMS.att.net',
    'alltel': 'message.alltel.com',
    'metropcs': 'MyMetroPcs.com',
    'googlevoice': 'txt.voice.google.com'}

def sms_carriers():
    '''returns a list of known sms carriers'''
    l = []
    for carrier in sms_domain:
        l.append(carrier)
    return l

def sms(phone, carrier, subject, message, sender=None):
    '''sends an sms message to a phone via email. this is a little dicey since
    carriers may change their domains at any time.
    '''
    # regex from ``Dive into Python''
    # http://diveintopython.org/regular_expressions/phone_numbers.html
    phone_pattern = re.compile(r'''
                    # don't match beginning of string, number can start anywhere
        (\d{3})     # area code is 3 digits (e.g. '800')
        \D*         # optional separator is any number of non-digits
        (\d{3})     # trunk is 3 digits (e.g. '555')
        \D*         # optional separator
        (\d{4})     # rest of number is 4 digits (e.g. '1212')
        \D*         # optional separator
        (\d*)       # extension is optional and can be any number of digits
        $           # end of string
        ''', re.VERBOSE)
    phone = ''.join(phone_pattern.search(phone).groups())

    try:
        to_address = str(phone) + '@' + sms_domain[carrier]
    except KeyError:
        print 'yelling: sms: Unknown SMS carrier', carrier
        raise

    email(to_address, subject, message, sender)

# HTTP POST
def http_post(url, params):
    '''post some key-value pairs to a url with an http post'''
    try:
        params = urllib.urlencode(params)
    except TypeError:
        print 'yelling: http_post: Unable to urlencode params'
        raise
    f = urllib.urlopen(url, params)
    print f.read()

