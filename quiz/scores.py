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

def ottieni_classifica(limit=10):
    """
    Legge i punteggi dal file CSV e restituisce una lista ordinata.
    
    :param limit: numero massimo di risultati da restituire
    :return: lista di tuple (nome, punteggio, tempo_medio, data)
    """
    if not os.path.exists(SCORES_FILE):
        return []
        
    punteggi = []
    try:
        with open(SCORES_FILE, mode="r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) == 4:  # verifica che la riga sia formattata correttamente
                    data, nome, punteggio, tempo = row
                    try:
                        punteggio = int(punteggio)
                        tempo = float(tempo)
                        data_formattata = datetime.fromisoformat(data).strftime("%d/%m/%Y")
                        punteggi.append((nome, punteggio, tempo, data_formattata))
                    except (ValueError, TypeError):
                        # Ignora righe con formato non valido
                        continue
    except Exception:
        # In caso di errori nella lettura del file, restituisci una lista vuota
        return []
    
    # Ordina per punteggio (decrescente) e tempo (crescente)
    punteggi_ordinati = sorted(punteggi, key=lambda x: (-x[1], x[2]))
    
    # Restituisci al massimo i primi 'limit' risultati
    return punteggi_ordinati[:limit]
