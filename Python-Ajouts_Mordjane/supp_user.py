import sqlite3
import datetime
import logging


def supp(conn, status, username_co):
    '''
    supp(): fonction permettant de supprimer un ou pls user de la table. 
    conn : connexion sqlite3
    status : status de l'utilisateur en cours.
    '''
    cur = conn.cursor()
    if status == 'patient': 
        current_date = datetime.datetime.today()
        logging.error("[ %s ], %s, supp_user access denied", username_co, current_date)
        print("Access Denied")
        return 0
    #Les patients n'ont pas les droits de suppression

    data=input("Do you want to see user table ? : Y/N  ")
    #Propose d'afficher la table avant la suppression d'un user
    if data.lower()=='y':
        current_date = datetime.datetime.today()
        logging.debug("[ %s ], %s, Show table/user before supp_user", username_co, current_date)
        for row in cur.execute("SELECT user_id, username, first_name, last_name,status, date FROM user"):
            print(row)
    print()

    i=0
    state=True
    while state==True:
        print("SUPPRESSION\n")
        print("Identification of user : ")
        username=input("username : ")    
        #Permet d'identifier le user à supprimer  dans la db.
        current_date = datetime.datetime.today()
        logging.info("[ %s ], %s, Request supp_user for user %s", username_co, current_date, username)
        cur.execute("SELECT username, status FROM user WHERE username = ?", (username,)) 
        #Recherche le user dans la db.
        data = cur.fetchall()
        if len(data) != 0:
            #Si le user exist bien
            if status == "sudo": #si sudo alors il peut tout faire
                del_user(conn, username, cur, username_co)
                #Supprime le user
                other=input("Remove another user ? Y/N :  ")
                #Posibilité de supprimer d'autres users.
                if other.lower()=='y':
                    i=0
                else:
                    return 0
            elif data[0][-1] == "patient" or data[0][-1]=="doctor":
                #Permet de restreindre les autres admins à la suppression de patients/docteurs 
                del_user(conn, username, cur, username_co)
                #Supprime le user
                other=input("Remove another user ? Y/N :  ")
                #Possibilité de supprimer d'autres users.
                if other.lower()=='y':
                    i=0
                else:
                    return 0
            else : 
                    current_date = datetime.datetime.today()
                    logging.error("[ %s ], %s, Attempt to supp user %s >> Unauthorized", username_co, current_date, username)
                    print("Unauthorized")
                    return 0
                    #Dans le cas ou un admin souhaite supprimer autre chose qu'un patient ou un odcteur
        else : 
            i+=1
            if i==3:
                print("Too many tries")
                return 0
                #3 tentatives max pour supprimer ce user. 
            print("Doesn't exists")
            

def del_user(conn, username, cur, username_co):
    '''
    conn : connexion sqlite3
    username : username de l'utilisateur à supprimer
    cur : cursor sqlite3
    '''
    data = cur.execute("SELECT user_id, username, first_name, last_name, status, date, medical_files FROM user WHERE username = ?", (username,)) #affiche la table
    for row in data:
        print()
        print("Id:           ", row[0])
        print("Pseudo:       ", row[1])
        print("First Name:   ", row[2])
        print("Second Name:  ", row[3])
        print("Status :      ", row[4])
        print("Last update : ", row[5])
        print("Data :        ", row[6])
        print()

    valid=input("Are you sure you want to delete this user ? Y/N :  ")
    #Demande de validation avant la suppression du user.
    if valid.lower()=='y':
        cur.execute("DELETE FROM user WHERE username = ?", (username,))
        conn.commit()
        #Suppression du user dans la db.
        current_date = datetime.datetime.today()
        logging.info("[ %s ], %s, User %s deleted from db.sqlite", username_co, current_date, username)
        print("User removed !")
        return 1
    else:
        current_date = datetime.datetime.today()
        logging.info("[ %s ], %s, Request to supp_user abort ", username_co, current_date)
        return 0
        #Dans le cas ou la suppression n'est pas validée.
    

