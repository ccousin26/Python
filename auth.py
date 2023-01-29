import hashlib
import getpass
import datetime

#TODO: voir en fonction du status si il peut ou non avoir accès à la db entière ou juste à ses informations personnels

def auth(conn):
    '''
    auth(): fonction permettant de s'authentifier avant d'avoir accès au contenu de la bd
    '''
    rep=input("Do you want to authentificate ? Y/N : ")
    i=0
    while(rep.lower()=="y"):
        if i<3:
            print("AUTHENTIFICATION\n")
            
            username_co=input("Username : ")
            pwd=getpass.getpass()
            print() 
            pwd=hashlib.sha256(pwd.encode('utf-8')).hexdigest()

            result = conn.execute("SELECT * FROM user WHERE username = ? AND password = ?", (username_co, pwd))
            if (len(result.fetchall()) != 0):
                cursor = conn.execute("SELECT status, username, date FROM user WHERE username = ? AND password = ?", (username_co, pwd))
                status, username_co, date = cursor.fetchone()
                if status == 'patient':
                    print("Unauthorized")
                    return False, None, None
                print("Authentification success")
                print("Last user update : ", date)
                current_date = datetime.date.today()
                print("Login Date : ", current_date)
                return True, status, username_co
            else:
                print("Authentification failed\n")
                i+=1
                if i==3:
                    rep="N"
                    print("END OF THE AUTHENTIFICATION\n")
                    return False, None, None



