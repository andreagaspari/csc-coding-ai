"""
Punto di ingresso del Quiz a scelta multipla.

Coordina il caricamento delle domande, l’interazione con l’utente,
il calcolo del punteggio e la visualizzazione dei risultati.

:author: Tuo Nome
:created: 2025-06-12
"""

import random
import sys
import argparse

from config import DIFFICULTY_SETTINGS
from data_loader import load_questions
from models import QuizSession

def main():
    """
    Ciclo principale del programma. Gestisce una o più sessioni quiz.
    """
    parser = argparse.ArgumentParser(description="Quiz a scelta multipla")
    parser.add_argument('--ui', choices=['terminale', 'tkinter', 'streamlit'], default='terminale', 
                      help='Scegli la UI: terminale, tkinter o streamlit')
    args = parser.parse_args()

    if args.ui == 'streamlit':
        print("Per avviare l'interfaccia Streamlit esegui:\nstreamlit run streamlit_app.py")
        print("Assicurati di aver installato le dipendenze con: pip install -r requirements.txt")
        import sys
        sys.exit(0)
        
    if args.ui == 'tkinter':
        from ui_tkinter import QuizUI
        from models import QuizSession
        import os
        import random
        from data_loader import load_questions
        from config import DIFFICULTY_SETTINGS
        import tkinter as tk
        from tkinter import messagebox

        class QuizController:
            def __init__(self, ui):
                self.ui = ui
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
                base_dir = os.path.dirname(os.path.abspath(__file__))
                file_path = os.path.join(base_dir, "questions.json")
                self.domande = load_questions(file_path)
                random.shuffle(self.domande)
                self.domande = self.domande[:num_domande]
                self.sessione = QuizSession(domande=self.domande, timeout=self.timeout)
                self.current_index = 0
                self.next_question()

            def next_question(self):
                domanda = self.sessione.next_question()
                if domanda:
                    self.ui.show_question(
                        domanda.testo,
                        [domanda.opzioni[k] for k in sorted(domanda.opzioni.keys())],
                        self.sessione.punteggio,
                        self.timeout,
                        lambda idx: self.rispondi(domanda, idx),
                        self.salta,
                        self.esci
                    )
                else:
                    self.fine_quiz()

            def rispondi(self, domanda, idx):
                lettera = sorted(domanda.opzioni.keys())[idx]
                import time
                tempo = 0.0  # Per ora non misuriamo il tempo reale nella UI grafica
                punti, is_correct, scaduto = self.sessione.record_answer(domanda, lettera, tempo)
                self.next_question()

            def salta(self):
                domanda = self.domande[self.sessione._index - 1]
                tempo = self.timeout + 1
                self.sessione.record_answer(domanda, '', tempo)
                self.next_question()

            def esci(self):
                # Prima di uscire, fermiamo il timer
                if hasattr(self.ui, 'stop_timer'):
                    self.ui.stop_timer()
                self.ui.root.destroy()

            def fine_quiz(self):
                dettagli = f"✔️ {self.sessione.stats['corrette']}  ❌ {self.sessione.stats['errate']}  ⏭️ {self.sessione.stats['saltate']}"
                self.ui.show_recap(
                    self.sessione.punteggio,
                    dettagli,
                    self.salva,
                    self.esci,
                    self.riavvia
                )

            def salva(self, nome):
                from scores import salva_punteggio
                
                # Verifica che ci siano esattamente 3 caratteri
                if len(nome) != 3 or not nome.isalpha():
                    messagebox.showwarning('Input non valido', 
                                         'Inserisci esattamente 3 lettere (A-Z)')
                    return
                    
                # Calcola tempo medio e salva
                media = sum(self.sessione.stats['tempi']) / len(self.sessione.stats['tempi']) if self.sessione.stats['tempi'] else 0.0
                salva_punteggio(nome.upper(), self.sessione.punteggio, media)
                messagebox.showinfo('Salvato', f"Punteggio salvato come '{nome.upper()}'!")

            def riavvia(self):
                self.ui.show_home()

        controller = QuizController(None)
        ui = QuizUI(controller)
        controller.ui = ui
        ui.run()
        return

    # --- UI terminale classica ---
    from ui_terminale import (
        prompt_difficulty,
        prompt_restart,
        display_question,
        prompt_answer,
        display_feedback,
        display_summary,
        prompt_initials_and_save
    )
    
    # Assicuriamoci che le importazioni necessarie siano disponibili
    import os
    import sys
    import random
    from data_loader import load_questions
    from models import QuizSession

    while True:
        try:
            # Caricamento domande
            # Trova la cartella dove si trova main.py
            base_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(base_dir, "questions.json")

            questions = load_questions(file_path)
        except Exception as e:
            print(f"❌ Errore nel caricamento delle domande: {e}")
            sys.exit(1)

        # Selezione difficoltà → imposta N domande e timeout
        num_domande, timeout = prompt_difficulty()

        # Mescola e seleziona le prime N domande
        random.shuffle(questions)
        domande_selezionate = questions[:num_domande]

        # Inizializza la sessione quiz
        sessione = QuizSession(domande=domande_selezionate, timeout=timeout)

        # Loop principale del quiz
        while (q := sessione.next_question()):
            display_question(q)
            risposta, tempo = prompt_answer(timeout)
            punti, is_correct, scaduto = sessione.record_answer(q, risposta, tempo)
            display_feedback(is_correct, punti, tempo, scaduto)

        # Mostra riepilogo finale
        display_summary(sessione.stats, sessione.punteggio)
        prompt_initials_and_save(sessione.punteggio, sessione.stats["tempi"])

        # Richiesta di ripetere il quiz
        if not prompt_restart():
            print("\n👋 Grazie per aver giocato!")
            break

if __name__ == "__main__":
    main()