# 🎓 Sistema di Gestione Registro Studenti

Un sistema completo per la gestione di un registro elettronico universitario, sviluppato in Python con funzionalità di esportazione PDF e suite di test completa.

## 🔗 Repository

**GitHub**: [Vai al repository](https://github.com/andreagaspari/csc-coding-ai)  
**Progetto**: Lezione 8 - Sistema di Gestione Registro Studenti

## 📋 Panoramica

Il **Sistema di Gestione Registro Studenti** è un'applicazione console che permette di gestire un registro universitario con le seguenti funzionalità:

- ✅ Visualizzazione lista studenti con medie
- ➕ Aggiunta di nuovi studenti
- 📝 Inserimento voti per studenti esistenti
- 🗑️ Rimozione studenti dal registro
- 📊 Visualizzazione dettagliata dei voti di uno studente
- 📥 **Esportazione della lista in formato PDF**

## 🚀 Funzionalità Principali

### 📋 Gestione Studenti
- **Aggiunta studenti**: Inserimento con validazione di matricola, nome e cognome
- **Matricole uniche**: Sistema di controllo per evitare duplicati
- **Voti opzionali**: Possibilità di aggiungere studenti senza voti iniziali

### 📝 Gestione Voti
- **Validazione automatica**: Voti devono essere compresi tra 18 e 30
- **Calcolo medie**: Media automatica con precisione decimale
- **Statistiche complete**: Min, max, numero voti per ogni studente

### 💾 Persistenza Dati
- **Formato JSON**: Dati salvati in formato leggibile e interoperabile
- **Encoding UTF-8**: Supporto completo per caratteri speciali e accentati
- **Backup automatico**: Salvataggio sicuro con gestione errori

### 📥 Esportazione PDF
- **Layout professionale**: Tabelle formattate con intestazioni
- **Statistiche generali**: Riassunto del registro nel PDF
- **Timestamp automatico**: Nome file con data e ora di creazione
- **Personalizzazione**: Possibilità di specificare nome file personalizzato

## 🛠️ Tecnologie Utilizzate

- **Python 3.12+**: Linguaggio di sviluppo principale
- **JSON**: Formato per la persistenza dei dati
- **ReportLab**: Libreria per la generazione di PDF
- **Pytest**: Framework per test unitari
- **Pytest-cov**: Analisi copertura del codice

## 📦 Installazione

### Prerequisiti
- Python 3.8 o superiore
- pip (gestore pacchetti Python)

### Setup del progetto

1. **Clona o scarica il progetto**
   ```bash
   # Clona il repository
   git clone https://github.com/andreagaspari/csc-coding-ai.git
   cd "csc-coding-ai/Lezione 8"
   
   # Oppure scarica i file direttamente dal repository
   ```

2. **Installa le dipendenze**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verifica l'installazione**
   ```bash
   python registro_studenti_ai.py
   ```

## 🚀 Come Usare

### Avvio dell'Applicazione
```bash
python registro_studenti_ai.py
```

### Menu Principale
```
🎓 Benvenuto nel Sistema di Gestione Registro Studenti
=====================================================

Cosa vuoi fare?
[1] 📋 Stampa lista studenti
[2] ➕ Aggiungi studente
[3] 📝 Aggiungi voto
[4] 🗑️  Cancella studente
[5] 📊 Visualizza voti di uno studente
[6] 📥 Esporta lista studenti in PDF
[0] 👋 Esci
```

### Esempi di Utilizzo

#### ➕ Aggiungere uno studente
```
Numero di matricola: 12345
Nome: Mario
Cognome: Rossi
Inserisci i voti separati da virgole (es. 24,26,30) o premi INVIO per saltare: 24,28,30
```

#### 📝 Aggiungere un voto
```
Inserisci il numero di matricola: 12345
Inserisci il nuovo voto: 27
```

#### 📥 Esportare in PDF
```
Inserisci il nome del file PDF (o premi INVIO per nome predefinito): report_studenti
```

## 📊 Struttura del Progetto

```
registro-studenti-ai/
├── 📄 registro_studenti_ai.py    # Applicazione principale
├── 📄 registro.txt               # File dati JSON
├── 📄 requirements.txt           # Dipendenze Python
├── 🧪 test_registro_studenti.py  # Suite test completa
├── 📚 README.md                  # Documentazione principale
├── 📚 README_TESTS.md            # Documentazione test
└── 📁 __pycache__/               # Cache Python
```

## 🧪 Test e Qualità del Codice

Il progetto include una **suite completa di 55 test** con copertura del **82%** del codice.

### Eseguire i Test
```bash
# Test base
python -m pytest test_registro_studenti.py -v

# Test con copertura
python -m pytest test_registro_studenti.py --cov=registro_studenti_ai -v

# Test specifici
python -m pytest test_registro_studenti.py::TestCalcolaMedia -v
```

### Tipologie di Test
- **Test unitari**: Funzioni individuali (calcola_media, valida_voto)
- **Test di integrazione**: Flussi completi (aggiunta → modifica → salvataggio)
- **Test di validazione**: Input dell'utente e gestione errori
- **Test I/O**: Lettura/scrittura file JSON

## 📁 Formato Dati

I dati sono salvati in formato JSON con la seguente struttura:

```json
[
  {
    "matricola": "12345",
    "nome": "Mario",
    "cognome": "Rossi",
    "voti": [24, 28, 30, 26]
  },
  {
    "matricola": "67890",
    "nome": "Lucia",
    "cognome": "Bianchi",
    "voti": [30, 29, 28]
  }
]
```

## 📥 Funzionalità PDF

### Caratteristiche PDF
- **Intestazione formattata**: Titolo e data di generazione
- **Tabella professionale**: Layout pulito con colori alternati
- **Statistiche riassuntive**: Totale studenti, media generale
- **Personalizzazione**: Nome file configurabile

### Esempio Output PDF
```
📋 Registro Elettronico Studenti
Generato il 03/06/2025 alle 14:30

┌─────────────┬──────────┬──────────┬─────────┬───────┐
│ Matricola   │ Nome     │ Cognome  │ N° Voti │ Media │
├─────────────┼──────────┼──────────┼─────────┼───────┤
│ 12345       │ Mario    │ Rossi    │ 4       │ 27.00 │
│ 67890       │ Lucia    │ Bianchi  │ 3       │ 29.00 │
└─────────────┴──────────┴──────────┴─────────┴───────┘

Statistiche Generali:
• Totale studenti: 2
• Studenti con voti: 2
• Media generale: 28.00
```

## 🛡️ Validazione e Sicurezza

### Validazione Input
- **Matricole**: Controllo univocità e formato
- **Nomi/Cognomi**: Campi obbligatori, supporto caratteri speciali
- **Voti**: Range 18-30, solo numeri interi
- **File**: Gestione errori I/O e JSON malformato

### Gestione Errori
- **File non esistenti**: Creazione automatica registro vuoto
- **JSON corrotto**: Messaggio errore e ripristino sicuro
- **Permessi file**: Gestione errori di scrittura
- **Input invalidi**: Messaggi utente chiari e ripetizione richiesta

## 🔧 Sviluppo e Contributi

### Architettura Codice
- **Separazione responsabilità**: Funzioni dedicate per ogni operazione
- **Type hints**: Annotazioni di tipo per migliore leggibilità
- **Documentazione**: Docstring complete per ogni funzione
- **Gestione errori**: Try-catch centralizzate e messaggi informativi

### Aggiungere Nuove Funzionalità
1. **Creare la funzione** nel file principale
2. **Aggiungere i test** in `test_registro_studenti.py`
3. **Aggiornare il menu** se necessario
4. **Documentare** la nuova funzionalità

### Convenzioni Codice
- **Naming**: Nomi funzioni in italiano, variabili descrittive
- **Formattazione**: Emoji per output utente, messaggi informativi
- **Encoding**: UTF-8 per supporto caratteri internazionali

## 📈 Statistiche Progetto

- **Linee di codice**: ~500 (principale) + ~800 (test)
- **Funzioni**: 12 funzioni principali
- **Test**: 55 test unitari e di integrazione
- **Copertura**: 82% del codice testato
- **Documentazione**: 100% funzioni documentate

## 🐛 Troubleshooting

### Problemi Comuni

**Errore "Module not found"**
```bash
pip install -r requirements.txt
```

**Errore permessi file**
```bash
# Su Linux/Mac
chmod 644 registro.txt
```

**JSON corrotto**
- Il sistema ripristina automaticamente con registro vuoto
- Backup manuale consigliato prima di modifiche massive

**Test falliscono**
```bash
# Verifica dipendenze
pip install pytest pytest-cov

# Esegui test singolarmente
python -m pytest test_registro_studenti.py::TestCalcolaMedia -v
```

## 📞 Supporto

Per problemi o suggerimenti:
1. Verificare la sezione **Troubleshooting**
2. Controllare i **test** per esempi di utilizzo
3. Consultare il **codice sorgente** per dettagli implementazione
4. Visitare il **repository GitHub**: [csc-coding-ai](https://github.com/andreagaspari/csc-coding-ai)

## 📝 Changelog

### Versione 2.0 (Attuale)
- ✨ Aggiunta esportazione PDF
- 🛡️ Validazione matricole univoche
- 📊 Statistiche avanzate nei voti
- 🧪 Suite test completa (55 test)
- 📚 Documentazione completa

### Versione 1.0
- 📋 Gestione base studenti e voti
- 💾 Persistenza JSON
- 🖥️ Interface console

## 📄 Licenza

Progetto educativo sviluppato per il corso "CSC - Programmare con AI".

---

**Sviluppato con ❤️ e AI per l'apprendimento della programmazione Python**
