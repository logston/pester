""" 
2013 Paul Logston

This script defines a class that manages all pesterings due 
at runtime.
"""

from django.utils import timezone

from pester.models import PesteringManagerRun, Pestering

from pester.pesterutils.imagemanager import ImageManager
from pester.pesterutils.pestering_pattern_checker import PesteringPatternChecker

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
            print 'Act on ' + str(pestering)
            
            image_manager = ImageManager(pestering)
            print image_manager.get_image()



            """
            Start Pestering attempt here"""
            
            # pull new image
            
            
            """ 
                 BUILD MODEL: APICALL(search_engine, search_term, offset, date_time, number of api calls left)
                 put model in bing and google apis or make parent ImageManager

            if number of unused images is 0, go get more"""
            # start pestering attempt
            """
            pestering_attempt = pestering_attempt_start(
                    pestering, 
                    self.pestering_manager_run,
                    image)
        
            try:
                # send image
                "
                "
                pass
                # end pestering attempt with success
                #pestering_attempt_success(pestering_attempt)
            except Exception as e:
                PesteringException.objects.create(
                        pestering_attempt=pestering_attempt,
                        exception_traceback=str(e))
        """
        # close up pestering manager run
        self.pestering_manager_run.completed=True
        self.pestering_manager_run.save()

    def pestering_attempt_start(self, pestering, pestering_manager_run, image):
        """Return pestering attempt object"""
        pestering_attempt = PesteringAttempt(
                pestering=pestering,
                pestering_manager_run=pestering_manager_run,
                image=image,
                success=False)
        pestering_attempt.save()      
        return pestering_attempt

    def pestering_attempt_success(self, pestering_attempt):
        pestering_attempt.success=True
        pestering_attempt.save()
