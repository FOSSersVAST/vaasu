import sqlite3
from telegram import Bot
import os
import libvaasu

def auto_msg():
    bot = Bot(token=os.getenv('BOT_TOKEN'))
    conn = sqlite3.connect("Attendance.sqlite3")
    cur = conn.cursor()
    cur.execute("Select * from Credentials;")
    data = cur.fetchall()

    for i in data:
        Attendance = libvaasu.get_attendance(i[2])
        for k,v in Attendance.items():
            if(v<75):
                Message = "You have " + str(v) + " % attendance in " + k
                bot.send_message(chat_id=i[2],text=Message)
    conn.close()
auto_msg()
