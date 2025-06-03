"""
Test unitari per il modulo student_service
==========================================
Testa il servizio di gestione degli studenti.
"""

import pytest
from unittest.mock import Mock, patch
from src.student_service import StudentService
from src.models import Studente, ListaStudenti
from src.data_manager import FileManager


class TestStudentService:
    """Test per la classe StudentService"""
    
    def test_init_student_service(self, file_manager_temp):
        """Test inizializzazione StudentService"""
        service = StudentService(file_manager_temp)
        assert service.file_manager == file_manager_temp
        # _lista_studenti è None all'inizio
        assert service._lista_studenti is None
    
    def test_carica_studenti_successo(self, sample_student_data):
        """Test caricamento studenti con successo"""
        mock_file_manager = Mock()
        mock_file_manager.leggi_studenti.return_value = sample_student_data
        service = StudentService(mock_file_manager)
        lista = service._carica_studenti()
        assert len(lista) == 3
        assert lista.trova_studente(12345) is not None
    
    def test_carica_studenti_file_vuoto(self):
        """Test caricamento da file vuoto"""
        mock_file_manager = Mock()
        mock_file_manager.leggi_studenti.return_value = []
        service = StudentService(mock_file_manager)
        lista = service._carica_studenti()
        assert len(lista) == 0
    
    def test_salva_studenti_successo(self, sample_student_data):
        """Test salvataggio studenti con successo"""
        mock_file_manager = Mock()
        mock_file_manager.salva_studenti.return_value = True
        mock_file_manager.leggi_studenti.return_value = sample_student_data
        service = StudentService(mock_file_manager)
        service._carica_studenti()
        assert service._salva_studenti() is True
        mock_file_manager.salva_studenti.assert_called_once()
    
    def test_salva_studenti_errore(self):
        """Test salvataggio studenti con errore"""
        mock_file_manager = Mock()
        mock_file_manager.salva_studenti.return_value = False
        service = StudentService(mock_file_manager)
        service._lista_studenti = ListaStudenti()
        assert service._salva_studenti() is False
    
    def test_aggiungi_studente_nuovo(self, student_service_temp):
        """Test aggiunta studente nuovo"""
        risultato = student_service_temp.aggiungi_studente("12345", "Mario", "Rossi")
        assert risultato is True
        studente = student_service_temp._carica_studenti().trova_studente(12345)
        assert studente is not None

    def test_aggiungi_studente_duplicato(self, student_service_temp):
        """Test aggiunta studente duplicato"""
        student_service_temp.aggiungi_studente("12345", "Mario", "Rossi")
        with pytest.raises(ValueError):
            student_service_temp.aggiungi_studente("12345", "Mario", "Rossi")
        assert len(student_service_temp._carica_studenti()) == 1

    def test_rimuovi_studente_esistente(self, student_service_temp):
        """Test rimozione studente esistente"""
        student_service_temp.aggiungi_studente("12345", "Mario", "Rossi")
        risultato = student_service_temp.rimuovi_studente("12345")
        assert risultato is True
        assert student_service_temp._carica_studenti().trova_studente(12345) is None

    def test_rimuovi_studente_inesistente(self, student_service_temp):
        risultato = student_service_temp.rimuovi_studente("99999")
        assert risultato is False

    def test_aggiungi_voto_studente_esistente(self, student_service_temp):
        student_service_temp.aggiungi_studente("12345", "Mario", "Rossi")
        risultato = student_service_temp.aggiungi_voto("12345", "28")
        assert risultato is True
        studente = student_service_temp._carica_studenti().trova_studente(12345)
        assert 28 in studente.voti

    def test_aggiungi_voto_studente_inesistente(self, student_service_temp):
        with pytest.raises(ValueError):
            student_service_temp.aggiungi_voto("99999", "28")

    def test_aggiungi_voto_invalido(self, student_service_temp):
        student_service_temp.aggiungi_studente("12345", "Mario", "Rossi")
        with pytest.raises(ValueError):
            student_service_temp.aggiungi_voto("12345", "17")
        studente = student_service_temp._carica_studenti().trova_studente(12345)
        assert len(studente.voti) == 0

    def test_ottieni_studente_esistente(self, student_service_temp):
        student_service_temp.aggiungi_studente("12345", "Mario", "Rossi")
        studente = student_service_temp.ottieni_studente(12345)
        assert studente is not None
        assert studente.nome == "Mario"

    def test_ottieni_studente_inesistente(self, student_service_temp):
        studente = student_service_temp.ottieni_studente(99999)
        assert studente is None

    def test_ottieni_tutti_studenti(self, student_service_temp):
        student_service_temp.aggiungi_studente("12345", "Mario", "Rossi")
        student_service_temp.aggiungi_studente("67890", "Lucia", "Bianchi")
        studenti = student_service_temp.ottieni_tutti_studenti()
        assert len(studenti) == 2

    def test_cerca_studenti_per_nome(self, student_service_temp):
        student_service_temp.aggiungi_studente("12345", "Mario", "Rossi")
        student_service_temp.aggiungi_studente("67890", "Maria", "Bianchi")
        risultati = student_service_temp.cerca_studenti("Mari")
        assert len(risultati) == 2

    def test_ottieni_studenti_eccellenti(self, student_service_temp):
        student_service_temp.aggiungi_studente("12345", "Mario", "Rossi")
        student_service_temp.aggiungi_voto("12345", "30")
        student_service_temp.aggiungi_voto("12345", "29")
        student_service_temp.aggiungi_studente("11111", "Paolo", "Verdi")
        student_service_temp.aggiungi_voto("11111", "20")
        eccellenti = student_service_temp.ottieni_studenti_eccellenti()
        assert len(eccellenti) == 1
        assert eccellenti[0].nome == "Mario"

    def test_ottieni_statistiche(self, student_service_temp):
        student_service_temp.aggiungi_studente("12345", "Mario", "Rossi")
        student_service_temp.aggiungi_voto("12345", "25")
        student_service_temp.aggiungi_studente("11111", "Paolo", "Verdi")
        stats = student_service_temp.ottieni_statistiche()
        assert stats["totale_studenti"] == 2
        assert stats["studenti_con_voti"] == 1
        assert stats["studenti_senza_voti"] == 1

    @pytest.mark.integration
    def test_ciclo_completo_crud(self, student_service_temp):
        """Test ciclo completo CRUD"""
        # Create
        assert student_service_temp.aggiungi_studente("12345", "Mario", "Rossi") is True
        # Read
        studente = student_service_temp.ottieni_studente(12345)
        assert studente is not None
        # Update
        assert student_service_temp.aggiungi_voto("12345", "30") is True
        studente = student_service_temp.ottieni_studente(12345)
        assert 30 in studente.voti
        # Delete
        assert student_service_temp.rimuovi_studente("12345") is True
        assert student_service_temp.ottieni_studente(12345) is None
    
    def test_validazione_parametri_aggiungi_studente(self, student_service_temp):
        """Test validazione parametri nell'aggiunta studente"""
        # Nome vuoto
        with pytest.raises(ValueError):
            student_service_temp.aggiungi_studente("", "Rossi", "12345")
        
        # Cognome vuoto
        with pytest.raises(ValueError):
            student_service_temp.aggiungi_studente("Mario", "", "12345")
        
        # Matricola invalida
        with pytest.raises(ValueError):
            student_service_temp.aggiungi_studente("Mario", "Rossi", "-1")
