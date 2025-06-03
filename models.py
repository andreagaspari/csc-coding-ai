"""
Modello dati per il registro studenti
====================================
Contiene le strutture dati e le funzioni di validazione.
"""

from typing import List, Dict, Optional


class Persona:
    """Classe base per rappresentare una persona"""
    
    def __init__(self, nome: str, cognome: str):
        """
        Inizializza una nuova persona.
        
        Args:
            nome: Nome della persona
            cognome: Cognome della persona
        """
        self.nome = nome
        self.cognome = cognome
    
    def nome_completo(self) -> str:
        """
        Restituisce il nome completo della persona.
        
        Returns:
            str: Nome e cognome concatenati
        """
        return f"{self.nome} {self.cognome}"
    
    def iniziali(self) -> str:
        """
        Restituisce le iniziali del nome e cognome.
        
        Returns:
            str: Iniziali (es. "M.R." per Mario Rossi)
        """
        nome_iniziale = self.nome[0].upper() if self.nome else ""
        cognome_iniziale = self.cognome[0].upper() if self.cognome else ""
        return f"{nome_iniziale}.{cognome_iniziale}." if nome_iniziale and cognome_iniziale else ""
    
    def __str__(self) -> str:
        """Rappresentazione stringa della persona"""
        return self.nome_completo()
    
    def __eq__(self, other) -> bool:
        """Confronto tra due persone basato su nome e cognome"""
        if not isinstance(other, Persona):
            return False
        return self.nome == other.nome and self.cognome == other.cognome
    
    def __hash__(self) -> int:
        """Hash della persona per poterla usare in set e dict"""
        return hash((self.nome, self.cognome))


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
    
    def voto_massimo(self) -> int:
        """
        Restituisce il voto più alto dello studente.
        
        Returns:
            int: Voto massimo, 0 se non ci sono voti
        """
        return max(self.voti) if self.voti else 0
    
    def voto_minimo(self) -> int:
        """
        Restituisce il voto più basso dello studente.
        
        Returns:
            int: Voto minimo, 0 se non ci sono voti
        """
        return min(self.voti) if self.voti else 0
    
    def numero_voti(self) -> int:
        """
        Restituisce il numero di voti dello studente.
        
        Returns:
            int: Numero di voti
        """
        return len(self.voti)
    
    def ha_superato_esami(self) -> bool:
        """
        Verifica se lo studente ha almeno un voto (ha superato almeno un esame).
        
        Returns:
            bool: True se ha almeno un voto, False altrimenti
        """
        return len(self.voti) > 0
    
    def is_eccellente(self) -> bool:
        """
        Verifica se lo studente è eccellente (media >= 28).
        
        Returns:
            bool: True se la media è >= 28, False altrimenti
        """
        return self.media_voti() >= 28.0
    
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
        """Rappresentazione stringa dello studente con informazioni estese"""
        media = self.media_voti()
        return f"[{self.matricola}] {self.nome_completo()} - Media: {media:.2f} ({len(self.voti)} voti)"
    
    def __eq__(self, other) -> bool:
        """Confronto tra due studenti basato sulla matricola"""
        if not isinstance(other, Studente):
            return False
        return self.matricola == other.matricola
    
    def __hash__(self) -> int:
        """Hash dello studente basato sulla matricola"""
        return hash(self.matricola)


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
    
    def trova_per_nome(self, nome: str, cognome: str = None) -> List[Studente]:
        """
        Trova studenti per nome e/o cognome.
        
        Args:
            nome: Nome da cercare
            cognome: Cognome da cercare (opzionale)
            
        Returns:
            List[Studente]: Lista di studenti trovati
        """
        risultati = []
        for studente in self.studenti:
            if cognome:
                if studente.nome.lower() == nome.lower() and studente.cognome.lower() == cognome.lower():
                    risultati.append(studente)
            else:
                if nome.lower() in studente.nome.lower() or nome.lower() in studente.cognome.lower():
                    risultati.append(studente)
        return risultati
    
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
    
    def studenti_eccellenti(self) -> List[Studente]:
        """
        Restituisce gli studenti eccellenti (media >= 28).
        
        Returns:
            List[Studente]: Lista di studenti eccellenti
        """
        return [s for s in self.studenti if s.is_eccellente()]
    
    def studenti_con_voti(self) -> List[Studente]:
        """
        Restituisce gli studenti che hanno almeno un voto.
        
        Returns:
            List[Studente]: Lista di studenti con voti
        """
        return [s for s in self.studenti if s.ha_superato_esami()]
    
    def studenti_senza_voti(self) -> List[Studente]:
        """
        Restituisce gli studenti che non hanno ancora voti.
        
        Returns:
            List[Studente]: Lista di studenti senza voti
        """
        return [s for s in self.studenti if not s.ha_superato_esami()]
    
    def media_generale(self) -> float:
        """
        Calcola la media generale di tutti gli studenti con voti.
        
        Returns:
            float: Media generale, 0.0 se nessuno studente ha voti
        """
        studenti_con_voti = self.studenti_con_voti()
        if not studenti_con_voti:
            return 0.0
        
        medie = [s.media_voti() for s in studenti_con_voti]
        return sum(medie) / len(medie)
    
    def statistiche(self) -> Dict:
        """
        Restituisce un dizionario con le statistiche della lista.
        
        Returns:
            Dict: Statistiche complete della lista
        """
        studenti_con_voti = self.studenti_con_voti()
        studenti_eccellenti = self.studenti_eccellenti()
        
        stats = {
            "totale_studenti": len(self.studenti),
            "studenti_con_voti": len(studenti_con_voti),
            "studenti_senza_voti": len(self.studenti_senza_voti()),
            "studenti_eccellenti": len(studenti_eccellenti),
            "media_generale": self.media_generale()
        }
        
        if studenti_con_voti:
            medie = [s.media_voti() for s in studenti_con_voti]
            stats.update({
                "media_piu_alta": max(medie),
                "media_piu_bassa": min(medie),
                "migliore_studente": max(studenti_con_voti, key=lambda s: s.media_voti()).nome_completo()
            })
        
        return stats
    
    def ordina_per_media(self, decrescente: bool = True) -> List[Studente]:
        """
        Restituisce la lista di studenti ordinata per media.
        
        Args:
            decrescente: Se True ordina dalla media più alta, altrimenti dalla più bassa
            
        Returns:
            List[Studente]: Lista ordinata per media
        """
        studenti_con_voti = self.studenti_con_voti()
        return sorted(studenti_con_voti, key=lambda s: s.media_voti(), reverse=decrescente)
    
    def ordina_per_nome(self) -> List[Studente]:
        """
        Restituisce la lista di studenti ordinata alfabeticamente per nome completo.
        
        Returns:
            List[Studente]: Lista ordinata per nome
        """
        return sorted(self.studenti, key=lambda s: s.nome_completo())
    
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
    
    def __contains__(self, matricola: int) -> bool:
        """Verifica se una matricola è presente nella lista"""
        return self.trova_studente(matricola) is not None


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
