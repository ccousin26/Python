import sqlite3
import auth
import create_user 
import supp_user
import show
import edit_user
import logging
import datetime
import getpass
import hashlib

'''
Fonction main: permet de nous connecter à la bd puis de selectionner les différentes actions du menu (create, supp, edit..)
'''
try:
    conn = sqlite3.connect('bd.sqlite')
    print("CONNECTED")
    
    isConnected, status, username_co, updated_passwd_date, isPasswdNeedToChange=auth.auth(conn)
    if isConnected:

        if status == 'doctor':
            menu=None
            while menu!='2':
                print()
                print("Actions :")
                print ("1 - Show user table")
                print ("2 - Logout")
                menu=input("Choose your number : ")
                match menu:
                    case '1' :
                        current_date = datetime.datetime.today()
                        show.show_table(conn, status, username_co)
                        logging.debug('[ %s ], %s, Action show table/user', username_co, current_date)
                    case '2' :
                        current_date = datetime.datetime.today()
                        logging.debug('[ %s ], %s, Action logout', username_co, current_date)
                        conn.close()
                    case _:
                        current_date = datetime.datetime.today()
                        logging.error('[ %s ], %s, Action not found', username_co, current_date)
                        print("Error")
        else:
            menu=None
            if status == 'patient':
                current_date = datetime.datetime.today()
                logging.error('[ %s ], %s, Patient in main, access denied', username_co, current_date)
                print("ACCESS DENIED")
                conn.close()

            current_date = datetime.datetime.today()
            updated_passwd_date = datetime.datetime.strptime(updated_passwd_date,'%Y-%m-%d %H:%M:%S.%f')
            expiration_passwd_check = current_date - updated_passwd_date
            if (expiration_passwd_check.days >= 90) or (isPasswdNeedToChange == 1) :
                current_date = datetime.datetime.today()
                logging.info("[ %s ], %s, Password has expired for %s", username_co, current_date, username_co)
                isPasswdNeedToChange = 1
                cur = conn.cursor()
                cur.execute("UPDATE user SET isPasswdNeedToChange = ? WHERE username = ?",(isPasswdNeedToChange, username_co))
                conn.commit() #envoyer la requete
                print("Your password has expired, please change it")
                current_date = datetime.datetime.today()
                logging.info("[ %s ], %s, Password update request for %s", username_co, current_date, username_co)
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
                            updated_passwd_date = datetime.datetime.today()
                            cur.execute("UPDATE user SET password = ?, updated_passwd_date=?, isPasswdNeedToChange=0 WHERE username = ?;", (newPassword,updated_passwd_date, username_co))#
                            conn.commit()
                            current_date = datetime.datetime.today()
                            logging.info("[ %s ], %s, Password updated for %s", username_co, current_date, username_co)
                        else: 
                            print("Edit your password : ")
                            pwd_check=False
                    else:
                        print("Incorrect password")
                        current_date = datetime.datetime.today()
                        logging.warning("[ %s ], %s, Attempt to update password for %s >> failed", username_co, current_date, username_co)
                        i+=1
                        if i==3:
                            print("Too many tries, you will be disconnected")
                            current_date = datetime.datetime.today()
                            logging.error("[ %s ], %s,  Password update failed >> Logout", username_co, current_date)
                            print("DISCONNECTED")
                            exit()

            while menu!='6':
                print()
                print("Actions :")
                print ("1 - Create user")
                print ("2 - Supp user") 
                print ("3 - Edit user")
                print ("4 - Show user table")
                print ("5 - change user passwd")
                print ("6 - Logout")
                menu=input("Choose your number : ")
                match menu:
                    case '1' :
                        current_date = datetime.datetime.today()
                        logging.debug('[ %s ], %s, Action create_user', username_co, current_date)
                        create_user.create(conn, status, username_co)
                    case '2' :
                        current_date = datetime.datetime.today()
                        logging.debug('[ %s ], %s, Action supp_user', username_co, current_date)
                        supp_user.supp(conn, status, username_co)
                    case '3' :
                        current_date = datetime.datetime.today()
                        logging.debug('[ %s ], %s, Action edit_user', username_co, current_date)
                        edit_user.edit(conn, status, username_co)
                    case '4' :
                        current_date = datetime.datetime.today()
                        logging.debug('[ %s ], %s, Action show_table', username_co, current_date)
                        show.show_table(conn, status, username_co)
                    case '5' :
                        cur = conn.cursor()
                        check_table = cur.execute("SELECT username, updated_passwd_date FROM user")
                        check_update = check_table.fetchall()
                        #print(check_update) 
                        for user in check_update:
                            current_date = datetime.datetime.today()
                            updated_passwd_date = datetime.datetime.strptime(user[1],'%Y-%m-%d %H:%M:%S.%f')
                            expiration_passwd_check = current_date - updated_passwd_date

                            if (expiration_passwd_check.days >= 90) :
                                current_date = datetime.datetime.today()
                                logging.info("[ %s ], %s, Password has expired for %s", username_co, current_date, user[0])
                                isPasswdNeedToChange = 1
                                cur = conn.cursor()
                                cur.execute("UPDATE user SET isPasswdNeedToChange = ? WHERE username = ?",(isPasswdNeedToChange, user[0]))
                                conn.commit() #envoyer la requete

                        req = cur.execute("SELECT username, status FROM user WHERE isPasswdNeedTochange = 1 ")
                        users = req.fetchall()
                        for user in users:
                            if (isPasswdNeedToChange == 1):
                                if(user[1] == "patient"):
                                    print("Patient", user[0])
                                    rep=input("Do you want to update this patient Y/N : ")
                                    if rep.lower()=='y': 
                                        i=0
                                        pwd_check=False
                                        while pwd_check==False:
                                            print("Password update for", user[0])
                                            pwd = create_user.generatePassword(9)
                                            print("Password generated : ",pwd)
                                            pwd = hashlib.sha256(pwd.encode('utf-8')).hexdigest()
                                            print("Password is hashed :", pwd)
                                            resp=input("Add this password in the db ? Y/N : ")
                                            if resp.lower() == 'y':
                                                updated_passwd_date = datetime.datetime.today()
                                                cur.execute("UPDATE user SET password = ?, updated_passwd_date=?, isPasswdNeedToChange=0 WHERE username = ?;", (pwd,updated_passwd_date, user[0]))
                                                conn.commit()
                                                print("Password changed for",user[0])
                                                print()
                                                pwd_check=True
                                                current_date = datetime.datetime.today()
                                                logging.info("[ %s ], %s, Password changed for %s", username_co, current_date, user[0])
                                            else: 
                                                retry=input("Do you want to start over ? Y/N : ")
                                                if retry.lower()=='y':
                                                    pwd_check=False
                                                else:
                                                    pwd_check=True
                                                    break
                        print("Nothing else to update")     


                    case '6' :
                        current_date = datetime.datetime.today()
                        logging.debug('[ %s ], %s, Action logout', username_co, current_date)
                        conn.close()
                    case _:
                        print("Error")
                        current_date = datetime.datetime.today()
                        logging.error('[ %s ], %s, Action not found', username_co, current_date)

                        

    conn.close() #déconnexion 
    print("CONNECTION SHUTDOWN")
    current_date = datetime.datetime.today()
    logging.info('[ %s ], %s, Disconnected from db.sqlite', username_co, current_date)

except sqlite3.Error as error:
    logging.error('[ %s ], %s, Connection failed', username_co, current_date)
    print("CONNECTION ERROR", error)






