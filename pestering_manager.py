"""
Paul Logston 2013
This script manages the collection and sending
of all pesterings that are due to be sent.
This script is called by a cronjob every minute.
"""

import sys, os
PESTERDIR = os.path.dirname(os.path.abspath(__file__))
PARENTDIR = os.path.dirname(PESTERDIR)
sys.path.append(PESTERDIR)
sys.path.append(PARENTDIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

from datetime import datetime
from random import randint

from pester.models import *

from pester.pesterutils import bingapi
from pester.pesterutils import sendpester
"""
OUTLINE
Start PesteringManagerRun
    Find out active Pesterings
        For each pestering
            if pattern says its time to send new pester
                Start pester attempt
                Get number of unused imageurls
                if number is 0
                    get more
                    go back to 'Get number of unused imageurls'
                take first unused image url 
                send pester
                save pester attempt results
    Save PesteringManagerRun
"""


DIR = os.path.join(PESTERDIR, 'priv/')

with open(DIR + 'bingapi.key') as fp:
    bing_api_key = fp.read().strip()

with open(DIR + 'paul.mmsaddress') as fp:
    user = fp.read().strip()

bobj = bingapi.BingAPI(bing_api_key)
d = bobj.query('Fat Cats')['d']['results']
url = d[randint(0, len(d)-1)]['MediaUrl']

image_0 = Image.objects.all()[0]
pestering_0 = Pestering.objects.all()[0]
pestering_manager_run_0 = PesteringManagerRun.objects.all()[0]

pestering_attempt = PesteringAttempt(pestering=pestering_0, 
                                    pestering_manager_run=pestering_manager_run_0,
                                     image=image_0,
                                     attempt_time=datetime.now())
pestering_attempt.save()
p = sendpester.SendPester()
p.send_pester(user, url)
pestering_attempt.success = True
pestering_attempt.save()
