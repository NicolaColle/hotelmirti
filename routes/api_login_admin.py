from flask import Blueprint, jsonify, request, session, flash, redirect, url_for, render_template
from bcrypt import checkpw
from db import get_db_connection

# Blueprint per la gestione delle operazioni dell'amministratore
admin_bp = Blueprint('admin', __name__)

# Rotta per il login dell'amministratore
@admin_bp.route('/administrator', methods=['GET', 'POST'])
def login_admin():
    if request.method == 'POST':  # Se il metodo è POST, l'utente sta tentando di effettuare l'accesso
        session.permanent = True  # Rendi la sessione permanente
        email = request.form['email']  # Ottieni l'email dal form
        password = request.form['password']  # Ottieni la password dal form

        # Connessione al database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Query per verificare se l'amministratore esiste e recuperare i dettagli
        cursor.execute(
            "SELECT cod_amministratore, hashed_password_amministratore FROM amministratore WHERE email_amministratore = %s",
            (email,)
        )
        admin = cursor.fetchone()  # Recupera i dati dell'amministratore

        # Verifica se l'amministratore esiste e se la password è corretta
        if admin and checkpw(password.encode('utf-8'), admin[1].encode('utf-8')):
            # Login riuscito: salva le informazioni nella sessione
            session['is_admin'] = True  # Flag per indicare che l'utente è amministratore
            session['admin_id'] = admin[0]  # Salva l'ID dell'amministratore nella sessione
            flash('Accesso effettuato con successo.', 'success')  # Messaggio di successo
            return redirect(url_for('pages.admin_dashboard'))  # Reindirizza alla dashboard dell'amministratore
        else:
            # Credenziali errate: mostra un messaggio di errore
            flash('Credenziali non valide.', 'danger')

    # Per richieste GET o in caso di errore, mostra la pagina di login
    return render_template('login_admin.html')