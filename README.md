# TobiChallenge ICT Days Vodafone Hackathon

## Recursion Fairies

Il nostro gruppo ha deciso di lavorare sul primo brief, ritenendo la challenge più stimolante. Sull’esempio di TOBi, abbiamo sviluppato un ChatBot “intelligente” in grado di interfacciarsi con un sistema di libretto universitario online (es: Esse3), tuttavia l’infrastruttura è scalabile, l’interfaccia è adattabile e fornisce degli strumenti per adeguarsi ai problemi più disparati.

Attualmente il nostro prototipo è in grado di supportare diverse funzioni di base come accesso ai voti, iscrizione agli esami, gestione delle tasse …

I valori aggiunti che il nostro progetto offre rispetto alle tradizionali soluzioni sono:

Language Understanding System: utilizziamo il servizio luis.ai offerto da Microsoft per l’analisi testuale e quindi il riconoscimento dei concetti chiave di un messaggio
Context Retrival: se dall’ultimo messaggio non è ben chiaro il contesto a cui ci si riferisce, vengono analizzati i messaggi nello storico alla ricerca dell’ultimo contesto valido all’interno della conversazione, e se questo contesto risulta ancora valido allora viene utilizzato. A livello tecnico questo viene implementato tramite uno stack che viene risalito man mano alla ricerca del contesto.
Context Prediction: in base ai pattern di utilizzo del sistema da parte degli utenti viene addestrata una Markov Chain in grado di prevedere il probabile comportamento futuro del singolo utente in modo da anticiparlo e ridurre il tempo necessario per ottenere le informazioni desiderate.
Dashboard: volevamo rendere disponibile all’amministratore statistiche riguardo i casi in cui l’intervento umano si rendeva necessario per sopperire alle mancanze del bot. In questo modo visualizzando le richieste più frequenti si possono decidere di sviluppare nuove funzionalità da integrare nel sistema. A livello tecnico questo è realizzato facendo un clustering dello storico degli interventi umani e generando i topic di questi clusters tramite un modello LDA.

Per installare ed eseguire il pacchetto, è necessario che i seguenti requisiti siano soddisfatti:
- Python==3.7.1
- Virtualenv==16.4.3
- Pip==19.0.3
- Chatbot framework emulator (https://github.com/microsoft/botframework-emulator)

Creare un virtaulev usando python 3.7.1
Clonare la repository da https://github.com/steber97/TobiChallenge, spostarsi nella cartella TobiChallenge/TobiChallenge, ed eseguire il comando 
`pip install -r requirements.txt`
E poi eseguire 
`spacy download it_core_news_sm`

Per allenare il modello LDA bisogna eseguire lo script train.py

Eseguire `./startserver` (consentire l’esecuzione come eseguibile come chmod +x startserver), e lasciare in esecuzione il server.
Eseguire l’app chatbot framework emulator, cliccare “open bot”, inserire come bot url “http://localhost:8000/api/messages”, lasciare vuoti i campi opzionali.
Interagire con il bot, eseguendo domande inerenti esse3.
Visitare la dashboard con un qualsiasi browser da “http://localhost:8000/”


