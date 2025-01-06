from flask import Blueprint, jsonify, request
from db import get_db_connection
from bcrypt import checkpw

# Blueprint per la gestione delle cancellazioni delle prenotazioni
cancellazione_admin_bp = Blueprint('cancellazione_prenotazione', __name__)

# Rotta per eliminare una prenotazione
@cancellazione_admin_bp.route('/api/elimina_prenotazione/<int:cod_prenotazione>/', methods=['DELETE'])
def elimina_prenotazione(cod_prenotazione):
    try:
        # Connessione al database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Recupera il codice cliente associato alla prenotazione
        cursor.execute("""
            SELECT cod_cliente
            FROM cliente
            JOIN prenotazione ON cliente.cod_cliente = prenotazione.cod_cliente_prenotazione
            WHERE cod_prenotazione = %s
        """, (cod_prenotazione,))
        cod_cliente = cursor.fetchone()

        # Verifica che il cliente esista
        cursor.execute("SELECT * FROM prenotazione WHERE cod_cliente_prenotazione = %s", (cod_cliente[0],))
        prenotazione = cursor.fetchone()

        # Recupera il codice della stanza e il numero di stanze prenotate
        cod_prenotazione_stanza = prenotazione[1]  # Supponendo che il codice stanza sia il secondo campo
        numero_stanze = prenotazione[5]  # Supponendo che il numero di stanze prenotate sia il sesto campo

        # Incrementa il numero di stanze disponibili per la stanza corrispondente
        cursor.execute(
            "UPDATE stanza SET stanze_disponibili = stanze_disponibili + %s WHERE cod_stanza = %s",
            (numero_stanze, cod_prenotazione_stanza)
        )

        # Esegui la query per eliminare la prenotazione
        cursor.execute("""
            DELETE FROM prenotazione WHERE cod_prenotazione = %s
        """, (cod_prenotazione,))

        # Elimina il cliente associato alla prenotazione
        cursor.execute("DELETE FROM cliente WHERE cod_cliente = %s", (cod_cliente[0],))

        # Conferma le modifiche al database
        conn.commit()

        # Verifica se la prenotazione è stata eliminata con successo
        if cursor.rowcount > 0:
            return jsonify({'success': True, 'message': 'Prenotazione eliminata'})
        else:
            # Restituisce un messaggio di errore se la prenotazione non è stata trovata
            return jsonify({'success': False, 'message': 'Prenotazione non trovata'}), 404

    except Exception as e:
        # Gestisce eventuali errori durante l'operazione
        print(f"Errore: {e}")
        return jsonify({'success': False, 'message': 'Errore durante la cancellazione della prenotazione'}), 500

    finally:
        # Chiude il cursore e la connessione al database
        cursor.close()
        conn.close()