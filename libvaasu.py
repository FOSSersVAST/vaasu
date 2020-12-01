import requests
import json
import sqlite3
from cryptography.fernet import Fernet
import os

def create_table():
    conn = sqlite3.connect("Attendance.sqlite3")
    conn.execute('''CREATE TABLE IF NOT EXISTS CREDENTIALS
         (username  CHAR(30)  NOT NULL,
         password   CHAR(30)   NOT NULL,
         telegram_id    CHAR(30)    NOT NULL);''')

def check(telegram_id):
    conn = sqlite3.connect("Attendance.sqlite3")
    cur = conn.cursor()
    data = cur.execute("select * from CREDENTIALS where telegram_id=?",(telegram_id,))
    
    if data.fetchall() == []:
        conn.close()
        return True
    else:
        conn.close()
        return False

def delete_from_table(telegram_id):
    conn = sqlite3.connect("Attendance.sqlite3")
    cur = conn.cursor()
    cur.execute("delete from CREDENTIALS where telegram_id=?",(telegram_id,))
    conn.commit()

def add_student(username, password, telegram_id):
    conn = sqlite3.connect("Attendance.sqlite3")
    cur = conn.cursor()
    data = cur.execute("select * from CREDENTIALS where telegram_id=?",(telegram_id,))
    if data.fetchall() == []:
        passkey = os.getenv('passkey').encode()
        f = Fernet(passkey)
        password = f.encrypt(password.encode())
        cur.execute("INSERT INTO CREDENTIALS VALUES(?,?,?)",(username, password, telegram_id))
    else:
        conn.close()
        return False
    conn.commit()
    conn.close()
    return True

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


def retrieve_attendance(sid, session_id):
    # Gets args value
    url = "https://erp.vidyaacademy.ac.in/web/dataset/call_kw"
    payload = {"jsonrpc":"2.0","method":"call","params":{"model":"vict.academics.duty.leave.status","method":"create","args":[{}],"kwargs":{"context":{}},"session_id":session_id,"context":{}}}
    r = requests.post(url,data=json.dumps(payload),cookies={"sid":sid})
    args = r.json()["result"]


    url = "https://erp.vidyaacademy.ac.in/web/dataset/call_button"
    payload = {"jsonrpc":"2.0","method":"call","params":{"model":"vict.academics.duty.leave.status","method":"button_check_status","domain_id":"null","context_id":1,"args":[[args],{}],"session_id":session_id},"id":"r54"}
    r = requests.post(url,data=json.dumps(payload),cookies={"sid":sid})

    # Gets the subject id
    url = "https://erp.vidyaacademy.ac.in/web/dataset/call_kw"
    payload = {"jsonrpc":"2.0","method":"call","params":{"model":"vict.academics.duty.leave.status","method":"read","args":[[args],["atten_status"]],"kwargs":{"context":{}},"session_id":session_id,"context":{}}}
    r = requests.post(url,data=json.dumps(payload),cookies={"sid":sid})
    subs = r.json()["result"][0]["atten_status"]

    # Gets the attendance
    payload = {"jsonrpc":"2.0","method":"call","params":{"model":"vict.academics.duty.leave.status.lines","method":"read","args":[subs,["course","course_percentage"]],"kwargs":{"context":{}},"session_id":session_id,"context":{}}}
    r = requests.post(url,data=json.dumps(payload),cookies={"sid":sid})
    Attendance = {}
    for i in r.json()["result"]:
        Attendance[i["course"][1]] = i["course_percentage"]
    return Attendance


def get_attendance(telegram_id):

    telegram_id = (telegram_id,)
    conn = sqlite3.connect("Attendance.sqlite3")
    cur = conn.cursor()
    cur.execute("Select * from CREDENTIALS where telegram_id=?",telegram_id)
    data = cur.fetchall()
    try:
        username = data[0][0]
        password = data[0][1]
        passkey = os.getenv('passkey').encode()
        f = Fernet(passkey)
        password = f.decrypt(password).decode()
    except IndexError:
        conn.close()
        return False
    conn.close()

    # Gets the session id and sid
    erplogin = login(username, password)
    if (erplogin == 'wrong'):
        raise Exception('Password wrong')
    else:
        sid = erplogin[0]
        session_id = erplogin[1]

    return retrieve_attendance(sid, session_id)
