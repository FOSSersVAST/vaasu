import requests
import json
import libvaasu


username = input("Enter the username: ").upper()
password = input("Enter the password: ")

def get_attendance(username, password):

    #Gets the session id and sid
    login = libvaasu.login(username, password)
    if (login == 'wrong'):
        print('Username or password wrong')
        raise Exception('Password wrong')
    else:
        sid = login[0]
        session_id = login[1]

    #Gets args value
    url = "https://erp.vidyaacademy.ac.in/web/dataset/call_kw"
    payload = {"jsonrpc":"2.0","method":"call","params":{"model":"vict.academics.duty.leave.status","method":"create","args":[{}],"kwargs":{"context":{}},"session_id":session_id,"context":{}}}
    r = requests.post(url,data=json.dumps(payload),cookies={"sid":sid})
    args = r.json()["result"]


    url = "https://erp.vidyaacademy.ac.in/web/dataset/call_button"
    payload = {"jsonrpc":"2.0","method":"call","params":{"model":"vict.academics.duty.leave.status","method":"button_check_status","domain_id":"null","context_id":1,"args":[[args],{}],"session_id":session_id},"id":"r54"}
    r = requests.post(url,data=json.dumps(payload),cookies={"sid":sid})
    #print(r.json())

    #Gets the subject id
    url = "https://erp.vidyaacademy.ac.in/web/dataset/call_kw"
    payload = {"jsonrpc":"2.0","method":"call","params":{"model":"vict.academics.duty.leave.status","method":"read","args":[[args],["atten_status"]],"kwargs":{"context":{}},"session_id":session_id,"context":{}}}
    r = requests.post(url,data=json.dumps(payload),cookies={"sid":sid})
    subs = r.json()["result"][0]["atten_status"]
    #print(subs)





    #Gets the attendance
    payload = {"jsonrpc":"2.0","method":"call","params":{"model":"vict.academics.duty.leave.status.lines","method":"read","args":[subs,["course","course_percentage"]],"kwargs":{"context":{}},"session_id":session_id,"context":{}}}
    headers = {'user-agent': "Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0"}
    r = requests.post(url,data=json.dumps(payload),cookies={"sid":sid})
    Attendance = {}
    for i in r.json()["result"]:
        Attendance[i["course"][1]] = i["course_percentage"]
    return Attendance


for k, v in get_attendance(username, password).items():
    print(k, ' - ', v)
