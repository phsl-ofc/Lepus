import requests
from bs4 import BeautifulSoup
from termcolor import colored

def init(domain):
    DNSD = []
    session = requests.Session()

    print(colored("[*]-Searching DNSDumpster...", "yellow"))

    try:

        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'max-age=0',
            'referer': 'https://dnsdumpster.com/',
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

        response = session.get('https://dnsdumpster.com/', headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        form = soup.find('form', {'data-form-id': 'mainform'})
        if not form or not form.has_attr('hx-headers'):
            print(colored("[!] Failed to retrieve Authorization token.", "red"))
            return []

        hx_headers = form['hx-headers']
        auth_token = eval(hx_headers).get("Authorization")
        if not auth_token:
            print(colored("[!] Authorization token not found.", "red"))
            return []
        headers.update({
            'Authorization': auth_token,
            'Content-Type': 'application/x-www-form-urlencoded',
            'HX-Current-URL': 'https://dnsdumpster.com/',
            'HX-Request': 'true',
            'HX-Target': 'results',
            'Origin': 'https://dnsdumpster.com',
        })

        data = {
            'target': domain,
        }
        response = session.post('https://api.dnsdumpster.com/htmld/', headers=headers, data=data)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', {'id': 'a_rec_table'})
        if table:
            rows = table.find('tbody').find_all('tr')
            for row in rows:
                columns = row.find_all('td')
                if columns:
                    subdomain = columns[0].text.strip()
                    if subdomain:
                        DNSD.append(subdomain)

        print("  \\__ {0}: {1}".format(colored("Subdomains found", "cyan"), colored(len(DNSD), "yellow")))
        return DNSD

    except requests.exceptions.RequestException as err:
        print("  \\__", colored(err, "red"))
        return []

    except Exception as e:
        print("  \\__", colored(f"Something went wrong! Error: {e}", "red"))
        return []
