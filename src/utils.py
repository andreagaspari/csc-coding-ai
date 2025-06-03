"""
Utilità e funzioni di supporto
=============================
Contiene funzioni di utilità e validazione.
"""

from typing import List
from src.config import VOTO_MIN, VOTO_MAX


def calcola_media(voti: List[float]) -> float:
    """
    Calcola la media aritmetica di una lista di voti numerici.
    
    Args:
        voti: Lista di voti per il calcolo della media
        
    Returns:
        float: Media calcolata con precisione decimale, 0.0 se non ci sono voti validi
    """
    voti_validi = [v for v in voti if isinstance(v, (int, float))]
    if not voti_validi:
        return 0.0
    return sum(voti_validi) / len(voti_validi)


def valida_voto(voto_str: str) -> int:
    """
    Valida un voto inserito come stringa.
    
    Args:
        voto_str: Stringa contenente il voto da validare
        
    Returns:
        int: Voto validato come intero
        
    Raises:
        ValueError: Se il voto non è valido
    """
    try:
        voto = int(float(voto_str.strip()))
        if not (VOTO_MIN <= voto <= VOTO_MAX):
            raise ValueError(f"Il voto deve essere compreso tra {VOTO_MIN} e {VOTO_MAX}")
        return voto
    except ValueError as e:
        if "invalid literal" in str(e):
            raise ValueError("Il voto deve essere un numero intero")
        raise


def valida_matricola(matricola_str: str) -> str:
    """
    Valida una matricola inserita come stringa.
    
    Args:
        matricola_str: Stringa contenente la matricola da validare
        
    Returns:
        str: Matricola validata
        
    Raises:
        ValueError: Se la matricola non è valida
    """
    matricola = matricola_str.strip()
    if not matricola:
        raise ValueError("La matricola non può essere vuota")
    
    if not matricola.isdigit():
        raise ValueError("La matricola deve contenere solo numeri")
    
    if len(matricola) < 3:
        raise ValueError("La matricola deve avere almeno 3 cifre")
    
    return matricola


def valida_nome(nome_str: str) -> str:
    """
    Valida un nome inserito come stringa.
    
    Args:
        nome_str: Stringa contenente il nome da validare
        
    Returns:
        str: Nome validato e formattato
        
    Raises:
        ValueError: Se il nome non è valido
    """
    nome = nome_str.strip()
    if not nome:
        raise ValueError("Il nome non può essere vuoto")
    
    if len(nome) < 2:
        raise ValueError("Il nome deve avere almeno 2 caratteri")
    
    # Permetti lettere, spazi, apostrofi e trattini
    caratteri_validi = all(c.isalpha() or c in " '-" for c in nome)
    if not caratteri_validi:
        raise ValueError("Il nome può contenere solo lettere, spazi, apostrofi e trattini")
    
    return nome.title()


def formatta_numero(numero: float, decimali: int = 2) -> str:
    """
    Formatta un numero con il numero specificato di decimali.
    
    Args:
        numero: Numero da formattare
        decimali: Numero di cifre decimali
        
    Returns:
        str: Numero formattato
    """
    return f"{numero:.{decimali}f}"


def genera_nome_file_timestamp(base_name: str, extension: str = "") -> str:
    """
    Genera un nome file con timestamp.
    
    Args:
        base_name: Nome base del file
        extension: Estensione del file (con o senza punto)
        
    Returns:
        str: Nome file con timestamp
    """
    from datetime import datetime
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if extension and not extension.startswith('.'):
        extension = f".{extension}"
    
    return f"{base_name}_{timestamp}{extension}"
