import sqlite3
import auth
import create_user 
import supp_user
import show
import edit_user
import logging
import datetime

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
                        current_date = datetime.datetime.today()
                        show.show_table(conn, status, username_co)
                        logging.debug('[ %s ], %s, Action show table/user', username_co, current_date)
                    case '2' :
                        current_date = datetime.datetime.today()
                        logging.debug('[ %s ], %s, Action logout', username_co, current_date)
                        conn.close()
                    case _:
                        current_date = datetime.datetime.today()
                        logging.error('[ %s ], %s, Action not found', username_co, current_date)
                        print("Error")

        else:
            menu=None
            if status == 'patient':
                current_date = datetime.datetime.today()
                logging.error('[ %s ], %s, Patient in main, access denied', username_co, current_date)
                print("Access denied")
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
                        current_date = datetime.datetime.today()
                        logging.debug('[ %s ], %s, Action create_user', username_co, current_date)
                        create_user.create(conn, status, username_co)
                    case '2' :
                        current_date = datetime.datetime.today()
                        logging.debug('[ %s ], %s, Action supp_user', username_co, current_date)
                        supp_user.supp(conn, status, username_co)
                    case '3' :
                        current_date = datetime.datetime.today()
                        logging.debug('[ %s ], %s, Action edit_user', username_co, current_date)
                        edit_user.edit(conn, status, username_co)
                    case '4' :
                        current_date = datetime.datetime.today()
                        logging.debug('[ %s ], %s, Action show_table', username_co, current_date)
                        show.show_table(conn, status, username_co)
                    case '5' :
                        current_date = datetime.datetime.today()
                        logging.debug('[ %s ], %s, Action logout', username_co, current_date)
                        conn.close()
                    case _:
                        print("Error")
                        current_date = datetime.datetime.today()
                        logging.error('[ %s ], %s, Action not found', username_co, current_date)

                        

    conn.close() #déconnexion 
    print("CONNECTION SHUTDOWN")
    current_date = datetime.datetime.today()
    logging.info('[ %s ], %s, Disconnected from db.sqlite', username_co, current_date)

except sqlite3.Error as error:
    logging.error('[ %s ], %s, Connection failed', username_co, current_date)
    print("Connection Error", error)






