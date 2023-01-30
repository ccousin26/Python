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
    else:
        mode=input("show table or only a user? user/table :  ")
        mode = mode.lower()
        loop = 0
        match mode:
            case 'user' :
                while loop<3:
                    user=input("Username : ")
                    cursor.execute("SELECT * FROM user WHERE username = ?", (user,))
                    data = cursor.fetchall()
                    if len(data)!=0:
                        if status == "doctor":
                            print(user, "informations :")
                            for row in data:
                                print()
                                print("Id:           ", row[0])
                                print("Pseudo:       ", row[1])
                                print("First Name:   ", row[2])
                                print("Second Name:  ", row[3])
                                print("Status :      ", row[5])
                                print("Last update : ", row[6])
                                print("Data :        ", row[7])
                            print()
                            loop=3
                        else :
                            print(user, "informations :")
                            for row in data:
                                print()
                                print("Id:           ", row[0])
                                print("Pseudo:       ", row[1])
                                print("First Name:   ", row[2])
                                print("Second Name:  ", row[3])
                                print("Password:     ", row[4])
                                print("Status :      ", row[5])
                                print("Last update : ", row[6])
                                print("Data :        ", row[7])
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
                    for row in records:
                        print("Id:           ", row[0])
                        print("Pseudo:       ", row[1])
                        print("First Name:   ", row[2])
                        print("Second Name:  ", row[3])
                        print("Status:       ", row[5])
                        print("Last update : ", row[6])
                        print("Data :        ", row[7])
                        print()
                else:
                    for row in records:
                        print("Id:           ", row[0])
                        print("Pseudo:       ", row[1])
                        print("First Name:   ", row[2])
                        print("Second Name:  ", row[3])
                        print("Password:     ", row[4])
                        print("Status:       ", row[5])
                        print("Last update : ", row[6])
                        print("Data :        ", row[7])
                        print()
            case _:
                print("Error")

                
        
    
