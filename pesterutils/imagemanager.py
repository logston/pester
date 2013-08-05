"""
2013 Paul Logston

This class defines methods for returning then next available Image instance for 
use in a pestering. It also manages call the image APIs in the event that more 
ImageDatas are necessary.
"""

from pester.models import ImageData, PesteringAttempt


class ImageManager(object):
    """Defines methods to manage Image instance acquisition and delivery"""

    def __init__(self, pestering):
        self.pestering = pestering
        self._used_image_pk_list = None
        self._unused_image_list = None

    def get_image(self):
        """Return unused ImageData instance or exception"""
        self._get_used_image_list()
        # add in a while for checking to see if image is readiy
        self._get_unused_image_list()

        return self._unused_image_list

    def _get_used_image_list(self):
        """
        Get list of images from successful pestering attempts for pestering
        """
        pa_list = PesteringAttempt.objects.filter(
                pestering=self.pestering, 
                success=True)
        self._used_image_pk_list = [pestering_attempt.image.pk 
                for pestering_attempt in pa_list
                if pestering_attempt.image]

    def _get_unused_image_list(self):
        """
        Get list of images that fullfill the requirements of the pestering
        that have not been sent.
        """
        self._unused_image_list = ImageData.objects.exclude(
                pk__in=self._used_image_pk_list
                ).filter(
                search_term=self.pestering.search_term,
                adult_safety_level=self.pestering.adult_safety_level
                )
