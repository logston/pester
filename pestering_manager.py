#! /home/paul/.virtualenvs/dj/bin/python
"""
Paul Logston 2013
This script manages the collection and sending
of all pesterings that are due to be sent.
This script is called by a cronjob every minute.
"""

from pesterutils import bingapi
from pesterutils import sendpester
from random import randint

with open('priv/bingapi.key') as fp:
    bing_api_key = fp.read().strip()

with open('priv/paul.mmsaddress') as fp:
    paul = fp.read().strip()

bobj = bingapi.BingAPI(bing_api_key)
d = bobj.query('CATZ')['d']['results']
url = d[randint(0, len(d)-1)]['MediaUrl']

p = sendpester.SendPester()
p.send_pester(paul, url)
