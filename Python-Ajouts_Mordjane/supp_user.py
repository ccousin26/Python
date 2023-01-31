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
    if status == 'patient': #le patient ne peut pas supprimer de user
        current_date = datetime.datetime.today()
        logging.error("[ %s ], %s, supp_user access denied", username_co, current_date)
        print("Access Denied")
        return 0

    data=input("Do you want to see user table ? : Y/N  ")
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
        current_date = datetime.datetime.today()
        logging.info("[ %s ], %s, Request supp_user for user %s", username_co, current_date, username)
        cur.execute("SELECT username, status FROM user WHERE username = ?", (username,)) 
        data = cur.fetchall()
        if len(data) != 0:
            if status == "sudo": #si sudo alors il peut tout faire
                del_user(conn, username, cur, username_co)
                other=input("Remove another user ? Y/N :  ")
                if other.lower()=='y':
                    i=0
                else:
                    return 0
            elif data[0][-1] == "patient" or data[0][-1]=="doctor": #on récupere le dernier element de la requete sql qui nous retourne toutes les informations de l'utilisateur séléctionné
                del_user(conn, username, cur, username_co)
                other=input("Remove another user ? Y/N :  ")
                if other.lower()=='y':
                    i=0
                else:
                    return 0
            else : #on ne peut supprimer qu'un patient en tant qu'admin
                    current_date = datetime.datetime.today()
                    logging.error("[ %s ], %s, Attempt to supp user %s >> Unauthorized", username_co, current_date, username)
                    print("Unauthorized")
                    return 0
        else : #si il n'est pas sudo alors conditions de suppression
            i+=1
            if i==3:
                print("Too many tries")
                return 0
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
    if valid.lower()=='y':
        cur.execute("DELETE FROM user WHERE username = ?", (username,))
        conn.commit()
        current_date = datetime.datetime.today()
        logging.info("[ %s ], %s, User %s deleted from db.sqlite", username_co, current_date, username)
        print("User removed !")
        return 1
    else:
        current_date = datetime.datetime.today()
        logging.info("[ %s ], %s, Request to supp_user abort ", username_co, current_date)
        return 0
    

