"""
Operazioni sui file per il registro studenti
===========================================
Gestisce il caricamento e salvataggio dei dati in formato JSON.
"""

import json
from typing import List, Dict
from pathlib import Path
from src.config import DEFAULT_DATA_PATH


class FileManager:
    """Gestisce le operazioni sui file per il registro studenti"""
    
    def __init__(self, file_path: Path = None):
        """
        Inizializza il gestore file.
        
        Args:
            file_path: Percorso del file dati (opzionale)
        """
        self.file_path = file_path or DEFAULT_DATA_PATH
        
    def leggi_studenti(self) -> List[Dict]:
        """
        Legge i dati degli studenti dal file JSON.
        
        Returns:
            List[Dict]: Lista di dizionari con i dati degli studenti
        """
        try:
            if not self.file_path.exists():
                # Se il file non esiste, crea un file vuoto
                self.salva_studenti([])
                return []
            
            with open(self.file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                
            # Validazione base della struttura dati
            if not isinstance(data, list):
                raise ValueError("Il file deve contenere una lista JSON")
            
            return data
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Errore nel formato JSON del file: {e}")
        except Exception as e:
            raise IOError(f"Errore nella lettura del file: {e}")
    
    def salva_studenti(self, studenti: List[Dict]) -> bool:
        """
        Salva i dati degli studenti nel file JSON.
        
        Args:
            studenti: Lista di dizionari con i dati degli studenti
            
        Returns:
            bool: True se il salvataggio è riuscito, False altrimenti
        """
        try:
            # Assicura che la directory esista
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.file_path, 'w', encoding='utf-8') as file:
                json.dump(studenti, file, ensure_ascii=False, indent=2)
            
            return True
            
        except Exception as e:
            print(f"❌ Errore nel salvataggio del file: {e}")
            return False
    
    def backup_data(self) -> Path:
        """
        Crea un backup dei dati correnti.
        
        Returns:
            Path: Percorso del file di backup creato
        """
        from src.utils import genera_nome_file_timestamp
        
        if not self.file_path.exists():
            raise FileNotFoundError("Nessun file dati da cui fare backup")
        
        backup_name = genera_nome_file_timestamp("backup_registro", "txt")
        backup_path = self.file_path.parent / backup_name
        
        # Copia il contenuto
        import shutil
        shutil.copy2(self.file_path, backup_path)
        
        return backup_path
    
    def verifica_integrità(self) -> bool:
        """
        Verifica l'integrità del file dati.
        
        Returns:
            bool: True se il file è integro, False altrimenti
        """
        try:
            data = self.leggi_studenti()
            
            # Verifica che ogni studente abbia i campi richiesti
            campi_richiesti = {'matricola', 'nome', 'cognome', 'voti'}
            for studente in data:
                if not isinstance(studente, dict):
                    return False
                if not campi_richiesti.issubset(studente.keys()):
                    return False
                if not isinstance(studente['voti'], list):
                    return False
            
            return True
            
        except Exception:
            return False


# Funzioni di compatibilità con il codice esistente
def leggi_studenti_da_file(percorso_file: str) -> List[Dict]:
    """
    Funzione di compatibilità per leggere studenti da file.
    
    Args:
        percorso_file: Percorso del file come stringa
        
    Returns:
        List[Dict]: Lista di studenti
    """
    file_manager = FileManager(Path(percorso_file))
    try:
        return file_manager.leggi_studenti()
    except Exception as e:
        print(f"❌ Errore nella lettura del file: {e}")
        return []


def salva_studenti_su_file(percorso_file: str, studenti: List[Dict]) -> bool:
    """
    Funzione di compatibilità per salvare studenti su file.
    
    Args:
        percorso_file: Percorso del file come stringa
        studenti: Lista di studenti da salvare
        
    Returns:
        bool: True se il salvataggio è riuscito
    """
    file_manager = FileManager(Path(percorso_file))
    return file_manager.salva_studenti(studenti)
