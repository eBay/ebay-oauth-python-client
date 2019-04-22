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

import json
import urllib
import requests
import logging
import model.util
from datetime import datetime, timedelta
from credentialutil import credentialutil
from model.model import oAuth_token

LOGFILE = 'eBay_Oauth_log.txt'
logging.basicConfig(level=logging.DEBUG, filename=LOGFILE, format="%(asctime)s: %(levelname)s - %(funcName)s: %(message)s", filemode='w')


class oauth2api(object):
    
           
    def generate_user_authorization_url(self, env_type, scopes, state=None):
        '''
            env_type = environment.SANDBOX or environment.PRODUCTION
            scopes = list of strings
        '''

        credential = credentialutil.get_credentials(env_type)   
    
        scopes = ' '.join(scopes)
        param = {
                'client_id':credential.client_id,
                'redirect_uri':credential.ru_name,
                'response_type':'code',
                'prompt':'login',
                'scope':scopes
                }
        
        if state != None:
            param.update({'state':state})
        
       
        query = urllib.urlencode(param)
        return env_type.web_endpoint + '?' + query
    

    def get_application_token(self, env_type, scopes):
        """
            makes call for application token and stores result in credential object
            returns credential object
        """
      
        logging.info("Trying to get a new application access token ... ")        
        credential = credentialutil.get_credentials(env_type)       
        headers = model.util._generate_request_headers(credential) 
        body = model.util._generate_application_request_body(credential, ' '.join(scopes))    
        
        resp = requests.post(env_type.api_endpoint, data=body, headers=headers)
        content = json.loads(resp.content)
        token = oAuth_token()     
    
        if resp.status_code == requests.codes.ok:
            token.access_token = content['access_token']
            # set token expiration time 5 minutes before actual expire time
            token.token_expiry = datetime.utcnow()+timedelta(seconds=int(content['expires_in']))-timedelta(minutes=5)

        else:
            token.error = str(resp.status_code) + ': ' + content['error_description']
            logging.error("Unable to retrieve token.  Status code: %s - %s", resp.status_code, requests.status_codes._codes[resp.status_code])
            logging.error("Error: %s - %s", content['error'], content['error_description'])
        return token     
    

    def exchange_code_for_access_token(self, env_type, code):       
        logging.info("Trying to get a new user access token ... ")  
        credential = credentialutil.get_credentials(env_type)   
    
        headers = model.util._generate_request_headers(credential)
        body = model.util._generate_oauth_request_body(credential, code)
        resp = requests.post(env_type.api_endpoint, data=body, headers=headers)
            
        content = json.loads(resp.content)
        token = oAuth_token()     
        
        if resp.status_code == requests.codes.ok:
            token.access_token = content['access_token']
            token.token_expiry = datetime.utcnow()+timedelta(seconds=int(content['expires_in']))-timedelta(minutes=5)
            token.refresh_token = content['refresh_token']
            token.refresh_token_expiry = datetime.utcnow()+timedelta(seconds=int(content['refresh_token_expires_in']))-timedelta(minutes=5)
        else:
            token.error = str(resp.status_code) + ': ' + content['error_description']
            logging.error("Unable to retrieve token.  Status code: %s - %s", resp.status_code, requests.status_codes._codes[resp.status_code])
            logging.error("Error: %s - %s", content['error'], content['error_description'])
        return token
    
    
    def get_access_token(self, env_type, refresh_token, scopes):
        """
        refresh token call
        """
        
        logging.info("Trying to get a new user access token ... ")  

        credential = credentialutil.get_credentials(env_type)   
    
        headers = model.util._generate_request_headers(credential)
        body = model.util._generate_refresh_request_body(' '.join(scopes), refresh_token)
        resp = requests.post(env_type.api_endpoint, data=body, headers=headers)
        content = json.loads(resp.content)
        token = oAuth_token()        
        token.token_response = content    
    
        if resp.status_code == requests.codes.ok:
            token.access_token = content['access_token']
            token.token_expiry = datetime.utcnow()+timedelta(seconds=int(content['expires_in']))-timedelta(minutes=5)
        else:
            token.error = str(resp.status_code) + ': ' + content['error_description']
            logging.error("Unable to retrieve token.  Status code: %s - %s", resp.status_code, requests.status_codes._codes[resp.status_code])
            logging.error("Error: %s - %s", content['error'], content['error_description'])
        return token