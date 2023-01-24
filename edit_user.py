import getpass
import hashlib

def edit(conn): 
    '''
    edit : editer un utilisateur : modifier son username, first name, last name ou password
    conn : connexion sqlite3
    '''
    #TODO : gerer les status.
    cur = conn.cursor()

    data=input("Do you want to see user table ? : Y/N  ") #afficher la table
    if data.lower()=='y':
        for row in cur.execute("SELECT user_id, username, first_name, last_name, status FROM user"):
            print(row)
    print()
    print("EDIT A USER")
    print("Which user do you want to modify ?")

    username=input("Username : ")   
    req = cur.execute("SELECT * FROM user WHERE username = ?", (username,)) #requete sql permettant de retrouver la ligne correspondant au username dans la bd
    resSql = req.fetchall()
    if len(resSql) != 0 and username!='Admin':
        element=None
        while element!='5':

                print()

                print("Actions you can do for", username, ":")
                print ("1 - Edit Username")
                print ("2 - Edit First Name")
                print ("3 - Edit Last Name")
                print ("4 - Edit Password")
                print ("5 - Exit")
                element=input("Choose your action : ")

                match element:
                    case '1' :
                        i=0
                        while i<3:
                            newUsername=input("New Username : ")
                            cur.execute("SELECT username FROM user WHERE username = ?", (newUsername,))
                            data = cur.fetchall()
                            if len(data) != 0:
                                print("username", newUsername, "already exist !\n")
                                i+=1
                                if i==3:
                                    print("Too many tries : EXIT")
                                    element='5'
                            else:
                                resp=input("Add this username in the db ? Y/N : ")
                                if resp.lower() == 'y':
                                    cur.execute("UPDATE user SET username = ? WHERE username = ?;", (newUsername, username))
                                    conn.commit()
                                    print("Modification add \n")
                                    i=3
                                    test=input("Other changes ? : Y/N  ")
                                    if test.lower()=='y':
                                        i=3
                                else:
                                    for row in cur.execute("SELECT * FROM user"):
                                        print(row)
                                    element='5'
                                    i=3
                    case '2' :
                        i=0
                        while i<3:
                            newFirstName=input("New First Name : ")
                            resp=input("Add this first name in the db ? Y/N : ")
                            if resp.lower() == 'y':
                                cur.execute("UPDATE user SET first_name = ? WHERE username = ?;", (newFirstName, username))
                                conn.commit()
                                test=input("Other changes ? : Y/N  ")
                                i=3
                                if test.lower()=='y':
                                    i=3
                                else:
                                    for row in cur.execute("SELECT * FROM user"):
                                        print(row)
                                    element='5'
                            else:
                                i+=1
                                    
                    case '3' :
                        i=0
                        while i<3:
                            newLastName=input("New Last Name : ")
                            resp=input("Add this last name in the db ? Y/N : ")
                            if resp.lower() == 'y': 
                                cur.execute("UPDATE user SET last_name = ? WHERE username = ?;", (newLastName, username))
                                conn.commit()                         
                                test=input("Other changes ? : Y/N  ")
                                i=3
                                if test.lower()=='y':
                                    i=3
                                else:
                                    for row in cur.execute("SELECT * FROM user"):
                                        print(row)
                                    element='5'
                            else:
                                i+=1
                    case '4' :
                        rep=input("Reset password? Y/N :  ")
                        if rep.lower()=='y':
                            i=0
                            pwd_check=False
                            while pwd_check==False:
                                newPassword=getpass.getpass()
                                newPassword=hashlib.sha256(newPassword.encode('utf-8')).hexdigest()
                                print("Confirmation of password : ")
                                pwd2=getpass.getpass()
                                pwd2=hashlib.sha256(pwd2.encode('utf-8')).hexdigest()
                                if newPassword==pwd2:
                                    pwd_check=True
                                    resp=input("Add this password in the db ? Y/N : ")
                                    if resp.lower() == 'y':
                                        cur.execute("UPDATE user SET password = ? WHERE username = ?;", (newPassword, username))
                                        conn.commit()
                                        test=input("Other changes ? : Y/N  ")
                                        if test.lower()=='y':
                                            continue
                                        else:
                                            for row in cur.execute("SELECT * FROM user"):
                                                print(row)
                                            element='5'
                                else:
                                    print("Incorrect password")
                                    print()
                                    i+=1
                                    if i==3:
                                        print("Too many tries")
                                        break
                    case '5' :
                        print("CONNECTION SHUTDOWN")
                        element='5'
                        break
                    case _:
                        print("Error match/case")
    else:
        if username=='Admin':
            print("Admin isn't editable")
        else:
            print("Username", username, "not exist")



