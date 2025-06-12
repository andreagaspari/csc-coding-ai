"""
Punto di ingresso del Quiz a scelta multipla.

Coordina il caricamento delle domande, l’interazione con l’utente,
il calcolo del punteggio e la visualizzazione dei risultati.

:author: Tuo Nome
:created: 2025-06-12
"""

import random
import sys

from config import DIFFICULTY_SETTINGS
from data_loader import load_questions
from models import QuizSession
from ui import (
    prompt_difficulty,
    prompt_restart,
    display_question,
    prompt_answer,
    display_feedback,
    display_summary,
    prompt_initials_and_save
)


def main():
    """
    Ciclo principale del programma. Gestisce una o più sessioni quiz.
    """
    while True:
        try:
            # Caricamento domande
            import os

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