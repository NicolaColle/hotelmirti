from flask import Blueprint, jsonify, request
from db import get_db_connection
from bcrypt import hashpw, checkpw

# Creazione del blueprint per le rotte di modifica
modifica_bp = Blueprint('modifica', __name__)

# Rotta per ottenere i dettagli completi della prenotazione e del cliente tramite email
@modifica_bp.route('/get_booking', methods=['POST'])
def crea_prenotazione():
    # Ricezione dei dati dalla richiesta JSON
    data = request.json
    email_cliente = data.get('email_cliente')
    password_cliente = data.get('password_cliente')
    cod_prenotazione_cliente = data.get('prenotazione_cliente')
    
    # Connessione al database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Query per ottenere i dettagli della prenotazione e del cliente
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
        WHERE cliente.email_cliente = %s
        and prenotazione.cod_prenotazione = %s
    """
    cursor.execute(query, (email_cliente, cod_prenotazione_cliente))
    booking = cursor.fetchone()

    # Verifica se la password fornita corrisponde a quella memorizzata (hash)
    if not checkpw(password_cliente.encode('utf-8'), booking[4].encode('utf-8')):
        return jsonify({'success': False, 'message': 'Password errata'}), 403

    cursor.close()
    conn.close()

    # Preparazione della risposta con i dettagli della prenotazione
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

    # Restituisce un errore se la prenotazione non è trovata
    return jsonify({"error": "Prenotazione non trovata"}), 404

# Rotta per modificare i dettagli della prenotazione e del cliente
@modifica_bp.route('/modifica_prenotazione/<string:email_cliente>', methods=['POST'])
def modifica_prenotazione_esistente(email_cliente):
    # Ricezione dei dati dalla richiesta JSON
    data = request.json
    password_cliente = data['password_cliente']  # Password inviata dal client
    cod_cliente = data['cod_cliente']
    nome_cliente = data['nome_cliente']
    cognome_cliente = data['cognome_cliente']
    stato_cliente = data['stato_cliente']
    regione_cliente = data['regione_cliente']
    provincia_cliente = data['provincia_cliente']
    comune_cliente = data['comune_cliente']
    data_nascita_cliente = data['data_nascita_cliente']
    cod_prenotazione = data['cod_prenotazione']
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
        

        # Ottenimento dei codici degli identificatori geografici dal database
        cursor.execute("SELECT cod_stato FROM stato WHERE nome_stato = %s", (stato_cliente,))
        stato = cursor.fetchone()
        cursor.execute("SELECT cod_regione FROM regione WHERE nome_regione = %s", (regione_cliente,))
        regione = cursor.fetchone()
        cursor.execute("SELECT cod_provincia FROM provincia WHERE nome_provincia = %s", (provincia_cliente,))
        provincia = cursor.fetchone()
        cursor.execute("SELECT cod_comune FROM comune WHERE nome_comune = %s", (comune_cliente,))
        comune = cursor.fetchone()

        # Aggiornamento delle informazioni del cliente
        cursor.execute("""
            UPDATE cliente
            SET nome_cliente = %s, cognome_cliente = %s, cod_stato_cliente = %s, cod_regione_cliente = %s,
                cod_provincia_cliente = %s, cod_comune_cliente = %s, data_nascita_cliente = %s
            WHERE email_cliente = %s
        """, (nome_cliente, cognome_cliente, stato[0], regione[0], provincia[0], comune[0],
              data_nascita_cliente, email_cliente))

        # Aggiornamento dei dettagli della prenotazione
        cursor.execute("""
            UPDATE prenotazione
            SET data_inizio = %s, data_fine = %s, numero_stanze = %s, cod_prenotazione_stanza = %s
            WHERE cod_prenotazione = %s
        """, (data_inizio, data_fine, numero_stanze, cod_prenotazione_stanza, data['cod_prenotazione']))

        # Conferma delle modifiche nel database
        conn.commit()
        cursor.close()
        conn.close()

        # Risposta di successo
        return jsonify({"success": True, "message": "Prenotazione aggiornata con successo"})

    except Exception as e:
        # Gestione degli errori
        print(f"Errore: {e}")
        print(f"Errore nel caricamento delle tipologie di stanza: {e}")
        return jsonify({"success": False, "message": "Errore durante l'aggiornamento della prenotazione"}), 500