"""
Operazioni sui file per il registro studenti
===========================================
Gestisce il caricamento e salvataggio dei dati in formato JSON.
"""

import json
from typing import List, Dict


def leggi_studenti_da_file(percorso_file: str) -> List[Dict]:
    """
    Legge il file JSON e restituisce la lista degli studenti come lista di dizionari.
    
    Args:
        percorso_file: Percorso completo del file JSON da leggere
        
    Returns:
        List[Dict]: Lista di dizionari, ognuno rappresenta uno studente
                   Restituisce lista vuota in caso di errore
    """
    try:
        with open(percorso_file, encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print("ℹ️ File not found. Starting with empty registry.")
        return []
    except json.JSONDecodeError:
        print("❌ Error: Invalid JSON format in file.")
        return []


def salva_studenti_su_file(percorso_file: str, studenti: List[Dict]) -> bool:
    """
    Salva la lista di studenti nel file JSON.
    
    Args:
        percorso_file: Percorso completo del file dati
        studenti: Lista di studenti da salvare
        
    Returns:
        bool: True se il salvataggio è riuscito, False altrimenti
    """
    try:
        with open(percorso_file, "w", encoding="utf-8") as file:
            json.dump(studenti, file, ensure_ascii=False, indent=2)
        return True
    except (IOError, OSError) as e:
        print(f"❌ Errore nel salvataggio del file: {e}")
        return False
