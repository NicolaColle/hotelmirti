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

// Funzione per caricare i dettagli della prenotazione quando la pagina è caricata
document.addEventListener('DOMContentLoaded', async () =>{

    // Estrae il codice della prenotazione dalla URL
    const cod_prenotazione = window.location.pathname.split("/")[2];
    const cod_prenotazione_admin = {
        cod_prenotazione: cod_prenotazione,  // Crea un oggetto con il codice della prenotazione
    };

    try {
        await
        loadTipologieStanza();
        // Richiesta al server per ottenere i dettagli della prenotazione
        const response = await fetch('/get_booking_admin', {
            method: 'POST',  // Metodo POST per inviare i dati
            headers: {
                'Content-Type': 'application/json'  // Specifica il tipo di contenuto come JSON
            },
            body: JSON.stringify(cod_prenotazione_admin)  // Corpo della richiesta con il codice della prenotazione
        });

        // Converte la risposta in formato JSON
        const data = await response.json();

        if (data.cod_cliente) {
            // Se i dati sono validi, popola i campi del modulo con le informazioni della prenotazione
            document.getElementById('cod_cliente').value = data.cod_cliente;
            document.getElementById('nome_cliente').value = data.nome_cliente;
            document.getElementById('cognome_cliente').value = data.cognome_cliente;
            document.getElementById('data_nascita_cliente').value = data.data_nascita_cliente;
            document.getElementById('stato_cliente').value = data.stato_cliente;
            document.getElementById('regione_cliente').value = data.regione_cliente;
            document.getElementById('provincia_cliente').value = data.provincia_cliente;
            document.getElementById('comune_cliente').value = data.comune_cliente;
            document.getElementById('cod_prenotazione').value = data.cod_prenotazione;

            // Popola i campi modificabili come le date e il numero di stanze
            document.getElementById('data_inizio').value = data.data_inizio;
            document.getElementById('data_fine').value = data.data_fine;
            document.getElementById('cod_tipologia_stanza').value = data.cod_prenotazione_stanza;
            document.getElementById('numero_stanze').value = data.numero_stanze;

            // Mostra la sezione dei dettagli della prenotazione
            document.getElementById('booking-details').style.display = 'block';
        } else {
            // Se si verifica un errore, mostra il messaggio di errore
            document.getElementById('error-message').textContent = data.error || "Errore sconosciuto";
            document.getElementById('error-message').style.display = 'block';
        }
    } catch (error) {
        // Gestisce gli errori in caso di problemi durante la richiesta
        console.error('Errore durante il caricamento:', error);
        document.getElementById('error-message').textContent = "Errore durante il caricamento dei dati";
        document.getElementById('error-message').style.display = 'block';
    }
});

// Funzione per inviare i dati modificati al server quando si preme "Modifica Prenotazione"
document.getElementById("modify-booking-form").addEventListener("submit", function (event) {
    event.preventDefault();  // Impedisce il comportamento predefinito del form (invio della pagina)
    
    const errorMessage = document.getElementById("error-message");
    const confirmationMessage = document.getElementById("confirmation-message");
    const confirmation = document.getElementById("confirmation");

    confirmation.style.display = 'none'; // Nasconde il messaggio di conferma

    // Ottiene i dati dal modulo e li trasforma in un oggetto
    const formData = Object.fromEntries(new FormData(this).entries());
    const cod_prenotazione = document.getElementById("cod_prenotazione").value;

    // Assicurati che la data di nascita sia nel formato corretto
    if (formData.data_nascita_cliente) {
        const dataNascita = new Date(formData.data_nascita_cliente);
        formData.data_nascita_cliente = dataNascita.toISOString().split('T')[0];  // Formatta la data come YYYY-MM-DD
    }

    // Invia la modifica della prenotazione al server
    fetch(`/modifica_prenotazione_admin/${encodeURIComponent(cod_prenotazione)}`, {
        method: "POST",  // Metodo POST per inviare i dati
        headers: { "Content-Type": "application/json" },  // Specifica il tipo di contenuto come JSON
        body: JSON.stringify(formData)  // Corpo della richiesta con i dati del modulo
    })
        .then(response => response.json())  // Converte la risposta in formato JSON
        .then(data => {
            if (data.success) {
                // Se la modifica ha successo, mostra il messaggio di conferma e nasconde i dettagli della prenotazione
                confirmationMessage.textContent = data.message;
                confirmation.style.display = 'block';
                document.getElementById("booking-details").style.display = 'none';  // Nasconde i dettagli modificabili
                document.getElementById("modify-booking-form").reset();  // Resetta il modulo
            } else {
                // Se si verifica un errore, mostra il messaggio di errore
                errorMessage.textContent = data.message;
                errorMessage.style.display = 'block';
            }
        })
        .catch(error => {
            // Gestisce gli errori in caso di problemi durante la richiesta
            errorMessage.textContent = "Errore nella modifica della prenotazione.";
            errorMessage.style.display = 'block';
            console.error("Errore nella modifica:", error);
        });
});