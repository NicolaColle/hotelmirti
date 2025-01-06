from flask import Blueprint, render_template, flash, session, redirect, url_for

# Crea un Blueprint per la gestione delle rotte delle pagine
page_blueprint = Blueprint('pages', __name__)

# Rotta per la home page
@page_blueprint.route('/')
def home():
    return render_template('index.html')

# Rotta per la pagina dei servizi offerti
@page_blueprint.route('/servizi_offerti')
def servizi_offerti():
    return render_template('servizi_offerti.html')

# Rotta per la pagina della nuova prenotazione
@page_blueprint.route('/nuova_prenotazione')
def nuova_prenotazione():
    return render_template('nuova_prenotazione.html')

# Rotta per la pagina di modifica prenotazione
@page_blueprint.route('/modifica_prenotazione')
def modifica_prenotazione():
    return render_template('modifica_prenotazione.html')

# Rotta per la pagina di cancellazione prenotazione
@page_blueprint.route('/cancella_prenotazione')
def cancella_prenotazione():
    return render_template('cancella_prenotazione.html')

# Rotta per la pagina della privacy policy
@page_blueprint.route('/privacy_policy')
def privacy_policy():
    return render_template('privacy_policy.html')

# Rotta per la dashboard dell'amministratore
@page_blueprint.route('/admin_dashboard')
def admin_dashboard():
    # Verifica se l'utente è un amministratore
    if not session.get('is_admin'):
        flash('Accesso non autorizzato.', 'danger')
        return redirect(url_for('pages.home'))
    return render_template('admin_dashboard.html')

# Rotta per la pagina di stampa delle prenotazioni
@page_blueprint.route('/stampa_prenotazioni')
def stampa_prenotazioni():
    # Verifica se l'utente è un amministratore
    if session.get('is_admin'):
        return render_template('stampa_prenotazioni.html')
    else:
        flash('Accesso non autorizzato.', 'danger')
        return redirect(url_for('pages.home'))

# Rotta per la pagina di modifica prenotazione dell'amministratore
@page_blueprint.route('/modifica_prenotazione_admin/<int:cod_prenotazione>/')
def modifica_prenotazione_admin(cod_prenotazione):
    # Verifica se l'utente è un amministratore
    if session.get('is_admin'):
        return render_template('modifica_prenotazione_admin.html')
    else:
        flash('Accesso non autorizzato.', 'danger')
        return redirect(url_for('pages.home'))

# Rotta per il logout
@page_blueprint.route("/logout")
def logout():
    # Rimuove i dati di sessione dell'amministratore
    session.pop("is_admin", None)
    session.pop("admin_id", None)
    return redirect(url_for("pages.home"))