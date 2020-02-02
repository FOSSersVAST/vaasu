import sqlite3


# A simple stats count
conn = sqlite3.connect("Attendance.sqlite3")
cur = conn.cursor()
data = cur.execute("select COUNT(username) from CREDENTIALS")
print(data.fetchall())

data = cur.execute("select username from CREDENTIALS")
print(data.fetchall())