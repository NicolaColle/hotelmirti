# Importa il modulo per connettersi al database MySQL
import mysql.connector
# Importa la configurazione del database dal modulo config
from config import db_config

# Funzione per creare una connessione al database
def get_db_connection():
    # Crea una connessione al database utilizzando le informazioni di configurazione
    conn = mysql.connector.connect(**db_config)
    # Restituisce la connessione creata
    return conn