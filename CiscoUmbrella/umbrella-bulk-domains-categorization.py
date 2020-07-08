import requests
import json

host="investigate.api.umbrella.com"
api_key = "a0b1c2d3-e4f5-g6h7-i8j9-kalbmcndoepf"
domains = "[\"internetbadguys.com\", \"cisco.com\",\"example.com\"]"

print(f"\n==> Checking multiple domains against Umbrella Investigate to retreive categorization")

url = f"https://{host}/domains/categorization?showLabels"
headers = {'Authorization':'Bearer ' + api_key, 'Content-Type': 'application/json'}

try:
	response = requests.post(url, data=domains, headers=headers)
except:
	response.raise_for_status()

print(str(domains))
print (response.json())