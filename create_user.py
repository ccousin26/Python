import logging
import random 
import datetime
import hashlib

def create(conn, status, username_co):
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
        current_date = datetime.datetime.today()
        logging.warning('[ %s ], %s, Patient in create_user, access denied', username_co, current_date)

    elif status == "doctor":
        print("You can't create user as a doctor.")
        current_date = datetime.datetime.today()
        logging.warning('[ %s ], %s, Doctor in create_user, access denied', username_co, current_date)
    else:
        while(rep.lower() == "y" and status_user == None): #permet de récupérer la lettre, peut importe la majuscule ou non.
            if i<3:
                print("USER CREATION\n")
                print("STATUS")
                print("1 - sudo")
                print("2 - admin")
                print("3 - patient")
                print("4 - doctor")
                print("else - EXIT")
                status_user = input("status number : ")
                print()
                match status_user : 
                    case '1':
                        if status == 'sudo':
                            status_user = 'sudo'
                            medical_data = None
                        else :
                            current_date = datetime.datetime.today()
                            logging.warning('[ %s ], %s, Sudo creation not allowed', username_co, current_date)
                            print("Unauthorized")
                            i+=1
                            break
                    case '2':
                        if status == 'sudo':
                            status_user = 'admin'
                            medical_data=None
                        else :
                            current_date = datetime.datetime.today()
                            logging.warning('[ %s ], %s, Admin creation not allowed', username_co, current_date)
                            print("Unauthorized")
                            break
                    case '3':
                        if status == 'sudo' or status == 'admin':
                            status_user = 'patient'
                            medical_data="Medical file"
                            print("Unauthorized")
                        else :
                            print("Unauthorized")
                            break
                    case '4':
                        if status == 'sudo' or status == 'admin':
                            status_user = 'doctor'
                            medical_data="Patient list"
                        else :
                            print("Unauthorized")
                            break
                    case _:
                        break
                if status_user == None:
                    current_date = datetime.datetime.today()
                    logging.warning('[ %s ], %s, Status is empty', username_co, current_date)
                    print('Error status is empty')
                    break
                    
                print("If you have a compound name, write everything attached")
                print("Example : JeanMichel")
                name = input("Name : ")
                if name == '':
                    print('Error name is empty')
                lastname = input("Last name : ")
                if lastname == '':
                    print('Error lastname is empty')
                    current_date = datetime.datetime.today()
                    logging.erroe('[ %s ], %s, User creation failed >> name/lastname empty', username_co, current_date)

                x = name.isalpha()
                y = lastname.isalpha()
                if x == True and y == True :
                    username = name[0] + name[1] + lastname #concatenation du prénom et nom.
                    #requete sql qui permet de selectionner le prénom du user en se basant sur son username. Si la requete aboutit, alors l'utilisateur existe déjà.
                    cur.execute("SELECT first_name, last_name FROM user WHERE username = ?", (username,)) 
                    data = cur.fetchall() #lance la requete.
                else :
                    print("Error it's not just letters")
                    current_date = datetime.datetime.today()
                    logging.erroe('[ %s ], %s, User creation failed >> not just letters', username_co, current_date)
                    break

                '''
                fetchall retourne un tableau, en vérifiant la taille du tableau on sait alors si la requete à aboutit à un résultat non null.
                '''
                
                if len(data) != 0: 
                    current_date = datetime.datetime.today()
                    logging.warning('[ %s ], %s, username already exist', username_co, current_date)
                    print("username", username, "already exist !")
                    status_user=None
                    i+=1
                    if i==3:
                        current_date = datetime.datetime.today()
                        logging.error('[ %s ], %s, Creation of user failed', username_co, current_date)
                        print("Too many tries")
                        break
                else:              
                    pwd = generatePassword(9)
                    print()
                    print("------| Adding user |------")
                    print("Username :      ", username)
                    print("Name :          ", name)
                    print("Last name :     ", lastname)
                    print("Your password : ", pwd)
                    print("Status :        ", status_user)
                    date = datetime.date.today()
                    print("Creation Date : ", date)
                    print("Medical data :  ", medical_data)
                    print("---------------------------")
                    print()
                    current_date = datetime.datetime.today()# pk t'as fait ca?
                    logging.info('[ %s ], %s, User %s generated', username_co, current_date, username)
                    pwd = hashlib.sha256(pwd.encode('utf-8')).hexdigest() #permet de hasher le pwd avant la sauvegarde dans la bd
                    #updated_passwd_date= datetime.today()
                    isPasswdNeedToChange = 0
                    resp=input("Add this user in the db ? Y/N : ")
                    if resp.lower() == 'y':
                        cur.execute("INSERT INTO user VALUES(NULL,?,?,?,?,?,?,?,?,?)", (username,name,lastname,pwd,status_user,date,medical_data,current_date,isPasswdNeedToChange)) #ajoute l'utilisateur à la db en passant en argument ses informations
                        conn.commit() #envoyer la requete
                        current_date = datetime.datetime.today()
                        logging.info('[ %s ], %s, User %s add in db.sqlite', username_co, current_date, username)
                        print()
                        print("------| USER ADD |------")
                        data = cur.execute("SELECT * FROM user WHERE username = ?", (username,)) #affiche la table
                        for row in data:
                            print("Id:           ", row[0])
                            print("Pseudo:       ", row[1])
                            print("First Name:   ", row[2])
                            print("Second Name:  ", row[3])
                            print("Password :    ", row[4])
                            print("Status :      ", row[5])
                            print("Last update : ", row[6])
                            print("Data :        ", row[7])
                        print("---------------------------")
                        print()
                    else:
                        current_date = datetime.datetime.today()
                        logging.info('[ %s ], %s, User generated not add in db.sqlite', username_co, current_date)
                        rep=input("Do you want to create another user ? Y/N  : ")
                        if rep.lower()=='y':
                            current_date = datetime.datetime.today()
                            logging.info('[ %s ], %s, New user creation', username_co, current_date)
                            i=0
                            status_user=None
                        else :
                            return 0                
                    

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
        
