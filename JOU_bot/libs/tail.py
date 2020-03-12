#-*- coding=utf-8 -*-
import requests
import random
import string

async def get_tail():
    url="https://chp.shadiao.app/api.php"
    try:
        r=requests.get(url)
        return "\n————"+r.text
    except:
        return "\n————".join(random.sample(string.ascii_letters+string.digits,15))