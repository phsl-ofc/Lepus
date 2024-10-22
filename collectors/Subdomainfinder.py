import requests
from urllib.parse import quote
from termcolor import colored
from bs4 import BeautifulSoup

def init(domain):
    SUBFINDER = []

    print(colored("[*]-Searching Subdomainfinder.io...", "yellow"))

    url = "https://subdomainfinder.io/"
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://subdomainfinder.io',
        'priority': 'u=0, i',
        'referer': 'https://subdomainfinder.io/',
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
        'domain': domain,
        'scan': '',
    }
    try:
        response = requests.post(url, headers=headers, data=data).text
        soup = BeautifulSoup(response, 'html.parser')
        table = soup.find('table', {'class': 'table table-striped text-white'})

        if table:
            rows = table.find('tbody').find_all('tr')
            for row in rows:
                columns = row.find_all('td')
                if len(columns) >= 2:
                    subdomain = columns[0].get_text(strip=True)
                    SUBFINDER.append((subdomain))

            print("  \\\__ {0}: {1}".format(colored("Subdomains found", "cyan"), colored(len(SUBFINDER), "yellow")))
            return SUBFINDER
        else:
            print("  \\\__", colored("No table found!", "red"))
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