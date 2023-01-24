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
        for row in cur.execute("SELECT user_id, username, first_name, last_name FROM user"):
            print(row)
    print()

    loop=True
    while loop==True:
        print("SUPPRESSION\n")
        print("Identification of user : ")
        i=0
        count=0
        state=True
        while state==True:
            username=input("username : ")    
            cur.execute("SELECT * FROM user WHERE username = ?", (username,)) #récupere toutes les données de l'utilisateur spécifié
            data = cur.fetchall()
            if status == "sudo": #si sudo alors il peut tout faire
                del_user(conn, username, cur)
                other=input("Remove another user ? Y/N :  ")
                if other.lower()=='y':
                    state==False
                else:
                    return 0
            else : #si il n'est pas sudo alors conditions de suppression
                if len(data) == 0: #on vérifie que l'utilsiateur spécifié existe
                    print("Doesn't exists")
                else :
                    if data[0][-1] == "patient": #on récupere le dernier element de la requete sql qui nous retourne toutes les informations de l'utilisateur séléctionné
                        del_user(conn, username, cur)
                        other=input("Remove another user ? Y/N :  ")
                        if other.lower()=='y':
                            state==False
                        else:
                            return 0
                    else : #on ne peut supprimer que un patient en tant qu'admin
                        print("Access denied")
                        return 0

            
def del_user(conn, username, cur):
    '''
    conn : connexion sqlite3
    username : username de l'utilisateur à supprimer
    cur : cursor sqlite3
    '''
    for row in cur.execute("SELECT user_id, username, first_name, last_name, status FROM user WHERE username = ?", (username,)):
        print(row)
    valid=input("Are you sure you want to delete this user ? Y/N :  ")
    if valid.lower()=='y':
        cur.execute("DELETE FROM user WHERE username = ?", (username,))
        conn.commit()
        print("User removed !")
        return 0
    else:
        return 0

