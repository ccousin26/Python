import sqlite3 #base de données
import auth #fichier d'authentification
import create_user #fichier de création de user
import supp_user #fichier de suppression de user
import show #fichier d'affichage de la table + user
import edit_user #Fichier de modification des users
import logging #Logs + traces des actions effectuées
import datetime #date/heure
import getpass #entrer un mdp
import hashlib #hash les mdp

'''
Fonction main: permet de nous connecter à la bd puis de selectionner les différentes actions du menu (create, supp, edit..)
'''
try:
    conn = sqlite3.connect('bd.sqlite')
    #Connexion à la base de données
    print("CONNECTED")
    
    isConnected, status, username_co, updated_passwd_date, isPasswdNeedToChange=auth.auth(conn)
    #Réception des datas du user authentifié retourné par auth.py.
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
                        #Case pour afficher la table user ou rechercher un user en particulier dans la db.
                    case '2' :
                        current_date = datetime.datetime.today()
                        logging.debug('[ %s ], %s, Action logout', username_co, current_date)
                        conn.close()
                        #Case Déconnexion 
                    case _:
                        current_date = datetime.datetime.today()
                        logging.error('[ %s ], %s, Action not found', username_co, current_date)
                        print("Error")
                    #Case Error
        #Menu dédié aux Docteurs (Droit de lecture uniquement)
        else:
            menu=None
            if status == 'patient':
                current_date = datetime.datetime.today()
                logging.error('[ %s ], %s, Patient in main, access denied', username_co, current_date)
                print("ACCESS DENIED")
                conn.close()
            #Règle de filtrage pour les patients, déconnexion 

            current_date = datetime.datetime.today()
            updated_passwd_date = datetime.datetime.strptime(updated_passwd_date,'%Y-%m-%d %H:%M:%S.%f')
            expiration_passwd_check = current_date - updated_passwd_date

            if (expiration_passwd_check.days >= 90) or (isPasswdNeedToChange == 1) :
            #Vérification de la validité du password du user connecté (90j de validité).
                current_date = datetime.datetime.today()
                logging.info("[ %s ], %s, Password has expired for %s", username_co, current_date, username_co)
                isPasswdNeedToChange = 1
                cur = conn.cursor()
                cur.execute("UPDATE user SET isPasswdNeedToChange = ? WHERE username = ?",(isPasswdNeedToChange, username_co))
                conn.commit() #envoyer la requete
                #Mise à jour du champ isPassdwToChange dans la db
                print("Your password has expired, please change it")
                current_date = datetime.datetime.today()
                logging.info("[ %s ], %s, Password update request for %s", username_co, current_date, username_co)
                i=0
                pwd_check=False
                while pwd_check==False:
                    print()
                    print("Enter new password ")
                    newPassword=getpass.getpass()
                    newPassword=hashlib.sha256(newPassword.encode('utf-8')).hexdigest()
                    print("Confirmation of password : ")
                    pwd2=getpass.getpass()
                    pwd2=hashlib.sha256(pwd2.encode('utf-8')).hexdigest()
                    #Modification manuelle du password pour les admins (confirmation + hash)
                    if newPassword==pwd2:
                        pwd_check=True
                        resp=input("Add this password in the db ? Y/N : ")
                        if resp.lower() == 'y':
                            updated_passwd_date = datetime.datetime.today()
                            cur.execute("UPDATE user SET password = ?, updated_passwd_date=?, isPasswdNeedToChange=0 WHERE username = ?;", (newPassword,updated_passwd_date, username_co))#
                            conn.commit()
                            #Mise à jour du password dans la db.
                            current_date = datetime.datetime.today()
                            logging.info("[ %s ], %s, Password updated for %s", username_co, current_date, username_co)
                        else: 
                            print("Edit your password : ")
                            pwd_check=False
                            #Dans le cas ou le user n'a pas validé son password, on force l'update
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
                        #Deconnexion du user en cas de non mise à jour du password (3 tentatives max)

            while menu!='6':
                print()
                print("Actions :")
                print ("1 - Create user")
                print ("2 - Supp user") 
                print ("3 - Edit user")
                print ("4 - Show user table")
                print ("5 - Update passwd")
                print ("6 - Logout")
                #Menu d'actions possibles
                menu=input("Choose your number : ")
                match menu:
                    case '1' :
                        current_date = datetime.datetime.today()
                        logging.debug('[ %s ], %s, Action create_user', username_co, current_date)
                        create_user.create(conn, status, username_co)
                    #Appel du fichier create_user.py.
                    case '2' :
                        current_date = datetime.datetime.today()
                        logging.debug('[ %s ], %s, Action supp_user', username_co, current_date)
                        supp_user.supp(conn, status, username_co)
                    #Appel du fichier supp_user.py.
                    case '3' :
                        current_date = datetime.datetime.today()
                        logging.debug('[ %s ], %s, Action edit_user', username_co, current_date)
                        edit_user.edit(conn, status, username_co)
                    #Appel du fichier edit_user.py.
                    case '4' :
                        current_date = datetime.datetime.today()
                        logging.debug('[ %s ], %s, Action show_table', username_co, current_date)
                        show.show_table(conn, status, username_co)
                    #Appel du fichier show.py.
                    case '5' :
                        cur = conn.cursor()
                        check_table = cur.execute("SELECT username, updated_passwd_date FROM user")
                        #Requête pour récupérer tous les username + updated_pwd de la table user.
                        check_update = check_table.fetchall()
                        for user in check_update:
                        #Check pour tous les users de la table user
                            current_date = datetime.datetime.today()
                            updated_passwd_date = datetime.datetime.strptime(user[1],'%Y-%m-%d %H:%M:%S.%f')
                            expiration_passwd_check = current_date - updated_passwd_date

                            if (expiration_passwd_check.days >= 90) :
                            #Check quels users ont un pwd expiré
                                current_date = datetime.datetime.today()
                                logging.info("[ %s ], %s, Password has expired for %s", username_co, current_date, user[0])
                                isPasswdNeedToChange = 1
                                cur = conn.cursor()
                                cur.execute("UPDATE user SET isPasswdNeedToChange = ? WHERE username = ?",(isPasswdNeedToChange, user[0]))
                                conn.commit() 
                            #Change la valeur de isPasswdToChange dans la db pour les users avec un pwd expiré

                        req = cur.execute("SELECT username, status FROM user WHERE isPasswdNeedTochange = 1 ")
                        #Requête pour récupérer les usernames + status des users qui on un pwd expiré
                        users = req.fetchall()
                        for user in users:
                            if (isPasswdNeedToChange == 1):
                                if(user[1] == "patient"):
                                    print()
                                    print("Patient", user[0])
                                    rep=input("Do you want to update this patient Y/N : ")
                                    #Propose de mettre à jour le pwd expiré des patients
                                    if rep.lower()=='y': 
                                        i=0
                                        pwd_check=False
                                        while pwd_check==False:
                                            print()
                                            print("Password update for", user[0])
                                            pwd = create_user.generatePassword(9)
                                            #Fonction permettant de générer un pwd aléatoire.
                                            print("Password generated : ",pwd)
                                            pwd = hashlib.sha256(pwd.encode('utf-8')).hexdigest()
                                            #Hash le pwd
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
                    #Déconnexion
                    case _:
                        print("Error")
                        current_date = datetime.datetime.today()
                        logging.error('[ %s ], %s, Action not found', username_co, current_date)
                    #En cas d'erreur 

                        

    conn.close() #Déconnexion 
    print("CONNECTION SHUTDOWN")
    current_date = datetime.datetime.today()
    logging.info('[ %s ], %s, Disconnected from db.sqlite', username_co, current_date)

except sqlite3.Error as error:
    logging.error('[ %s ], %s, Connection failed', username_co, current_date)
    print("CONNECTION ERROR", error) #Erreur lors dela connexion à la db.





