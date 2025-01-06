from flask import Blueprint, jsonify, request
from db import get_db_connection
from bcrypt import checkpw

# Blueprint per la gestione delle cancellazioni
cancellazione_bp = Blueprint('cancellazione', __name__)

# Rotta per cancellare una prenotazione
@cancellazione_bp.route('/api/cancella_prenotazione/<string:email_cliente>/<string:cod_prenotazione_cliente>', methods=['DELETE'])
def cancella_prenotazione_esistente(email_cliente, cod_prenotazione_cliente):
    try:
        # Ottieni la password inviata dal client dal corpo della richiesta
        password_cliente = request.json.get('password_cliente')

        # Connessione al database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Verifica se il cliente esiste nel database
        cursor.execute("SELECT * FROM cliente JOIN prenotazione ON cliente.cod_cliente = prenotazione.cod_cliente_prenotazione WHERE email_cliente = %s and prenotazione.cod_prenotazione = %s", (email_cliente, cod_prenotazione_cliente))
        cliente = cursor.fetchone()  # Recupera i dettagli del cliente

        print(cliente)  # Debug: Visualizza i dettagli del cliente trovato

        # Se il cliente non esiste, restituisci un messaggio di errore
        if not cliente:
            return jsonify({'success': False, 'message': 'Cliente non trovato'}), 404

        print(f"Password memorizzata: {cliente[4]}")  # Debug: Mostra la password hashata salvata
        print(f"Password inserita: {password_cliente}")  # Debug: Mostra la password inviata dal client

        # Verifica se la password inserita corrisponde a quella hashata memorizzata
        if not checkpw(password_cliente.encode('utf-8'), cliente[4].encode('utf-8')):
            return jsonify({'success': False, 'message': 'Password errata'}), 403

        # Recupera il codice cliente
        cod_cliente = cliente[0]

        # Verifica se il cliente ha prenotazioni esistenti
        cursor.execute("SELECT * FROM prenotazione WHERE cod_cliente_prenotazione = %s AND cod_prenotazione = %s", (cod_cliente, cod_prenotazione_cliente))
        prenotazione = cursor.fetchone()  # Recupera i dettagli della prenotazione

        # Se non ci sono prenotazioni, restituisci un messaggio di errore
        if not prenotazione:
            return jsonify({'success': False, 'message': 'Nessuna prenotazione trovata per questo cliente'}), 404

        # Recupera il codice stanza e il numero di stanze prenotate
        cod_prenotazione_stanza = prenotazione[1]  # Supponendo che cod_stanza sia il secondo campo
        numero_stanze = prenotazione[5]  # Supponendo che il numero di stanze sia il sesto campo

        # Aggiorna il numero di stanze disponibili, incrementandolo
        cursor.execute(
            "UPDATE stanza SET stanze_disponibili = stanze_disponibili + %s WHERE cod_stanza = %s",
            (numero_stanze, cod_prenotazione_stanza)
        )

        # Elimina la prenotazione associata al cliente
        cursor.execute("DELETE FROM prenotazione WHERE cod_cliente_prenotazione = %s", (cod_cliente,))

        # Elimina il cliente dal database
        cursor.execute("DELETE FROM cliente WHERE cod_cliente = %s", (cod_cliente,))

        # Conferma le modifiche
        conn.commit()

        # Restituisci una risposta di successo
        return jsonify({'success': True, 'message': 'Prenotazione cancellata con successo!'})

    except Exception as e:
        # Gestione degli errori: stampa e restituisci un messaggio di errore
        print(f"Errore: {e}")
        return jsonify({'success': False, 'message': 'Errore durante la cancellazione della prenotazione'}), 500

    finally:
        # Chiudi il cursore e la connessione al database
        cursor.close()
        conn.close()