# Test Suite - Sistema di Gestione Registro Studenti

## 📋 Panoramica

Questa suite di test completa copre tutte le funzioni principali dell'applicazione `registro_studenti_ai.py` con **55 test** che garantiscono il corretto funzionamento del sistema.

## 🎯 Copertura del Codice

- **Copertura attuale: 82%**
- **Test passati: 55/55 ✅**
- **Linee di codice testate: 154/188**

## 📂 Struttura dei Test

### 1. **Test Funzioni Base (15 test)**
- `TestCalcolaMedia` - Calcolo delle medie dei voti
- `TestValidaVoto` - Validazione dei voti (18-30)

### 2. **Test Gestione File (5 test)**
- `TestLeggiStudentiDaFile` - Lettura dati JSON
- `TestSalvaStudentiSuFile` - Salvataggio dati JSON

### 3. **Test Ricerca e Validazione (6 test)**
- `TestTrovaStudentePerMatricola` - Ricerca studenti
- `TestMatricolaEsiste` - Controllo matricole duplicate

### 4. **Test Interfaccia Utente (8 test)**
- `TestStampaStudenti` - Visualizzazione lista studenti
- `TestStampaVotiStudente` - Visualizzazione dettagli voti

### 5. **Test Validazione Input (19 test)** 🆕
- `TestValidazioneInput` - Test aggiungi studente con input non validi
- `TestValidazioneInputAggiungiVoto` - Test aggiunta voti con validazione
- `TestValidazioneInputCancellaStudente` - Test cancellazione con conferme
- `TestValidazioneInputStampaVoti` - Test input per visualizzazione voti
- `TestValidazioneInputEdgeCases` - Test casi limite e caratteri speciali

### 6. **Test di Integrazione (2 test)**
- `TestIntegrazione` - Test flussi completi e operazioni combinate

## 🚀 Come Eseguire i Test

### Eseguire Tutti i Test
```bash
python -m pytest test_registro_studenti.py
```

### Eseguire con Dettagli Verbose
```bash
python -m pytest test_registro_studenti.py -v
```

### Eseguire con Copertura del Codice
```bash
python -m pytest test_registro_studenti.py --cov=registro_studenti_ai --cov-report=term-missing
```

### Eseguire Test Specifici
```bash
# Solo test validazione input
python -m pytest test_registro_studenti.py::TestValidazioneInput -v

# Solo test calcola media
python -m pytest test_registro_studenti.py::TestCalcolaMedia -v

# Solo test integrazione
python -m pytest test_registro_studenti.py::TestIntegrazione -v
```

### Eseguire Direttamente
```bash
python test_registro_studenti.py
```

## 🔍 Test di Validazione Input

I nuovi test di validazione input coprono:

### ✅ **Validazione Dati Studente**
- Matricola vuota o duplicata
- Nome e cognome vuoti
- Gestione spazi extra nell'input
- Caratteri speciali (accenti, trattini)

### ✅ **Validazione Voti**
- Voti fuori range (< 18 o > 30)
- Voti non numerici
- Formattazione irregolare con virgole e spazi
- Voti misti (validi e non validi)

### ✅ **Conferme Utente**
- Conferma cancellazione studente (s/n)
- Varianti di conferma (S/s/N/n)
- Annullamento operazioni

### ✅ **Gestione Errori**
- Studenti non esistenti
- File registro vuoto
- Matricole non trovate
- Input non validi

### ✅ **Casi Limite**
- Matricole con zero iniziale
- Input con caratteri speciali
- Formattazione irregolare
- File temporanei per test sicuri

## 📊 Dettagli Tecnici

### Strumenti Utilizzati
- **pytest** - Framework di testing
- **unittest.mock** - Mock per input/output e file
- **tempfile** - File temporanei per test sicuri
- **pytest-cov** - Analisi copertura del codice

### Metodologie di Test
- **Test unitari** per funzioni singole
- **Test di integrazione** per flussi completi
- **Test parametrizzati** per casi multipli
- **Mock degli input utente** per test automatizzati
- **Gestione file temporanei** per test sicuri

## 🛡️ Sicurezza dei Test

- Tutti i test utilizzano **file temporanei** per evitare modifiche ai dati reali
- **Cleanup automatico** dei file temporanei dopo ogni test
- **Isolamento completo** tra i test
- **Nessun impatto** sui file di produzione

## 📈 Miglioramenti Futuri

Le parti di codice non ancora coperte (18%) includono:
- Menu principale interattivo
- Alcune funzioni di stampa specifiche
- Gestione errori molto specifici

Questi rappresentano principalmente codice di interfaccia utente che richiede interazione manuale.

## 🎉 Risultati

✅ **55 test passati**  
✅ **82% copertura del codice**  
✅ **Tutte le funzioni principali testate**  
✅ **Validazione input completa**  
✅ **Gestione errori verificata**  

La suite di test garantisce che l'applicazione funzioni correttamente in tutti gli scenari principali e gestisca appropriatamente gli input non validi dell'utente.
