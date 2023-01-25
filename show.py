def show_table(conn, status, username_co):
    '''
    show(): fonction permettant d'afficher la table user ou un user en particulier
    conn : connexion sqlite3
    '''
    cursor = conn.cursor()
    if status == 'patient':
        username=input("Your username : ")
        cursor.execute("SELECT * FROM user WHERE username = ?", (username,))
        data = cursor.fetchall()
        if len(data)!=0 and username==username_co:
            print(username, "informations :")
            for row in data:
                print()
                print("Id:           ", row[0])
                print("Pseudo:       ", row[1])
                print("First Name:   ", row[2])
                print("Second Name:  ", row[3])
                print("Password:     ", row[4])
                print("Status :      ", row[5])
            print()
            return 0
        else:
            print("Incorrect username") 
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
                        print(user, "informations :")
                        for row in data:
                            print()
                            print("Id:           ", row[0])
                            print("Pseudo:       ", row[1])
                            print("First Name:   ", row[2])
                            print("Second Name:  ", row[3])
                            print("Password:     ", row[4])
                            print("Status :      ", row[5])
                        print()
                        loop=3
                    else:
                        print(user,"doesn't exist") 
                        loop+=1      
            case 'table':
                if(status == "patient"):
                    print("Not authorized :)")
                    return 0
                show_table = "SELECT * FROM user"
                cursor.execute(show_table)
                records = cursor.fetchall()
                print()
                print("Total rows are:  ", len(records),"\n")
                print("Printing each row : \n")
                for row in records:
                    print("Id:           ", row[0])
                    print("Pseudo:       ", row[1])
                    print("First Name:   ", row[2])
                    print("Second Name:  ", row[3])
                    print("Password:     ", row[4])
                    print("Status:       ", row[5])
                    print()
            case _:
                print("Error")

                
        
    
