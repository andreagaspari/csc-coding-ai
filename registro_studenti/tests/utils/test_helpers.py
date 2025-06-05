"""
Utilità per i test
==================
Contiene funzioni helper e utilità comuni per i test.
"""

import tempfile
import json
from pathlib import Path
from typing import List, Dict
from src.models import Studente, ListaStudenti


def crea_file_test_json(data: List[Dict], encoding='utf-8') -> Path:
    """
    Crea un file JSON temporaneo per i test.
    
    Args:
        data: Dati da scrivere nel file
        encoding: Encoding del file
        
    Returns:
        Path: Percorso del file creato
    """
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', 
                                     delete=False, encoding=encoding) as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        return Path(f.name)


def crea_studenti_test(count: int = 5) -> List[Studente]:
    """
    Crea una lista di studenti per i test.
    
    Args:
        count: Numero di studenti da creare
        
    Returns:
        List[Studente]: Lista di studenti test
    """
    studenti = []
    nomi = ["Mario", "Lucia", "Paolo", "Anna", "Marco"]
    cognomi = ["Rossi", "Bianchi", "Verdi", "Neri", "Gialli"]
    
    for i in range(min(count, len(nomi))):
        studente = Studente(
            nome=nomi[i],
            cognome=cognomi[i],
            matricola=10000 + i,
            voti=[18 + (i * 2), 20 + (i * 2), 22 + (i * 2)]
        )
        studenti.append(studente)
    
    return studenti


def verifica_struttura_dati(data: List[Dict]) -> bool:
    """
    Verifica che i dati abbiano la struttura corretta.
    
    Args:
        data: Dati da verificare
        
    Returns:
        bool: True se la struttura è corretta
    """
    if not isinstance(data, list):
        return False
    
    required_fields = ["matricola", "nome", "cognome", "voti"]
    
    for item in data:
        if not isinstance(item, dict):
            return False
        
        for field in required_fields:
            if field not in item:
                return False
        
        if not isinstance(item["voti"], list):
            return False
    
    return True


def confronta_studenti(studente1: Studente, studente2: Studente) -> bool:
    """
    Confronta due studenti per verificare se sono uguali.
    
    Args:
        studente1: Primo studente
        studente2: Secondo studente
        
    Returns:
        bool: True se sono uguali
    """
    return (studente1.matricola == studente2.matricola and
            studente1.nome == studente2.nome and
            studente1.cognome == studente2.cognome and
            studente1.voti == studente2.voti)


def calcola_statistiche_test(studenti: List[Studente]) -> Dict:
    """
    Calcola statistiche per i test.
    
    Args:
        studenti: Lista di studenti
        
    Returns:
        Dict: Statistiche calcolate
    """
    studenti_con_voti = [s for s in studenti if s.ha_superato_esami()]
    
    if not studenti_con_voti:
        return {
            "totale": len(studenti),
            "con_voti": 0,
            "media_generale": 0.0,
            "eccellenti": 0
        }
    
    medie = [s.media_voti() for s in studenti_con_voti]
    eccellenti = [s for s in studenti_con_voti if s.is_eccellente()]
    
    return {
        "totale": len(studenti),
        "con_voti": len(studenti_con_voti),
        "media_generale": sum(medie) / len(medie),
        "eccellenti": len(eccellenti)
    }


class AssertHelper:
    """Helper per asserzioni personalizzate nei test"""
    
    @staticmethod
    def assert_studente_valido(studente: Studente):
        """Verifica che uno studente sia valido"""
        assert studente is not None
        assert isinstance(studente.matricola, int)
        assert studente.matricola > 0
        assert len(studente.nome) > 0
        assert len(studente.cognome) > 0
        assert isinstance(studente.voti, list)
        
        for voto in studente.voti:
            assert isinstance(voto, int)
            assert 18 <= voto <= 30
    
    @staticmethod
    def assert_lista_studenti_valida(lista: ListaStudenti):
        """Verifica che una lista studenti sia valida"""
        assert lista is not None
        assert isinstance(lista.studenti, list)
        
        for studente in lista.studenti:
            AssertHelper.assert_studente_valido(studente)
    
    @staticmethod
    def assert_file_json_valido(file_path: Path):
        """Verifica che un file JSON sia valido"""
        assert file_path.exists()
        assert file_path.suffix == '.json'
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            assert verifica_struttura_dati(data)
        except (json.JSONDecodeError, FileNotFoundError):
            assert False, f"File JSON non valido: {file_path}"


def cleanup_test_files(*file_paths: Path):
    """
    Pulisce i file di test.
    
    Args:
        *file_paths: Percorsi dei file da eliminare
    """
    for file_path in file_paths:
        if file_path and file_path.exists():
            try:
                file_path.unlink()
            except OSError:
                pass  # Ignora errori di cancellazione
