// Funzione per caricare le tipologie di stanza
const loadTipologieStanza = async () => {
    try {
        console.log("Caricamento delle tipologie di stanza...");
        const response = await fetch("/api/tipologie_stanza");
        console.log("Risposta ricevuta:", response);

        if (!response.ok) {
            throw new Error(`Errore HTTP: ${response.status}`);
        }

        const data = await response.json();
        console.log("Dati ricevuti:", data);

        const tipologiaSelect = document.getElementById("cod_tipologia_stanza");
        tipologiaSelect.innerHTML = '';

        if (data.length === 0) {
            alert('Nessuna tipologia di stanza disponibile');
            return;
        }

        // Aggiungi le opzioni nel menu a tendina
        data.forEach(tipologia => {
            const option = document.createElement('option');
            option.value = tipologia.cod_tipo_stanza;
            option.textContent = tipologia.nome_tipo_stanza;
            tipologiaSelect.appendChild(option);
        });

        // Carica la disponibilità per la prima tipologia di stanza
        if (tipologiaSelect.value) {
            updateNumeroStanzeOptions(tipologiaSelect.value);
        }
    } catch (error) {
        console.error('Errore nel caricamento delle tipologie di stanza:', error);
        alert('Errore nel caricamento delle tipologie di stanza.');
    }
};

// Funzione per caricare il numero massimo di stanze disponibili per la tipologia selezionata
const updateNumeroStanzeOptions = async (codStanza) => {
    try {
        const response = await fetch(`/api/stanze_disponibili/${codStanza}`);
        const data = await response.json();

        const numeroStanzeInput = document.getElementById("numero_stanze");
        const stanzeDisponibiliInfo = document.getElementById("stanze_disponibili_info");

        // Aggiorna l'attributo 'max' e il messaggio informativo
        if (data.stanze_disponibili > 0) {
            numeroStanzeInput.max = data.stanze_disponibili;
            stanzeDisponibiliInfo.textContent = `Massimo disponibile: ${data.stanze_disponibili} stanze`;
        } else {
            numeroStanzeInput.max = 0;
            stanzeDisponibiliInfo.textContent = 'Nessuna stanza disponibile';
        }
    } catch (error) {
        console.error('Errore nel caricamento del numero di stanze disponibili:', error);
        alert('Errore nel caricamento delle stanze disponibili.');
    }
};

// Event listener per aggiornare la disponibilità quando si cambia la tipologia di stanza
document.getElementById("cod_tipologia_stanza").addEventListener("change", (event) => {
    const codStanza = event.target.value;
    if (codStanza) {
        updateNumeroStanzeOptions(codStanza);
    }
});

// Funzione per caricare i dettagli della prenotazione
document.getElementById('load-booking').addEventListener('click', async function () {
    
    // Crea un oggetto con email e password dell'utente
    const email_password_prenotazione = {
        email_cliente: document.getElementById('email_cliente').value,
        password_cliente: document.getElementById('password_cliente').value,
        prenotazione_cliente: document.getElementById('cod_prenotazione_cliente').value,
    };

    try {
        await
        loadTipologieStanza();
        // Effettua una richiesta POST per ottenere i dettagli della prenotazione
        const response = await fetch('/get_booking', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(email_password_prenotazione)
        });

        const data = await response.json();

        // Se i dati sono validi, mostra i dettagli della prenotazione
        if (data.cod_cliente) {
            document.getElementById('cod_cliente').value = data.cod_cliente;
            document.getElementById('nome_cliente').value = data.nome_cliente;
            document.getElementById('cognome_cliente').value = data.cognome_cliente;
            document.getElementById('data_nascita_cliente').value = data.data_nascita_cliente;
            document.getElementById('stato_cliente').value = data.stato_cliente;
            document.getElementById('regione_cliente').value = data.regione_cliente;
            document.getElementById('provincia_cliente').value = data.provincia_cliente;
            document.getElementById('comune_cliente').value = data.comune_cliente;
            document.getElementById('cod_prenotazione').value = data.cod_prenotazione;
            
            // Popola i campi modificabili
            document.getElementById('data_inizio').value = data.data_inizio;
            document.getElementById('data_fine').value = data.data_fine;
            document.getElementById('cod_tipologia_stanza').value = data.cod_prenotazione_stanza;
            document.getElementById('numero_stanze').value = data.numero_stanze;

            // Mostra la sezione con i dettagli della prenotazione
            document.getElementById('booking-details').style.display = 'block';
        } else {
            // Mostra un messaggio di errore se i dati non sono validi
            document.getElementById('error-message').textContent = data.error || "Errore sconosciuto";
            document.getElementById('error-message').style.display = 'block';
        }
    } catch (error) {
        // Gestisce errori durante il caricamento
        console.error('Errore durante il caricamento:', error);
        document.getElementById('error-message').textContent = "Errore durante il caricamento dei dati";
        document.getElementById('error-message').style.display = 'block';
    }
});

// Funzione per inviare i dati modificati al server quando si preme "Modifica Prenotazione"
document.getElementById("modify-booking-form").addEventListener("submit", function (event) {
    event.preventDefault();  // Previene il comportamento di invio del modulo
    const errorMessage = document.getElementById("error-message");
    const confirmationMessage = document.getElementById("confirmation-message");
    const confirmation = document.getElementById("confirmation");

    // Nasconde eventuali messaggi di errore o conferma precedenti
    errorMessage.style.display = 'none';
    confirmation.style.display = 'none';

    // Ottiene i dati del modulo
    const email_cliente = document.getElementById("email_cliente").value;
    const password_cliente = document.getElementById("password_cliente").value;
    const formData = Object.fromEntries(new FormData(this).entries());

    // Aggiunge la password ai dati del modulo
    formData.password_cliente = password_cliente;

    // Assicura che la data di nascita sia nel formato corretto
    if (formData.data_nascita_cliente) {
        const dataNascita = new Date(formData.data_nascita_cliente);
        formData.data_nascita_cliente = dataNascita.toISOString().split('T')[0];
    }

    // Invia la modifica della prenotazione al server
    fetch(`/modifica_prenotazione/${encodeURIComponent(email_cliente)}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData)
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Mostra il messaggio di conferma se la modifica è avvenuta con successo
                confirmationMessage.textContent = data.message;
                confirmation.style.display = 'block';
                document.getElementById("booking-details").style.display = 'none';  // Nasconde i dettagli modificabili
                document.getElementById("modify-booking-form").reset();  // Resetta il modulo
            } else {
                // Mostra un messaggio di errore in caso di problemi
                errorMessage.textContent = data.message;
                errorMessage.style.display = 'block';
            }
        })
        .catch(error => {
            // Gestisce errori durante la modifica della prenotazione
            errorMessage.textContent = "Errore nella modifica della prenotazione.";
            errorMessage.style.display = 'block';
            console.error("Errore nella modifica:", error);
        });
});