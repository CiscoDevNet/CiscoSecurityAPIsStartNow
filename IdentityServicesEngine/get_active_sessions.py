import requests
import xml.dom.minidom

try:
    requests.packages.urllib3.disable_warnings()
except:
    pass

hostname = "198.18.133.27"
username = "admin"
password = "C1sco12345"

print(f"\n==> Prints all active sessions in formatted XML")

if __name__ == "__main__":

    url = f"https://{hostname}/admin/API/mnt/Session/ActiveList"

    try:
        response = requests.request("GET", url, auth=(username,password), verify=False)
    except:
        response.raise_for_status()

    raw = xml.dom.minidom.parseString(response.text)
    print (raw.toprettyxml())

