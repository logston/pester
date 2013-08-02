""""
Paul Logston 2013

This class class defines a class for retreiving 
media resource URLs from the Bing Image Search API.
"""

import urllib, urllib2, base64
import simplejson

class BingAPI(object):
    """Encapsulates Bing Image Search calls"""

    def __init__(self, key):
        if not key:
            raise ValueError("""key is not a valid Windows Azure"""
                             """Marketplace Account Key: %s""" % key)
        self.key = key
        self.search_terms = ''
        self.top = 50
        self.skip = 0
        self.frmt = 'JSON'
        self.adult = 'Off'
        self.market = 'en-US'

    def _quote(self, value):
        # first strip quotes just in case value was pre-quoted
        return "'"+value.strip("'")+"'"

    def query(self, search_terms, top=50, skip=0,
              frmt='JSON', adult='Off', market='en-US'):
        """Return Bing Image Search results as dictionary"""
        if not search_terms:
            raise ValueError("No search terms given.")

        self.search_terms = self._quote(search_terms)
        self.top = top
        self.skip = skip
        self.frmt = frmt
        self.adult = self._quote(adult)
        self.market = self._quote(self.market)

        return simplejson.load(self._make_request(self._get_query_string()))

    def _get_query_string(self):
        """Return URL safe query string"""
        query_args = {'Query':self.search_terms,
                      '$top':self.top,
                      '$skip':self.skip,
                      '$format':self.frmt,
                      'Adult':self.adult,
                      'Market':self.market}

        return '?'+urllib.urlencode(query_args)

    def _make_request(self, query_string):
        """Return request result from api call"""
        APIURL = 'https://api.datamarket.azure.com/Data.ashx/Bing/Search/Image'
        url = APIURL+query_string
        auth_string = base64.encodestring('%s:%s' % ('', self.key)).strip()
        
        request = urllib2.Request(url)
        request.add_header('Authorization', 'Basic %s' % auth_string)
        result = urllib2.urlopen(request)
        return result
