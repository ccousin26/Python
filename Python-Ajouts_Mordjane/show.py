import datetime
import logging

def show_table(conn, status, username_co):
    '''
    show(): fonction permettant d'afficher la table user ou un user en particulier
    conn : connexion sqlite3
    '''
    cursor = conn.cursor()
    if status == 'patient':
        current_date = datetime.datetime.today()
        logging.error("[ %s ], %s, Attempt to change an unknown user >> %s", username_co, current_date, username_co)
        print("access unauthorized")
        return 0
        #Accès non autorisé pour les patients
    else:
        mode=input("show table or only a user? user/table :  ")
        #Demande si le user veut voir toute la table user ou juste un user en particulier.
        mode = mode.lower()
        loop = 0
        match mode:
            case 'user' :
                while loop<3:
                    user=input("Username : ")
                    #Identification du user à afficher
                    cursor.execute("SELECT * FROM user WHERE username = ?", (user,))
                    #Recherche du user dans la db.
                    data = cursor.fetchall()
                    if len(data)!=0:
                        #Si le user existe bien dans la table, on l'affiche
                        if status == "doctor":
                            #Si le user connecté est un docteur, on n'affiche pas le pwd.
                            print(user, "informations :")
                            for row in data:
                                print("Id:              ", row[0])
                                print("Pseudo:          ", row[1])
                                print("First Name:      ", row[2])
                                print("Last Name:       ", row[3])
                                print("Status:          ", row[5])
                                print("Creation Date :  ", row[6])
                                print("Data :           ", row[7])
                                print("Pwd update :     ", row[8])
                                print("pwd up to date ? :     ", row[9])
                                print()
                            loop=3
                        else :
                            print(user, "informations :")
                            for row in data:
                                print("Id:              ", row[0])
                                print("Pseudo:          ", row[1])
                                print("First Name:      ", row[2])
                                print("Last Name:       ", row[3])
                                print("Password:        ", row[4])
                                print("Status:          ", row[5])
                                print("Creation Date :  ", row[6])
                                print("Data :           ", row[7])
                                print("Pwd update :     ", row[8])
                                print("pwd up to date ? :     ", row[9])
                                print()
                            loop=3
                    else:
                        print(user,"doesn't exist") 
                        loop+=1
                        if loop==3:
                            print("Too many tries")   
                            break   

            case 'table':
                show_table = "SELECT * FROM user"
                cursor.execute(show_table)
                records = cursor.fetchall()
                print()
                print("Total rows are:  ", len(records),"\n")
                if status == "doctor":
                    #Si le user connecté est un docteur, on affiche tous sauf le pwd.
                    for row in records:
                        print("Id:              ", row[0])
                        print("Pseudo:          ", row[1])
                        print("First Name:      ", row[2])
                        print("Last Name:       ", row[3])
                        print("Status:          ", row[5])
                        print("Creation Date :  ", row[6])
                        print("Data :           ", row[7])
                        print("Pwd update :     ", row[8])
                        print("pwd up to date ? :     ", row[9])
                        print()
                else:
                    for row in records:
                        print("Id:              ", row[0])
                        print("Pseudo:          ", row[1])
                        print("First Name:      ", row[2])
                        print("Last Name:       ", row[3])
                        print("Password:        ", row[4])
                        print("Status:          ", row[5])
                        print("Creation Date :  ", row[6])
                        print("Data :           ", row[7])
                        print("Pwd update :     ", row[8])
                        print("pwd up to date ? :     ", row[9])
                        print()
            case _:
                print("Error")

                
    
