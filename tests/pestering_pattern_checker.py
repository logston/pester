"""
Tests pestering pattern Checker class and patterns module definitions.
"""
from datetime import timedelta as timedelta

from django.test import TestCase
from django.utils import timezone

from pester.models import *

from pester.pesterutils.pestering_pattern_checker import PesteringPatternChecker

class PesteringPatternCheckerTest(TestCase):
    
    pat_code_list = [
            ('every_5_min', 5, 5, 5),
            ('every_1_day', 1, 1, 1), 
            ('fibonacci_day', 1, 1, 2),
            ]

    def setUp(self):
        carrier_1 = Carrier.objects.create(
                name='Fake Carrier 1',
                gateway='fakegateway1.com')
        carrier_2 = Carrier.objects.create(
                name='Fake Carrier 2',
                gateway='fakeGateway2.com')
        user = User.objects.create(
                first_name='TestUserFirstN', 
                last_name='TestUserLastN',
                email='testUseremail@email.com',
                phone_number='5108889999',
                carrier=carrier_1)
        recipient = Recipient.objects.create(
                first_name='RecipientFN',
                last_name='RecipientLN',
                email='testRecipEmail@email.com',
                phone_number='5101112222',
                carrier=carrier_2,
                created_by=user)
        for pat in self.pat_code_list:
            pattern = Pattern.objects.create(
                    name=pat[0],
                    description='',
                    code=pat[0])
            Pestering.objects.create(
                    user=user, 
                    recipient=recipient, 
                    search_term='Test',
                    pattern=pattern,
                    start_time=timezone.now()+timedelta(hours=-1),
                    end_time=timezone.now()+timedelta(hours=1),
                    title='Test')
        pestering_manager_run = PesteringManagerRun.objects.create()
        image = ImageData.objects.create(
                search_term='Test',
                url='TestURL',
                file_type='test',
                height=50,
                width=50)
        for pestering in Pestering.objects.all():
            PesteringAttempt.objects.create(
                    pestering=pestering,
                    pestering_manager_run=pestering_manager_run,
                    image=image,
                    attempt_time=timezone.now(),
                    success=True)

    def test_number_pestering_attempts_created_by_set_up(self):
        self.assertEqual(
                len(self.pat_code_list), 
                PesteringAttempt.objects.all().count())
        
    def test_is_due_for_every_5_min(self):
        pestering = Pestering.objects.filter(pattern__name='every_5_min')[0]
        pa = PesteringAttempt.objects.get(pestering=pestering)
        # pestering save just moments ago. should return false
        self.assertEqual(PesteringPatternChecker().is_due(pestering), False)

        # pestering attempt 6 minutes ago. Should return true
        pa.attempt_time=timezone.now()+timedelta(minutes=-6)
        pa.save()
        self.assertEqual(PesteringPatternChecker().is_due(pestering), True)
        
        # no pestering attempts should cause is_due to return true
        pa.delete()
        self.assertEqual(PesteringPatternChecker().is_due(pestering),True)
        
    def test_is_due_for_every_1_day(self):
        pestering = Pestering.objects.filter(pattern__name='every_1_day')[0]
        pa = PesteringAttempt.objects.get(pestering=pestering)
        # pestering save just moments ago. should return false
        self.assertEqual(PesteringPatternChecker().is_due(pestering), False)

        # pestering attempt 1 day and 1 minute  ago. Should return true
        pa.attempt_time=timezone.now()+timedelta(days=-1,minutes=-1)
        pa.save()
        self.assertEqual(PesteringPatternChecker().is_due(pestering), True)
        
        # pestering attempt 23 hours and 59 minutes ago, should return false
        pa.attempt_time=timezone.now()+timedelta(days=-1,minutes=1)
        pa.save()
        self.assertEqual(PesteringPatternChecker().is_due(pestering), False)

    def test_is_due_for_fibonacci_day(self):
        pestering = Pestering.objects.filter(pattern__name='fibonacci_day')[0]
        # one pestering just created, should return false
        self.assertEqual(
                PesteringAttempt.objects.filter(pestering=pestering).count(), 1)
        self.assertEqual(PesteringPatternChecker().is_due(pestering), False)
        
        # 1 attempt, 23 hours 59 min ago, shoud return false 
        pa = PesteringAttempt.objects.get(pestering=pestering)
        pa.attempt_time = timezone.now()+timedelta(days=-1,minutes=1)
        pa.save()
        self.assertEqual(PesteringPatternChecker().is_due(pestering), False)
        # 1 attempt 1 day and 1 minute ago, should return true
        pa.attempt_time=timezone.now()+timedelta(days=-1,minutes=-1)
        pa.save()
        self.assertEqual(PesteringPatternChecker().is_due(pestering), True)
        # 6 attempts, last was more than a day ago, should return false
        for i in range(5):
            pa.pk = None
            pa.attempt_time=timezone.now()+timedelta(days=-i,minutes=-1)
            pa.save()
        self.assertEqual(
                PesteringAttempt.objects.filter(pestering=pestering).count(),
                6)
        self.assertEqual(PesteringPatternChecker().is_due(pestering), False)
        # 6 attempts, last was 13 days and a mintue ago, should return true
        for pa in PesteringAttempt.objects.filter(pestering=pestering):
            pa.attempt_time=timezone.now()+timedelta(days=-13,minutes=-1)
            pa.save()
        self.assertEqual(
                PesteringAttempt.objects.filter(pestering=pestering).count(),
                6)
        self.assertEqual(PesteringPatternChecker().is_due(pestering), True)
