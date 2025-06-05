# 🧪 Test Suite - Sistema Registro Studenti

Questa directory contiene la suite completa di test per l'applicazione Registro Studenti.

## 📁 Struttura dei Test

```
tests/
├── __init__.py                 # Package test
├── conftest.py                 # Fixtures globali
├── unit/                       # Test unitari
│   ├── test_models.py         # Test per models.py
│   ├── test_utils.py          # Test per utils.py
│   ├── test_data_manager.py   # Test per data_manager.py
│   ├── test_student_service.py # Test per student_service.py
│   ├── test_pdf_exporter.py   # Test per pdf_exporter.py
│   ├── test_ui.py             # Test per ui.py
│   └── test_config.py         # Test per config.py
├── integration/               # Test di integrazione
│   └── test_integration.py   # Test integrazione moduli
└── utils/                     # Utilità per i test
    └── test_helpers.py        # Helper e funzioni di supporto
```

## 🚀 Esecuzione dei Test

### Eseguire tutti i test
```bash
pytest
```

### Eseguire test con coverage
```bash
pytest --cov=src --cov-report=html
```

### Eseguire solo test unitari
```bash
pytest tests/unit/
```

### Eseguire solo test di integrazione
```bash
pytest tests/integration/
```

### Eseguire test specifici
```bash
pytest tests/unit/test_models.py
pytest tests/unit/test_models.py::TestStudente::test_media_voti
```

### Eseguire test con marker specifici
```bash
pytest -m unit           # Solo test unitari
pytest -m integration    # Solo test di integrazione
pytest -m slow           # Solo test lenti
pytest -m data           # Solo test che usano file di dati
```

## 📊 Coverage Report

Dopo aver eseguito i test con coverage, il report HTML sarà disponibile in:
```
htmlcov/index.html
```

## 🏷️ Marker dei Test

I test sono organizzati con i seguenti marker:

- **`@pytest.mark.unit`**: Test unitari per singoli moduli
- **`@pytest.mark.integration`**: Test di integrazione tra moduli
- **`@pytest.mark.slow`**: Test che richiedono più tempo
- **`@pytest.mark.data`**: Test che utilizzano file di dati

## 🔧 Configurazione

La configurazione dei test si trova in:
- `pytest.ini`: Configurazione principale pytest
- `conftest.py`: Fixtures globali e configurazione fixtures

### Fixtures Principali

- **`sample_student_data`**: Dati di test per studenti
- **`studente_mario`**: Fixture per studente singolo
- **`lista_studenti_popolata`**: Lista studenti con dati
- **`temp_file`**: File temporaneo per test
- **`file_manager_temp`**: FileManager con file temporaneo
- **`student_service_temp`**: StudentService per test

## 📋 Checklist Test

### Test Unitari Implementati ✅

- [x] **Models** - Test per classi Persona, Studente, ListaStudenti
- [x] **Utils** - Test per funzioni di utilità e validazione
- [x] **DataManager** - Test per gestione file JSON
- [x] **StudentService** - Test per operazioni CRUD studenti
- [x] **PDFExporter** - Test per esportazione PDF
- [x] **UI** - Test per interfaccia utente
- [x] **Config** - Test per configurazioni

### Test di Integrazione Implementati ✅

- [x] **Salvataggio/Caricamento** - Test ciclo completo dati
- [x] **Modifica/Persistenza** - Test modifiche e persistenza
- [x] **Statistiche** - Test calcolo statistiche complete
- [x] **Backup/Ripristino** - Test funzionalità backup
- [x] **Ricerca** - Test ricerca avanzata
- [x] **Performance** - Test con dataset grandi

## 🎯 Obiettivi di Coverage

- **Obiettivo minimo**: 80% (configurato in pytest.ini)
- **Obiettivo ideale**: 90%+
- **Coverage per modulo**:
  - `models.py`: >95%
  - `utils.py`: >90%
  - `data_manager.py`: >85%
  - `student_service.py`: >90%
  - Altri moduli: >80%

## 🐛 Best Practices

### Scrittura Test
1. **Un test, un concetto**: Ogni test dovrebbe verificare una sola funzionalità
2. **Nomi descrittivi**: `test_aggiungi_voto_valido_successo`
3. **AAA Pattern**: Arrange, Act, Assert
4. **Isolamento**: Ogni test deve essere indipendente

### Fixtures
1. **Riutilizzo**: Definire fixtures comuni in `conftest.py`
2. **Scope appropriato**: Usare scope function/class/module/session
3. **Cleanup**: Pulire sempre risorse create

### Mocking
1. **Mock esterno**: Moccare dipendenze esterne (file, network)
2. **Non mock interno**: Non moccare codice sotto test
3. **Verifiche**: Verificare che i mock siano chiamati correttamente

## 🔍 Debugging Test

### Test falliti
```bash
pytest -v --tb=long  # Output verboso con traceback completo
pytest --pdb        # Debugger automatico su fallimento
```

### Test lenti
```bash
pytest --durations=10  # Mostra i 10 test più lenti
```

### Coverage dettagliato
```bash
pytest --cov=src --cov-report=term-missing  # Mostra linee mancanti
```

## 📈 Metriche Qualità

### Tempo Esecuzione Target
- Test unitari: < 5 secondi totali
- Test integrazione: < 30 secondi totali
- Suite completa: < 1 minuto

### Stabilità
- 0% test flaky (che falliscono casualmente)
- 100% test deterministici
- Cleanup completo di tutte le risorse

## 🚨 Troubleshooting

### Problemi Comuni

1. **Import Error**: Verificare PYTHONPATH e struttura moduli
2. **File Permission**: Verificare permessi su file temporanei
3. **Mock Issues**: Verificare path dei mock e target corretti
4. **Fixture Scope**: Verificare scope delle fixtures utilizzate

### Comandi Utili

```bash
# Pulire cache pytest
pytest --cache-clear

# Eseguire test in parallelo (con pytest-xdist)
pytest -n auto

# Eseguire solo test modificati
pytest --lf  # Last failed
pytest --ff  # Failed first
```
