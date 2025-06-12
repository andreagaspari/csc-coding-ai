"""
Modulo di interfaccia a riga di comando per il Quiz.

Contiene funzioni per:
- chiedere all’utente la difficoltà
- visualizzare le domande
- raccogliere risposte con timer
- mostrare il feedback e i risultati finali

:author: Tuo Nome
:created: 2025-06-12
"""

import sys
import time
from typing import Tuple
from models import Domanda
from config import DIFFICULTY_SETTINGS, DEFAULT_DIFFICULTY
from timer import start_timer, elapsed_time, is_timeout


def prompt_difficulty() -> Tuple[int, int]:
    """
    Chiede all’utente di selezionare un livello di difficoltà (1–3).
    Massimo 3 tentativi. Se falliti, usa DEFAULT_DIFFICULTY.

    :return: tuple (numero_domande, timeout)
    """
    print("📊 Seleziona la difficoltà:")
    print("1 - Facile   (5 domande, 15s)")
    print("2 - Medio    (10 domande, 10s)")
    print("3 - Difficile (15 domande, 5s)")

    for _ in range(3):
        scelta = input("👉 Inserisci un numero tra 1 e 3: ").strip()
        if scelta.isdigit() and int(scelta) in DIFFICULTY_SETTINGS:
            return DIFFICULTY_SETTINGS[int(scelta)]
        print("⚠️  Input non valido.")

    print("🔁 Nessuna scelta valida. Impostata difficoltà media (2).")
    return DIFFICULTY_SETTINGS[DEFAULT_DIFFICULTY]


def prompt_restart() -> bool:
    """
    Chiede all’utente se vuole rigiocare. Massimo 3 tentativi.

    :return: True se l’utente vuole rigiocare, False altrimenti
    """
    for _ in range(3):
        scelta = input("🔁 Vuoi rigiocare? (S/N): ").strip().upper()
        if scelta in ("S", "N"):
            return scelta == "S"
        print("⚠️  Inserisci 'S' o 'N'.")
    print("⛔ Input non valido. Uscita dal quiz.")
    return False


def display_question(domanda: Domanda) -> None:
    """
    Mostra il testo della domanda e le opzioni.

    :param domanda: oggetto Domanda
    """
    print("\n📌", domanda.testo)
    for lettera in sorted(domanda.opzioni.keys()):
        print(f"  {lettera}) {domanda.opzioni[lettera]}")


def prompt_answer(timeout: int) -> Tuple[str, float]:
    """
    Richiede una risposta all’utente entro il timeout.
    Restituisce la risposta e il tempo impiegato.
    Se il tempo scade o input assente → risposta = "", tempo = timeout.

    :param timeout: tempo massimo concesso per rispondere (secondi)
    :return: tuple (risposta: str, tempo: float)
    """
    print(f"⏳ Hai {timeout} secondi per rispondere...")

    start = start_timer()
    risposta = ""

    # Legge input bloccante entro tempo limite
    try:
        while True:
            if sys.stdin in select.select([sys.stdin], [], [], 0.1)[0]:
                risposta = input("👉 Risposta (A–D): ").strip().upper()
                break
            if is_timeout(elapsed_time(start), timeout):
                print("⏱️  Tempo scaduto!")
                break
    except Exception:
        risposta = ""

    tempo = min(elapsed_time(start), timeout)
    if risposta not in ("A", "B", "C", "D"):
        risposta = ""  # risposta nulla o malformata
    return risposta, tempo


def display_feedback(is_correct: bool, punti: int, tempo: float) -> None:
    """
    Mostra un messaggio in base all’esito della risposta.

    :param is_correct: True se risposta corretta
    :param punti: punteggio ottenuto (positivo o negativo)
    :param tempo: tempo impiegato per rispondere
    """
    stato = "✅ Corretto!" if is_correct else "❌ Sbagliato!"
    print(f"{stato} ({tempo:.1f}s) ➤ {'+' if punti >= 0 else ''}{punti} punti")


def display_summary(stats: dict) -> None:
    """
    Mostra le statistiche finali del quiz.

    :param stats: dizionario con campi: corrette, errate, saltate, tempi
    """
    print("\n📊 Risultati Finali")
    print("--------------------")
    print(f"✔️  Corrette : {stats['corrette']}")
    print(f"❌ Errate   : {stats['errate']}")
    print(f"⏭️  Saltate  : {stats['saltate']}")

    if stats["tempi"]:
        media = sum(stats["tempi"]) / len(stats["tempi"])
        print(f"⏱️  Tempo medio: {media:.2f} s")
