import requests
from bs4 import BeautifulSoup
from termcolor import colored
from configparser import RawConfigParser

def init(domain):
    subdomains = []

    print(colored("[*]-Searching Digger Tools...", "yellow"))

    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"}
    url = f"https://digger.tools/lookup/{domain}/subdomains"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        table_rows = soup.select("table tbody tr")
        for row in table_rows:
            domain_cell = row.select_one("td:first-child span")
            if domain_cell:
                subdomains.append(domain_cell.text.strip())

        subdomains = list(set(subdomains))
        print("  \\__ {0}: {1}".format(colored("Subdomains found", "cyan"), colored(len(subdomains), "yellow")))
        return subdomains

    except requests.exceptions.RequestException as err:
        print("  \\__", colored(err, "red"))
        return []

    except Exception as e:
        print("  \\__", colored(f"An unexpected error occurred: {e}", "red"))
        return []