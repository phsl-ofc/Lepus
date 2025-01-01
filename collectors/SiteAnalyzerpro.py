import requests
from termcolor import colored
from configparser import RawConfigParser

def init(domain):
    subdomains = []
    print(colored("[*]-Searching Site-Analyzer.pro...", "yellow"))
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"}
    url = f"https://site-analyzer.pro/pages/services-seo/site-all-subdomains/search.php?url={domain}"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        res = data.get("json", {}).get("res", {})
        for subdomain in res.keys():
            if "translate.google" not in subdomain:
                subdomains.append(subdomain)

        subdomains = list(set(subdomains))
        print("  \\__ {0}: {1}".format(colored("Subdomains found", "cyan"), colored(len(subdomains), "yellow")))
        return subdomains

    except requests.exceptions.RequestException as err:
        print("  \\__", colored(err, "red"))
        return []

    except Exception as e:
        print("  \\__", colored(f"An unexpected error occurred: {e}", "red"))
        return []