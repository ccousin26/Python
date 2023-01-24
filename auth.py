import hashlib
import getpass


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
            
            username=input("Username : ")
            pwd=getpass.getpass()
            print("\n") 
            pwd=hashlib.sha256(pwd.encode('utf-8')).hexdigest()

            result = conn.execute("SELECT * FROM user WHERE username = ? AND password = ?", (username, pwd))
            if (len(result.fetchall()) != 0):
                print("Authentification success")
                cursor = conn.execute("SELECT status FROM user WHERE username = ? AND password = ?", (username, pwd))
                status = cursor.fetchone()[0] 
                cursor = conn.execute("SELECT username FROM user WHERE username = ? AND password = ?", (username, pwd))
                username_co = cursor.fetchone()[0]
                print(status)
                print(username_co)
                return True, status, username_co
            else:
                print("Authentification failed\n")
                i+=1
                if i==3:
                    rep="N"
                    print("END OF THE AUTHENTIFICATION\n")
                    return False, None, None



