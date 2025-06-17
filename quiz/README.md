# Quiz App

Semplice applicazione di quiz a risposta multipla con diverse opzioni di interfaccia utente.

## Caratteristiche

- Domande a scelta multipla caricate da un file JSON
- Vari livelli di difficoltà
- Timer per le risposte
- Sistema di punteggio basato su risposte corrette e tempo
- Salvataggio dei punteggi

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

### Interfaccia Streamlit - Opzioni disponibili

Abbiamo fornito diverse versioni dell'interfaccia Streamlit per soddisfare vari casi d'uso:

1. **Versione standard** - Timer che richiede refresh manuale
```bash
streamlit run streamlit_app.py
```

2. **Versione semplificata** - Interfaccia minimale, timer statico
```bash
streamlit run streamlit_app_simple.py
```

3. **Versione con auto-refresh** - Usa il componente streamlit-autorefresh per aggiornare automaticamente la pagina
```bash
pip install streamlit-autorefresh
streamlit run streamlit_component_app.py
```

4. **Versione con timer JavaScript** - Timer fluido che aggiorna solo il componente timer senza refresh completo
```bash
streamlit run streamlit_js_timer_app.py
```

**Nota sul timer in Streamlit**: 
- Le versioni 1-3 richiedono un refresh completo della pagina, che può causare sfarfallio e reset degli input utente. 
- La versione 4 utilizza JavaScript/HTML per creare un timer più fluido che non richiede refresh dell'intera pagina.
- La versione 4 è consigliata per la migliore esperienza utente, specialmente per la persistenza degli elementi UI come gli alert.