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
