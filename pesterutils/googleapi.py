""""
Paul Logston 2013

This class class defines a class for retreiving 
media resource URLs from the Bing Image Search API.
"""

import urllib, urllib2, base64
import simplejson

class GoogleAPI():
    """Encapsulates Google Custom Search calls"""

    def __init__(self, key, cx):
        if not key:
            raise ValueError("""key is not a valid Google API"""
                             """ Access Key: %s""" % key)
        if not cx:
            raise ValueError("""cx is not a valid Google Custom"""
                             """ Search engine id: %s""" % cx)
        self.key = key
        self.cx = cx
        self.q = ''
        self.safe = 'off' #or medium, high
        self.APIURL = 'https://www.googleapis.com/customsearch/v1'

    def query(self, q, safe='off'):
        """Return Google Search results as dictionary"""
        if not q:
            raise ValueError("No search terms given.")

        self.q = q
        self.safe = safe

        return simplejson.load(self._make_request(self._get_query_string()))

    def _get_query_string(self):
        """Return query string wih google search query parameters"""
        query_args = {'key':self.key,
                      'cx':self.cx,
                      'searchType':'image',
                      'imgSize':'medium',
                      'q':self.q,
                      'safe':self.safe}

        return '?'+urllib.urlencode(query_args)

    def _make_request(self, query_string):
        """Return request result from api call"""
        url = self.APIURL+query_string
        request = urllib2.Request(url)
        result = urllib2.urlopen(request)
        return result
