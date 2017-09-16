# Ambrosia
# Ahmed Elmaleh, John W. Miller, Qingyang Su
# See LICENSE for details
# 2017-09-16

"""A food library"""

from __future__ import print_function

import requests
import urllib2
from urllib import urlencode
import json

class API(object):
    """Ambrosia API"""
    
    """Interface with the Food2Fork.com API"""            
    
    def __init__(self):        
        # Food2Fork links
        self._API_KEY = self._load_credentials()
        self._API_URI = "http://food2fork.com/api/"        
        self._HEADER = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)'}

    def _load_credentials(self):
        """Load the Food2Fork.com API credentials"""
        lines = [str(line.rstrip('\n')) for line in open('../secrets.txt')]
        for line in lines:
            if "api_key" in line:
                api_key = line.split(": ")[1]

        return api_key    
        
    def search(self, query, page=1, count=1):
        """Return a list of recipes from the Food2Fork.com database"""                        
        assert(0 < count <= 30), 'max 30 results per call, min 1' #https://github.com/davebshow/food2forkclient/
        
        # Format the Request URI
        query_params = {"key":self._API_KEY, "q":query, "page":page, "count":count}
        api_request = self._API_URI + "search?" + urlencode(query_params)
        
        # Make the request
        request = urllib2.Request(api_request, headers=self._HEADER)
        response = urllib2.urlopen(request)
        raw = response.read()
        
        # Make the request
        json_obj = json.loads(raw)
        
        return json_obj['recipes']
