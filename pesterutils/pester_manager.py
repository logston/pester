""" 
2013 Paul Logston

This script defines a class that manages all pesterings due 
at runtime.
"""

from django.utils import timezone

from pester.models import PesteringManagerRun, Pestering

class PesteringManager(object):
    """Manages all Pesterings due at runtime."""

    def __init__(self):
        self.pestering_manager_run = PesteringManagerRun()

    def run(self):
        self.pestering_manager_run.save()
        pesterings = Pestering.objects.filter(start_time__lte=timezone.now(),
                                              end_time__gte=timezone.now())
        print pesterings
