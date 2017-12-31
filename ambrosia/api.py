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
        lines = [str(line.rstrip('\n')) for line in open('secrets.txt')]
        for line in lines:
            if "api_key" in line:
                api_key = line.split(": ")[1]
                break

        return api_key    
    
    def _make_api_request(self, api_request):
        """Make an API request to the Food2Fork API"""                
        
        # Make the request
        request = urllib2.Request(api_request, headers=self._HEADER)
        response = urllib2.urlopen(request)
        raw = response.read()
        
        request_type = api_request.split('/api/')[1].split('?')[0]
        print('\n*************')
        print(raw)
        print('\n*************')        
        if request_type == 'search':
            json_obj = json.loads(raw)['recipes']
        elif request_type == 'get':
            json_obj = json.loads(raw)['recipe']        
            
        return json_obj
    
        
    def _api_search(self, query, count=1):
        """Return a list of recipes from the Food2Fork.com database"""                        
        # assert(0 < count <= 30), 'max 30 results per call, min 1' #https://github.com/davebshow/food2forkclient/
                
        page = 1
        all_responses = []
        if count > 30:            
            while count > 30:
                # Format the request URI
                query_params = {"key":self._API_KEY, "q":query, "page":page, "count":count}#, "sort":"t"}
                api_request = self._API_URI + "search?" + urlencode(query_params)
                all_responses.append(self._make_api_request(api_request))
                page += 1
                count -= 30
            query_params = {"key":self._API_KEY, "q":query, "page":page, "count":count}#, "sort":"t"}
            api_request = self._API_URI + "search?" + urlencode(query_params)
            all_responses.append(self._make_api_request(api_request))

            return all_responses[0]
        else:
            page = 1
            # Format the request URI
            query_params = {"key":self._API_KEY, "q":query, "page":page, "count":count}#, "sort":"t"}
            api_request = self._API_URI + "search?" + urlencode(query_params)            
            # Make the request
            return self._make_api_request(api_request)
       
    
    def _api_get_recipe(self, recipe_id):
        """Get a specific recipe object from Food2Fork.com"""
        
        # Format the request URI
        query_params = {"key":self._API_KEY, "rId":recipe_id}
        api_request = self._API_URI + "get?" + urlencode(query_params)
        
        # Make the request
        return self._make_api_request(api_request)
    
    def search(self, search_term, count=1):
        """Return a list of recipe json objects from Food2Fork"""
        
        search_result = self._api_search(search_term, count)        
                
        return [self._api_get_recipe(r['recipe_id']) for r in search_result]                
