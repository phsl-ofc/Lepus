import requests
from urllib.parse import quote
from termcolor import colored
from bs4 import BeautifulSoup

def init(domain):
    PRINSH = []

    print(colored("[*]-Searching Prinsh.com...", "yellow"))

    url = "https://tools.prinsh.com/home/"
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://tools.prinsh.com',
        'priority': 'u=0, i',
        'referer': 'https://tools.prinsh.com/home/?tools=Subdofinder',
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
    params = {
        'tools': 'Subdofinder',
    }
    data = {
        'url': domain,
        'go': 'Go',
    }
    
    try:
        response = requests.post(url, params=params, headers=headers, data=data).text
        soup = BeautifulSoup(response, 'html.parser')
        textarea = soup.find('textarea', {'name': 'subdo'})
        if textarea:
            subdomains = textarea.get_text(strip=True).splitlines()
            for subdomain in subdomains:
                PRINSH.append(subdomain.strip())
            print("  \\\__ {0}: {1}".format(colored("Subdomains found", "cyan"), colored(len(PRINSH), "yellow")))
            return PRINSH
        else:
            print("  \\\__", colored("No textarea found!", "red"))
            return []
    except requests.exceptions.RequestException as err:
        print("  \\\__", colored(err, "red"))
        return []
    except requests.exceptions.ConnectionError as errc:
        print("  \\\__", colored(errc, "red"))
        return []
    except requests.exceptions.Timeout as errt:
        print("  \\\__", colored(errt, "red"))
        return []
    except Exception as e:
        print("  \\\__", colored(f"Something went wrong! {str(e)}", "red"))
        return []