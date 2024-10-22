import requests
from termcolor import colored
from bs4 import BeautifulSoup

def init(domain):
    DNSHISTORY = []

    print(colored("[*]-Searching Dnshistory.org...", "yellow"))

    url = f"https://dnshistory.org/subdomains/1/{domain}"
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        'priority': 'u=0, i',
        'referer': f'https://dnshistory.org/dns-records/{domain}',
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
    
    try:
        response = requests.get(url, headers=headers)
        if response.ok:
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.select('#mainarea a')
            for link in links:
                subdomain = link.get_text(strip=True)
                DNSHISTORY.append(subdomain)

            print("  \\\__ {0}: {1}".format(colored("Subdomains found", "cyan"), colored(len(DNSHISTORY), "yellow")))
            return DNSHISTORY
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