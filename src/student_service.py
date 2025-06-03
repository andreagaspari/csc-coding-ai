"""
Operazioni CRUD sugli studenti
=============================
Contiene tutte le operazioni per gestire gli studenti.
"""

from typing import List, Dict, Optional
from src.models import Studente, ListaStudenti
from src.data_manager import FileManager
from src.utils import valida_voto, valida_matricola, valida_nome, calcola_media


class StudentService:
    """Servizio per la gestione degli studenti"""
    
    def __init__(self, file_manager: FileManager):
        """
        Inizializza il servizio studenti.
        
        Args:
            file_manager: Gestore dei file per la persistenza
        """
        self.file_manager = file_manager
        self._lista_studenti = None
    
    def _carica_studenti(self) -> ListaStudenti:
        """Carica gli studenti dal file"""
        if self._lista_studenti is None:
            data = self.file_manager.leggi_studenti()
            self._lista_studenti = ListaStudenti()
            if data:
                self._lista_studenti.from_dict_list(data)
        return self._lista_studenti
    
    def _salva_studenti(self) -> bool:
        """Salva gli studenti nel file"""
        if self._lista_studenti is None:
            return True
        
        data = self._lista_studenti.to_dict_list()
        return self.file_manager.salva_studenti(data)
    
    def ottieni_tutti_studenti(self) -> List[Studente]:
        """
        Ottiene tutti gli studenti.
        
        Returns:
            List[Studente]: Lista di tutti gli studenti
        """
        lista = self._carica_studenti()
        return list(lista.studenti)
    
    def trova_studente_per_matricola(self, matricola: str) -> Optional[Studente]:
        """
        Trova uno studente per matricola.
        
        Args:
            matricola: Matricola dello studente
            
        Returns:
            Optional[Studente]: Studente trovato o None
        """
        lista = self._carica_studenti()
        return lista.trova_studente(int(matricola))
    
    def aggiungi_studente(self, matricola: str, nome: str, cognome: str, 
                         voti: List[int] = None) -> bool:
        """
        Aggiunge un nuovo studente.
        
        Args:
            matricola: Matricola del nuovo studente
            nome: Nome del nuovo studente
            cognome: Cognome del nuovo studente
            voti: Lista di voti opzionale
            
        Returns:
            bool: True se l'aggiunta è riuscita
            
        Raises:
            ValueError: Se i dati non sono validi
        """
        # Validazione input
        matricola_valida = valida_matricola(matricola)
        nome_valido = valida_nome(nome)
        cognome_valido = valida_nome(cognome)
        
        lista = self._carica_studenti()
        
        # Verifica unicità matricola
        if lista.trova_studente(int(matricola_valida)):
            raise ValueError(f"La matricola {matricola_valida} esiste già")
        
        # Crea nuovo studente
        nuovo_studente = Studente(
            nome=nome_valido,
            cognome=cognome_valido,
            matricola=int(matricola_valida),
            voti=voti or []
        )
        
        # Aggiunge alla lista
        if lista.aggiungi_studente(nuovo_studente):
            return self._salva_studenti()
        return False
    
    def rimuovi_studente(self, matricola: str) -> bool:
        """
        Rimuove uno studente.
        
        Args:
            matricola: Matricola dello studente da rimuovere
            
        Returns:
            bool: True se la rimozione è riuscita
        """
        lista = self._carica_studenti()
        if lista.rimuovi_studente(int(matricola)):
            return self._salva_studenti()
        return False
    
    def aggiungi_voto_studente(self, matricola: str, voto: str) -> bool:
        """
        Aggiunge un voto a uno studente.
        
        Args:
            matricola: Matricola dello studente
            voto: Voto da aggiungere (come stringa)
            
        Returns:
            bool: True se l'aggiunta è riuscita
            
        Raises:
            ValueError: Se il voto non è valido
        """
        voto_valido = valida_voto(voto)
        lista = self._carica_studenti()
        studente = lista.trova_studente(int(matricola))
        
        if not studente:
            raise ValueError(f"Studente con matricola {matricola} non trovato")
        
        if studente.aggiungi_voto(voto_valido):
            return self._salva_studenti()
        return False
    
    def ottieni_statistiche(self) -> Dict:
        """
        Ottiene le statistiche generali.
        
        Returns:
            Dict: Dizionario con le statistiche
        """
        lista = self._carica_studenti()
        return lista.statistiche()
    
    def cerca_studenti_per_nome(self, nome: str, cognome: str = None) -> List[Studente]:
        """
        Cerca studenti per nome/cognome.
        
        Args:
            nome: Nome da cercare
            cognome: Cognome da cercare (opzionale)
            
        Returns:
            List[Studente]: Lista di studenti trovati
        """
        lista = self._carica_studenti()
        return lista.trova_per_nome(nome, cognome)
    
    def ottieni_studenti_ordinati(self, criterio: str = "nome") -> List[Studente]:
        """
        Ottiene studenti ordinati secondo un criterio.
        
        Args:
            criterio: Criterio di ordinamento ("nome" o "media")
            
        Returns:
            List[Studente]: Lista di studenti ordinati
        """
        lista = self._carica_studenti()
        if criterio == "media":
            return lista.ordina_per_media()
        else:
            return lista.ordina_per_nome()


# Funzioni di compatibilità con il codice esistente
def trova_studente_per_matricola(studenti: List[Dict], matricola: str) -> Optional[Dict]:
    """
    Funzione di compatibilità per trovare uno studente per matricola.
    
    Args:
        studenti: Lista di studenti come dizionari
        matricola: Matricola da cercare
        
    Returns:
        Optional[Dict]: Studente trovato o None
    """
    for studente in studenti:
        if studente.get("matricola") == matricola:
            return studente
    return None


def matricola_esiste(studenti: List[Dict], matricola: str) -> bool:
    """
    Funzione di compatibilità per verificare se una matricola esiste.
    
    Args:
        studenti: Lista di studenti come dizionari
        matricola: Matricola da verificare
        
    Returns:
        bool: True se la matricola esiste
    """
    return trova_studente_per_matricola(studenti, matricola) is not None


def stampa_studenti(studenti: List[Dict]):
    """
    Stampa a schermo la lista degli studenti con i loro dati.
    
    Args:
        studenti: Lista di studenti da stampare
    """
    if not studenti:
        print("\n📋 Nessuno studente presente nel registro.")
        return
        
    print(f"\n📋 Lista studenti ({len(studenti)} studenti):")
    print("-" * 60)
    for studente in studenti:
        matricola = studente.get("matricola", "N/D")
        nome = studente.get("nome", "N/D")
        cognome = studente.get("cognome", "N/D")
        voti = studente.get("voti", [])
        media = calcola_media(voti)
        num_voti = len(voti)
        print(f"[{matricola}] {nome} {cognome} - Media: {media:.2f} ({num_voti} voti)")


def stampa_voti_studente(studenti: List[Dict], matricola: str):
    """
    Stampa i voti dettagliati di uno studente specifico.
    
    Args:
        studenti: Lista di studenti
        matricola: Matricola dello studente
    """
    studente = trova_studente_per_matricola(studenti, matricola)
    
    if not studente:
        print(f"❌ Nessuno studente trovato con matricola {matricola}")
        return
    
    nome = studente.get("nome", "N/D")
    cognome = studente.get("cognome", "N/D")
    voti = studente.get("voti", [])
    
    print(f"\n📊 Voti di {nome} {cognome} (Matricola: {matricola})")
    print("-" * 50)
    
    if not voti:
        print("   Nessun voto presente")
        return
    
    # Stampa i voti
    for i, voto in enumerate(voti, 1):
        print(f"   Esame {i}: {voto}")
    
    # Statistiche
    media = calcola_media(voti)
    print(f"\n📈 Statistiche:")
    print(f"   • Numero voti: {len(voti)}")
    print(f"   • Media: {media:.2f}")
    print(f"   • Voto massimo: {max(voti)}")
    print(f"   • Voto minimo: {min(voti)}")
    
    # Status dello studente
    if media >= 27:
        status = "🌟 Eccellente"
    elif media >= 24:
        status = "👍 Buono"
    elif media >= 18:
        status = "✅ Sufficiente"
    else:
        status = "❓ Da valutare"
    
    print(f"   • Stato: {status}")
