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
import os, logging, json, time, urllib, re, yaml
from selenium import webdriver

sandbox_key = "sandbox-user"
production_key = "production-user"
_user_credential_list = {}

def read_user_info(conf = None):

    logging.info("Loading user credential configuration file at: %s", conf)
    with open(conf, 'r') as f:
        if conf.endswith('.yaml') or conf.endswith('.yml'):
            content = yaml.load(f)
        elif conf.endswith('.json'):
            content = json.loads(f.read())
        else:
            raise ValueError('Configuration file need to be in JSON or YAML')

        for key in content:
            logging.debug("Environment attempted: %s", key)
            
            if key in [sandbox_key, production_key]:       
                userid = content[key]['username']
                password = content[key]['password']        
                _user_credential_list.update({key:[userid, password]})
        
        
def get_authorization_code(signin_url):

    user_config_path = os.path.join(os.path.split(__file__)[0], 'config\\test-config-sample.yaml')
    read_user_info(user_config_path)
    
    env_key = production_key
    if "sandbox" in signin_url:
        env_key = sandbox_key
    
    userid = _user_credential_list[env_key][0]
    password = _user_credential_list[env_key][1]
    
    browser = webdriver.Chrome()
    browser.get(signin_url)
    time.sleep(5)

    form_userid = browser.find_element_by_name('userid')
    form_pw = browser.find_element_by_name('pass')  
    
    form_userid.send_keys(userid)
    form_pw.send_keys(password)    
    
    browser.find_element_by_id('sgnBt').submit()

    time.sleep(5)
    
    url = browser.current_url
    browser.quit()

    if 'code=' in url:
        code = re.findall('code=(.*?)&', url)[0]
        logging.info("Code Obtained: %s", code)
    else:
        logging.error("Unable to obtain code via sign in URL")
    
    decoded_code = urllib.unquote(code).decode('utf8')
    return decoded_code
    
