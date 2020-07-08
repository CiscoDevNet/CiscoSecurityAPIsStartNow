import requests
import json

host = "s-platform.api.opendns.com"
api_key = "a0b1c2d3-e4f5-g6h7-i8j9-kalbmcndoepf"

print(f"\n==> Finding all of the domains in a custom enforcement list")

url = f"https://{host}/1.0/domains?customerKey={api_key}"
headers = {'Authorization':'Bearer ' + api_key}

try:
	response = requests.get(url, headers=headers)
except:
	response.raise_for_status()

print (response.json())