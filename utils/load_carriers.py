#! /home/paul/.virtualenvs/dj/bin/python
"""
2013 Paul Logston

File imports carriers from JSON file and inserts each carrier
into pester_carrier table of pester database.

This file was designed to sit in a subdirectory (utils) off the 
Pester app which in turn would sit as a subdirectory of the 
project hosting the Pester app.
+-+ mysite/
  +-+ mysite/
  + +- settings.py
  |
  +-+ pester/
    +-+ utils/
      +- load_carriers.py
"""
def main():
    import os
    UTILS_DIR = os.path.dirname(os.path.abspath(__file__))
    PESTER_DIR = os.path.dirname(UTILS_DIR)
    MYSITE_DIR = os.path.dirname(PESTER_DIR)
    import sys
    sys.path.append(MYSITE_DIR)

    os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

    import simplejson
    from pester.models import Carrier

    with open(os.path.join(UTILS_DIR,'sms_mms_gateways.json')) as fp:
        jobj = simplejson.load(fp)

    for carrier in jobj['mms_carriers']['us'].values():
        print 'saving ' + carrier[0] + ' to db ...',
        Carrier(name=carrier[0], gateway=carrier[1].split('@')[1]).save()
        print 'saved'

if __name__ == '__main__':
    main()
