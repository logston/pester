"""
2013 Paul Logston

This module defines a class that defines methods for checking
whether a Pestering is due or not
"""
from django.utils import timezone

from pester.models import PesteringAttempt
from pester.pesterutils import patterns

class PesteringPatternChecker(object):
    """A suite of pattern checkers"""

    def __init__(self):
        pass
    
    def _get_next_due_datetime(self, code, pestering_attempts):
        """Return pattern fucntion for a given code"""
        if   code == 'every_5_min':
            return patterns.every_5_min(pestering_attempts)
        elif code == 'every_10_min':
            return patterns.every_10_min(pestering_attempts)
        elif code == 'every_30_min':
            return patterns.every_30_min(pestering_attempts)
        elif code == 'every_1_hr':
            return patterns.every_1_hr(pestering_attempts)
        elif code == 'every_2_hr':
            return patterns.every_2_hr(pestering_attempts)
        elif code == 'every_4_hr':
            return patterns.every_4_hr(pestering_attempts)
        elif code == 'every_8_hr':
            return patterns.every_8_hr(pestering_attempts)
        elif code == 'every_16_hr':
            return patterns.every_16_hr(pestering_attempts)
        elif code == 'every_1_day':
            return patterns.every_1_day(pestering_attempts)
        elif code == 'fibonacci_min':
            return patterns.fibonacci_min(pestering_attempts)
        elif code == 'fibonacci_day':
            return patterns.fibonacci_day(pestering_attempts)
        else:
            return patterns.never(pestering_attempts)

    def is_due(self, pestering):
        """Return True if another Pester form Pestering is due"""
        pestering_attempts = PesteringAttempt.objects.filter(
                pestering=pestering,
                success=True).order_by('-attempt_time')
        if not len(pestering_attempts):
            return True
        next_due_datetime = self._get_next_due_datetime(
                pestering.pattern.code,
                pestering_attempts)
        if next_due_datetime < timezone.now():
            return True
        return False


