import hashlib
import getpass
import datetime
import logging

#TODO: voir en fonction du status si il peut ou non avoir accès à la db entière ou juste à ses informations personnels

def auth(conn):
    '''
    auth(): fonction permettant de s'authentifier avant d'avoir accès au contenu de la bd
    '''
    logging.basicConfig(filename='conn.log', encoding='utf-8', level=logging.DEBUG)

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
                cursor = conn.execute("SELECT status, username FROM user WHERE username = ? AND password = ?", (username_co, pwd))
                status, username_co= cursor.fetchone()

                if status == 'patient':
                    current_date = datetime.datetime.today()
                    logging.warning('[ %s ], %s Connection Attempt ', username_co, current_date)
                    logging.warning('[ %s ], %s, Authentification failed', username_co, current_date)
                    print("Unauthorized")
                    print()
                    return False, None, None

                print("Authentification success")
                current_date = datetime.datetime.today()
                logging.info('[ %s ], %s, Authentification Success', username_co, current_date)
                logging.info('[ %s ], %s, Connection to db.sqlite', username_co, current_date)
                return True, status, username_co
            else:
                print("Authentification failed\n")
                current_date = datetime.datetime.today()
                logging.warning('[ %s ], %s, Connection Attempt ', username_co, current_date)
                logging.warning('[ %s ], %s, Authentification Failed', username_co, current_date)
                i+=1
                if i==3:
                    rep="N"
                    print("END OF THE AUTHENTIFICATION\n")
                    return False, None, None



