import requests
import json
import libvaasu

username = input("Enter the Username: ").upper()
password = input("Enter the Password: ")

def get_attendance(username, password):
    #Gets the session id and sid
    login = libvaasu.login(username, password)
    if (login == 'wrong'):
        print('Username or password is wrong!')
        #raise Exception('Password wrong')
    else:
        sid = login[0]
        session_id = login[1]

    #Gets args value
    url = "https://erp.vidyaacademy.ac.in/web/dataset/call_kw"
    payload = {"jsonrpc":"2.0","method":"call","params":{"model":"vict.academics.duty.leave.status","method":"create","args":[{}],"kwargs":{"context":{}},"session_id":session_id,"context":{}}}
    req = requests.post(url,data=json.dumps(payload),cookies={"sid":sid})
    args = req.json()["result"]

    #Getting all attendance
    url = "https://erp.vidyaacademy.ac.in/web/dataset/call_button"
    payload = {"jsonrpc":"2.0","method":"call","params":{"model":"vict.academics.duty.leave.status","method":"button_check_status","domain_id":"null","context_id":1,"args":[[args],{}],"session_id":session_id},"id":"r54"}
    req = requests.post(url,data=json.dumps(payload),cookies={"sid":sid})
    #print(req.json())

    #Gets the subject id
    url = "https://erp.vidyaacademy.ac.in/web/dataset/call_kw"
    payload = {"jsonrpc":"2.0","method":"call","params":{"model":"vict.academics.duty.leave.status","method":"read","args":[[args],["atten_status"]],"kwargs":{"context":{}},"session_id":session_id,"context":{}}}
    req = requests.post(url,data=json.dumps(payload),cookies={"sid":sid})
    subjects = req.json()["result"][0]["atten_status"]
    #print(subjects)

    #Gets the attendance for each subject
    payload = {"jsonrpc":"2.0","method":"call","params":{"model":"vict.academics.duty.leave.status.lines","method":"read","args":[subs,["course","course_percentage"]],"kwargs":{"context":{}},"session_id":session_id,"context":{}}}
    headers = {'user-agent': "Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0"}
    req = requests.post(url,data=json.dumps(payload),cookies={"sid":sid})
    attendance = {}
    for i in req.json()["result"]:
        attendance[i["course"][1]] = i["course_percentage"]
    return attendance

for k, v in get_attendance(username, password).items():
    print(k, ' - ', v)
