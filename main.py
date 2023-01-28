import sqlite3
import auth
import create_user 
import supp_user
import show
import edit_user

'''
Fonction main: permet de nous connecter à la bd puis de selectionner les différentes actions du menu (create, supp, edit..)
'''
try:
    conn = sqlite3.connect('bd.sqlite')
    print("Connected")
    
    isConnected, status, username_co=auth.auth(conn)
    print(isConnected)
    print(status)
    print(username_co)
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
                        show.show_table(conn, status, username_co)
                    case '2' :
                        conn.close()
                    case _:
                        print("Error")
        else:
            menu=None
            if status == 'patient':
                ("Access denied")
                conn.close()
            while menu!='5':
                print()
                print("Actions :")
                print ("1 - Create user")
                print ("2 - Supp user") 
                print ("3 - Edit user")
                print ("4 - Show user table")
                print ("5 - Logout")
                menu=input("Choose your number : ")
                match menu:
                    case '1' :
                        create_user.create(conn, status)
                    case '2' :
                        supp_user.supp(conn, status)
                    case '3' :
                        edit_user.edit(conn, status, username_co)
                    case '4' :
                        show.show_table(conn, status, username_co)
                    case '5' :
                        conn.close()
                    case _:
                        print("Error")

    conn.close() #déconnexion 
    print("CONNECTION SHUTDOWN")
except sqlite3.Error as error:
    print("Connection Error", error)






