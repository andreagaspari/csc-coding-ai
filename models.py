"""
Modello dati per il registro studenti
====================================
Contiene le strutture dati e le funzioni di validazione.
"""

from typing import List, Dict, Optional


class Studente:
    """Classe per rappresentare uno studente del registro"""
    
    def __init__(self, nome: str, cognome: str, matricola: int, voti: List[int] = None):
        """
        Inizializza un nuovo studente.
        
        Args:
            nome: Nome dello studente
            cognome: Cognome dello studente
            matricola: Numero di matricola (intero)
            voti: Lista dei voti (opzionale)
        """
        self.nome = nome
        self.cognome = cognome
        self.matricola = matricola
        self.voti = voti or []
    
    def media_voti(self) -> float:
        """
        Calcola la media dei voti dello studente.
        
        Returns:
            float: Media dei voti, 0.0 se non ci sono voti
        """
        if not self.voti:
            return 0.0
        return sum(self.voti) / len(self.voti)
    
    def aggiungi_voto(self, voto: int) -> bool:
        """
        Aggiunge un voto allo studente dopo validazione.
        
        Args:
            voto: Voto da aggiungere (deve essere tra 18 e 30)
            
        Returns:
            bool: True se il voto è stato aggiunto, False se non valido
        """
        if 18 <= voto <= 30:
            self.voti.append(voto)
            return True
        return False
    
    def to_dict(self) -> Dict:
        """
        Converte lo studente in un dizionario per compatibilità con il sistema esistente.
        
        Returns:
            Dict: Rappresentazione dello studente come dizionario
        """
        return {
            "matricola": str(self.matricola),
            "nome": self.nome,
            "cognome": self.cognome,
            "voti": self.voti
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Studente':
        """
        Crea uno studente da un dizionario.
        
        Args:
            data: Dizionario contenente i dati dello studente
            
        Returns:
            Studente: Nuova istanza di Studente
        """
        return cls(
            nome=data.get("nome", ""),
            cognome=data.get("cognome", ""),
            matricola=int(data.get("matricola", 0)),
            voti=data.get("voti", [])
        )
    
    def __str__(self) -> str:
        """Rappresentazione stringa dello studente"""
        media = self.media_voti()
        return f"[{self.matricola}] {self.nome} {self.cognome} - Media: {media:.2f} ({len(self.voti)} voti)"


class ListaStudenti:
    """Classe per gestire una lista di studenti"""
    
    def __init__(self):
        """Inizializza una lista vuota di studenti"""
        self.studenti: List[Studente] = []
    
    def trova_studente(self, matricola: int) -> Optional[Studente]:
        """
        Trova uno studente per matricola.
        
        Args:
            matricola: Numero di matricola da cercare
            
        Returns:
            Optional[Studente]: Studente trovato o None se non esiste
        """
        for studente in self.studenti:
            if studente.matricola == matricola:
                return studente
        return None
    
    def aggiungi_studente(self, studente: Studente) -> bool:
        """
        Aggiunge uno studente alla lista se la matricola è unica.
        
        Args:
            studente: Studente da aggiungere
            
        Returns:
            bool: True se aggiunto, False se matricola già esistente
        """
        if self.trova_studente(studente.matricola) is None:
            self.studenti.append(studente)
            return True
        return False
    
    def rimuovi_studente(self, matricola: int) -> bool:
        """
        Rimuove uno studente dalla lista per matricola.
        
        Args:
            matricola: Numero di matricola dello studente da rimuovere
            
        Returns:
            bool: True se rimosso, False se non trovato
        """
        studente = self.trova_studente(matricola)
        if studente:
            self.studenti.remove(studente)
            return True
        return False
    
    def to_dict_list(self) -> List[Dict]:
        """
        Converte la lista di studenti in una lista di dizionari.
        
        Returns:
            List[Dict]: Lista di dizionari per compatibilità con il sistema esistente
        """
        return [studente.to_dict() for studente in self.studenti]
    
    def from_dict_list(self, data: List[Dict]) -> None:
        """
        Carica la lista di studenti da una lista di dizionari.
        
        Args:
            data: Lista di dizionari contenenti i dati degli studenti
        """
        self.studenti = [Studente.from_dict(item) for item in data]
    
    def __len__(self) -> int:
        """Restituisce il numero di studenti nella lista"""
        return len(self.studenti)
    
    def __iter__(self):
        """Permette di iterare sulla lista di studenti"""
        return iter(self.studenti)


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


# Funzioni di utilità per l'integrazione con il codice esistente
def converti_lista_a_oggetti(data: List[Dict]) -> ListaStudenti:
    """
    Converte una lista di dizionari in un oggetto ListaStudenti.
    
    Args:
        data: Lista di dizionari rappresentanti studenti
        
    Returns:
        ListaStudenti: Oggetto contenente gli studenti
    """
    lista = ListaStudenti()
    lista.from_dict_list(data)
    return lista


def converti_oggetti_a_lista(lista_studenti: ListaStudenti) -> List[Dict]:
    """
    Converte un oggetto ListaStudenti in una lista di dizionari.
    
    Args:
        lista_studenti: Oggetto ListaStudenti
        
    Returns:
        List[Dict]: Lista di dizionari per compatibilità
    """
    return lista_studenti.to_dict_list()
