import time
import requests

def solve_recaptcha_v3(api_key, site_key, page_url, min_score):
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
            'min_score': min_score
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
                        return response_data
                    elif 'CAPCHA_NOT_READY' in response.text:
                        time.sleep(5)
                    else:
                        return None
                else:
                    return None
        else:
            return None
    except requests.exceptions.RequestException as e:
        print('Erro na solicitação HTTP:', e)
        return None

# Exemplo de uso
api_key = 'YOUR_2CAPTCHA_API_KEY'
site_key = 'RECAPTCHA_SITE_KEY'
page_url = 'URL_DA_PÁGINA_ONDE_O_RECAPTCHA_ESTÁ'
min_score = 0.5

response_data = solve_recaptcha_v3(api_key, site_key, page_url, min_score)
if response_data:
    # Recaptcha resolvido com sucesso
    print('Resultado:', response_data)
else:
    # Erro ao resolver o recaptcha
    print('Erro ao resolver o reCAPTCHA V3')
