import requests
from re import findall
from json import loads
from termcolor import colored
from configparser import RawConfigParser


def init(domain):
	ST = []

	print(colored("[*]-Searching SecurityTrails...", "yellow"))

	parser = RawConfigParser()
	parser.read("config.ini")
	SECURITYTRAILS_API_KEY = parser.get("SecurityTrails", "SECURITYTRAILS_API_KEY")

	if SECURITYTRAILS_API_KEY == "":
		print("  \\__", colored("No SecurityTrails API key configured", "red"))
		return []

	else:
		headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0", "APIKEY": SECURITYTRAILS_API_KEY}
		url = "https://api.securitytrails.com/v1/domain/{0}/subdomains".format(domain)

		try:
			response = requests.get(url, headers=headers)

			if response.status_code == 429:
				print("  \\__", colored("You've exceeded the usage limits for your account.", "red"))
				return []

			results = loads(response.text)["subdomains"]
			
			if results:
				for result in results:
					ST.append("{0}.{1}".format(result, domain))
				ST = set(ST)

			print("  \\__ {0}: {1}".format(colored("Subdomains found", "cyan"), colored(len(ST), "yellow")))
			return ST

		except requests.exceptions.RequestException as err:
			print("  \\__", colored(err, "red"))
			return []

		except requests.exceptions.HTTPError as errh:
			print("  \\__", colored(errh, "red"))
			return []

		except requests.exceptions.ConnectionError as errc:
			print("  \\__", colored(errc, "red"))
			return []

		except requests.exceptions.Timeout as errt:
			print("  \\__", colored(errt, "red"))
			return []
		
		except Exception:
			print("  \\__", colored("Something went wrong!", "red"))
			return []