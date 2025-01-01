import requests
from termcolor import colored
from configparser import RawConfigParser
from threading import Thread
from queue import Queue
import os

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

    brute_force_status = parser.get('BruteForceWordlist', 'BRUTE_FORCE_WORD_LIST_STATUS')
    brute_force_level = parser.get('BruteForceWordlist', 'BRUTE_FORCE_WORD_LIST_LEVEL')
    brute_force_timeout = int(parser.get('BruteForceWordlist', 'BRUTE_FORCE_WORD_LIST_TIME_OUT'))
    brute_force_thread = int(parser.get('BruteForceWordlist', 'BRUTE_FORCE_WORD_LIST_THREAD'))

    if brute_force_status.lower() != "true" or brute_force_level == "":
        print(colored("[*] Searching Wordlist brute force...", "yellow"))
        print("  \\__", colored("Wordlist brute force disabled", "red"))
        return []

    results = []
    print(colored("[*] Searching Wordlist brute force...", "yellow"))

    folder = "lists"
    wordlist_path = None
    for file in os.listdir(folder):
        if f"n0kovo_subdomains_{brute_force_level}.txt" in file:
            wordlist_path = os.path.join(folder, file)
            break

    if not wordlist_path:
        print(colored(f"[!] Wordlist level '{brute_force_level}' not found.", "red"))
        return []

    print(colored(f"[+] Using wordlist: {wordlist_path}", "cyan"))

    with open(wordlist_path, "r") as file:
        subdomains = [line.strip() for line in file.readlines()]

    print(colored(f"[+] Loaded {len(subdomains)} subdomains from wordlist.", "cyan"))

    queue = Queue()
    for subdomain in subdomains:
        queue.put(subdomain)

    def worker():
        while not queue.empty():
            subdomain = queue.get()
            url = f"http://{subdomain}.{domain}"
            try:
                if proxy_status:
                    response = requests.head(url, timeout=brute_force_timeout, proxies=proxies)
                else:
                    response = requests.head(url, timeout=brute_force_timeout)
                if response.status_code in range(100, 600):
                    results.append(f"{subdomain}.{domain}")
                    print(colored(f"[+] Found: {url} [Status: {response.status_code}]", "green"))
                else:
                    print(colored(f"[-] Not Found: {url}", "red"))
            except requests.RequestException as e:
                print(colored(f"[!] Error for {url}: {str(e)}", "red"))
            finally:
                queue.task_done()

    threads = []
    for _ in range(brute_force_thread):
        thread = Thread(target=worker)
        threads.append(thread)
        thread.start()

    queue.join()
    for thread in threads:
        thread.join()

    print(colored(f"[+] Total subdomains found: {len(results)}", "yellow"))
    return results