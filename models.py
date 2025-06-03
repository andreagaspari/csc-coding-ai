"""
Modello dati per il registro studenti
====================================
Contiene le strutture dati e le funzioni di validazione.
"""

from typing import List, Dict, Optional


class StudentModel:
    """Modello per rappresentare uno studente"""
    
    @staticmethod
    def create_student(matricola: str, nome: str, cognome: str, voti: List[int] = None) -> Dict:
        """
        Crea un nuovo studente come dizionario.
        
        Args:
            matricola: Numero di matricola
            nome: Nome dello studente
            cognome: Cognome dello studente
            voti: Lista dei voti (opzionale)
            
        Returns:
            Dict: Dizionario rappresentante lo studente
        """
        return {
            "matricola": matricola,
            "nome": nome,
            "cognome": cognome,
            "voti": voti or []
        }
    
    @staticmethod
    def find_student_by_matricola(studenti: List[Dict], matricola: str) -> Optional[Dict]:
        """
        Trova uno studente nella lista tramite matricola.
        
        Args:
            studenti: Lista di studenti in cui cercare
            matricola: Matricola dello studente da trovare
            
        Returns:
            Dict: Dizionario dello studente trovato, None se non trovato
        """
        return next((s for s in studenti if s.get("matricola") == matricola), None)
    
    @staticmethod
    def matricola_exists(studenti: List[Dict], matricola: str) -> bool:
        """
        Verifica se una matricola esiste già nella lista studenti.
        
        Args:
            studenti: Lista di studenti in cui cercare
            matricola: Matricola da verificare
            
        Returns:
            bool: True se la matricola esiste, False altrimenti
        """
        return any(s.get("matricola") == matricola for s in studenti)


def valida_voto(voto_str: str) -> int:
    """
    Valida e converte una stringa di voto in intero.
    
    Args:
        voto_str: Stringa contenente il voto da validare
        
    Returns:
        int: Voto validato, solleva ValueError se non valido
        
    Raises:
        ValueError: Se il voto non è valido (non numerico o fuori dal range 18-30)
    """
    try:
        voto = int(voto_str.strip())
        if not 18 <= voto <= 30:
            raise ValueError(f"Il voto deve essere compreso tra 18 e 30, ricevuto: {voto}")
        return voto
    except ValueError:
        raise ValueError("Il voto deve essere un numero intero tra 18 e 30")
