""""
Paul Logston 2013

This class class defines a class for retreiving 
media resource URLs from the Bing Image Search API.
"""

import urllib, urllib2, base64
import simplejson

class GoogleAPI(object):
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

    def query(self, search_terms, offset=0, adult='M'):
        """Return Google Search results as dictionary"""
        if not search_terms:
            raise ValueError("No search terms given.")
            
        adult_levels = {'O':'off', 'M':'medium', 'H':'high'}
        
        self.q = search_terms
        self.safe = adult_levels[adult]

        return self._parse_result(
                simplejson.load(self._make_request(self._get_query_string())))

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

    def _parse_result(self, result_dict):
        """Return a list of tuples [(url, file_type, width, height)]"""
        result_list = result_dict['items']
        return [(
            result['link'],
            result['mime'],
            int(result['image']['width']),
            int(result['image']['height'])) for result in result_list]
