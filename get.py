import requests
import json

username = input("Enter the username: ")
password = input("Enter the password: ")

#Gets the session id and sid
url = "https://erp.vidyaacademy.ac.in/web/session/authenticate"
payload = {"jsonrpc":"2.0","method":"call","params":{"db":"liveone","login":username,"password":password,"base_location":"https://erp.vidyaacademy.ac.in","context":{}},"id":"r7"}
headers = {'user-agent': "Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0"}
r = requests.post(url,data=json.dumps(payload))
sid = r.cookies.get_dict()["sid"]
session_id = r.json()["result"]["session_id"]

#Gets args value
url = "https://erp.vidyaacademy.ac.in/web/dataset/call_kw"
payload = {"jsonrpc":"2.0","method":"call","params":{"model":"vict.academics.duty.leave.status","method":"create","args":[{}],"kwargs":{"context":{}},"session_id":session_id,"context":{}}}
r = requests.post(url,data=json.dumps(payload),cookies={"sid":sid})
args = r.json()["result"]

#Clicks the button
url = "https://erp.vidyaacademy.ac.in/web/dataset/call_button"
payload = {"jsonrpc":"2.0","method":"call","params":{"model":"vict.academics.duty.leave.status","method":"button_check_status","domain_id":"null","context_id":1,"args":[[args],{}],"session_id":session_id},"id":"r54"}
r = requests.post(url,data=json.dumps(payload),cookies={"sid":sid})


#Gets the subject id
url = "https://erp.vidyaacademy.ac.in/web/dataset/call_kw"
payload = {"jsonrpc":"2.0","method":"call","params":{"model":"vict.academics.duty.leave.status","method":"read","args":[[args],["atten_status"]],"kwargs":{"context":{}},"session_id":session_id,"context":{}}}
r = requests.post(url,data=json.dumps(payload),cookies={"sid":sid})
subs = r.json()["result"][0]["atten_status"]



#Gets the attendence
payload = {"jsonrpc":"2.0","method":"call","params":{"model":"vict.academics.duty.leave.status.lines","method":"read","args":[subs,["course","course_percentage"]],"kwargs":{"context":{}},"session_id":session_id,"context":{}}}
headers = {'user-agent': "Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0"}
r = requests.post(url,data=json.dumps(payload),cookies={"sid":sid})
for i in r.json()["result"]:
    print(i["course"][1], " : ", i["course_percentage"])
