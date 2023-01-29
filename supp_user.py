import sqlite3


def supp(conn, status):
    '''
    supp(): fonction permettant de supprimer un ou pls user de la table. 
    conn : connexion sqlite3
    status : status de l'utilisateur en cours.
    '''
    cur = conn.cursor()
    if status == 'patient': #le patient ne peut pas supprimer de user
        print("Access Denied")
        return 0

    data=input("Do you want to see user table ? : Y/N  ")
    if data.lower()=='y':
        for row in cur.execute("SELECT user_id, username, first_name, last_name,status, date FROM user"):
            print(row)
    print()

    i=0
    state=True
    while state==True:
        print("SUPPRESSION\n")
        print("Identification of user : ")
        username=input("username : ")    
        cur.execute("SELECT username, status FROM user WHERE username = ?", (username,)) 
        data = cur.fetchall()
        if len(data) != 0:
            if status == "sudo": #si sudo alors il peut tout faire
                del_user(conn, username, cur)
                other=input("Remove another user ? Y/N :  ")
                if other.lower()=='y':
                    i=0
                else:
                    return 0
            elif data[0][-1] == "patient": #on récupere le dernier element de la requete sql qui nous retourne toutes les informations de l'utilisateur séléctionné
                del_user(conn, username, cur)
                other=input("Remove another user ? Y/N :  ")
                if other.lower()=='y':
                    i=0
                else:
                    return 0
            else : #on ne peut supprimer que un patient en tant qu'admin
                    print("Unauthorized")
                    return 0
        else : #si il n'est pas sudo alors conditions de suppression
            i+=1
            if i==3:
                print("Too many tries")
                return 0
            print("Doesn't exists")


def del_user(conn, username, cur):
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
        print("User removed !")
        return 1
    else:
        return 0
    

