import requests
import json


def login(username, password):
    username = username.upper()
    # Gets the session id and sid
    url = "https://erp.vidyaacademy.ac.in/web/session/authenticate"
    payload = {"jsonrpc":"2.0","method":"call","params":{"db":"liveone","login":username,"password":password,"base_location":"https://erp.vidyaacademy.ac.in","context":{}},"id":"r7"}
    headers = {'user-agent': "Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0"}
    r = requests.post(url,data=json.dumps(payload))
    result = r.json()

    if result['result']['uid'] is False:
        return 'wrong'
    else:
        sid = r.cookies.get_dict()["sid"]
        session_id = result["result"]["session_id"]

        return sid, session_id
