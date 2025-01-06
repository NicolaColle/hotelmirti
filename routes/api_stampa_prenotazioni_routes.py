from flask import Blueprint, jsonify, request
from db import get_db_connection
from bcrypt import checkpw

# Crea un Blueprint per la gestione delle rotte relative alle prenotazioni
stampa_bp = Blueprint('stampa_prenotazioni', __name__)

# Rotta per stampare le prenotazioni
@stampa_bp.route('/api/stampa_prenotazioni/', methods=['GET'])
def stampa_prenotazioni():
    try:
        # Connessione al database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Esegui la query per ottenere tutte le prenotazioni
        cursor.execute("""
            SELECT cliente.cognome_cliente, cliente.nome_cliente, cliente.email_cliente, tipo_stanza.nome_tipo_stanza, prenotazione.numero_stanze, prenotazione.data_inizio, prenotazione.data_fine, prenotazione.cod_prenotazione
            FROM prenotazione
            JOIN cliente ON prenotazione.cod_cliente_prenotazione = cliente.cod_cliente
            JOIN stanza ON prenotazione.cod_prenotazione_stanza = stanza.cod_stanza
            JOIN tipo_stanza ON stanza.cod_tipologia_stanza = tipo_stanza.cod_tipo_stanza
        """)
        
        # Recupera tutte le prenotazioni dalla query
        prenotazioni = cursor.fetchall()

        # Organizza i dati delle prenotazioni in una lista di dizionari
        result = []
        for prenotazione in prenotazioni:

            # Permette di formattare la data in formato italiano
            data_inizio_formattata = prenotazione[5].strftime("%d/%m/%Y")   
            data_fine_formattata = prenotazione[6].strftime("%d/%m/%Y")

            result.append({
                'cognome_cliente': prenotazione[0],  # Cognome del cliente
                'nome_cliente': prenotazione[1],     # Nome del cliente
                'email_cliente': prenotazione[2],    # Email del cliente
                'nome_tipo_stanza': prenotazione[3], # Nome della tipologia di stanza
                'numero_stanze': prenotazione[4],    # Numero di stanze prenotate
                'data_inizio': data_inizio_formattata,      # Data di inizio della prenotazione
                'data_fine': data_fine_formattata,        # Data di fine della prenotazione
                'cod_prenotazione': prenotazione[7]  # Codice della prenotazione
            })

        # Ritorna i dati come risposta JSON
        return jsonify(result)

    except Exception as e:
        # Gestione degli errori: in caso di eccezione, ritorna un messaggio di errore
        print(f"Errore: {e}")
        return jsonify({'success': False, 'message': 'Errore durante il caricamento delle prenotazioni'}), 500

    finally:
        # Assicurati di chiudere il cursore e la connessione al database
        cursor.close()
        conn.close()
