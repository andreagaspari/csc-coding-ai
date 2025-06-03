"""
Test unitari per il modulo data_manager
======================================
Testa la gestione dei file e il salvataggio/caricamento dati.
"""

import pytest
import json
from pathlib import Path
from src.data_manager import FileManager


class TestFileManager:
    """Test per la classe FileManager"""
    
    def test_init_con_file_path(self, temp_file):
        fm = FileManager(temp_file)
        assert fm.file_path == temp_file
    
    def test_init_senza_file_path(self):
        fm = FileManager()
        assert fm.file_path is not None
    
    def test_carica_dati_file_esistente(self, temp_file, sample_student_data):
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(sample_student_data, f)
        fm = FileManager(temp_file)
        dati = fm.leggi_studenti()
        assert len(dati) == 3
        assert dati[0]["nome"] == "Mario"
    
    def test_carica_dati_file_inesistente(self, temp_file):
        if temp_file.exists():
            temp_file.unlink()
        fm = FileManager(temp_file)
        dati = fm.leggi_studenti()
        assert dati == []
    
    def test_carica_dati_file_json_invalido(self, temp_file):
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write("{ invalid json }")
        fm = FileManager(temp_file)
        with pytest.raises(ValueError):
            fm.leggi_studenti()
    
    def test_salva_dati_successo(self, temp_file, sample_student_data):
        fm = FileManager(temp_file)
        assert fm.salva_studenti(sample_student_data) is True
        with open(temp_file, 'r', encoding='utf-8') as f:
            dati_salvati = json.load(f)
        assert len(dati_salvati) == 3
        assert dati_salvati[0]["nome"] == "Mario"
    
    def test_salva_dati_lista_vuota(self, temp_file):
        fm = FileManager(temp_file)
        assert fm.salva_studenti([]) is True
        with open(temp_file, 'r', encoding='utf-8') as f:
            dati_salvati = json.load(f)
        assert dati_salvati == []
    
    def test_salva_dati_cartella_inesistente(self):
        file_path = Path("/cartella/inesistente/test.txt")
        fm = FileManager(file_path)
        assert fm.salva_studenti([]) is False
    
    def test_crea_backup_successo(self, temp_file, sample_student_data):
        fm = FileManager(temp_file)
        fm.salva_studenti(sample_student_data)
        backup_path = fm.backup_data()
        assert backup_path is not None
        assert backup_path.exists()
        with open(backup_path, 'r', encoding='utf-8') as f:
            dati_backup = json.load(f)
        assert len(dati_backup) == 3
        backup_path.unlink()
    
    def test_crea_backup_file_inesistente(self, temp_file):
        if temp_file.exists():
            temp_file.unlink()
        fm = FileManager(temp_file)
        with pytest.raises(FileNotFoundError):
            fm.backup_data()
    
    def test_verifica_integrità_file_valido(self, temp_file, sample_student_data):
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(sample_student_data, f)
        fm = FileManager(temp_file)
        assert fm.verifica_integrità() is True
    
    def test_verifica_integrità_file_invalido(self, temp_file):
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write("invalid json")
        fm = FileManager(temp_file)
        assert fm.verifica_integrità() is False
    
    def test_verifica_integrità_file_inesistente(self, temp_file):
        if temp_file.exists():
            temp_file.unlink()
        fm = FileManager(temp_file)
        # Un file inesistente viene considerato valido (nessun dato corrotto)
        assert fm.verifica_integrità() is True
    
    @pytest.mark.data
    def test_ciclo_completo_salvataggio_caricamento(self, temp_file, sample_student_data):
        fm = FileManager(temp_file)
        assert fm.salva_studenti(sample_student_data) is True
        dati_caricati = fm.leggi_studenti()
        assert dati_caricati == sample_student_data
    
    def test_gestione_encoding_utf8(self, temp_file):
        dati_con_accenti = [
            {
                "matricola": "12345",
                "nome": "José",
                "cognome": "García",
                "voti": [25, 30]
            }
        ]
        fm = FileManager(temp_file)
        assert fm.salva_studenti(dati_con_accenti) is True
        dati_caricati = fm.leggi_studenti()
        assert dati_caricati[0]["nome"] == "José"
        assert dati_caricati[0]["cognome"] == "García"
