# Quiz App

Semplice applicazione di quiz a risposta multipla con diverse opzioni di interfaccia utente.

## Caratteristiche

- Domande a scelta multipla caricate da un file JSON
- Vari livelli di difficoltà
- Timer per le risposte
- Sistema di punteggio basato su risposte corrette e tempo
- Salvataggio dei punteggi
- Visualizzazione della classifica dei migliori punteggi

## Interfacce utente disponibili

1. **Terminale** (default): Interfaccia a riga di comando con caratteri ASCII
2. **Tkinter**: Interfaccia grafica desktop
3. **Streamlit**: Interfaccia web

## Come eseguire

### Interfaccia a terminale (default)
```bash
python main.py
```

### Interfaccia Tkinter
```bash
python main.py --ui tkinter
```

### Interfaccia Streamlit (con auto-refresh)
```bash
streamlit run streamlit_app.py
```

**Nota**: Assicurati di aver installato le dipendenze necessarie con:
```bash
pip install -r requirements.txt
```

Questa versione utilizza il componente streamlit-autorefresh per aggiornare automaticamente la pagina, offrendo una migliore esperienza utente con il timer.