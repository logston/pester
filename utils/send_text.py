#! /home/paul/.virtualenvs/dj/bin/python

"""
Paul Logston 2013
Text Testing Script.
Made to test the functionality of the texting scripts.

"""
from __future__ import print_function
import smtplib
from datetime import datetime 

FROM = 'text@logston.me'
TO = '5107554474@vzwpix.com'
MESSAGE = ''.join(('Content-Type: text/plain\n\n',
                    'Test Text sent at ',
                    str(datetime.now()))
                )

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
    sendmail = server.sendmail(FROM, TO, MESSAGE)
    print('Sendmail Result', str(sendmail))
except Exception as e:
    for recip, msg in e.recipients.items():
        print('ERROR:', recip, msg, sep=' ')
q = server.quit()
print('Stop Server', str(q))
