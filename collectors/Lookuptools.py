import requests
from bs4 import BeautifulSoup
from termcolor import colored


def init(domain):
    subdomains = []

    print(colored("[*]-Searching Lookups Tools...", "yellow"))

    headers = {
        'accept': '*/*',
        'referer': 'https://lookup.tools/subdomain',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 OPR/114.0.0.0 (Edition std-2)'
    }
    url = f"https://lookup.tools/subdomain/{domain}?_rsc=14ll"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        table = soup.find('table', {'class': 'w-full caption-bottom text-sm'})
        if table:
            rows = table.find_all('tr')[1:]
            for row in rows:
                columns = row.find_all('td')
                if columns:
                    subdomain = columns[0].text.strip()
                    subdomains.append(subdomain)

        if subdomains:
            subdomains = list(set(subdomains))
            print("  \\__ {0}: {1}".format(colored("Subdomains found", "cyan"), colored(len(subdomains), "yellow")))
        else:
            print("  \\__", colored("No subdomains found.", "red"))

        return subdomains

    except requests.exceptions.RequestException as err:
        print("  \\__", colored(f"HTTP Request Error: {err}", "red"))
        return []

    except Exception as e:
        print("  \\__", colored(f"An unexpected error occurred: {e}", "red"))
        return []