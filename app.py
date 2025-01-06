# Importa le librerie necessarie da Flask e altre dipendenze
from flask import Flask, render_template, request, jsonify
from datetime import datetime
from flask_cors import CORS  # Per gestire le richieste cross-origin
from datetime import timedelta  # Per impostare scadenze temporali
import mysql.connector  # Per connettersi al database MySQL

# Importa i blueprint per le varie route dell'applicazione
from routes.page_routes import page_blueprint
from routes.api_prenotazione_routes import prenotazione_bp
from routes.api_modifica_routes import modifica_bp
from routes.api_cancellazione_routes import cancellazione_bp
from routes.api_login_admin import admin_bp
from routes.api_stampa_prenotazioni_routes import stampa_bp
from routes.api_modifica_admin_routes import modifica_admin_bp
from routes.api_cancellazione_admin_routes import cancellazione_admin_bp

# Crea l'app Flask
app = Flask(__name__)
# Abilita CORS per permettere la comunicazione cross-origin
CORS(app)

# Imposta la durata della sessione admin a 5 minuti
app.permanent_session_lifetime = timedelta(minutes=5)

# Imposta una chiave segreta per gestire sessioni sicure
app.secret_key = 'operativo'

# Registra i blueprint per gestire diverse funzionalità e route dell'app
app.register_blueprint(page_blueprint)
app.register_blueprint(prenotazione_bp)
app.register_blueprint(modifica_bp)
app.register_blueprint(cancellazione_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(stampa_bp)
app.register_blueprint(modifica_admin_bp)
app.register_blueprint(cancellazione_admin_bp)

# Se il file viene eseguito direttamente, avvia il server Flask
if __name__ == '__main__':
    # Avvia il server Flask ascoltando su tutte le interfacce e sulla porta 3000
    app.run(host='0.0.0.0', port=3000, debug=True)