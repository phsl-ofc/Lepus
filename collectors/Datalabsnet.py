import requests
import json
from bs4 import BeautifulSoup
from termcolor import colored
from configparser import RawConfigParser

def init(domain):
    parser = RawConfigParser()
    parser.read("config.ini")
    proxy_status = parser.get('ProxyServer', 'PROXY_STATUS')
    proxy_server = parser.get('ProxyServer', 'PROXY_SERVER')
    proxy_port = parser.get('ProxyServer', 'PROXY_PORT')
    proxy_user = parser.get('ProxyServer', 'PROXY_USER')
    proxy_password = parser.get('ProxyServer', 'PROXY_PASSWORD')

    if proxy_status:
        if proxy_user and proxy_password:
            proxy_url = f"http://{proxy_user}:{proxy_password}@{proxy_server}:{proxy_port}"
        else:
            proxy_url = f"http://{proxy_server}:{proxy_port}"
		    
    proxies = {"http": proxy_url, "https": proxy_url}
    subdomains = []

    print(colored("[*]-Searching Datalabs...", "yellow"))

    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"}
    url = f"https://datalabs.net/tools/subdomainfinder"

    try:
        session = requests.session()
        if proxy_status:
            response = session.get(url, headers=headers, proxies=proxies)
        else:
            response = session.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        csrf_meta = soup.find('meta', {'name': 'csrf'})
        if csrf_meta:
            csrf_token = csrf_meta.get('content')
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'max-age=0',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://datalabs.net',
            'priority': 'u=0, i',
            'referer': 'https://datalabs.net/tools/subdomainfinder',
            'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Opera GX";v="114"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 OPR/114.0.0.0 (Edition std-2)',
        }
        data = {
            'Params[domain]': domain,
            'csrf': csrf_token,
        }
        if proxy_status:
            response = session.post('https://datalabs.net/tools/subdomainfinder', headers=headers, data=data, proxies=proxies)
        else:
            response = session.post('https://datalabs.net/tools/subdomainfinder', headers=headers, data=data)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        textarea = soup.find('textarea', {'class': 'form-control', 'readonly': True})
        if not textarea:
            return []
        json_data = textarea.text.strip()
        data = json.loads(json_data)
        subdomains = [item['subdomain'] for item in data.get('subdomains', [])]
        subdomains = list(set(subdomains))
        print("  \\__ {0}: {1}".format(colored("Subdomains found", "cyan"), colored(len(subdomains), "yellow")))
        return subdomains

    except requests.exceptions.RequestException as err:
        print("  \\__", colored(err, "red"))
        return []

    except Exception as e:
        print("  \\__", colored(f"An unexpected error occurred: {e}", "red"))
        return []