"""
Test di integrazione per l'applicazione
======================================
Testa l'integrazione tra i vari moduli del sistema.
"""

import pytest
import json
from pathlib import Path
from src.models import Studente, ListaStudenti
from src.data_manager import FileManager
from src.student_service import StudentService


class TestIntegrazioneCompleta:
    """Test di integrazione tra tutti i moduli"""
    
    @pytest.mark.integration
    def test_integrazione_salvataggio_caricamento(self, temp_file):
        """Test integrazione completa salvataggio e caricamento"""
        # Fase 1: Crea servizio e aggiungi studenti
        file_manager = FileManager(temp_file)
        service = StudentService(file_manager)
        
        # Aggiungi studenti
        service.aggiungi_studente("12345", "Mario", "Rossi")
        service.aggiungi_studente("67890", "Lucia", "Bianchi")
        
        # Aggiungi voti
        service.aggiungi_voto_studente("12345", "24")
        service.aggiungi_voto_studente("12345", "28")
        service.aggiungi_voto_studente("67890", "30")
        service.aggiungi_voto_studente("67890", "29")
        
        # Salva dati
        assert service._salva_studenti() is True
        
        # Fase 2: Crea nuovo servizio e carica dati
        service2 = StudentService(FileManager(temp_file))
        service2._carica_studenti()
        
        # Verifica che i dati siano stati caricati correttamente
        assert len(service2.ottieni_tutti_studenti()) == 2
        
        mario = service2.trova_studente_per_matricola("12345")
        assert mario is not None
        assert mario.nome == "Mario"
        assert mario.voti == [24, 28]
        assert mario.media_voti() == 26.0
        
        lucia = service2.trova_studente_per_matricola("67890")
        assert lucia is not None
        assert lucia.nome == "Lucia"
        assert lucia.voti == [30, 29]
        assert lucia.media_voti() == 29.5
    
    @pytest.mark.integration
    def test_integrazione_modifica_persistenza(self, temp_file):
        """Test integrazione modifica dati e persistenza"""
        file_manager = FileManager(temp_file)
        service = StudentService(file_manager)
        
        # Aggiungi studente iniziale
        service.aggiungi_studente("55555", "Marco", "Neri")
        service.aggiungi_voto_studente("55555", "25")
        service._salva_studenti()
        
        # Ricarica dati
        service._carica_studenti()
        
        # Modifica studente
        service.aggiungi_voto_studente("55555", "30")
        service.aggiungi_voto_studente("55555", "27")
        
        # Aggiungi nuovo studente
        service.aggiungi_studente("77777", "Anna", "Verdi")
        service.aggiungi_voto_studente("77777", "29")
        
        # Salva modifiche
        service._salva_studenti()
        
        # Verifica persistenza delle modifiche
        service_verifica = StudentService(FileManager(temp_file))
        service_verifica._carica_studenti()
        
        marco = service_verifica.trova_studente_per_matricola("55555")
        assert len(marco.voti) == 3
        assert marco.voti == [25, 30, 27]
        
        anna = service_verifica.trova_studente_per_matricola("77777")
        assert anna is not None
        assert anna.voti == [29]
    
    @pytest.mark.integration
    def test_integrazione_statistiche_complete(self, temp_file):
        """Test integrazione calcolo statistiche complete"""
        file_manager = FileManager(temp_file)
        service = StudentService(file_manager)
        
        # Crea dataset completo
        studenti_test = [
            ("Mario", "Rossi", 10001, [24, 26, 28]),      # Media: 26
            ("Lucia", "Bianchi", 10002, [30, 29, 28]),    # Media: 29 (eccellente)
            ("Paolo", "Verdi", 10003, []),                # Senza voti
            ("Anna", "Neri", 10004, [18, 20, 22]),        # Media: 20
            ("Roberto", "Gialli", 10005, [30, 30, 29]),   # Media: 29.67 (eccellente)
        ]
        
        for nome, cognome, matricola, voti in studenti_test:
            service.aggiungi_studente(str(matricola), nome, cognome)
            for voto in voti:
                service.aggiungi_voto_studente(str(matricola), str(voto))
        
        # Salva e ricarica per test completo
        service.salva_studenti()
        service.carica_studenti()
        
        # Verifica statistiche
        stats = service.ottieni_statistiche()
        assert stats["totale_studenti"] == 5
        assert stats["studenti_con_voti"] == 4
        assert stats["studenti_senza_voti"] == 1
        assert stats["studenti_eccellenti"] == 2
        
        # Verifica media generale (26+29+20+29.67)/4 = 26.17 circa
        assert abs(stats["media_generale"] - 26.1675) < 0.001
        
        # Verifica studenti eccellenti
        eccellenti = service.ottieni_studenti_eccellenti()
        nomi_eccellenti = [s.nome for s in eccellenti]
        assert "Lucia" in nomi_eccellenti
        assert "Roberto" in nomi_eccellenti
    
    @pytest.mark.integration
    def test_integrazione_backup_ripristino(self, temp_file):
        """Test integrazione backup e ripristino"""
        file_manager = FileManager(temp_file)
        service = StudentService(file_manager)
        
        # Aggiungi dati iniziali
        service.aggiungi_studente("12345", "Mario", "Rossi")
        service.aggiungi_voto_studente("12345", "25")
        service._salva_studenti()
        
        # Crea backup
        backup_path = file_manager.backup_data()
        assert backup_path is not None
        
        # Modifica dati
        service.aggiungi_studente("67890", "Paolo", "Verdi")
        service.rimuovi_studente(12345)
        service.salva_studenti()
        
        # Verifica modifiche
        assert len(service.ottieni_tutti_studenti()) == 1
        assert service.ottieni_studente(12345) is None
        
        # Ripristina backup
        assert file_manager.ripristina_backup(backup_path) is True

        # Invalida la cache per forzare il reload dal file
        service.invalida_cache()

        # Ricarica dati
        service.carica_studenti()
        
        # Verifica ripristino
        assert len(service.ottieni_tutti_studenti()) == 1
        mario = service.ottieni_studente(12345)
        assert mario is not None
        assert mario.nome == "Mario"
        assert mario.voti == [25]
        
        # Pulisci backup
        backup_path.unlink()
    
    @pytest.mark.integration
    def test_integrazione_ricerca_avanzata(self, temp_file):
        """Test integrazione ricerca avanzata"""
        file_manager = FileManager(temp_file)
        service = StudentService(file_manager)
        
        # Crea dataset per ricerca
        studenti_test = [
            ("Mario", "Rossi", 10001, [24, 26]),
            ("Maria", "Bianchi", 10002, [30, 29]),
            ("Marco", "Rossi", 10003, [22, 23]),
            ("Lucia", "Verdi", 10004, [28, 30]),
        ]
        
        for nome, cognome, matricola, voti in studenti_test:
            service.aggiungi_studente(str(matricola), nome, cognome)
            for voto in voti:
                service.aggiungi_voto_studente(str(matricola), str(voto))
        
        # Test ricerca per nome parziale
        risultati_mari = service.cerca_studenti("Mari")
        assert len(risultati_mari) == 2  # Mario e Maria
        
        risultati_marco = service.cerca_studenti("Marco")
        assert len(risultati_marco) == 1
        assert risultati_marco[0].nome == "Marco"
        
        # Test ricerca per cognome
        risultati_rossi = service.cerca_studenti("Rossi")
        assert len(risultati_rossi) == 2  # Mario e Marco Rossi
        
        # Salva e verifica persistenza ricerca
        service.salva_studenti()
        service.carica_studenti()
        
        risultati_dopo_reload = service.cerca_studenti("Mari")
        assert len(risultati_dopo_reload) == 2
    
    @pytest.mark.integration
    @pytest.mark.slow
    def test_integrazione_performance_grandi_dataset(self, temp_file):
        """Test integrazione con dataset più grandi"""
        file_manager = FileManager(temp_file)
        service = StudentService(file_manager)
        
        # Crea dataset grande (100 studenti)
        import random
        nomi = ["Mario", "Lucia", "Paolo", "Anna", "Marco", "Giulia", "Roberto", "Elena"]
        cognomi = ["Rossi", "Bianchi", "Verdi", "Neri", "Gialli", "Blu", "Rosa", "Viola"]
        
        for i in range(100):
            nome = random.choice(nomi)
            cognome = random.choice(cognomi)
            matricola = str(10000 + i)
            service.aggiungi_studente(matricola, nome, cognome)
            
            # Aggiungi voti casuali
            num_voti = random.randint(0, 5)
            for _ in range(num_voti):
                voto = random.randint(18, 30)
                service.aggiungi_voto(matricola, str(voto))
        
        # Test salvataggio grande dataset
        assert service.salva_studenti() is True
        
        # Test caricamento grande dataset
        service_test = StudentService(FileManager(temp_file))
        service_test.carica_studenti()
        assert len(service_test.ottieni_tutti_studenti()) == 100
        
        # Test statistiche su grande dataset
        stats = service_test.ottieni_statistiche()
        assert stats["totale_studenti"] == 100
        
        # Test ricerca su grande dataset
        risultati_mario = service_test.cerca_studenti("Mario")
        assert len(risultati_mario) > 0
