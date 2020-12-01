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

    return libvaasu.retrieve_attendance(sid, session_id)

for k, v in get_attendance(username, password).items():
    print(k, ' - ', v)
