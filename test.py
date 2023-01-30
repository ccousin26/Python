import logging
import datetime

username_co = 'Sudo'
current_date = datetime.datetime.today()
logging.basicConfig(filename='conn.log', encoding='utf-8', level=logging.DEBUG)
logging.debug('This message should go to the log file')
logging.info('[ %s ] Connexion db.sqlite', username_co)
logging.info('[ %s ] Date/heure de connexion : %s', username_co, current_date)
logging.info('[ %s ] Date/heure de déconnexion : %s', username_co, current_date)