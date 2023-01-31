import datetime
import sqlite3

# birthday = input('Please enter your birthday(YYYY/MM/DD): ')
# birthdate = datetime.datetime.strptime(birthday,'%Y-%M-%d')
# currentDate = datetime.datetime.today()

# days = birthdate - currentDate


username='Sudo'
conn = sqlite3.connect('bd.sqlite')
cur = conn.execute("SELECT updated_passwd_date, username, date FROM user WHERE username = ?;", (username,))
updated_passwd_date, username, date = cur.fetchone()
print(updated_passwd_date)
print(type(updated_passwd_date))

print(username)
print(date)
current_date = datetime.datetime.today()
print(current_date)
updated_passwd_date = datetime.datetime.strptime(updated_passwd_date,'%Y-%m-%d %H:%M:%S.%f')
print(type(updated_passwd_date))
print(type(current_date))
expiration_passwd_check = current_date - updated_passwd_date
print(expiration_passwd_check)


