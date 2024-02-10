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


# Exemplo de uso
opcao = int(input("""
    1 - Capmonster [reCaptcha V2]           5 - 2Captcha [reCaptcha V2]
    2 - Capmonster [reCaptcha V3]           6 - 2Captcha [reCaptcha V3]
    3 - Capmonster [hCaptcha]               7 - 2Captcha [hCaptcha]
    4 - Capmonster [captcha text]           
    
> """))

api_key_twoCaptcha = '85de0716493e6d30320ea9ca46cc6241'
api_key_capmonster = 'c04e07d104412a6aee9f17fd5ae82b96'

page_url = 'https://2captcha.com/demo/hcaptcha'

solver = CaptchaSolver()
if opcao == 1:
    site_key = '6LdFEWkkAAAAAJ3HaF3FziFMnBtf6eZ27q_mnzfn'
    page_url = 'https://www.bigcommerce.com/start-your-trial'
    bypass = solver.reCaptchaV2_capmonster(api_key_capmonster, site_key, page_url)
    print(bypass)

elif opcao == 2:
    site_key = '6LdFEWkkAAAAAJ3HaF3FziFMnBtf6eZ27q_mnzfn'
    page_url = 'https://www.bigcommerce.com/start-your-trial'
    bypass = solver.reCaptchaV3_capmonster(api_key_capmonster, site_key, page_url)
    print(bypass)

elif opcao == 3:
    site_key = 'f7de0da3-3303-44e8-ab48-fa32ff8ccc7b'
    page_url = 'https://2captcha.com/demo/hcaptcha'
    bypass = solver.hCaptcha_capmonster(api_key_capmonster, site_key, page_url)
    print(bypass)

elif opcao == 4:
    base64_body = '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'
    bypass = solver.captchaLetra_capmonster(api_key_capmonster, base64_body)
    print(bypass)

if opcao == 5:
    site_key = '6LdFEWkkAAAAAJ3HaF3FziFMnBtf6eZ27q_mnzfn'
    page_url = 'https://www.bigcommerce.com/start-your-trial'
    bypass = solver.reCaptchaV2_2captcha(api_key_twoCaptcha, site_key, page_url)
    print(bypass)

elif opcao == 6:
    site_key = '6LdFEWkkAAAAAJ3HaF3FziFMnBtf6eZ27q_mnzfn'
    page_url = 'https://www.bigcommerce.com/start-your-trial'
    bypass = solver.reCaptchaV3_2captcha(api_key_twoCaptcha, site_key, page_url)
    print(bypass)

elif opcao == 7:
    site_key = 'f7de0da3-3303-44e8-ab48-fa32ff8ccc7b'
    page_url = 'https://2captcha.com/demo/hcaptcha'
    bypass = solver.hCaptcha_2captcha(api_key_twoCaptcha, site_key, page_url)
    print(bypass)
