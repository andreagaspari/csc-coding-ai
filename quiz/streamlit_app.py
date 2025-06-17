# streamlit_app.py
# File principale per avviare l'app Streamlit

import streamlit as st
import os
import sys
import random
from ui_streamlit import QuizUI
from models import QuizSession
from data_loader import load_questions
from config import DIFFICULTY_SETTINGS
from scores import salva_punteggio

class QuizController:
    def __init__(self):
        self.sessione = None
        self.domande = []
        self.difficolta = None
        self.timeout = None
        self.punteggio = 0
        self.stats = None
        self.current_index = 0
        
    def start_quiz(self, difficolta):
        diff_map = {'facile': 1, 'medio': 2, 'difficile': 3}
        livello = diff_map[difficolta]
        self.difficolta = difficolta
        self.timeout = DIFFICULTY_SETTINGS[livello][1]
        num_domande = DIFFICULTY_SETTINGS[livello][0]
        
        # Carica le domande
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, "questions.json")
        self.domande = load_questions(file_path)
        
        # Mescola e seleziona il numero di domande in base alla difficoltà
        random.shuffle(self.domande)
        self.domande = self.domande[:num_domande]
        
        # Inizializza la sessione
        self.sessione = QuizSession(domande=self.domande, timeout=self.timeout)
        self.current_index = 0
    
    def get_current_question(self):
        try:
            if self.current_index < len(self.domande):
                return self.domande[self.current_index]
            return None
        except:
            return None
    
    def next_question(self):
        self.current_index += 1
    
    def rispondi(self, domanda, idx):
        lettera = sorted(domanda.opzioni.keys())[idx]
        tempo = 0.0  # Per ora non misuriamo il tempo reale
        self.sessione.record_answer(domanda, lettera, tempo)
        self.next_question()
    
    def salta(self):
        domanda = self.get_current_question()
        if domanda:
            tempo = self.timeout + 1
            self.sessione.record_answer(domanda, '', tempo)
            self.next_question()
    
    def fine_quiz(self):
        # Genera dettagli per la schermata finale
        dettagli = f"✓{self.sessione.stats['corrette']} ✗{self.sessione.stats['errate']} →{self.sessione.stats['saltate']}"
        
        # Salva nello stato della sessione per la pagina di recap
        st.session_state.punteggio_finale = self.sessione.punteggio
        st.session_state.dettagli = dettagli
    
    def salva(self, nome):
        if len(nome) != 3 or not nome.isalpha():
            st.error("Inserisci esattamente 3 lettere")
            return False
            
        media = sum(self.sessione.stats['tempi']) / len(self.sessione.stats['tempi']) if self.sessione.stats['tempi'] else 0.0
        salva_punteggio(nome.upper(), self.sessione.punteggio, media)
        return True

def main():
    # Configura la pagina Streamlit
    st.set_page_config(
        page_title="Quiz App",
        page_icon="❓",
        layout="centered",
        initial_sidebar_state="collapsed",
    )
    
    # Aggiungi il controller alla sessione se non esiste già
    if 'controller' not in st.session_state:
        st.session_state.controller = QuizController()
    
    # Crea l'interfaccia utente
    ui = QuizUI(st.session_state.controller)
    ui.run()

if __name__ == "__main__":
    main()
