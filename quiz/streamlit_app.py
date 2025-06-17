# streamlit_component_app.py
# Versione con timer basato su componente React custom
# Richiede l'installazione del pacchetto: pip install streamlit-autorefresh

import streamlit as st

# Configurazione pagina (DEVE essere la prima chiamata Streamlit)
st.set_page_config(
    page_title="Quiz App (Timer avanzato)",
    page_icon="⏱️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

import time
import os
import random
import pandas as pd
from streamlit_autorefresh import st_autorefresh
from models import QuizSession
from data_loader import load_questions
from config import DIFFICULTY_SETTINGS
from scores import salva_punteggio, ottieni_classifica

# Componente auto-refresh (esegue un refresh ogni secondo solo quando necessario)
# Il refresh viene disabilitato nella pagina di recap
if 'pagina' not in st.session_state or st.session_state.pagina != 'recap':
    count = st_autorefresh(interval=1000, key="timer_refresh")

# Inizializzazione stato
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.pagina = 'home'
    st.session_state.punteggio = 0
    st.session_state.domande = []
    st.session_state.indice_domanda = 0
    st.session_state.timeout = 0
    st.session_state.stats = {"corrette": 0, "errate": 0, "saltate": 0, "tempi": []}
    st.session_state.tempo_inizio = None
    st.session_state.punteggio_salvato = False
    st.session_state.mostra_alert = False
    st.session_state.alert_message = ""
    st.session_state.mostra_classifica = False

# Funzioni di controllo
def start_quiz(difficolta):
    diff_map = {'facile': 1, 'medio': 2, 'difficile': 3}
    livello = diff_map[difficolta]
    st.session_state.timeout = DIFFICULTY_SETTINGS[livello][1]
    num_domande = DIFFICULTY_SETTINGS[livello][0]
    
    # Carica le domande
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "questions.json")
    domande = load_questions(file_path)
    
    random.shuffle(domande)
    st.session_state.domande = domande[:num_domande]
    st.session_state.indice_domanda = 0
    st.session_state.punteggio = 0
    st.session_state.stats = {"corrette": 0, "errate": 0, "saltate": 0, "tempi": []}
    st.session_state.pagina = 'domanda'
    st.session_state.tempo_inizio = time.time()  # Inizializza il timer

def rispondi(indice_opzione):
    from score_calculator import calculate_score
    
    # Calcola tempo trascorso
    tempo_trascorso = 0.0
    if st.session_state.tempo_inizio:
        tempo_trascorso = time.time() - st.session_state.tempo_inizio
    
    # Prepara la risposta
    domanda = st.session_state.domande[st.session_state.indice_domanda]
    lettera = sorted(domanda.opzioni.keys())[indice_opzione]
    
    # Determina correttezza
    is_correct = lettera == domanda.corretta
    punti = calculate_score(is_correct, tempo_trascorso, st.session_state.timeout)
    st.session_state.punteggio += punti
    st.session_state.stats["tempi"].append(tempo_trascorso)
    
    if is_correct:
        st.session_state.stats["corrette"] += 1
    else:
        st.session_state.stats["errate"] += 1
        
    st.session_state.indice_domanda += 1
    st.session_state.tempo_inizio = time.time()  # Resetta il timer
    
    # Verifica se siamo alla fine del quiz
    if st.session_state.indice_domanda >= len(st.session_state.domande):
        st.session_state.pagina = 'recap'
    
def salta():
    # Logica per saltare una domanda
    if st.session_state.indice_domanda < len(st.session_state.domande) - 1:
        # Aggiorna statistiche
        st.session_state.stats["saltate"] += 1
        
        # Passa alla domanda successiva
        st.session_state.indice_domanda += 1
        st.session_state.tempo_inizio = time.time()
    else:
        # Fine del quiz
        st.session_state.pagina = 'recap'
        
def salva_risultato(iniziali):
    """Salva il punteggio nel file scores.csv"""
    if len(iniziali.strip()) != 3:
        return False
        
    try:
        # Calcola il tempo medio delle risposte (se ci sono risposte date)
        tempi = st.session_state.stats["tempi"]
        tempo_medio = sum(tempi) / len(tempi) if tempi else 0
        
        salva_punteggio(
            iniziali, 
            st.session_state.punteggio, 
            tempo_medio
        )
        return True
    except Exception as e:
        st.error(f"Errore nel salvataggio del punteggio: {e}")
        return False

def mostra_classifica():
    """
    Visualizza la classifica dei migliori punteggi
    """
    # Ottieni la classifica
    classifica = ottieni_classifica(10)
    
    if not classifica:
        st.warning("Nessun punteggio disponibile nella classifica")
        return
        
    st.markdown("### 🏆 CLASSIFICA TOP 10 🏆")
    
    # Converti la classifica in un dataframe pandas per una migliore visualizzazione
    df = pd.DataFrame(classifica, columns=['Nome', 'Punti', 'Tempo', 'Data'])
    
    # Aggiungi una colonna per la posizione
    df.insert(0, 'Pos', range(1, len(df) + 1))
    
    # Formatta il tempo con 2 decimali
    df['Tempo'] = df['Tempo'].apply(lambda x: f"{x:.2f}s")
    
    # Visualizza il dataframe come una tabella
    st.dataframe(
        df,
        column_config={
            "Pos": st.column_config.NumberColumn(
                "Pos",
                help="Posizione in classifica",
                width="small"
            ),
            "Nome": st.column_config.TextColumn(
                "Nome",
                width="small"
            ),
            "Punti": st.column_config.NumberColumn(
                "Punti",
                width="medium"
            ),
            "Tempo": st.column_config.TextColumn(
                "Tempo",
                width="medium"
            ),
            "Data": st.column_config.TextColumn(
                "Data",
                width="medium"
            )
        },
        use_container_width=True,
        hide_index=True
    )

def check_timeout():
    """Verifica se il tempo è scaduto per la domanda corrente"""
    if not st.session_state.tempo_inizio:
        return False
        
    tempo_trascorso = time.time() - st.session_state.tempo_inizio
    if tempo_trascorso >= st.session_state.timeout:
        # Tempo scaduto, segna come domanda saltata
        st.session_state.stats["saltate"] += 1
        
        # Passa alla domanda successiva o termina
        if st.session_state.indice_domanda < len(st.session_state.domande) - 1:
            st.session_state.indice_domanda += 1
            st.session_state.tempo_inizio = time.time()
        else:
            # Fine del quiz
            st.session_state.pagina = 'recap'
        
        return True
    return False

# Logica di gestione del timeout
if st.session_state.pagina == 'domanda' and check_timeout():
    salta()  # Tempo scaduto, salta automaticamente

# Home page
if st.session_state.pagina == 'home':
    st.title("BENVENUTO AL QUIZ")
    st.subheader("SCEGLI LA DIFFICOLTÀ")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("FACILE", use_container_width=True):
            start_quiz('facile')
            st.rerun()
    
    with col2:
        if st.button("MEDIO", use_container_width=True):
            start_quiz('medio')
            st.rerun()
    
    with col3:
        if st.button("DIFFICILE", use_container_width=True):
            start_quiz('difficile')
            st.rerun()

# Pagina domanda
elif st.session_state.pagina == 'domanda':
    # Verifica se siamo alla fine
    if st.session_state.indice_domanda >= len(st.session_state.domande):
        st.session_state.pagina = 'recap'
        st.rerun()
    else:
        domanda = st.session_state.domande[st.session_state.indice_domanda]
        
        # Header con punteggio
        col_exit, col_punteggio = st.columns([4, 1])
        
        with col_exit:
            if st.button("⬅️ ESCI"):
                st.session_state.pagina = 'home'
                st.rerun()
        
        with col_punteggio:
            st.write(f"**Punteggio: {st.session_state.punteggio}**")
        
        # Timer
        if st.session_state.tempo_inizio:
            tempo_trascorso = time.time() - st.session_state.tempo_inizio
            tempo_rimasto = max(0, st.session_state.timeout - tempo_trascorso)
            percentuale = tempo_rimasto / st.session_state.timeout
            
            # Scegli il colore in base al tempo rimanente
            color = 'green'
            if percentuale < 0.6:
                color = 'orange'
            if percentuale < 0.3:
                color = 'red'
                
            st.progress(percentuale)
            st.markdown(f"<p style='text-align: center; color: {color}; font-weight: bold;'>{int(tempo_rimasto)}s</p>",
                      unsafe_allow_html=True)
        
        # Testo della domanda
        st.markdown(f"### {domanda.testo}")
        
        # Opzioni di risposta
        opzioni_chiavi = sorted(domanda.opzioni.keys())  # ['A', 'B', 'C', 'D']
        
        for i, lettera in enumerate(opzioni_chiavi):
            if st.button(f"{lettera}) {domanda.opzioni[lettera]}", key=f"opt_{i}", use_container_width=True):
                rispondi(i)
                st.rerun()
        
        # Bottone per saltare
        if st.button("SALTA", use_container_width=False, key="skip_btn"):
            salta()
            st.rerun()

# Pagina recap finale
elif st.session_state.pagina == 'recap':
    st.title("IL TUO PUNTEGGIO")
    
    # Punteggio grande
    st.markdown(f"<h1 style='text-align: center;'>{st.session_state.punteggio}</h1>", unsafe_allow_html=True)
    
    # Statistiche con icone
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"✓ **{st.session_state.stats['corrette']}**")
    with col2:
        st.markdown(f"✗ **{st.session_state.stats['errate']}**")
    with col3:
        st.markdown(f"→ **{st.session_state.stats['saltate']}**")
        
    st.write("---")
    
    # Input per le iniziali (3 lettere)
    st.write("### Inserisci le tue iniziali (3 lettere)")
    
    # Usa 3 colonne per creare l'effetto dei trattini
    col1, col2, col3 = st.columns(3)
    with col1:
        lettera1 = st.text_input("Lettera 1", max_chars=1, key="lettera1", label_visibility="collapsed", placeholder="_")
    with col2:
        lettera2 = st.text_input("Lettera 2", max_chars=1, key="lettera2", label_visibility="collapsed", placeholder="_")
    with col3:
        lettera3 = st.text_input("Lettera 3", max_chars=1, key="lettera3", label_visibility="collapsed", placeholder="_")
        
    iniziali = (lettera1 + lettera2 + lettera3).upper()
    
    # Bottone salva
    if 'mostra_alert' in st.session_state and st.session_state.mostra_alert:
        st.success(st.session_state.alert_message)
        
    # Aggiungiamo due colonne per i bottoni Salva e Visualizza Classifica
    col_salva, col_classifica = st.columns(2)
    
    with col_salva:
        if st.button("Salva il tuo risultato", use_container_width=True):
            if len(iniziali.strip()) == 3:
                if not st.session_state.punteggio_salvato:
                    if salva_risultato(iniziali):
                        st.session_state.punteggio_salvato = True
                        st.session_state.mostra_alert = True
                        st.session_state.alert_message = f"Punteggio salvato come '{iniziali}'!"
                        st.session_state.mostra_classifica = True
                        st.rerun()
            else:
                st.session_state.mostra_alert = True
                st.session_state.alert_message = "Inserisci esattamente 3 lettere per le tue iniziali"
                st.rerun()
    
    with col_classifica:
        if st.button("Visualizza Classifica", use_container_width=True):
            st.session_state.mostra_classifica = True
            st.rerun()
    
    # Mostra la classifica se richiesto
    if st.session_state.mostra_classifica:
        mostra_classifica()
            
    # Bottoni finali
    st.write("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("ESCI", use_container_width=True):
            st.session_state.pagina = 'home'
            st.session_state.mostra_classifica = False
            st.rerun()
            
    with col2:
        if st.button("RIPROVA", use_container_width=True):
            st.session_state.pagina = 'home'
            st.session_state.mostra_classifica = False
            st.rerun()

    # Mostra classifica se attivato
    if st.session_state.mostra_classifica:
        mostra_classifica()
