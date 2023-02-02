import getpass
import hashlib
import show
import logging
import datetime

def edit(conn, status, username_co): 
    '''
    edit : editer les informations d'un utilisateur 
    conn : connexion sqlite3
    '''
    cur = conn.cursor()
    if status == 'admin' or status == 'sudo':
        #Seuls les admins ont les droits de modification dans la db.
        data=input("Do you want to see db content before? : Y/N  ") 
        #Propose d'afficher la table avant la modification d'un user.
        if data.lower()=='y':
            current_date = datetime.datetime.today()
            logging.debug('[ %s ], %s, Show table before edit_user', username_co, current_date)
            show.show_table(conn, status,username_co)
    print()
    print("EDIT A USER")
    print("Which user do you want to modify ?")
    username=input("Username : ")  
    #Identification du user à modifier. 
    current_date = datetime.datetime.today()
    logging.info('[ %s ], %s, Change request for user %s', username_co, current_date, username)
    req = cur.execute("SELECT * FROM user WHERE username = ?", (username,)) 
    #Recherche le username dans la db.
    resSql = req.fetchall()
    if len(resSql) != 0:
        #Si le user existe bien dans la db
        req = cur.execute("SELECT status FROM user WHERE username = ?", (username,))
        #Recherche le status du user dans la db.
        user_status = req.fetchall()
        if status == 'patient':
            print("You haven't the right as patient.")
            current_date = datetime.datetime.today()
            logging.warning("[ %s ], %s, Patient doesn't have edit rights", username_co, current_date)
            return 0
            #Les patients n'ont pas les droits de modifications
        if status == 'admin' and user_status[0][-1] == 'sudo':
            current_date = datetime.datetime.today()
            logging.warning("[ %s ], %s, Admin doesn't have this edit rights", username_co, current_date)
            print("You doesn't have this rights")
            return 0
            #Les admins standards n'ont pas les droits pour modifier un sudo
        if status == 'admin' and user_status[0][-1] == 'admin':
            current_date = datetime.datetime.today()
            logging.warning("[ %s ], %s, Admin doesn't have this edit rights", username_co, current_date)
            print("You doesn't have this rights")
            return 0
            #Les admins standards n'ont pas les droits pour modifier un autre admin
        else:
            element=None
            while element!='6':
                    conn.commit()
                    print()
                    print("Actions you can do for", username, ":")
                    print ("1 - Edit Username")
                    print ("2 - Edit First Name")
                    print ("3 - Edit Last Name")
                    print ("4 - Edit Password")
                    print ("5 - Edit Status")
                    print ("6 - Exit")
                    #Menu des champs modifiables
                    
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
                                        element='6'
                                #Demande de changement de username
                                else:
                                    resp=input("Add this username in the db ? Y/N : ")
                                    #Demande de validation du username avant de l'ajouter dans la db.
                                    if resp.lower() == 'y':
                                        cur.execute("UPDATE user SET username = ? WHERE username = ?;", (newUsername, username))
                                        conn.commit()
                                        #Modification du username dans la db.
                                        current_date = datetime.datetime.today()
                                        logging.info("[ %s ], %s, Username changed for %s", username_co, current_date, username)
                                        print("Modification add \n")
                                        i=3
                                        test=input("Other changes ? : Y/N  ")
                                        #Demande si il y aura d'autres modification pour ce user.
                                        if test.lower()=='y':
                                            i=3
                                        else:
                                            element='6'
                                    else:
                                        print("No change")
                                        i=3
                        case '2' :
                            i=0
                            while i<3:
                                newFirstName=input("New First Name : ")
                                resp=input("Add this first name in the db ? Y/N : ")
                                if resp.lower() == 'y':
                                    cur.execute("UPDATE user SET first_name = ? WHERE username = ?;", (newFirstName, username))
                                    conn.commit()
                                    current_date = datetime.datetime.today()
                                    logging.info("[ %s ], %s, Firstname changed for %s", username_co, current_date, username)
                                    test=input("Other changes ? : Y/N  ")
                                    i=3
                                    if test.lower()=='y':
                                        i=3
                                    else:
                                        element='6'
                                else:
                                    print("No change")
                                    i=3
                                #Modification du prénom, même fonctionnement que pour le username
                        case '3' :
                            i=0
                            while i<3:
                                newLastName=input("New Last Name : ")
                                resp=input("Add this last name in the db ? Y/N : ")
                                if resp.lower() == 'y': 
                                    cur.execute("UPDATE user SET last_name = ? WHERE username = ?;", (newLastName, username))
                                    conn.commit()      
                                    current_date = datetime.datetime.today()
                                    logging.info("[ %s ], %s, Lastname changed for %s", username_co, current_date, username)                   
                                    test=input("Other changes ? : Y/N  ")
                                    i=3
                                    if test.lower()=='y':
                                        i=3
                                    else:
                                        element='6'
                                else:
                                    print("No change")
                                    i=3
                                #Modification du nom de famille, même fonctionnement que pour le username
                        case '4' :
                            rep=input("Reset password? Y/N :  ")
                            #Vérification du choix
                            if rep.lower()=='y':
                                i=0
                                pwd_check=False
                                while pwd_check==False:
                                    newPassword=getpass.getpass()
                                    newPassword=hashlib.sha256(newPassword.encode('utf-8')).hexdigest()
                                    print("Confirmation of password : ")
                                    pwd2=getpass.getpass()
                                    pwd2=hashlib.sha256(pwd2.encode('utf-8')).hexdigest()
                                    #Modification manuelle du mot de passe (confirmation + hash)
                                    if newPassword==pwd2:
                                        pwd_check=True
                                        resp=input("Add this password in the db ? Y/N : ")
                                        #Demande de vérification avant modification du pwd dans la db.
                                        if resp.lower() == 'y':
                                            updated_passwd_date = datetime.datetime.today()
                                            cur.execute("UPDATE user SET password = ?,updated_passwd_date=?,isPasswdNeedToChange=0 WHERE username = ?;", (newPassword,updated_passwd_date, username))#
                                            conn.commit()
                                            #Modification du pwd dans la db.
                                            current_date = datetime.datetime.today()
                                            logging.info("[ %s ], %s, Password changed for %s", username_co, current_date, username)
                                            test=input("Other changes ? : Y/N  ")
                                            if test.lower()=='y':
                                                continue
                                            else:
                                                element='6'
                                    else:
                                        print("Incorrect password")
                                        current_date = datetime.datetime.today()
                                        logging.warning("[ %s ], %s, Attempt to change password for %s >> failed", username_co, current_date, username)
                                        print()
                                        i+=1
                                        if i==3:
                                            print("Too many tries")
                                            current_date = datetime.datetime.today()
                                            logging.error("[ %s ], %s,  Attempt to change password for %s >> failed, too many tries", username_co, current_date, username)
                                            break
                                        #3 tentatives max pour changer le mot de passe.
                        case '5' :
                            i=0
                            while i<3:
                                print("STATUS")
                                print("- sudo")
                                print("- admin")
                                print("- patient")
                                print("- doctor")
                                #Menu de status existants
                                newStatus=input("Status : ")
                                #Choix du nouveau status
                                newStatus=newStatus.lower()
                                if newStatus==None:
                                    print("Error Status is empty")
                                    break
                                print(newStatus)
                                if status=='admin' and newStatus=='sudo':
                                    print("You can't choose sudo status if you're admin")
                                    break
                                if status=='admin' and newStatus=='admin':
                                    print("As admin you can't manage other admins")
                                    break
                                #Vérification des droits avant modification du status
                                if newStatus=='sudo' or newStatus=='admin' or newStatus=="patient" or newStatus=='doctor':
                                    #On vérifié que le status est un status existant
                                    resp=input("Add this status in the db ? Y/N : ")
                                    #Demande de vérification du status avant modification dans la db.
                                    if resp.lower() == 'y': 
                                        cur.execute("UPDATE user SET status = ? WHERE username = ?;", (newStatus, username))#update le statu
                                        conn.commit()       
                                        #Modification dans la db.
                                        current_date = datetime.datetime.today()
                                        logging.info("[ %s ], %s, Status changed for %s", username_co, current_date, username)
                                        if username == username_co:
                                            print("Your account has been modified, you will be disconnected")
                                            exit()     
                                            #Si la modification du user connecté > déconnexion car il n'a peut être plus les droits pour être ici   
                                        test=input("Other changes ? : Y/N  ")
                                        i=3
                                        if test.lower()=='y':
                                            i=3
                                        else:
                                            element='6'
                                    else:
                                        print("No change")
                                        i=3
                                else:
                                    print("Incorrect Status")
                                    current_date = datetime.datetime.today()
                                    logging.info("[ %s ], %s, Attempt to change status for %s >> failed", username_co, current_date, username)
                                    break
                                    #En cas de status non existant
                        case '6' :
                            print("EXIT")
                            current_date = datetime.datetime.today()
                            logging.debug("[ %s ], %s, Exit edit mode", username_co, current_date)
                            element='6'
                            break
                            #Sortir du mode edit
                        case _:
                            print("Error match/cases")
                            current_date = datetime.datetime.today()
                            logging.error("[ %s ], %s, Error match/cases", username_co, current_date)
                            #Erreur du choix d'action
    else:
        current_date = datetime.datetime.today()
        logging.error("[ %s ], %s, Attempt to change an unknown user >> %s", username_co, current_date, username)
        print("Username", username, "doesn't exist")
        #En cas de demande de modfication d'un user inexistant dans la db.
        



