import requests

host="visibility.amp.cisco.com"

username = "client-a0b1c2d3-e4f5-g6h7-i8j9-kalbmcndoepf"
password = "w-n-a0b1c2-d3e_4f5g6h7i8j9kalbmcndoepfq0r1-s2t3u4v5w6x7"

print(f"\n==> Request an Access Token from CTR")

url = f"https://{host}/iroh/oauth2/token"
headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'application/json'}
payload = 'grant_type=client_credentials'

try:
	response = requests.post(url, headers=headers, auth=(username, password), data=payload)
except:
	response.raise_for_status()

print(response.json()["access_token"])
