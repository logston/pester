#! /home/paul/.virtualenvs/dj/bin/python

"""
Paul Logston 2013
Text Testing Script.
Made to test the functionality of the texting scripts.

"""
from __future__ import print_function
import smtplib
from datetime import datetime
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import os
import urllib2
DIR = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(DIR, 'kitten.jpg')

# BUILD MESSAGE
FROM = 'pester@pestering.me'
TO = '5107554474@vzwpix.com'
SUBJECT = str(datetime.now())

MIMEMSG = MIMEMultipart()
MIMEMSG['From'] = FROM
MIMEMSG['To'] = TO
MIMEMSG['Subject'] = SUBJECT

URL = 'http://doblelol.com/uploads/1/funny-cat-picture-wallpaper.jpg'

# open URL
fp = urllib2.urlopen(URL)
MIMEMSG.attach(MIMEImage(fp.read()))

# SEND
server = smtplib.SMTP()
server.set_debuglevel(1)
print('Server Created', str(server))
conn = server.connect('localhost')
print('Connected', str(conn))
tls = server.starttls()
print('TLS Started', str(tls))
ehlo = server.ehlo()
print('ehlo', str(ehlo))
#login = server.login('text@logston.me', 'HappyDude')
#print('Login', str(login))

try: 
    sendmail = server.sendmail(FROM, TO, MIMEMSG.as_string())
    print('Sendmail Result', str(sendmail))
except Exception as e:
    for recip, msg in e.recipients.items():
        print('ERROR:', recip, msg, sep=' ')
q = server.quit()
print('Stop Server', str(q))
