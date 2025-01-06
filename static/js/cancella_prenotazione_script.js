// Aggiunge un event listener al pulsante per la cancellazione della prenotazione
document.getElementById("delete-booking").addEventListener("click", async function() {

    // Recupera i valori inseriti nel modulo
    const email_cliente = document.getElementById("email_cliente").value;  // Email del cliente
    const password_cliente = document.getElementById("password_cliente").value;  // Password del cliente
    const prenotazione_cliente = document.getElementById("cod_prenotazione_cliente").value //Cod prenotazione cliente

    // Verifica che tutti i campi siano stati riempiti
    if (!email_cliente || !password_cliente || !prenotazione_cliente) {
        alert("Inserisci email, password e codice della prenotazione.");
        return;  // Esce dalla funzione se i campi non sono validi
    }

    try {
        // Effettua una richiesta fetch per cancellare la prenotazione
        const response = await fetch(`/api/cancella_prenotazione/${email_cliente}/${prenotazione_cliente}`, {
            method: "DELETE",  // Metodo DELETE per la cancellazione
            headers: {
                "Content-Type": "application/json",  // Specifica che il corpo della richiesta è in formato JSON
            },
            body: JSON.stringify({
                password_cliente: password_cliente  // Invia la password nel corpo della richiesta
            })
        });

        // Converte la risposta in formato JSON
        const result = await response.json();

        // Gestisce la risposta in caso di successo o errore
        if (result.success) {
            document.getElementById("confirmation-message").innerText = result.message;  // Mostra il messaggio di conferma
            document.getElementById("confirmation").style.display = "block";  // Mostra il blocco di conferma
            document.getElementById("error").style.display = "none";  // Nasconde il blocco di errore
        } else {
            document.getElementById("error-message").innerText = result.message;  // Mostra il messaggio di errore
            document.getElementById("error").style.display = "block";  // Mostra il blocco di errore
            document.getElementById("confirmation").style.display = "none";  // Nasconde il blocco di conferma
        }
    } catch (error) {
        // Gestisce eventuali errori durante la richiesta
        document.getElementById("error-message").innerText = "Errore durante la cancellazione della prenotazione";  // Mostra il messaggio di errore generico
        document.getElementById("error").style.display = "block";  // Mostra il blocco di errore
    }
});