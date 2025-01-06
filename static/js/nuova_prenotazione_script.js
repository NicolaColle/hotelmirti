// Funzione per verificare se lo stato selezionato è Italia
function verificaItalia() {
    const statoSelect = document.getElementById('cod_stato_cliente');
    const selectedStato = statoSelect.value;
    const isItalia = selectedStato === '106';
    console.log(`Il valore selezionato è Italia? ${isItalia}`);
    return isItalia;
}

// Funzione per abilitare o disabilitare i campi Regione, Provincia, e Comune
function toggleAddressFields() {
    verificaItalia();

    // Ottieni i select per Regione, Provincia, e Comune
    const regioneSelect = document.getElementById('cod_regione_cliente');
    const provinciaSelect = document.getElementById('cod_provincia_cliente');
    const comuneSelect = document.getElementById('cod_comune_cliente');

    // Abilita o disabilita i campi a seconda che lo stato sia Italia
    if (verificaItalia()) {
        // Mostra i campi e abilita la selezione
        regioneSelect.style.display = 'block';
        provinciaSelect.style.display = 'block';
        comuneSelect.style.display = 'block';
        
        regioneSelect.disabled = false;
        provinciaSelect.disabled = false;
        comuneSelect.disabled = false;
        loadRegioni();
    } else {
        loadRegioni();
        loadProvince();
        loadComuni();
        
        regioneSelect.style.display = 'block';
        provinciaSelect.style.display = 'block';
        comuneSelect.style.display = 'block';

        regioneSelect.disabled = true;
        provinciaSelect.disabled = true;
        comuneSelect.disabled = true;
    }
}

// Funzione per caricare gli stati nel menu a tendina
async function loadStati() {
    try {
        const response = await fetch('/api/stati');
        const stati = await response.json();

        const statoSelect = document.getElementById('cod_stato_cliente');

        // Aggiungi ogni stato come opzione nel select
        stati.forEach(stato => {
            const option = document.createElement('option');
            option.value = stato.cod_stato;
            option.textContent = stato.nome_stato;
            statoSelect.appendChild(option);
        });

        // Chiamato una volta che gli stati sono caricati per abilitare/disabilitare i campi
        toggleAddressFields();
    } catch (error) {
        console.error('Errore nel caricamento degli stati:', error);
    }
}

// Funzione per caricare le regioni nel menu a tendina
async function loadRegioni() {
    try {
        const response = await fetch('/api/regioni');
        const regioni = await response.json();
        const regioneSelect = document.getElementById('cod_regione_cliente');
        if(verificaItalia())
        {
            regioneSelect.innerHTML = '<option value="">Seleziona Regione</option>';  // Aggiungi l'opzione vuota per la selezione

            // Aggiungi ogni regione come opzione nel select
            regioni.forEach(regione => {
                const option = document.createElement('option');
                option.value = regione.cod_regione;
                option.textContent = regione.nome_regione;
                regioneSelect.appendChild(option);
            });
        }
        else
        {
            regioneSelect.innerHTML = '<option value="21" selected>Estero</option>';
        }
    } catch (error) {
        console.error('Errore nel caricamento delle regioni:', error);
    }
}

// Funzione per caricare le province nel menu a tendina
async function loadProvince() {
    try {
        const provinciaSelect = document.getElementById('cod_provincia_cliente');
        if(verificaItalia())
        {
            cod_regione_cliente = document.getElementById('cod_regione_cliente').value
            const response = await fetch(`/api/province/${cod_regione_cliente}`);
            const province = await response.json();
            provinciaSelect.innerHTML = '<option value="">Seleziona Provincia</option>';
            // Aggiungi ogni provincia come opzione nel select
            province.forEach(provincia => {
                const option = document.createElement('option');
                option.value = provincia.cod_provincia;
                option.textContent = provincia.nome_provincia;
                provinciaSelect.appendChild(option);
            });
        }
        else
        {
            provinciaSelect.innerHTML = '<option value="108" selected>Estero</option>';
        }
    } catch (error) {
        console.error('Errore nel caricamento delle province:', error);
    }
}

// Funzione per caricare i comuni nel menu a tendina
async function loadComuni() {
    try {
        const comuneSelect = document.getElementById('cod_comune_cliente');
        if(verificaItalia())
        {
            cod_provincia_cliente = document.getElementById('cod_provincia_cliente').value
            const response = await fetch(`/api/comuni/${cod_provincia_cliente}`);
            const comuni = await response.json();
            comuneSelect.innerHTML = '<option value="">Seleziona Comune</option>';
            // Aggiungi ogni comune come opzione nel select
            comuni.forEach(comune => {
                const option = document.createElement('option');
                option.value = comune.cod_comune;
                option.textContent = comune.nome_comune;
                comuneSelect.appendChild(option);
            });
        }
        else
        {
            comuneSelect.innerHTML = '<option value="7902" selected>Estero</option>';
        }
    } catch (error) {
        console.error('Errore nel caricamento dei comuni:', error);
    }
}

// Funzione per inizializzare il caricamento dei dati una volta che la pagina è pronta
document.addEventListener('DOMContentLoaded', function () {
    loadStati();
    loadRegioni();

    const selectregione = document.getElementById("cod_regione_cliente");
    selectregione.addEventListener("change", (selectregione) => {loadProvince();});

    const selectprovincia = document.getElementById("cod_provincia_cliente");
    selectprovincia.addEventListener("change", (selectprovincia) => {loadComuni();});

    // Aggiungi listener per la selezione dello stato
    document.getElementById('cod_stato_cliente').addEventListener('change', toggleAddressFields);
});

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

loadTipologieStanza();

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

// Listener per il submit del modulo di prenotazione
document.getElementById('booking-form').addEventListener('submit', async function (event) {
    event.preventDefault(); // Evita il refresh della pagina

    // Raccolta dati dal modulo
    const data = {
        nome_cliente: document.getElementById('nome_cliente').value,
        cognome_cliente: document.getElementById('cognome_cliente').value,
        email_cliente: document.getElementById('email_cliente').value,
        password_cliente: document.getElementById('password_cliente').value,
        cod_stato_cliente: document.getElementById('cod_stato_cliente').value,
        cod_regione_cliente: document.getElementById('cod_regione_cliente').value,
        cod_provincia_cliente: document.getElementById('cod_provincia_cliente').value,
        cod_comune_cliente: document.getElementById('cod_comune_cliente').value,
        data_nascita_cliente: document.getElementById('data_nascita_cliente').value,
        data_inizio: document.getElementById('data_inizio').value,
        data_fine: document.getElementById('data_fine').value,
        numero_stanze: document.getElementById('numero_stanze').value,
        cod_tipologia_stanza: document.getElementById('cod_tipologia_stanza').value
    };
    // Verifica che la data di check-out sia successiva alla data di check-in
    if (data.data_fine <= data.data_inizio) 
    {
        // Impediamo l'invio del modulo
        event.preventDefault();
        
        // Mostra un messaggio di errore
        alert('La data di check-out deve essere successiva alla data di check-in.');
    }

    try {
        const response = await fetch('/api/nuova_prenotazione', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        // Mostra il messaggio di conferma sotto al form
        const confirmationElement = document.getElementById('confirmation');
        const confirmationMessage = document.getElementById('confirmation-message');

        if (result.success) {
            confirmationElement.style.display = 'block';
            confirmationElement.classList.remove('alert-danger');
            confirmationElement.classList.add('alert-success');
            confirmationMessage.textContent = `${result.message} ${result.cod}`;

            // Ricarica le stanze disponibili
            loadTipologieStanza();

            // Pulisce il modulo dopo una prenotazione riuscita
            document.getElementById('booking-form').reset();
        } else {
            confirmationElement.style.display = 'block';
            confirmationElement.classList.remove('alert-success');
            confirmationElement.classList.add('alert-danger');
            confirmationMessage.textContent = result.message;
        }
    } catch (error) {
        console.error('Errore:', error);

        const confirmationElement = document.getElementById('confirmation');
        const confirmationMessage = document.getElementById('confirmation-message');

        confirmationElement.style.display = 'block';
        confirmationElement.classList.remove('alert-success');
        confirmationElement.classList.add('alert-danger');
        confirmationMessage.textContent = 'Errore nella prenotazione.';
    }
});