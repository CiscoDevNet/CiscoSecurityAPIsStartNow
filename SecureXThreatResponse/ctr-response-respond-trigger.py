import requests

host = "visibility.amp.cisco.com"

username = "client-a0b1c2d3-e4f5-g6h7-i8j9-kalbmcndoepf"
password = "w-n-a0b1c2-d3e_4f5g6h7i8j9kalbmcndoepfq0r1-s2t3u4v5w6x7"
ctr_observables = "[{ \"value\": \"b1380fd95bc5c0729738dcda2696aa0a7c6ee97a93d992931ce717a0df523967\", \"type\": \"sha256\" }]"

print(f"\n==> Creating CTR Response Trigger for Observables")

def get_ctr_token(host, username, password):
	url = f"https://{host}/iroh/oauth2/token"
	headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'application/json'}
	payload = 'grant_type=client_credentials'
	try:
		response = requests.post(url, headers=headers, auth=(username, password), data=payload)
	except:
		response.raise_for_status()

	return(response.json()["access_token"])

def get_ctr_response_url(token):
	url = f"https://{host}/iroh/iroh-response/respond/observables"
	headers = {'Content-Type': 'application/json',
						 'Accept': '*/*',
						 'Authorization': 'Bearer ' + token}
	payload = ctr_observables
	
	response = requests.post(url, headers=headers, data = payload)
	return (response.json()["data"][0]["url"])

if __name__ == "__main__":

	token = get_ctr_token(host, username, password)
	response_url = get_ctr_response_url(token)

	url = f"https://{host}/iroh/iroh-response/{response_url}"
	headers = {'Content-Type': 'application/json',
						 'Accept': '*/*',
						 'Authorization': 'Bearer ' + token}
	
	response = requests.post(url, headers=headers)
	print(response.json())
