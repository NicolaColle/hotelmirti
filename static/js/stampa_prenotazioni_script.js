// Funzione per caricare e stampare tutte le prenotazioni
document.addEventListener('DOMContentLoaded', async function () {
    try {
        // Effettua una richiesta per ottenere i dati delle prenotazioni
        const response = await fetch('/api/stampa_prenotazioni/');
        const data = await response.json();

        // Verifica se ci sono prenotazioni da mostrare
        if (data.length > 0) {
            // Ottieni il corpo della tabella
            const tbody = document.querySelector('tbody');

            // Cicla su tutte le prenotazioni e aggiungile alla tabella
            data.forEach(prenotazione => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${prenotazione.cognome_cliente}</td>
                    <td>${prenotazione.nome_cliente}</td>
                    <td>${prenotazione.email_cliente}</td>
                    <td>${prenotazione.nome_tipo_stanza}</td>
                    <td>${prenotazione.numero_stanze}</td>
                    <td>${prenotazione.data_inizio}</td>
                    <td>${prenotazione.data_fine}</td>
                    <td><a href="/modifica_prenotazione_admin/${prenotazione.cod_prenotazione}/">Modifica</a></td>
                    <td><button class="delete-btn" data-id="${prenotazione.cod_prenotazione}">Elimina</button></td>
                `;
                tbody.appendChild(row);
            });

            // Aggiungi evento per il bottone di eliminazione
            document.querySelectorAll('.delete-btn').forEach(button => {
                button.addEventListener('click', async function () {
                    // Ottieni l'ID della prenotazione da eliminare
                    const codPrenotazione = this.getAttribute('data-id');
                    try {
                        // Invia richiesta di eliminazione
                        const response = await fetch(`/api/elimina_prenotazione/${codPrenotazione}`, {
                            method: 'DELETE',
                        });
                        const data = await response.json();

                        // Verifica se l'eliminazione è stata effettuata con successo
                        if (data.success) {
                            // Rimuovi la riga della tabella
                            this.closest('tr').remove();
                        } else {
                            alert('Errore durante la cancellazione della prenotazione');
                        }
                    } catch (error) {
                        console.error('Errore durante la cancellazione:', error);
                    }
                });
            });
        } else {
            console.log("Nessuna prenotazione trovata.");
        }
    } catch (error) {
        console.error('Errore durante il caricamento delle prenotazioni:', error);
    }
});