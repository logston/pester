"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from datetime import timedelta as timedelta

from django.test import TestCase
from django.utils import timezone

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

class UserModelTest(TestCase):
    pass

class RecipientModelTest(TestCase):
    pass

class PatternModelTest(TestCase):
    pass

class PesteringModelTest(TestCase):
    def setUp(self):
        carrier_1 = Carrier.objects.create(name='Fake Carrier 1',
                                           gateway='fakegateway1.com')
        carrier_2 = Carrier.objects.create(name='Fake Carrier 2',
                                           gateway='fakeGateway2.com')
        user = User.objects.create(first_name='TestUserFirstN', 
                                   last_name='TestUserLastN',
                                   email='testUseremail@email.com',
                                   phone_number='5108889999',
                                   carrier=carrier_1)
        recipient = Recipient.objects.create(first_name='RecipientFN',
                                             last_name='RecipientLN',
                                             email='testRecipEmail@email.com',
                                             phone_number='5101112222',
                                             carrier=carrier_2,
                                             created_by=user)
        pattern = Pattern.objects.create(name='Once a Test',
                                         description='Once every test')
        pestering = Pestering.objects.create(user=user, 
                                 recipient=recipient, 
                                 search_term='CATS!',
                                 pattern=pattern,
                                 start_time=timezone.now(),
                                 end_time=timezone.now()+timedelta(hours=1),
                                 title='Test Pestering Now')
        pestering.pk = None
        pestering.start_time=timezone.now()+timedelta(hours=-2)
        pestering.end_time=timezone.now()+timedelta(hours=-1)
        pestering.title='Test Pestering Past'
        pestering.save()

        pestering.pk = None
        pestering.start_time=timezone.now()+timedelta(hours=1)
        pestering.end_time=timezone.now()+timedelta(hours=2)
        pestering.title='Test Pestering Future'
        pestering.save()

    def test_model_pestering_now(self):
        now = Pestering.objects.filter(start_time__lte=timezone.now(),
                                       end_time__gte=timezone.now())
        self.assertEqual(len(now), 1)
    def test_model_pestering_past(self):
        past = Pestering.objects.filter(start_time__lt=timezone.now(),
                                        end_time__lt=timezone.now())
        self.assertEqual(len(past), 1)
    def test_modelpestering_future(self):
        future = Pestering.objects.filter(start_time__gt=timezone.now(),
                                          end_time__gt=timezone.now())
        self.assertEqual(len(future),1)
