def show_table(conn, status):
    '''
    show(): fonction permettant d'afficher la table user ou un user en particulier
    conn : connexion sqlite3
    '''
    cursor = conn.cursor()
    mode=input("show table or only a user? user/table :  ")
    loop=0

    #TODO : user ne peut voir que le sien, passer en argument son username récupéré dans auth et comparer avec sa requete

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
                        print("Id: ", row[0])
                        print("Pseudo : ", row[1])
                        print("First Name: ", row[2])
                        print("Second Name: ", row[3])
                        print("Password: ", row[4])
                        print("Status : ", row[5])
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
                print("Id: ", row[0])
                print("Pseudo : ", row[1])
                print("First Name: ", row[2])
                print("Second Name: ", row[3])
                print("Password: ", row[4])
                print()
        case _:
            print("Error")

            
    
   
