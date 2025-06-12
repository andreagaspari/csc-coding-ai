"""
Modulo per il caricamento e la validazione delle domande del quiz.

Supporta due formati di input:
- JSON: array di oggetti con campi "domanda", "opzioni", "corretta"
- CSV: file con intestazioni "domanda", "A", "B", "C", "D", "corretta"

Una domanda valida deve avere:
- un testo non vuoto
- esattamente 4 opzioni (A, B, C, D)
- una risposta corretta che sia una delle lettere "A", "B", "C" o "D"

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
    Carica le domande da un file (JSON o CSV) e restituisce una lista di oggetti Domanda validi.

    :param path: percorso al file delle domande. Estensioni supportate: .json, .csv
    :return: lista di Domanda validate
    :raises ValueError: se il file è mancante, malformato o se nessuna domanda è valida
    """
    _, ext = os.path.splitext(path)  # Estrae l'estensione del file (.json o .csv)
    raw_questions = []  # Lista temporanea per le domande grezze da validare

    # -- Caso 1: file JSON
    if ext.lower() == ".json":
        try:
            with open(path, encoding="utf-8") as f:
                raw_questions = json.load(f)  # Carica un array di dizionari
        except json.JSONDecodeError as e:
            raise ValueError(f"Errore nel parsing del file JSON: {e}")

    # -- Caso 2: file CSV
    elif ext.lower() == ".csv":
        with open(path, newline='', encoding="utf-8") as f:
            reader = csv.DictReader(f)  # Usa le intestazioni della prima riga
            for row in reader:
                # Crea un dizionario in formato compatibile con Domanda
                opzioni = {key: row[key].strip() for key in ("A", "B", "C", "D") if key in row}
                raw_questions.append({
                    "domanda": row.get("domanda", "").strip(),
                    "opzioni": opzioni,
                    "corretta": row.get("corretta", "").strip().upper()
                })

    # -- Caso 3: formato non supportato
    else:
        raise ValueError("Formato file non supportato. Utilizzare .json o .csv")

    # -- Validazione delle domande
    domande_valide = []  # Lista finale di oggetti Domanda
    for raw in raw_questions:
        if validate_question(raw):
            domanda = Domanda(
                testo=raw["domanda"],
                opzioni=raw["opzioni"],
                corretta=raw["corretta"]
            )
            domande_valide.append(domanda)

    # -- Controllo finale: almeno una domanda valida deve essere presente
    if not domande_valide:
        raise ValueError("Nessuna domanda valida trovata nel file.")

    return domande_valide


def validate_question(raw: dict) -> bool:
    """
    Verifica che una struttura di domanda sia completa e corretta.

    :param raw: dizionario con i campi "domanda", "opzioni", "corretta"
    :return: True se la struttura è valida, False altrimenti
    """
    # Il dizionario deve esistere
    if not isinstance(raw, dict):
        return False

    # Il campo "domanda" deve essere una stringa non vuota
    if not raw.get("domanda") or not isinstance(raw.get("domanda"), str):
        return False

    # Il campo "opzioni" deve essere un dizionario con esattamente 4 chiavi (A, B, C, D)
    opzioni = raw.get("opzioni")
    if not isinstance(opzioni, dict) or len(opzioni) != 4:
        return False
    if not all(k in opzioni for k in ("A", "B", "C", "D")):
        return False

    # La risposta "corretta" deve essere una tra "A", "B", "C", "D"
    corretta = raw.get("corretta")
    if corretta not in ("A", "B", "C", "D"):
        return False

    return True
