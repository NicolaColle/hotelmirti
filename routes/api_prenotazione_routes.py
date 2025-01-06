from flask import Blueprint, jsonify, request
from bcrypt import hashpw, gensalt
from db import get_db_connection

prenotazione_bp = Blueprint('prenotazione', __name__)

# Rotta per ottenere gli stati
@prenotazione_bp.route('/api/stati', methods=['GET'])
def get_stati():
    try:
        # Connessione al database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Query per ottenere tutti gli stati
        query = "SELECT cod_stato, nome_stato FROM stato ORDER BY nome_stato"
        cursor.execute(query)
        stati = cursor.fetchall()

        # Restituisce i dati in formato JSON
        return jsonify([{'cod_stato': s[0], 'nome_stato': s[1]} for s in stati]), 200
    except Exception as e:
        # Gestione degli errori
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Rotta per ottenere le regioni
@prenotazione_bp.route('/api/regioni', methods=['GET'])
def get_regioni():
    try:
        # Connessione al database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Query per ottenere tutte le regioni
        query = "SELECT cod_regione, nome_regione FROM regione WHERE (nome_regione != 'Estero') ORDER BY nome_regione"
        cursor.execute(query)
        regioni = cursor.fetchall()

        # Restituisce i dati in formato JSON
        return jsonify([{'cod_regione': r[0], 'nome_regione': r[1]} for r in regioni]), 200
    except Exception as e:
        # Gestione degli errori
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Rotta per ottenere le province in base alla regione
@prenotazione_bp.route('/api/province/<int:cod_regione_cliente>', methods=['GET'])
def get_province(cod_regione_cliente):
    try:
        # Connessione al database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Query per ottenere le province della regione specificata
        query = "SELECT cod_provincia, nome_provincia FROM provincia WHERE cod_regione = %s"
        cursor.execute(query, (cod_regione_cliente,))
        province = cursor.fetchall()

        # Restituisce i dati in formato JSON
        province_list = [{'cod_provincia': provincia[0], 'nome_provincia': provincia[1]} for provincia in province]
        return jsonify(province_list), 200
    except Exception as e:
        # Gestione degli errori
        return jsonify({'success': False, 'message': str(e)}), 500

# Rotta per ottenere i comuni in base alla provincia
@prenotazione_bp.route('/api/comuni/<int:cod_provincia_cliente>', methods=['GET'])
def get_comuni(cod_provincia_cliente):
    try:
        # Connessione al database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Query per ottenere i comuni della provincia specificata
        query = "SELECT cod_comune, nome_comune FROM comune WHERE cod_provincia = %s"
        cursor.execute(query, (cod_provincia_cliente,))
        comuni = cursor.fetchall()

        # Restituisce i dati in formato JSON
        comuni_list = [{'cod_comune': comune[0], 'nome_comune': comune[1]} for comune in comuni]
        return jsonify(comuni_list), 200
    except Exception as e:
        # Gestione degli errori
        return jsonify({'success': False, 'message': str(e)}), 500

# Rotta per ottenere le tipologie di stanza disponibili
@prenotazione_bp.route('/api/tipologie_stanza', methods=['GET'])
def get_tipologie_stanza():
    try:
        # Connessione al database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Query per ottenere solo le tipologie di stanza con disponibilità
        query = '''
        SELECT tipo_stanza.cod_tipo_stanza, tipo_stanza.nome_tipo_stanza
        FROM tipo_stanza
        JOIN stanza ON tipo_stanza.cod_tipo_stanza = stanza.cod_tipologia_stanza
        WHERE stanza.stanze_disponibili > 0
        GROUP BY tipo_stanza.cod_tipo_stanza, tipo_stanza.nome_tipo_stanza
        '''
        cursor.execute(query)
        tipologie = cursor.fetchall()

        # Restituisce i dati in formato JSON
        return jsonify([{"cod_tipo_stanza": t[0], "nome_tipo_stanza": t[1]} for t in tipologie]), 200
    except Exception as e:
        # Gestione degli errori
        print(f"Errore nel caricamento delle tipologie di stanza: {e}")
        return jsonify({"error": "Errore nel caricamento delle tipologie di stanza"}), 500
    finally:
        cursor.close()
        conn.close()

# Rotta per ottenere il numero di stanze disponibili per una tipologia specifica
@prenotazione_bp.route('/api/stanze_disponibili/<int:cod_tipologia>', methods=['GET'])
def get_stanze_disponibili(cod_tipologia):
    try:
        # Connessione al database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Query per ottenere il numero di stanze disponibili
        query = '''
        SELECT stanze_disponibili FROM stanza 
        WHERE cod_tipologia_stanza = %s
        '''
        cursor.execute(query, (cod_tipologia,))
        result = cursor.fetchone()

        # Restituisce il numero di stanze disponibili o 0 se non trovate
        if result:
            return jsonify({"stanze_disponibili": result[0]}), 200
        else:
            return jsonify({"stanze_disponibili": 0}), 404
    except Exception as e:
        # Gestione degli errori
        print(f"Errore: {e}")
        return jsonify({"error": "Errore nel caricamento delle stanze disponibili"}), 500
    finally:
        cursor.close()
        conn.close()

# Rotta per creare una nuova prenotazione
@prenotazione_bp.route('/api/nuova_prenotazione', methods=['POST'])
def crea_prenotazione():
    # Ottieni i dati dalla richiesta JSON
    data = request.json
    nome_cliente = data.get('nome_cliente')
    cognome_cliente = data.get('cognome_cliente')
    email_cliente = data.get('email_cliente')
    password_cliente = data.get('password_cliente')
    hashed_password_cliente = hashpw(password_cliente.encode('utf-8'), gensalt()).decode('utf-8')
    cod_stato_cliente = data.get('cod_stato_cliente')
    cod_regione_cliente = data.get('cod_regione_cliente')
    cod_provincia_cliente = data.get('cod_provincia_cliente')
    cod_comune_cliente = data.get('cod_comune_cliente')
    data_nascita_cliente = data.get('data_nascita_cliente')
    data_inizio = data.get('data_inizio')
    data_fine = data.get('data_fine')
    numero_stanze = int(data.get('numero_stanze'))
    cod_tipologia_stanza = int(data.get('cod_tipologia_stanza'))

    # Validazione dei campi obbligatori
    if not all([nome_cliente, cognome_cliente, email_cliente, password_cliente, cod_stato_cliente, cod_regione_cliente,
                cod_provincia_cliente, cod_comune_cliente, data_nascita_cliente, data_inizio, data_fine, numero_stanze, cod_tipologia_stanza]):
        return jsonify({'success': False, 'message': 'Tutti i campi sono obbligatori e lo stato deve essere valido.'}), 400

    try:
        # Connessione al database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Step 1: Controlla se ci sono stanze disponibili per la tipologia selezionata
        query_check_stanze = '''
        SELECT stanze_disponibili 
        FROM stanza 
        WHERE cod_tipologia_stanza = %s
        '''
        cursor.execute(query_check_stanze, (cod_tipologia_stanza,))
        disponibilita = cursor.fetchone()

        # Verifica la disponibilità delle stanze
        if not disponibilita or disponibilita[0] < numero_stanze:
            return jsonify({'success': False, 'message': 'Stanze insufficienti per questa tipologia.'}), 400

        # Step 2: Inserisci il cliente nella tabella `cliente`
        query_cliente = """
        INSERT INTO cliente (nome_cliente, cognome_cliente, email_cliente, hashed_password_cliente, cod_stato_cliente, cod_regione_cliente, 
                             cod_provincia_cliente, cod_comune_cliente, data_nascita_cliente)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query_cliente, (nome_cliente, cognome_cliente, email_cliente, hashed_password_cliente, cod_stato_cliente, cod_regione_cliente,
                                       cod_provincia_cliente, cod_comune_cliente, data_nascita_cliente))
        conn.commit()

        # Ottieni l'ID del cliente appena inserito
        cod_cliente_prenotazione = cursor.lastrowid

        # Step 3: Inserisci la prenotazione nella tabella `prenotazione`
        query_prenotazione = """
        INSERT INTO prenotazione (cod_prenotazione_stanza, cod_cliente_prenotazione, data_inizio, data_fine, numero_stanze)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query_prenotazione, (cod_tipologia_stanza, cod_cliente_prenotazione, data_inizio, data_fine, numero_stanze))
        conn.commit()

        # Ottieni l'ID deLla prenotazione appena inserito
        cod_prenotazione_cliente = cursor.lastrowid

        # Step 4: Aggiorna il numero di stanze disponibili nella tabella `stanza`
        query_update_stanze = """
        UPDATE stanza 
        SET stanze_disponibili = stanze_disponibili - %s 
        WHERE cod_tipologia_stanza = %s
        """
        cursor.execute(query_update_stanze, (numero_stanze, cod_tipologia_stanza))
        conn.commit()

        # Restituisce il successo
        return jsonify({'success': True, 'message': 'Prenotazione effettuata con successo. Conserva il codice della prenotazione, potrà servirti per modificarla e/o cancellarla: ', 'cod': cod_prenotazione_cliente}), 200

    except Exception as e:
        conn.rollback()
        print(f"Errore: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

    finally:
        cursor.close()
        conn.close()