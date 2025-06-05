"""
Modelli dati per il registro studenti
====================================
Contiene le classi e strutture dati principali.
"""

from typing import List, Dict, Optional
from src.config import VOTO_MIN, VOTO_MAX


class Persona:
    """Classe base per rappresentare una persona"""
    
    def __init__(self, nome: str, cognome: str):
        """
        Inizializza una nuova persona.
        
        Args:
            nome: Nome della persona
            cognome: Cognome della persona
        """
        self.nome = nome.strip().title()
        self.cognome = cognome.strip().title()
    
    def nome_completo(self) -> str:
        """Restituisce il nome completo"""
        return f"{self.nome} {self.cognome}"
    
    def iniziali(self) -> str:
        """Restituisce le iniziali"""
        return f"{self.nome[0]}.{self.cognome[0]}."
    
    def __str__(self) -> str:
        return self.nome_completo()


class Studente(Persona):
    """Classe per rappresentare uno studente del registro che estende Persona"""
    
    def __init__(self, nome: str, cognome: str, matricola: int, voti: List[int] = None):
        """
        Inizializza un nuovo studente.
        
        Args:
            nome: Nome dello studente
            cognome: Cognome dello studente
            matricola: Numero di matricola (intero)
            voti: Lista dei voti (opzionale)
        """
        super().__init__(nome, cognome)
        self.matricola = matricola
        self.voti = voti or []
    
    def media_voti(self) -> float:
        """Calcola la media dei voti dello studente"""
        if not self.voti:
            return 0.0
        return sum(self.voti) / len(self.voti)
    
    def aggiungi_voto(self, voto: int) -> bool:
        """Aggiunge un voto alla lista"""
        if VOTO_MIN <= voto <= VOTO_MAX:
            self.voti.append(voto)
            return True
        return False
    
    def voto_massimo(self) -> int:
        """Restituisce il voto massimo"""
        return max(self.voti) if self.voti else 0
    
    def voto_minimo(self) -> int:
        """Restituisce il voto minimo"""
        return min(self.voti) if self.voti else 0
    
    def numero_voti(self) -> int:
        """Restituisce il numero di voti"""
        return len(self.voti)
    
    def ha_superato_esami(self) -> bool:
        """Verifica se lo studente ha almeno un voto"""
        return len(self.voti) > 0
    
    def is_eccellente(self) -> bool:
        """Verifica se lo studente è eccellente (media >= 27)"""
        return self.media_voti() >= 27.0
    
    def to_dict(self) -> Dict:
        """Converte lo studente in dizionario"""
        return {
            "matricola": str(self.matricola),
            "nome": self.nome,
            "cognome": self.cognome,
            "voti": self.voti
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Studente':
        """Crea uno studente da un dizionario"""
        return cls(
            nome=data["nome"],
            cognome=data["cognome"],
            matricola=int(data["matricola"]),
            voti=data.get("voti", [])
        )
    
    def __str__(self) -> str:
        """Rappresentazione stringa dello studente con informazioni estese"""
        media = self.media_voti()
        stato = "Eccellente" if self.is_eccellente() else "Buono" if media >= 24 else "Sufficiente" if media >= 18 else "Nessun voto"
        return f"[{self.matricola}] {self.nome_completo()} - Media: {media:.2f} ({len(self.voti)} voti) - {stato}"


class ListaStudenti:
    """Classe per gestire una lista di studenti"""
    
    def __init__(self):
        """Inizializza una lista vuota di studenti"""
        self.studenti: List[Studente] = []
    
    def trova_studente(self, matricola: int) -> Optional[Studente]:
        """Trova uno studente per matricola"""
        for studente in self.studenti:
            if studente.matricola == matricola:
                return studente
        return None
    
    def trova_per_nome(self, nome: str, cognome: str = None) -> List[Studente]:
        """Trova studenti per nome/cognome"""
        risultati = []
        for studente in self.studenti:
            if nome.lower() in studente.nome.lower():
                if cognome is None or cognome.lower() in studente.cognome.lower():
                    risultati.append(studente)
        return risultati
    
    def aggiungi_studente(self, studente: Studente) -> bool:
        """Aggiunge uno studente se non esiste già"""
        if self.trova_studente(studente.matricola) is None:
            self.studenti.append(studente)
            return True
        return False
    
    def rimuovi_studente(self, matricola: int) -> bool:
        """Rimuove uno studente per matricola"""
        studente = self.trova_studente(matricola)
        if studente:
            self.studenti.remove(studente)
            return True
        return False
    
    def studenti_eccellenti(self) -> List[Studente]:
        """Restituisce gli studenti eccellenti"""
        return [s for s in self.studenti if s.is_eccellente()]
    
    def studenti_con_voti(self) -> List[Studente]:
        """Restituisce gli studenti che hanno almeno un voto"""
        return [s for s in self.studenti if s.ha_superato_esami()]
    
    def studenti_senza_voti(self) -> List[Studente]:
        """Restituisce gli studenti che non hanno ancora voti"""
        return [s for s in self.studenti if not s.ha_superato_esami()]
    
    def media_generale(self) -> float:
        """Calcola la media generale di tutti gli studenti con voti"""
        studenti_con_voti = self.studenti_con_voti()
        if not studenti_con_voti:
            return 0.0
        medie = [s.media_voti() for s in studenti_con_voti]
        return sum(medie) / len(medie)
    
    def statistiche(self) -> Dict:
        """Restituisce statistiche generali"""
        stats = {
            "totale_studenti": len(self.studenti),
            "studenti_con_voti": len(self.studenti_con_voti()),
            "studenti_senza_voti": len(self.studenti_senza_voti()),
            "studenti_eccellenti": len(self.studenti_eccellenti()),
            "media_generale": self.media_generale()
        }
        
        studenti_con_voti = self.studenti_con_voti()
        if studenti_con_voti:
            medie = [s.media_voti() for s in studenti_con_voti]
            stats.update({
                "media_più_alta": max(medie),
                "media_più_bassa": min(medie),
                "migliore_studente": max(studenti_con_voti, key=lambda s: s.media_voti()).nome_completo()
            })
        
        return stats
    
    def ordina_per_media(self, decrescente: bool = True) -> List[Studente]:
        """Ordina gli studenti per media"""
        return sorted(self.studenti_con_voti(), key=lambda s: s.media_voti(), reverse=decrescente)
    
    def ordina_per_nome(self) -> List[Studente]:
        """Ordina gli studenti per nome"""
        return sorted(self.studenti, key=lambda s: (s.cognome, s.nome))
    
    def to_dict_list(self) -> List[Dict]:
        """Converte la lista in formato dizionario"""
        return [s.to_dict() for s in self.studenti]
    
    def from_dict_list(self, data: List[Dict]) -> None:
        """Carica studenti da una lista di dizionari"""
        self.studenti = [Studente.from_dict(item) for item in data]
    
    def __len__(self) -> int:
        """Restituisce il numero di studenti nella lista"""
        return len(self.studenti)
    
    def __iter__(self):
        """Permette di iterare sulla lista di studenti"""
        return iter(self.studenti)
    
    def __contains__(self, matricola: int) -> bool:
        """Verifica se una matricola è presente nella lista"""
        return self.trova_studente(matricola) is not None


# Funzioni di utilità per compatibilità con il codice esistente
def converti_lista_a_oggetti(data: List[Dict]) -> ListaStudenti:
    """Converte una lista di dizionari in oggetti ListaStudenti"""
    lista = ListaStudenti()
    lista.from_dict_list(data)
    return lista


def converti_oggetti_a_lista(lista_studenti: ListaStudenti) -> List[Dict]:
    """Converte oggetti ListaStudenti in lista di dizionari"""
    return lista_studenti.to_dict_list()
