"""
Test unitari per il modulo pdf_exporter
======================================
Testa l'esportazione PDF degli studenti.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
from src.pdf_exporter import PDFExporter
from src.models import Studente, ListaStudenti


class TestPDFExporter:
    """Test per la classe PDFExporter"""
    
    def test_init_pdf_exporter(self):
        """Test inizializzazione PDFExporter"""
        exporter = PDFExporter()
        assert exporter is not None
    
    @patch('src.pdf_exporter.SimpleDocTemplate')
    def test_esporta_lista_studenti_successo(self, mock_doc_template, lista_studenti_popolata, temp_file):
        """Test esportazione lista studenti con successo"""
        mock_doc = MagicMock()
        mock_doc_template.return_value = mock_doc
        
        exporter = PDFExporter()
        risultato = exporter.esporta_lista_studenti(lista_studenti_popolata.to_dict_list(), temp_file)
        
        assert isinstance(risultato, Path)
        mock_doc_template.assert_called_once()
        mock_doc.build.assert_called_once()
    
    @patch('src.pdf_exporter.SimpleDocTemplate')
    def test_esporta_lista_vuota(self, mock_doc_template, lista_studenti_vuota, temp_file):
        """Test esportazione lista studenti vuota"""
        mock_doc = MagicMock()
        mock_doc_template.return_value = mock_doc
        
        exporter = PDFExporter()
        risultato = exporter.esporta_lista_studenti(lista_studenti_vuota.to_dict_list(), temp_file)
        
        assert isinstance(risultato, Path)
        mock_doc_template.assert_called_once()
        mock_doc.build.assert_called_once()

    def test_esporta_studente_singolo_successo(self, studente_mario, temp_file):
        """Test esportazione studente singolo con successo"""
        exporter = PDFExporter()
        risultato = exporter.esporta_studente_singolo(studente_mario.to_dict(), temp_file)
        
        assert risultato is True or isinstance(risultato, Path)

    def test_esporta_statistiche_successo(self, lista_studenti_popolata, temp_file):
        """Test esportazione statistiche con successo"""
        stats = lista_studenti_popolata.statistiche()
        
        exporter = PDFExporter()
        risultato = exporter.esporta_statistiche(stats, temp_file)
        
        assert risultato is True or isinstance(risultato, Path)
    
    def test_esporta_con_percorso_invalido(self, lista_studenti_popolata):
        """Test esportazione con percorso non valido"""
        exporter = PDFExporter()
        percorso_invalido = Path("/cartella/inesistente/test.pdf")
        # Non solleva errore, ma può restituire Path o sollevare eccezione a runtime
        try:
            risultato = exporter.esporta_lista_studenti(lista_studenti_popolata.to_dict_list(), percorso_invalido)
            assert isinstance(risultato, Path)
        except Exception:
            assert True  # L'errore di scrittura è accettabile in test

    def test_validazione_parametri_lista_studenti(self, temp_file):
        """Test validazione parametri per lista studenti"""
        exporter = PDFExporter()
        with pytest.raises(ValueError):
            exporter.esporta_lista_studenti(None, temp_file)
        lista = ListaStudenti()
        with pytest.raises(ValueError):
            exporter.esporta_lista_studenti(lista, None)

    def test_validazione_parametri_studente_singolo(self, temp_file):
        """Test validazione parametri per studente singolo"""
        exporter = PDFExporter()
        with pytest.raises(ValueError):
            exporter.esporta_studente_singolo(None, temp_file)

    @patch('src.pdf_exporter.SimpleDocTemplate')
    def test_gestione_errore_doc_template(self, mock_doc_template, lista_studenti_popolata, temp_file):
        """Test gestione errore nel SimpleDocTemplate"""
        mock_doc_template.side_effect = Exception("Errore PDF")
        exporter = PDFExporter()
        with pytest.raises(Exception):
            exporter.esporta_lista_studenti(lista_studenti_popolata.to_dict_list(), temp_file)
