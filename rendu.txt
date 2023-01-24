import sqlite3
import auth
import random
import getpass
import hashlib


#########################################################################
'''
Fonction main: permet de nous connecter à la bd puis de selectionner les différentes actions du menu (create, supp, edit..)
'''
try:
    conn = sqlite3.connect('bd.sqlite')
    print("Connected")
    
    isConnected, status=auth.auth(conn)
    print(isConnected)
    print(status)
    if isConnected:
        menu=None
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
                    edit_user.edit(conn)
                case '4' :
                    show.show_table(conn, status)
                case '5' :
                    conn.close()
                case _:
                    print("Error")

    conn.close() #déconnexion 
    print("CONNECTION SHUTDOWN")
except sqlite3.Error as error:
    print("Connection Error", error)


#########################################################################

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


#########################################################################

def create(conn, status):
    '''
    Create an user based on his name and lastname, concatenate them and check if it's already in db
    conn: Sqlite3 connexion into db "bd.sqlite"
    '''
    cur = conn.cursor() #connexion avec la base de donnée
    rep=input("Do you want to create a user ? Y/N : ")
    i=0
    status_user = None
    if status == "patient":
        print("You can't create user as a patient.")
    else:
        while(rep.lower() == "y" and status_user == None): #permet de récupérer la lettre, peut importe la majuscule ou non.
            if i<5:
                print("USER CREATION\n")
                print("STATUS")
                print("1 - sudo")
                print("2 - admin")
                print("3 - patient")
                status_user = input("status number : ")
                match status_user : 
                    case '1':
                        if status == 'sudo':
                            status_user = 'sudo'
                        else :
                            print("Unauthorized")
                            i+=1
                            break
                    case '2':
                        if status == 'sudo':
                            status_user = 'admin'
                        else :
                            print("Unauthorized")
                            break
                    case '3':
                        if status == 'sudo' or status == 'admin':
                            status_user = 'patient'
                        else :
                            print("Unauthorized")
                            break
                    case _:
                        print("error")
                        break
                if(status_user == None):
                    break
                name = input("Name : ")
                lastname = input("Last name : ")
                username = name[0] + lastname #concatenation du prénom et nom.
                print(username)
                #requete sql qui permet de selectionner le prénom du user en se basant sur son username. Si la requete aboutit, alors l'utilisateur existe déjà.
                cur.execute("SELECT first_name FROM user WHERE username = ?", (username,)) 
                data = cur.fetchall() #lance la requete.
                
                '''
                fetchall retourne un tableau, en vérifiant la taille du tableau on sait alors si la requete à aboutit à un résultat non null.
                '''
                if len(data) != 0: 
                    print("username", username, "already exist !")
                    i+=1
                    if i==5:
                        print("Too many tries")
                        break
                else:              
                    pwd = generatePassword(9)
                    print("Your password is : " + pwd)
                    print("---Adding user---")
                    print("Username : ", username)
                    print("Name : ", name)
                    print("Last name : ", lastname)
                    print("Your password :", pwd)
                    print("Status : ", status_user)
                    pwd = hashlib.sha256(pwd.encode('utf-8')).hexdigest() #permet de hasher le pwd avant la sauvegarde dans la bd
                    resp=input("Add this user in the db ? Y/N : ")
                    if resp.lower() == 'y':
                        cur.execute("INSERT INTO user VALUES(NULL,?,?,?,?,?)", (username,name,lastname,pwd,status_user)) #ajoute l'utilisateur à la db en passant en argument ses informations
                        conn.commit() #envoyer la requete
                        print("USER ADD\n")
                        for row in cur.execute("SELECT * FROM user"): #affiche la table
                            print(row)
                        i=0
                    else:
                        i=0
                    break
                    
                        

def generatePassword(pwdLen):
    '''
    generatePassword(int pwdLen) : Generates a random password with numbers, letters, and special characters. 
    pwdLen : password lenght, integer. 
    '''
    letters = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
    numbers = []
    spec = ["*","/","!",";","_","-"]
    pwd = ''
    for i in range(9): #créer la liste de chiffres
        numbers.append(i)
    for i in range(pwdLen): 
        lorn = random.randint(0,2) #letter or number : permet de choisir entre une letter, un chiffre, ou un caractere spécial
        if(lorn == 0):
            pwd += random.choice(letters) #random.choice() fonction qui permet de choisir un élément aléatoirement dans une liste
        elif(lorn == 1):
            pwd += str(random.choice(numbers)) #str += str, permet de concatener une string, d'ajouter à la fin de cette derniere un nouveau caractère.
        else:
            pwd += random.choice(spec)
    return pwd


#########################################################################
    
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



#########################################################################


def edit(conn): 
    '''
    edit : editer un utilisateur : modifier son username, first name, last name ou password
    conn : connexion sqlite3
    '''
    #TODO : gerer les status.
    cur = conn.cursor()

    data=input("Do you want to see user table ? : Y/N  ") #afficher la table
    if data.lower()=='y':
        for row in cur.execute("SELECT user_id, username, first_name, last_name, status FROM user"):
            print(row)
    print()
    print("EDIT A USER")
    print("Which user do you want to modify ?")

    username=input("Username : ")   
    req = cur.execute("SELECT * FROM user WHERE username = ?", (username,)) #requete sql permettant de retrouver la ligne correspondant au username dans la bd
    resSql = req.fetchall()
    if len(resSql) != 0 and username!='Admin':
        element=None
        while element!='5':

                print()

                print("Actions you can do for", username, ":")
                print ("1 - Edit Username")
                print ("2 - Edit First Name")
                print ("3 - Edit Last Name")
                print ("4 - Edit Password")
                print ("5 - Exit")
                element=input("Choose your action : ")

                match element:
                    case '1' :
                        i=0
                        while i<3:
                            newUsername=input("New Username : ")
                            cur.execute("SELECT username FROM user WHERE username = ?", (newUsername,))
                            data = cur.fetchall()
                            if len(data) != 0:
                                print("username", newUsername, "already exist !\n")
                                i+=1
                                if i==3:
                                    print("Too many tries : EXIT")
                                    element='5'
                            else:
                                resp=input("Add this username in the db ? Y/N : ")
                                if resp.lower() == 'y':
                                    cur.execute("UPDATE user SET username = ? WHERE username = ?;", (newUsername, username))
                                    conn.commit()
                                    print("Modification add \n")
                                    i=3
                                    test=input("Other changes ? : Y/N  ")
                                    if test.lower()=='y':
                                        i=3
                                else:
                                    for row in cur.execute("SELECT * FROM user"):
                                        print(row)
                                    element='5'
                                    i=3
                    case '2' :
                        i=0
                        while i<3:
                            newFirstName=input("New First Name : ")
                            resp=input("Add this first name in the db ? Y/N : ")
                            if resp.lower() == 'y':
                                cur.execute("UPDATE user SET first_name = ? WHERE username = ?;", (newFirstName, username))
                                conn.commit()
                                test=input("Other changes ? : Y/N  ")
                                i=3
                                if test.lower()=='y':
                                    i=3
                                else:
                                    for row in cur.execute("SELECT * FROM user"):
                                        print(row)
                                    element='5'
                            else:
                                i+=1
                                    
                    case '3' :
                        i=0
                        while i<3:
                            newLastName=input("New Last Name : ")
                            resp=input("Add this last name in the db ? Y/N : ")
                            if resp.lower() == 'y': 
                                cur.execute("UPDATE user SET last_name = ? WHERE username = ?;", (newLastName, username))
                                conn.commit()                         
                                test=input("Other changes ? : Y/N  ")
                                i=3
                                if test.lower()=='y':
                                    i=3
                                else:
                                    for row in cur.execute("SELECT * FROM user"):
                                        print(row)
                                    element='5'
                            else:
                                i+=1
                    case '4' :
                        rep=input("Reset password? Y/N :  ")
                        if rep.lower()=='y':
                            i=0
                            pwd_check=False
                            while pwd_check==False:
                                newPassword=getpass.getpass()
                                newPassword=hashlib.sha256(newPassword.encode('utf-8')).hexdigest()
                                print("Confirmation of password : ")
                                pwd2=getpass.getpass()
                                pwd2=hashlib.sha256(pwd2.encode('utf-8')).hexdigest()
                                if newPassword==pwd2:
                                    pwd_check=True
                                    resp=input("Add this password in the db ? Y/N : ")
                                    if resp.lower() == 'y':
                                        cur.execute("UPDATE user SET password = ? WHERE username = ?;", (newPassword, username))
                                        conn.commit()
                                        test=input("Other changes ? : Y/N  ")
                                        if test.lower()=='y':
                                            continue
                                        else:
                                            for row in cur.execute("SELECT * FROM user"):
                                                print(row)
                                            element='5'
                                else:
                                    print("Incorrect password")
                                    print()
                                    i+=1
                                    if i==3:
                                        print("Too many tries")
                                        break
                    case '5' :
                        print("CONNECTION SHUTDOWN")
                        element='5'
                        break
                    case _:
                        print("Error match/case")
    else:
        if username=='Admin':
            print("Admin isn't editable")
        else:
            print("Username", username, "not exist")


#########################################################################

#TODO: voir en fonction du status si il peut ou non avoir accès à la db entière ou juste à ses informations personnels

def auth(conn):
    '''
    auth(): fonction permettant de s'authentifier avant d'avoir accès au contenu de la bd
    '''
    rep=input("Do you want to authentificate ? Y/N : ")
    i=0
    while(rep.lower()=="y"):
        if i<3:
            print("AUTHENTIFICATION\n")
            
            username=input("Username : ")
            pwd=getpass.getpass()
            print("\n")
            pwd=hashlib.sha256(pwd.encode('utf-8')).hexdigest()

            result = conn.execute("SELECT * FROM user WHERE username = ? AND password = ?", (username, pwd))
            if (len(result.fetchall()) != 0):
                print("Authentification success")
                cursor = conn.execute("SELECT status FROM user WHERE username = ? AND password = ?", (username, pwd))
                status = cursor.fetchone()[0] 
                print(status)
                return True, status
            else:
                print("Authentification failed\n")
                i+=1
                if i==3:
                    rep="N"
                    print("END OF THE AUTHENTIFICATION\n")
                    return False, None




      
    
#########################################################################

 #base de donnée  
'''
-- SQLite

-- description de la table user de notre base de données
DROP TABLE user; --supprime la db pour remettre à zéro lors de nos tests

-- création des colonnes de la table user
CREATE TABLE IF NOT EXISTS user ( 
	user_id INTEGER PRIMARY KEY,
    username VARCHAR(100) UNIQUE,
	first_name VARCHAR(100),
	last_name VARCHAR(100),
	password VARCHAR(50),
	status VARCHAR(50) 
);
-- insertion des valeurs de chaque colonne d'un user
INSERT INTO user (username,first_name, last_name, password, status) 
VALUES('Sudo','sudo', 'sudo','9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08','sudo'),
('Admin1','admin', 'admin','9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08','admin'),
('Admin2','admin', 'admin','9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08','admin'),
('Admin3','admin', 'admin','9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08','admin'),
('Admin4','admin', 'admin','9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08','admin'),
('CCOUSIN','Clemence', 'COUSIN','9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08', 'patient'),
('MARRAR','Mordjane', 'ARRAR','9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08', 'patient');

---------------- POUR TESTER / MDP POUR CHAQUE USER : test -----------------------

SELECT * FROM user; 
-- afficher la table user

-- Requetes test

--DELETE FROM user WHERE pseudo is 'Admin';
--UPDATE user SET first_name = 'Michel' WHERE username = 'Clem';
--SELECT * FROM user WHERE username = 'Clem'; 

SELECT status FROM user WHERE username = 'Admin' AND password = 'test';

'''