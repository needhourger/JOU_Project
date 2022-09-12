import json
import requests

URL = "https://saying.api.azwcl.com/saying/get"


def getSaying():
    ret = "null"
    r = requests.get(URL)
    # print(r.text)
    try:
        data = json.loads(r.text)
        # print(data)
        if data.get("code") == 200:
            return data.get("data",{}).get("content",ret)
    except Exception as e:
        print(e)
    return ret

print(getSaying())
