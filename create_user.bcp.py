import getpass
import hashlib

def create(conn):
    cur = conn.cursor()
    rep=input("Do you want to create a user ? Y/N : ")
    i=0
    while(rep.lower() == "y"):
        if i<5:
            print("USER CREATION\n")
            username = input("username : ")
            
            cur.execute("SELECT first_name FROM user WHERE username = ?", (username,))
            data = cur.fetchall()
            
            if len(data) != 0:
                print("username", username, "already exist !")
                i+=1
                if i==5:
                    print("Too many tries")
                    break
                else:
                    continue
            else:
                fname = input("First name : ")
                sname = input("Second name : ")
                password_check=False
                count=0
                while password_check==False and count<5:
                    print()
                    print("New password")
                    pwd = getpass.getpass()
                    pwd = hashlib.sha256(pwd.encode('utf-8')).hexdigest()
                    #print(pwd)
                    print ("Confirmation of password")
                    pwd2 = getpass.getpass()
                    pwd2 = hashlib.sha256(pwd2.encode('utf-8')).hexdigest()
                    #print(pwd)
                    if pwd==pwd2:
                        password_check=True
                        resp=input("Add this user in the db ? Y/N : ")
                        if resp.lower() == 'y':
                            cur.execute("INSERT INTO user VALUES(NULL,?,?,?,?)", (username, fname, sname, pwd))
                            conn.commit()
                            print("USER ADD\n")
                            for row in cur.execute("SELECT * FROM user"):
                                print(row)
                            i=0
                        else:
                            i=0
                        rep=input("Do you want to create another user ? Y/N : ")
                    else:
                        count+=1
                        print("Incorrect password")
                        print()
                    if count==5:
                        print('Too many tries')
                        i=5
                        rep='N'
                        


        
