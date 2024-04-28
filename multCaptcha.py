import os
import re
import time
import uuid
import base64
import string
import random
import string
import asyncio
import secrets
import urllib3
import requests
from capmonster_python import HCaptchaTask
from capmonster_python.utils import CapmonsterException
from requests.exceptions import ProxyError, ConnectionError
from capmonstercloudclient import CapMonsterClient, ClientOptions
from capmonstercloudclient.requests import RecaptchaV2ProxylessRequest, RecaptchaV3ProxylessRequest

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class CaptchaSolver:
    def __init__(self):
        pass
    
    #  A P I  ~  C A P M O N S T E R

    def captchaLetra_capmonster(self, api_key, img_base64):
        url_create_task = "https://api.capmonster.cloud/createTask"
        url_get_result = "https://api.capmonster.cloud/getTaskResult"

        # Enviar a tarefa para resolver o captcha
        dados = {
            "clientKey": api_key,
            "task": {
                "type": "ImageToTextTask",
                "body": img_base64
            }
        }
        response = requests.post(url_create_task, json=dados, verify=False)
        task_id = response.json().get("taskId")

        if not task_id:
            return None

        # Aguardar até que a tarefa seja concluída
        while True:
            dados = {
                "clientKey": api_key,
                "taskId": task_id
            }
            response = requests.post(url_get_result, json=dados, verify=False)
            resposta_json = response.json()

            if resposta_json.get("status") == 'ready':
                if resposta_json.get("errorId") == 0:
                    return resposta_json.get("solution", {}).get("text")
                else:
                    return None
            elif resposta_json.get("status") == 'processing':
                time.sleep(5)
            else:
                return None
        
    def hCaptcha_capmonster(self, api_key, site_key, page_url):
        capmonster = HCaptchaTask(api_key)
        #capmonster = HCaptchaTask("c04e07d104412a6aee9f17fd5ae82b96")
        task_id = capmonster.create_task(page_url, site_key)

        try:
            result = capmonster.join_task_result(task_id)
            return result.get("gRecaptchaResponse")

        except CapmonsterException as e:
            #print(f"Erro ao contornar o captcha: {e}")
            return None
        
    def reCaptchaV2_capmonster(self, api_key, site_key, page_url):
        try:
            client_options = ClientOptions(api_key=api_key)
            cap_monster_client = CapMonsterClient(options=client_options)

            async def solve_captcha():
                return await cap_monster_client.solve_captcha(recaptcha3request)

            recaptcha3request = RecaptchaV2ProxylessRequest(websiteUrl=page_url, websiteKey=site_key)

            return asyncio.run(solve_captcha())['gRecaptchaResponse']

        except Exception as e:
            return None
        
    def reCaptchaV3_capmonster(self, api_key, site_key, page_url):
        try:
            client_options = ClientOptions(api_key=api_key)
            cap_monster_client = CapMonsterClient(options=client_options)

            async def solve_captcha():
                return await cap_monster_client.solve_captcha(recaptcha3request)

            recaptcha3request = RecaptchaV3ProxylessRequest(websiteUrl=page_url, websiteKey=site_key)

            return asyncio.run(solve_captcha())['gRecaptchaResponse']

        except Exception as e:
            return None
        

    
    #  A P I  ~  2 C A P T C H A
        
    def reCaptchaV2_2captcha(self, api_key, site_key, page_url):
        endpoint = 'https://www.2captcha.com/in.php'
        response_url = 'https://www.2captcha.com/res.php'

        try:
            response = requests.post(endpoint, data={
                'key': api_key,
                'method': 'userrecaptcha',
                'googlekey': site_key,
                'pageurl': page_url,
                'version': 'v2',
                'action': 'verify'
            })

            if response.ok and '|' in response.text:
                captcha_id = response.text.split('|')[1]

                while True:
                    response = requests.get(response_url, params={
                        'key': api_key,
                        'action': 'get',
                        'id': captcha_id
                    })
                    
                    if response.ok:
                        if response.text.startswith('OK'):
                            response_data = response.text.split('|')[1:]
                            return response_data[0]
                        elif 'CAPCHA_NOT_READY' in response.text:
                            time.sleep(5)
                        else:
                            return None
                    else:
                        return None
            else:
                return None
        except requests.exceptions.RequestException as e:
            return None
        
    def reCaptchaV3_2captcha(self, api_key, site_key, page_url):
        endpoint = 'https://www.2captcha.com/in.php'
        response_url = 'https://www.2captcha.com/res.php'

        try:
            response = requests.post(endpoint, data={
                'key': api_key,
                'method': 'userrecaptcha',
                'googlekey': site_key,
                'pageurl': page_url,
                'version': 'v3',
                'action': 'verify',
                'min_score': '0.5'
                #'min_score': '0.3'
            })

            if response.ok and '|' in response.text:
                captcha_id = response.text.split('|')[1]

                while True:
                    response = requests.get(response_url, params={
                        'key': api_key,
                        'action': 'get',
                        'id': captcha_id
                    })
                    
                    if response.ok:
                        if response.text.startswith('OK'):
                            response_data = response.text.split('|')[1:]
                            return response_data[0]
                        elif 'CAPCHA_NOT_READY' in response.text:
                            time.sleep(5)
                        else:
                            return None
                    else:
                        return None
            else:
                return None
        except requests.exceptions.RequestException as e:
            return None
        
    def hCaptcha_2captcha(self, api_key, site_key, page_url):
            endpoint = 'https://www.2captcha.com/in.php'
            response_url = 'https://www.2captcha.com/res.php'

            try:
                response = requests.post(endpoint, data={
                    'key': api_key,
                    'method': 'hcaptcha',
                    'sitekey': site_key,
                    'pageurl': page_url,
                    'action': 'verify'
                })

                if response.ok and '|' in response.text:
                    captcha_id = response.text.split('|')[1]

                    while True:
                        response = requests.get(response_url, params={
                            'key': api_key,
                            'action': 'get',
                            'id': captcha_id
                        })
                        
                        if response.ok:
                            if response.text.startswith('OK'):
                                response_data = response.text.split('|')[1:]
                                return response_data[0]
                            elif 'CAPCHA_NOT_READY' in response.text:
                                time.sleep(5)
                            else:
                                return None
                        else:
                            return None
                else:
                    return None
            except requests.exceptions.RequestException as e:
                return None
