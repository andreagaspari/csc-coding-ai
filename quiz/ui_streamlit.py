# ui_streamlit.py
# Interfaccia utente Streamlit per il quiz
import streamlit as st
import time
import threading
import pandas as pd
from models import Domanda
from scores import ottieni_classifica

class QuizUI:
    def __init__(self, controller):
        self.controller = controller
        # In Streamlit l'interfaccia viene ricaricata a ogni interazione
        # utilizziamo la sessione per mantenere lo stato
        if 'initialized' not in st.session_state:
            st.session_state.initialized = True
            st.session_state.pagina = 'home'
            st.session_state.tempo_rimasto = 0
            st.session_state.timer_attivo = False
            st.session_state.punteggio = 0
            st.session_state.punteggio_finale = 0
            st.session_state.dettagli = ''
            st.session_state.mostra_classifica = False

        # Disegna l'interfaccia in base alla pagina corrente
        if st.session_state.pagina == 'home':
            self.show_home()
        elif st.session_state.pagina == 'domanda':
            self.show_question()
        elif st.session_state.pagina == 'recap':
            self.show_recap()
    
    def show_home(self):
        st.title("BENVENUTO AL QUIZ")
        st.subheader("SCEGLI LA DIFFICOLTÀ")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("FACILE", use_container_width=True):
                self.controller.start_quiz('facile')
                st.session_state.pagina = 'domanda'
                st.session_state.reset_timer = True
                st.rerun()
        
        with col2:
            if st.button("MEDIO", use_container_width=True):
                self.controller.start_quiz('medio')
                st.session_state.pagina = 'domanda'
                st.session_state.reset_timer = True
                st.rerun()
        
        with col3:
            if st.button("DIFFICILE", use_container_width=True):
                self.controller.start_quiz('difficile')
                st.session_state.pagina = 'domanda'
                st.session_state.reset_timer = True
                st.rerun()
    
    def show_question(self):
        # Recupera la domanda corrente
        domanda = self.controller.get_current_question()
        if not domanda:
            self.controller.fine_quiz()
            st.session_state.pagina = 'recap'
            st.rerun()
            return
            
        # Intestazione e layout principale
        col_punteggio, col_timer = st.columns([4, 1])
        with col_punteggio:
            if st.button("⬅️ ESCI"):
                st.session_state.pagina = 'home'
                st.rerun()
                return
        
        with col_timer:
            st.write(f"**Punteggio: {self.controller.sessione.punteggio}**")
        
        # Timer semplificato (senza auto-refresh problematico)
        timeout = self.controller.timeout
        
        # Impostazione iniziale del timer
        if 'tempo_inizio' not in st.session_state or st.session_state.get('reset_timer', False):
            st.session_state.tempo_inizio = time.time()
            st.session_state.tempo_rimasto = timeout
            st.session_state.reset_timer = False
            
        # Calcola il tempo rimanente
        now = time.time()
        elapsed = now - st.session_state.tempo_inizio
        tempo_rimasto = max(0, timeout - elapsed)
        st.session_state.tempo_rimasto = tempo_rimasto
        
        # Visualizza il timer con il colore appropriato
        percentuale = tempo_rimasto / timeout
        color = 'green' if percentuale > 0.6 else 'orange' if percentuale > 0.3 else 'red'
        
        # Informazioni sul timer (solo testo per chiarezza)
        timer_container = st.container()
        with timer_container:
            # Barra del timer (singola)
            st.progress(percentuale)
            
            # Testo del timer
            st.markdown(f"<p style='text-align: center; color: {color}; font-weight: bold;'>{int(tempo_rimasto)}s</p>", 
                      unsafe_allow_html=True)
            
            # Istruzioni per l'auto-refresh manuale
            if tempo_rimasto > 0:
                st.caption("Premi R per aggiornare il timer", unsafe_allow_html=True)
        
        # Mostra la barra del timer con il colore appropriato
        percentuale = tempo_rimasto / timeout
        color = 'green' if percentuale > 0.6 else 'orange' if percentuale > 0.3 else 'red'
        st.progress(percentuale)
        st.write(f"<p style='text-align: center; color: {color}; font-weight: bold;'>{int(tempo_rimasto)}s</p>", unsafe_allow_html=True)
        
        # Controlla se il tempo è scaduto
        if tempo_rimasto <= 0:
            self.controller.salta()
            st.session_state.reset_timer = True
            st.rerun()
            return
            
        # Testo della domanda
        st.markdown(f"### {domanda.testo}")
        
        # Opzioni di risposta
        risposte = list(domanda.opzioni.values())
        opzioni_chiavi = sorted(domanda.opzioni.keys())  # ['A', 'B', 'C', 'D']
        
        # Crea i bottoni per le risposte
        for i, (lettera, risposta) in enumerate(zip(opzioni_chiavi, risposte)):
            if st.button(f"{lettera}) {risposta}", key=f"opt_{i}", use_container_width=True):
                self.controller.rispondi(domanda, i)
                st.session_state.reset_timer = True
                st.rerun()
                return
        
        # Bottone per saltare
        if st.button("SALTA", use_container_width=False, key="skip_btn"):
            self.controller.salta()
            st.session_state.reset_timer = True
            st.rerun()
            return
            
    def show_recap(self):
        st.title("IL TUO PUNTEGGIO")
        
        # Punteggio grande
        st.markdown(f"<h1 style='text-align: center;'>{self.controller.sessione.punteggio}</h1>", unsafe_allow_html=True)
        
        # Statistiche con icone
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"✓ **{self.controller.sessione.stats['corrette']}**")
        with col2:
            st.markdown(f"✗ **{self.controller.sessione.stats['errate']}**")
        with col3:
            st.markdown(f"→ **{self.controller.sessione.stats['saltate']}**")
            
        st.write("---")
        
        # Input per le iniziali (3 lettere)
        st.write("### Inserisci le tue iniziali (3 lettere)")
        
        # Usa 3 colonne per creare l'effetto dei trattini
        col1, col2, col3 = st.columns(3)
        with col1:
            lettera1 = st.text_input("", max_chars=1, key="lettera1", label_visibility="collapsed", placeholder="_")
        with col2:
            lettera2 = st.text_input("", max_chars=1, key="lettera2", label_visibility="collapsed", placeholder="_")
        with col3:
            lettera3 = st.text_input("", max_chars=1, key="lettera3", label_visibility="collapsed", placeholder="_")
            
        iniziali = (lettera1 + lettera2 + lettera3).upper()
        
        col1, col2 = st.columns(2)
        with col1:
            # Bottone salva
            if st.button("Salva il tuo risultato"):
                if len(iniziali) == 3 and iniziali.isalpha():
                    self.controller.salva(iniziali)
                    st.success(f"Punteggio salvato come '{iniziali}'!")
                    
                    # Mostra la classifica dopo il salvataggio
                    st.session_state.mostra_classifica = True
                    self.show_leaderboard()
                else:
                    st.error("Inserisci esattamente 3 lettere (A-Z)")
        
        with col2:
            # Bottone per visualizzare la classifica
            if st.button("Visualizza Classifica"):
                st.session_state.mostra_classifica = True
                self.show_leaderboard()
        
        # Se è stato richiesto di mostrare la classifica, la visualizziamo qui
        if st.session_state.mostra_classifica:
            self.show_leaderboard()
                
        # Bottoni finali
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
    
    def show_leaderboard(self):
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
        df['Tempo'] = df['Tempo'].apply(lambda x: f"{x:.2f}")
        
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
                    "Tempo (s)",
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
    
    def run(self):
        # In Streamlit non c'è bisogno di un loop esplicito come in Tkinter
        pass
