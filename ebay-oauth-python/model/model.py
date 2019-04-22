# -*- coding: utf-8 -*-
"""
Copyright 2019 eBay Inc.
 
Licensed under the Apache License, Version 2.0 (the "License");
You may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,

WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

See the License for the specific language governing permissions and
limitations under the License.

"""

class env_type(object):
    def __init__(self, config_id, web_endpoint, api_endpoint):
        self.config_id = config_id
        self.web_endpoint = web_endpoint
        self.api_endpoint = api_endpoint
    
class environment(object):
    PRODUCTION = env_type("api.ebay.com", "https://auth.ebay.com/oauth2/authorize", "https://api.ebay.com/identity/v1/oauth2/token")
    SANDBOX = env_type("api.sandbox.ebay.com", "https://auth.sandbox.ebay.com/oauth2/authorize", "https://api.sandbox.ebay.com/identity/v1/oauth2/token")


class credentials(object):
    def __init__(self, client_id, client_secret, dev_id, ru_name):
        self.client_id = client_id 
        self.dev_id = dev_id
        self.client_secret = client_secret
        self.ru_name = ru_name
    

class oAuth_token(object):

    def __init__(self, error=None, access_token=None, refresh_token=None, refresh_token_expiry=None, token_expiry=None):
        '''
            token_expiry: datetime in UTC
            refresh_token_expiry: datetime in UTC
        '''
        self.access_token = access_token
        self.token_expiry = token_expiry
        self.refresh_token = refresh_token
        self.refresh_token_expiry = refresh_token_expiry
        self.error = error
        
        
    def __str__(self):
        token_str = '{' 
        if self.error != None:
            token_str += '"error": "' + self.error + '"'
        elif self.access_token != None:
            token_str += '"access_token": "'  + self.access_token + '", "expires_in": "' + self.token_expiry.strftime('%Y-%m-%dT%H:%M:%S:%f') + '"'
            if self.refresh_token != None:
                token_str += ', "refresh_token": "' + self.refresh_token  + '", "refresh_token_expire_in": "' + self.refresh_token_expiry.strftime('%Y-%m-%dT%H:%M:%S:%f')+ '"'
        token_str += '}'
        return token_str