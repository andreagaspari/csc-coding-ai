"""
Modulo per la registrazione dei punteggi delle sessioni completate.

Salva i risultati in un file CSV appendendo una riga per ciascun giocatore.

:author: Tuo Nome
:created: 2025-06-12
"""

import csv
import os
from datetime import datetime


# Percorso assoluto al file scores.csv nella cartella quiz/
SCORES_FILE = os.path.join(os.path.dirname(__file__), "scores.csv")

def salva_punteggio(nome: str, punteggio: int, tempo_medio: float):
    """
    Salva una voce nel file dei punteggi.

    :param nome: sigla a 3 lettere inserita dall'utente
    :param punteggio: punteggio finale
    :param tempo_medio: tempo medio per risposta
    """
    with open(SCORES_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now().isoformat(), nome.upper(), punteggio, f"{tempo_medio:.2f}"])
