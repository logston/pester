#! /home/paul/.virtualenvs/dj/bin/python

"""
Paul Logston 2013
Text Testing Script.
Made to test the functionality of the texting scripts.

"""
import smtplib
from datetime import datetime 

FROM = 'text@logston.me'
TO = '5107554474@vzwpix.com'
MESSAGE = ''.join(('Content-Type: text/html\n\n',
                    'Test Text sent at ',
                    str(datetime.now()))
                )

server = smtplib.SMTP()
print('Server Created', str(server))
conn = server.connect('smtp.logston.me')
print('Connected', str(conn))
tls = server.starttls()
print('TLS Started', str(tls))
ehlo = server.ehlo()
print('ehlo', str(ehlo))
login = server.login('text@logston.me', 'SorryDude')
print('Login', str(login))
sendmail = server.sendmail(FROM, TO, MESSAGE)
print('Sendmail Result', str(sendmail))
q = server.quit()
print('Stop Server', str(q))
