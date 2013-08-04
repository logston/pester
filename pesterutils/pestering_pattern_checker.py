"""
2013 Paul Logston

This module defines a class that defines methods for checking
whether a Pestering is due or not
"""
from django.utils import timezone

from pester.models import PesteringAttempt
class PesteringPatternChecker(object):
    """A suite of pattern checkers"""

    def __init__(self):
        pass

    def is_due(self, pestering):
        """Return True if another Pester form Pestering is due"""
        pattern_name = pestering.pattern.name
        
        pestering_attempts = PesteringAttempt.objects.filter(
                pestering=pestering,
                success=True).order_by('-attempt_time')
        
        print len(pestering_attempts) 

        return False
