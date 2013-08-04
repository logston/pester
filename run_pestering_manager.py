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

from pester.pesterutils.pester_manager import PesteringManager

pestering_manager = PesteringManager()
pestering_manager.run()
