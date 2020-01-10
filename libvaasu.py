import requests
import json
import sqlite3


def create_table(conn):
    conn.execute('''CREATE TABLE IF NOT EXISTS CREDENTIALS 
         (username  CHAR(30)  NOT NULL,
         password   CHAR(30)   NOT NULL
         telegram_id    CHAR(30)    NOT NULL);''')

def add_student(username, password, telegram_id):
    conn = sqlite3.connect("Attendance.sqlite3")
    create_table(conn)
    cur = conn.cursor()
    cur.execute("INSERT INTO CREDENTIALS VALUES(?,?,?)",(username, password, telegram_id))
    conn.commit()
    conn.close()

def login(username, password):
    username = username.upper()
    # Gets the session id and sid
    url = "https://erp.vidyaacademy.ac.in/web/session/authenticate"
    payload = {"jsonrpc":"2.0","method":"call","params":{"db":"liveone","login":username,"password":password,"base_location":"https://erp.vidyaacademy.ac.in","context":{}},"id":"r7"}
    r = requests.post(url,data=json.dumps(payload))
    result = r.json()

    if result['result']['uid'] is False:
        return 'wrong'
    else:
        sid = r.cookies.get_dict()["sid"]
        session_id = result["result"]["session_id"]

        return sid, session_id


def get_attendance(username, password):

    #Gets the session id and sid
    login = login(username, password)
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

    #Gets the subject id
    url = "https://erp.vidyaacademy.ac.in/web/dataset/call_kw"
    payload = {"jsonrpc":"2.0","method":"call","params":{"model":"vict.academics.duty.leave.status","method":"read","args":[[args],["atten_status"]],"kwargs":{"context":{}},"session_id":session_id,"context":{}}}
    r = requests.post(url,data=json.dumps(payload),cookies={"sid":sid})
    subs = r.json()["result"][0]["atten_status"]

    #Gets the attendance
    payload = {"jsonrpc":"2.0","method":"call","params":{"model":"vict.academics.duty.leave.status.lines","method":"read","args":[subs,["course","course_percentage"]],"kwargs":{"context":{}},"session_id":session_id,"context":{}}}
    r = requests.post(url,data=json.dumps(payload),cookies={"sid":sid})
    Attendance = {}
    for i in r.json()["result"]:
        Attendance[i["course"][1]] = i["course_percentage"]
    return Attendance