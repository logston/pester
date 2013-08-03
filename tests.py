"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from pester.models import *

class CarrierModelTest(TestCase):
    def setUp(self):
        Carrier.objects.create(name='Fake Carrier', 
                               gateway='fakegateway.com')
        Carrier.objects.create(name='Wireless',
                               gateway='Wireless.wire.com')

    def test_model_carrier_unicode(self):
        """
        Test to see that __unicode__ method is working.
        """
        car_1 = Carrier.objects.get(name='Fake Carrier')
        car_2 = Carrier.objects.get(name='Wireless')
        self.assertEqual(car_1.gateway, 'fakegateway.com')
        self.assertEqual(car_2.gateway, 'Wireless.wire.com')
