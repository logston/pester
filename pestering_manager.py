"""
Paul Logston 2013
This script manages the collection and sending
of all pesterings that are due to be sent.
This script is called by a cronjob every minute.
"""

from datetime import datetime
from random import randint

from models import PesteringAttempt

from pesterutils import bingapi
from pesterutils import sendpester

DIR = '/home/paul/djprojs/mysite/pester/priv/'

with open(DIR + 'bingapi.key') as fp:
    bing_api_key = fp.read().strip()

with open(DIR + 'paul.mmsaddress') as fp:
    user = fp.read().strip()

bobj = bingapi.BingAPI(bing_api_key)
d = bobj.query('Fat Cats')['d']['results']
url = d[randint(0, len(d)-1)]['MediaUrl']

pestering_attempt = PesteringAttempt(pestering=1, 
                                     pestering_manager_run=1,
                                     image=url,
                                     attempt_time=datetime.now())
pestering_attempt.save()
p = sendpester.SendPester()
p.send_pester(user, url)
pestering_attempt.success = True
pestering_attempt.save()
