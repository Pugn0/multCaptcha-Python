try:    
    import os
    import re
    import time
    import uuid
    import base64
    import string
    import random
    import string
    import secrets
    import urllib3
    import requests
    import urllib.parse
    from requests.exceptions import ProxyError, ConnectionError
    from playwright.sync_api import sync_playwright
    from capmonster_python import RecaptchaV3Task
    from bs4 import BeautifulSoup
    
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
except Exception as e:
    print(f"PUGNO - {e}")
    exit()
capmonster_key = "c9123f96cfe19602dcfb8954b9ed20ba"
website_url = "https://sacola.magazineluiza.com.br"
website_key = "6LdZgd8nAAAAACORQAbrn5mzgAXTgwTmp3pSjPKe"

def create_task():
    response = requests.post('https://api.capmonster.cloud/createTask', verify= False, json={
        "clientKey": capmonster_key,
        "task": {
            "type": "RecaptchaV3TaskProxyless",
            "websiteURL": website_url,
            "websiteKey": website_key
        }
    })
    return response.json()['taskId']

def get_task_result(task_id):
    while True:
        response = requests.post('https://api.capmonster.cloud/getTaskResult', verify= False, json={
            "clientKey": capmonster_key,
            "taskId": task_id
        })
        result = response.json()
        if result['status'] == "ready":
            return result['solution']['gRecaptchaResponse']
        time.sleep(2)  # Espera 2 segundos antes de verificar novamente

def bypass_captcha():
    try:
        task_id = create_task()
        bypass = get_task_result(task_id)
        return bypass
    except Exception as error:
        print('Erro ao resolver CAPTCHA:', error)