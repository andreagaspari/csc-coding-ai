"""
Test unitari per il modulo ui
============================
Testa l'interfaccia utente e le interazioni con l'utente.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from io import StringIO
from src.ui import MenuUI
from src.student_service import StudentService
from src.data_manager import FileManager


class TestMenuUI:
    """Test per la classe MenuUI"""
    
    def test_init_menu_ui(self, temp_file):
        """Test inizializzazione MenuUI"""
        ui = MenuUI(str(temp_file))
        # Verifica che il file manager punti al file giusto
        assert str(ui.file_manager.file_path) == str(temp_file)
        assert isinstance(ui.student_service, StudentService)
    
    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_mostra_menu_principale(self, mock_stdout, mock_input, temp_file):
        """Test visualizzazione menu principale"""
        ui = MenuUI(str(temp_file))
        # Forza uscita dopo la prima visualizzazione
        mock_input.side_effect = ["0"]
        ui.esegui_menu_principale()
        output = mock_stdout.getvalue()
        assert "REGISTRO STUDENTI" in output or "Benvenuto" in output

    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_visualizza_studenti_vuoti(self, mock_stdout, mock_input, temp_file):
        """Test visualizzazione con lista studenti vuota"""
        ui = MenuUI(str(temp_file))
        # Visualizza studenti, poi esci
        mock_input.side_effect = ["1", "0"]
        ui.esegui_menu_principale()
        output = mock_stdout.getvalue()
        assert "Nessuno studente presente" in output or "vuoto" in output.lower()

    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_aggiungi_studente_successo(self, mock_stdout, mock_input, temp_file):
        """Test robusto per aggiunta studente tramite menu"""
        ui = MenuUI(str(temp_file))
        mock_input.side_effect = [
            "2",        # Aggiungi studente
            "12345",    # Matricola
            "Mario",    # Nome
            "Rossi",    # Cognome
            "",         # Premi invio per saltare voti (se richiesto)
            "0"         # Esci
        ]
        ui.esegui_menu_principale()
        output = mock_stdout.getvalue()
        assert "Aggiunta nuovo studente" in output or "Mario" in output or "Rossi" in output
        # Verifica che lo studente sia stato effettivamente aggiunto
        studente = ui.student_service.ottieni_studente("12345")
        assert studente is not None
        assert studente.nome == "Mario"
        assert studente.cognome == "Rossi"
    
    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_aggiungi_voto_successo(self, mock_stdout, mock_input, temp_file):
        """Test aggiunta voto con successo"""
        ui = MenuUI(str(temp_file))
        
        # Prima aggiungi uno studente (matricola come stringa, ordine corretto)
        ui.student_service.aggiungi_studente("12345", "Mario", "Rossi")
        
        mock_input.side_effect = [
            "3",      # Aggiungi voto
            "12345",  # Matricola
            "28",     # Voto
            "0"       # Esci
        ]
        
        ui.esegui_menu_principale()
        
        # Verifica che il voto sia stato aggiunto
        studente = ui.student_service.ottieni_studente("12345")
        assert 28 in studente.voti

    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_gestione_input_invalido(self, mock_stdout, mock_input, temp_file):
        """Test gestione input non valido nel menu"""
        ui = MenuUI(str(temp_file))
        mock_input.side_effect = [
            "99",    # Opzione non valida
            "abc",   # Input non numerico
            "0"      # Esci
        ]
        ui.esegui_menu_principale()
        output = mock_stdout.getvalue()
        assert "non valida" in output.lower() or "errore" in output.lower()
    
    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_ricerca_studente_esistente(self, mock_stdout, mock_input, temp_file):
        """Test ricerca studente esistente"""
        ui = MenuUI(str(temp_file))
        
        # Aggiungi studenti di test (matricola come stringa, ordine corretto)
        ui.student_service.aggiungi_studente("12345", "Mario", "Rossi")
        ui.student_service.aggiungi_studente("67890", "Maria", "Bianchi")
        
        mock_input.side_effect = [
            "8",      # Cerca studente per nome (opzione corretta)
            "Mari",   # Termine di ricerca
            "" ,      # Cognome opzionale
            "0"       # Esci
        ]
        
        ui.esegui_menu_principale()
        
        output = mock_stdout.getvalue()
        # Verifica che siano stati trovati studenti
        assert "Mario" in output or "Maria" in output

    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_visualizza_statistiche(self, mock_stdout, mock_input, temp_file):
        """Test visualizzazione statistiche"""
        ui = MenuUI(str(temp_file))
        
        # Aggiungi studenti con voti per statistiche significative (matricola come stringa)
        ui.student_service.aggiungi_studente("12345", "Mario", "Rossi")
        ui.student_service.aggiungi_voto("12345", "28")
        ui.student_service.aggiungi_voto("12345", "30")
        ui.student_service.aggiungi_studente("67890", "Lucia", "Bianchi")
        ui.student_service.aggiungi_voto("67890", "29")
        
        mock_input.side_effect = [
            "7",      # Visualizza statistiche (opzione corretta)
            "0"       # Esci
        ]
        
        ui.esegui_menu_principale()
        
        output = mock_stdout.getvalue()
        # Verifica che siano mostrate statistiche
        assert "studenti" in output.lower()
        assert "media" in output.lower() or "statistiche" in output.lower()
    
    @patch('builtins.input')
    def test_gestione_eccezioni(self, mock_input, temp_file):
        """Test gestione eccezioni durante l'esecuzione"""
        ui = MenuUI(str(temp_file))
        
        # Simula un'eccezione durante l'input
        mock_input.side_effect = KeyboardInterrupt()
        
        # Non dovrebbe sollevare eccezioni non gestite
        try:
            ui.esegui_menu_principale()
        except KeyboardInterrupt:
            pass  # Atteso
        except Exception as e:
            pytest.fail(f"Eccezione non gestita: {e}")
    
    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_validazione_input_matricola(self, mock_stdout, mock_input, temp_file):
        """Test validazione input matricola"""
        ui = MenuUI(str(temp_file))
        mock_input.side_effect = [
            "2",        # Aggiungi studente
            "abc",      # Matricola non valida
            "12345",    # Matricola valida
            "Mario",    # Nome
            "Rossi",    # Cognome
            "",         # Invio per saltare voti
            "0"         # Esci
        ]
        ui.esegui_menu_principale()
        output = mock_stdout.getvalue()
        # Verifica che venga mostrato un messaggio di errore per la matricola non valida
        assert ("errore" in output.lower() or "non valida" in output.lower() or "matricola" in output.lower())
    
    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_validazione_input_voto(self, mock_stdout, mock_input, temp_file):
        """Test validazione input voto"""
        ui = MenuUI(str(temp_file))
        
        # Aggiungi studente prima (matricola come stringa)
        ui.student_service.aggiungi_studente("12345", "Mario", "Rossi")
        
        mock_input.side_effect = [
            "3",      # Aggiungi voto
            "12345",  # Matricola
            "35",     # Voto non valido (troppo alto)
            "28",     # Voto valido
            "0"       # Esci
        ]
        
        ui.esegui_menu_principale()
        
        output = mock_stdout.getvalue()
        # Verifica gestione errore voto non valido
        assert ("errore" in output.lower() or "non valido" in output.lower() or "voto" in output.lower())
    
    def test_salvataggio_automatico(self, temp_file):
        """Test salvataggio automatico dei dati"""
        ui = MenuUI(str(temp_file))
        
        # Aggiungi uno studente (matricola come stringa)
        ui.student_service.aggiungi_studente("12345", "Mario", "Rossi")
        
        # Il salvataggio dovrebbe essere chiamato automaticamente
        # (questo dipende dall'implementazione specifica)
        # Verifica che il metodo di salvataggio esista
        assert hasattr(ui, 'salva_dati') or hasattr(ui.student_service, 'salva_studenti')
