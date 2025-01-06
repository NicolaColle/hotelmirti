from flask import Blueprint, jsonify, request
from db import get_db_connection
from bcrypt import hashpw, checkpw

# Creazione di un Blueprint per le rotte relative alla modifica delle prenotazioni da parte degli amministratori
modifica_admin_bp = Blueprint('modifica_prenotazione', __name__)

# Rotta per ottenere i dettagli completi della prenotazione e del cliente tramite il codice prenotazione
@modifica_admin_bp.route('/get_booking_admin', methods=['POST'])
def crea_prenotazione():
    data = request.json  # Ottiene i dati inviati dal client in formato JSON
    cod_prenotazione = data.get('cod_prenotazione')  # Recupera il codice prenotazione dai dati

    # Connessione al database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Query per ottenere i dettagli della prenotazione e del cliente associato
    query = """
        SELECT 
            cliente.cod_cliente, cliente.nome_cliente, cliente.cognome_cliente, cliente.email_cliente, cliente.hashed_password_cliente,
            stato.nome_stato, regione.nome_regione, provincia.nome_provincia, comune.nome_comune,
            cliente.data_nascita_cliente, prenotazione.cod_prenotazione, prenotazione.data_inizio, prenotazione.data_fine, prenotazione.cod_prenotazione_stanza, prenotazione.numero_stanze
        FROM cliente
        JOIN prenotazione ON cliente.cod_cliente = prenotazione.cod_cliente_prenotazione
        LEFT JOIN stato ON cliente.cod_stato_cliente = stato.cod_stato
        LEFT JOIN regione ON cliente.cod_regione_cliente = regione.cod_regione
        LEFT JOIN provincia ON cliente.cod_provincia_cliente = provincia.cod_provincia
        LEFT JOIN comune ON cliente.cod_comune_cliente = comune.cod_comune
        WHERE prenotazione.cod_prenotazione = %s
    """
    cursor.execute(query, (cod_prenotazione,))  # Esegue la query con il codice prenotazione
    booking = cursor.fetchone()  # Recupera i risultati della query

    # Chiude la connessione al database
    cursor.close()
    conn.close()

    # Se la prenotazione esiste, restituisce i dettagli
    if booking:
        response = {
            "cod_cliente": booking[0],
            "nome_cliente": booking[1],
            "cognome_cliente": booking[2],
            "email_cliente": booking[3],
            "password_cliente": booking[4],
            "stato_cliente": booking[5],
            "regione_cliente": booking[6],
            "provincia_cliente": booking[7],
            "comune_cliente": booking[8],
            "data_nascita_cliente": booking[9].strftime('%Y-%m-%d') if booking[9] else None,
            "cod_prenotazione": booking[10],
            "data_inizio": booking[11].strftime('%Y-%m-%d') if booking[11] else None,
            "data_fine": booking[12].strftime('%Y-%m-%d') if booking[12] else None,
            "cod_prenotazione_stanza": booking[13],
            "numero_stanze": booking[14]
        }
        return jsonify(response)

    # Se la prenotazione non esiste, restituisce un errore
    return jsonify({"error": "Prenotazione non trovata"}), 404

# Rotta per modificare i dettagli della prenotazione e del cliente
@modifica_admin_bp.route('/modifica_prenotazione_admin/<int:cod_prenotazione>', methods=['POST'])
def modifica_prenotazione_esistente(cod_prenotazione):
    data = request.json  # Ottiene i dati inviati dal client in formato JSON

    # Recupera i dettagli del cliente e della prenotazione dai dati
    cod_cliente = data['cod_cliente']
    nome_cliente = data['nome_cliente']
    cognome_cliente = data['cognome_cliente']
    stato_cliente = data['stato_cliente']
    regione_cliente = data['regione_cliente']
    provincia_cliente = data['provincia_cliente']
    comune_cliente = data['comune_cliente']
    data_nascita_cliente = data['data_nascita_cliente']
    data_inizio = data['data_inizio']
    data_fine = data['data_fine']
    cod_prenotazione_stanza = data['cod_tipologia_stanza']
    numero_stanze = data['numero_stanze']

    try:
        # Connessione al database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Query per ottenere il codice della prenotazione della stanza con disponibilità
        query = '''
        SELECT prenotazione.cod_prenotazione_stanza, prenotazione.numero_stanze
        FROM prenotazione
        WHERE cod_prenotazione = %s
        '''
        cursor.execute(query, (cod_prenotazione,))
        stanza_prenotata = cursor.fetchone()

        if stanza_prenotata[0] == cod_prenotazione_stanza:
            if stanza_prenotata[1] > numero_stanze:
                stanza_disponibile = stanza_prenotata[1] - numero_stanze
                # Aggiorna il numero di stanze disponibili, incrementandolo
                cursor.execute(
                "UPDATE stanza SET stanze_disponibili = stanze_disponibili + %s WHERE cod_stanza = %s",
                (stanza_disponibile, cod_prenotazione_stanza))
            else:
                stanza_disponibile = numero_stanze - stanza_prenotata[1]
                # Aggiorna il numero di stanze disponibili, diminuendolo
                cursor.execute(
                "UPDATE stanza SET stanze_disponibili = stanze_disponibili - %s WHERE cod_stanza = %s",
                (stanza_disponibile, cod_prenotazione_stanza))
        else:
            # Aggiorna il numero di stanze iniziale
            cursor.execute(
            "UPDATE stanza SET stanze_disponibili = stanze_disponibili + %s WHERE cod_stanza = %s",
            (stanza_prenotata[1], stanza_prenotata[0]))
            cursor.execute(
            "UPDATE stanza SET stanze_disponibili = stanze_disponibili - %s WHERE cod_stanza = %s",
            (numero_stanze, cod_prenotazione_stanza))

        # Recupera i codici di stato, regione, provincia e comune dai rispettivi nomi
        cursor.execute("SELECT cod_stato FROM stato WHERE nome_stato = %s", (stato_cliente,))
        stato = cursor.fetchone()
        cursor.execute("SELECT cod_regione FROM regione WHERE nome_regione = %s", (regione_cliente,))
        regione = cursor.fetchone()
        cursor.execute("SELECT cod_provincia FROM provincia WHERE nome_provincia = %s", (provincia_cliente,))
        provincia = cursor.fetchone()
        cursor.execute("SELECT cod_comune FROM comune WHERE nome_comune = %s", (comune_cliente,))
        comune = cursor.fetchone()

        # Recupera l'email del cliente associato alla prenotazione
        cursor.execute("""
            SELECT email_cliente
            FROM prenotazione
            JOIN cliente ON cliente.cod_cliente = prenotazione.cod_cliente_prenotazione
            WHERE cod_prenotazione = %s
        """, (cod_prenotazione,))
        email_cliente = cursor.fetchone()

        # Aggiorna i dettagli del cliente nel database
        cursor.execute("""
            UPDATE cliente
            SET nome_cliente = %s, cognome_cliente = %s, cod_stato_cliente = %s, cod_regione_cliente = %s,
                cod_provincia_cliente = %s, cod_comune_cliente = %s, data_nascita_cliente = %s
            WHERE email_cliente = %s
        """, (nome_cliente, cognome_cliente, stato[0], regione[0], provincia[0], comune[0],
              data_nascita_cliente, email_cliente[0]))

        # Aggiorna i dettagli della prenotazione nel database
        cursor.execute("""
            UPDATE prenotazione
            SET data_inizio = %s, data_fine = %s, numero_stanze = %s, cod_prenotazione_stanza = %s
            WHERE cod_prenotazione = %s
        """, (data_inizio, data_fine, numero_stanze, cod_prenotazione_stanza, cod_prenotazione))

        # Salva le modifiche nel database
        conn.commit()

        # Chiude la connessione al database
        cursor.close()
        conn.close()

        # Restituisce un messaggio di successo
        return jsonify({"success": True, "message": "Prenotazione aggiornata con successo"})

    except Exception as e:
        # Gestisce eventuali errori e restituisce un messaggio di errore
        print(f"Errore: {e}")
        return jsonify({"success": False, "message": "Errore durante l'aggiornamento della prenotazione"}), 500