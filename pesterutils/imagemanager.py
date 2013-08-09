"""
2013 Paul Logston

This class defines methods for returning then next available Image instance for 
use in a pestering. It also manages call the image APIs in the event that more 
ImageDatas are necessary.
"""
from django.db.utils import IntegrityError
import simplejson

from pester.models import API, APICall, ImageData, PesteringAttempt

from pester.pesterutils.bingapi import BingAPI
from pester.pesterutils.googleapi import GoogleAPI


class APIException(Exception):
    """Exception class for all API issues"""
    pass

class NoAPIException(APIException):
    """Exception for no available APIs"""
    
    def __init__(self, msg):
        """ msg -- explination of error """
        self.msg = msg

class NoAPIResultsException(APIException):
    """Exception for no when API returns no results"""

    def __init__(self, api, msg):
        """ msg -- explination of error"""
        self.msg = api + ': ' + msg

class ImageManager(object):
    """Defines methods to manage Image instance acquisition and delivery"""

    def __init__(self, pestering):
        self.pestering = pestering
        self._used_image_pk_list = None
        self._unused_image_list = None
        self._use_bing = True
        self._bing_offset = 0
        self._use_google = True
        self._google_offset = 0
        self._get_used_image_list()
        self._get_unused_image_list()

    def get_image(self):
        """Return unused ImageData instance or exception"""
        if not self._unused_image_list:
            self._get_more_images()

        if self._unused_image_list:
            return self._unused_image_list[0]

        raise NoAPIResultsException('ALL APIs', 'No API results recieved')

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

    def _get_api_offset(self, api):
        """return the offset for the api, search_term, options combo"""
        if api == 'Bing':
           apic=APICall.objects.filter(
                    api=api,
                    pestering.search_term=self.pestering.search_term,
                    pestering.adult_safety_level=self.pestering.adult_safety_level)
            self._bing_offset=len(apic)*50

        if self._use_google:
            apic=APICall.objects.filter(
                    api=api,
                    pestering.search_term=self.pestering.search_term,
                    pestering.adult_safety_level=self.pestering.adult_safety_level)         
            self._google_offset=len(apic)*10
                
    def _get_more_images(self):
        """Query API for more images and load them into db"""
        if self._use_bing:
            api = API.objects.get(name='Bing')
            bapi = BingAPI(api.key)
            self._insert_images_into_db(
                    bapi.query(
                        search_terms=self.pestering.search_term,
                        offset=self._bing_offset,
                        adult=self.pestering.adult_safety_level))
            APICall.objects.create(api=api,pestering=pestering)
            return
        if self._use_google:
            g = API.objects.get(name='Google')
            key = g.key
            params = simplejson.loads(g.params)
            gapi = GoogleAPI(key, params['cx'])
            self._insert_images_into_db(
                    gapi.query(
                        search_terms=self.pestering.search_term,
                        offset=self._google_offset,
                        adult=self.pestering.adult_safety_level))
            APICall.objects.create(api=g, pestering=pestering)
            return
        raise NoAPIException('No available APIs to query.') 

    def _insert_images_into_db(self, image_list):
        """Insert new images into db"""
        for image in image_list:
            try:
                ImageData.objects.create(
                    search_term=self.pestering.search_term,
                    url=image[0],
                    file_type=image[1],
                    width=image[2],
                    height=image[3],
                    adult_safety_level=self.pestering.adult_safety_level)
            except IntegrityError:
                pass
        self._get_unused_image_list()
