"""
Fixtures comuni per i test
=========================
Contiene fixtures e dati di test riutilizzabili.
"""

import pytest
import tempfile
from pathlib import Path
from typing import List, Dict
from src.models import Studente, ListaStudenti
from src.data_manager import FileManager
from src.student_service import StudentService


@pytest.fixture
def sample_student_data() -> List[Dict]:
    """Fixture con dati di test per studenti"""
    return [
        {
            "matricola": "12345",
            "nome": "Mario",
            "cognome": "Rossi",
            "voti": [24, 28, 30, 26]
        },
        {
            "matricola": "67890",
            "nome": "Lucia",
            "cognome": "Bianchi",
            "voti": [30, 29, 28]
        },
        {
            "matricola": "11111",
            "nome": "Paolo",
            "cognome": "Verdi",
            "voti": []
        }
    ]


@pytest.fixture
def studente_mario() -> Studente:
    """Fixture per uno studente singolo - Mario"""
    return Studente(
        nome="Mario",
        cognome="Rossi", 
        matricola=12345,
        voti=[24, 28, 30, 26]
    )


@pytest.fixture
def studente_lucia() -> Studente:
    """Fixture per uno studente singolo - Lucia"""
    return Studente(
        nome="Lucia",
        cognome="Bianchi",
        matricola=67890,
        voti=[30, 29, 28]
    )


@pytest.fixture
def studente_senza_voti() -> Studente:
    """Fixture per uno studente senza voti"""
    return Studente(
        nome="Paolo",
        cognome="Verdi",
        matricola=11111,
        voti=[]
    )


@pytest.fixture
def lista_studenti_vuota() -> ListaStudenti:
    """Fixture per una lista studenti vuota"""
    return ListaStudenti()


@pytest.fixture
def lista_studenti_popolata(studente_mario, studente_lucia, studente_senza_voti) -> ListaStudenti:
    """Fixture per una lista studenti popolata"""
    lista = ListaStudenti()
    lista.aggiungi_studente(studente_mario)
    lista.aggiungi_studente(studente_lucia)
    lista.aggiungi_studente(studente_senza_voti)
    return lista


@pytest.fixture
def temp_file():
    """Fixture per un file temporaneo inizializzato come lista JSON vuota"""
    import json
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write('[]')
        temp_path = Path(f.name)
    yield temp_path
    if temp_path.exists():
        temp_path.unlink()


@pytest.fixture
def file_manager_temp(temp_file):
    """Fixture per FileManager con file temporaneo"""
    return FileManager(temp_file)


@pytest.fixture
def student_service_temp(file_manager_temp):
    """Fixture per StudentService con file temporaneo"""
    return StudentService(file_manager_temp)


@pytest.fixture
def voti_validi() -> List[int]:
    """Fixture con voti validi"""
    return [18, 24, 27, 30]


@pytest.fixture
def voti_invalidi() -> List[int]:
    """Fixture con voti non validi"""
    return [10, 17, 31, 35]
