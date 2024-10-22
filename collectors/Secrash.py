import requests
from urllib.parse import quote
from termcolor import colored

def init(domain):
    SCRASH = []

    print(colored("[*]-Searching Secrash.com...", "yellow"))

    url = "https://api.hackertarget.com/hostsearch/"
    headers = {
        'accept': '*/*',
        'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'origin': 'https://www.secrash.com',
        'priority': 'u=1, i',
        'referer': 'https://www.secrash.com/',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Opera GX";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 OPR/114.0.0.0 (Edition std-2)',
    }
    params = {
        'q': domain,
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.ok:
            results = response.text.strip().split('\n')
            for result in results:
                subdomain = result.split(',')[0]
                SCRASH.append(subdomain.strip())

            print("  \\\__ {0}: {1}".format(colored("Subdomains found", "cyan"), colored(len(SCRASH), "yellow")))
            return SCRASH
        else:
            print("  \\\__", colored("Failed to retrieve data!", "red"))
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