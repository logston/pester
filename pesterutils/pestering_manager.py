""" 
2013 Paul Logston

This script defines a class that manages all pesterings due 
at runtime.
"""
import traceback

from django.utils import timezone

from pester.models import PesteringManagerRun, Pestering, PesteringAttempt
from pester.models import PesteringException
from pester.models import User, Recipient, Carrier

from pester.pesterutils.imagemanager import ImageManager
from pester.pesterutils.pestering_pattern_checker import PesteringPatternChecker
from pester.pesterutils.sendpester import SendPester
class PesteringManager(object):
    """Manages all Pesterings due at runtime."""

    def __init__(self):
        self.pestering_manager_run = PesteringManagerRun()

    def run(self):
        """Send active and due Pesterings"""
        self.pestering_manager_run.completed=False
        self.pestering_manager_run.save()
        pesterings = Pestering.objects.filter(start_time__lte=timezone.now(),
                                              end_time__gte=timezone.now())
        ppc = PesteringPatternChecker()
        for pestering in pesterings:
            if not ppc.is_due(pestering):
                continue

            pestering_attempt = PesteringAttempt.objects.create(
                    pestering=pestering,
                    pestering_manager_run=self.pestering_manager_run)

            pestering_attempt.success=False 
            pestering_attempt.save()

            try:
                image_manager = ImageManager(pestering)
                image = image_manager.get_image()
                pestering_attempt.image = image
                pestering_attempt.save()
                
                # send pester
                pester = SendPester()
                for to in self._get_recipient_emails(pestering):
                    pester.send_pester(
                        to=str(to),
                        url=image.url,
                        frm=pestering.user.email,
                        subject=pestering.title) 
                pestering_attempt.success=True
                pestering_attempt.save()
            except:
                PesteringException.objects.create(
                        pestering_attempt=pestering_attempt,
                        exception_traceback=traceback.format_exc())
        
        # close up pestering manager run
        self.pestering_manager_run.completed=True
        self.pestering_manager_run.save()

    def _get_recipient_emails(self, pestering):
        """Get email addresses for all recipients of this pestering"""
        recip_emails = []
        if pestering.notify_user_method == 'E':
            recip_emails.append(pestering.user.email)
        if pestering.notify_user_method == 'T':
            recip_emails.append(
                    self._build_email_from_phone_number(
                        pestering.user))
        if pestering.notify_user_method == 'B':
            recip_emails.append(pestering.user.email)
            recip_emails.append(
                    self._build_email_from_phone_number(
                        pesering.user))
        if pestering.notify_recipient_method == 'E':  
            recip_emails.append(pestering.recipient.email)
        if pestering.notify_recipient_method == 'T':
            recip_emails.append(
                    self._build_email_from_phone_number(
                        pestering.recipient))
        if pestering.notify_recipient_method == 'B':
            recip_emails.append(pestering.recipient.email)
            recip_emails.append(
                    self._build_email_from_phone_number(
                        pesering.recipient))
        return recip_emails

    def _build_email_from_phone_number(self, person):
        """Build email from a person's carrier and phone number"""
        return person.phone_number + '@' + person.carrier.gateway
