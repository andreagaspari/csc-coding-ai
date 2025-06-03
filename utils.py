"""
Modulo di utilità per il registro studenti
==========================================
Contiene funzioni di supporto per calcoli e operazioni comuni.
"""

from typing import List


def calcola_media(voti: List[float]) -> float:
    """
    Calculates the arithmetic mean of a list of numeric grades.
    
    Args:
        voti: List of grades to calculate the average from
        
    Returns:
        float: Average calculated with decimal precision, 0.0 if there are no valid grades
        
    Note:
        - Filters only numeric values (integers or decimals) from the list
        - Uses list comprehension to create a new filtered list
        - Checks that the list is not empty before calculating the average
    """
    # Filtra solo i valori numerici (interi o float) dalla lista dei voti
    voti_validi = [v for v in voti if isinstance(v, (int, float))]
    if not voti_validi:
        # Se non ci sono voti validi, restituisce 0.0 come media
        return 0.0
    # Calcola la media aritmetica dei voti validi
    return sum(voti_validi) / len(voti_validi)
