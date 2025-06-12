"""
Modulo per il caricamento e la validazione delle domande del quiz.

Supporta il parsing da file in formato JSON o CSV. Ogni riga/oggetto deve contenere:
- domanda: str
- opzioni: dict con chiavi A–D
- corretta: str (una tra "A", "B", "C", "D")

:author: Tuo Nome
:created: 2025-06-12
"""

import json
import csv
import os
from typing import List, Dict
from models import Domanda


def load_questions(path: str) -> List[Domanda]:
    """
    Carica le domande da un file JSON o CSV e restituisce una lista di oggetti Domanda validi.

    :param path: percorso al file delle domande (.json o .csv)
    :return: lista di Domanda
    :raises ValueError: se il file è malformato o contiene domande non valide
    """
    _, ext = os.path.splitext(path)
    raw_questions = []

    if ext.lower() == ".json":
        with open(path, encoding="utf-8") as f:
            try:
                raw_questions = json.load(f)
            except json.JSONDecodeError as e:
                raise ValueError(f"Errore nel parsing JSON: {e}")
    elif ext.lower() == ".csv":
        with open(path, newline='', encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Normalizza opzioni da colonne A,B,C,D
                opzioni = {key: row[key].strip() for key in ("A", "B", "C", "D") if key in row}
                raw_questions.append({
                    "domanda": row.get("domanda", "").strip(),
                    "opzioni": opzioni,
                    "corretta": row.get("corretta", "").strip().upper()
                })
    else:
        raise ValueError("Formato file non supportato. Usa .json o .csv")

    # Filtra domande valide
    domande_valide = []
    for raw in raw_questions:
        if validate_question(raw):
            domanda = Domanda(
                testo=raw["domanda"],
                opzioni=raw["opzioni"],
                corretta=raw["corretta"]
            )
            domande_valide.append(domanda)

    if not domande_valide:
        raise ValueError("Nessuna domanda valida trovata nel file.")

    return domande_valide


def validate_question(raw: dict) -> bool:
    """
    Verifica che una domanda contenga tutti i campi richiesti.

    :param raw: dizionario contenente la struttura di una domanda
    :return: True se la domanda è considerata valida, False altrimenti
    """
    if not isinstance(raw, dict):
        return False

    if not raw.get("domanda") or not isinstance(raw.get("domanda"), str):
        return False

    opzioni = raw.get("opzioni")
    if not isinstance(opzioni, dict) or len(opzioni) != 4:
        return False

    if not all(k in opzioni for k in ("A", "B", "C", "D")):
        return False

    corretta = raw.get("corretta")
    if corretta not in ("A", "B", "C", "D"):
        return False

    return True
