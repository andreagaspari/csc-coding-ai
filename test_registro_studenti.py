"""
Test suite per il sistema di gestione registro studenti
=======================================================

Questo modulo contiene i test unitari per tutte le funzioni principali
dell'applicazione registro_studenti_ai.py.

Struttura dei test:
- Test per le funzioni di utilità (calcola_media, valida_voto, etc.)
- Test per le funzioni di I/O file (leggi_studenti_da_file, salva_studenti_su_file)
- Test per le funzioni di ricerca e validazione
- Test di integrazione per i flussi principali

Per eseguire i test:
    python -m pytest test_registro_studenti.py -v

Per eseguire i test con coverage:
    python -m pytest test_registro_studenti.py --cov=registro_studenti_ai -v
"""

import pytest
import json
import os
import tempfile
from unittest.mock import patch, mock_open, MagicMock
from registro_studenti_ai import (
    calcola_media,
    valida_voto,
    leggi_studenti_da_file,
    salva_studenti_su_file,
    trova_studente_per_matricola,
    matricola_esiste,
    stampa_studenti,
    stampa_voti_studente,
    aggiungi_studente,
    aggiungi_voto,
    cancella_studente
)


class TestCalcolaMedia:
    """Test per la funzione calcola_media"""
    
    def test_media_con_voti_validi(self):
        """Test calcolo media con voti numerici validi"""
        voti = [18, 24, 30]
        assert calcola_media(voti) == 24.0
        
    def test_media_con_voti_decimali(self):
        """Test calcolo media con voti decimali"""
        voti = [18.5, 24.5, 30.0]
        assert calcola_media(voti) == 24.333333333333332
        
    def test_media_lista_vuota(self):
        """Test calcolo media con lista vuota"""
        assert calcola_media([]) == 0.0
        
    def test_media_con_voti_misti(self):
        """Test calcolo media con voti misti (int e float)"""
        voti = [18, 24.5, 30]
        expected = (18 + 24.5 + 30) / 3
        assert calcola_media(voti) == expected
        
    def test_media_con_valori_non_numerici(self):
        """Test calcolo media ignorando valori non numerici"""
        voti = [18, "invalid", 24, None, 30]
        assert calcola_media(voti) == 24.0
        
    def test_media_solo_valori_non_numerici(self):
        """Test calcolo media con solo valori non numerici"""
        voti = ["invalid", None, "test"]
        assert calcola_media(voti) == 0.0


class TestValidaVoto:
    """Test per la funzione valida_voto"""
    
    def test_voto_valido_minimo(self):
        """Test validazione voto minimo (18)"""
        assert valida_voto("18") == 18
        
    def test_voto_valido_massimo(self):
        """Test validazione voto massimo (30)"""
        assert valida_voto("30") == 30
        
    def test_voto_valido_intermedio(self):
        """Test validazione voto intermedio"""
        assert valida_voto("25") == 25
        
    def test_voto_con_spazi(self):
        """Test validazione voto con spazi all'inizio e alla fine"""
        assert valida_voto("  24  ") == 24
        
    def test_voto_troppo_basso(self):
        """Test validazione voto troppo basso (< 18)"""
        with pytest.raises(ValueError, match="Il voto deve essere un numero intero tra 18 e 30"):
            valida_voto("17")
            
    def test_voto_troppo_alto(self):
        """Test validazione voto troppo alto (> 30)"""
        with pytest.raises(ValueError, match="Il voto deve essere un numero intero tra 18 e 30"):
            valida_voto("31")
            
    def test_voto_non_numerico(self):
        """Test validazione voto non numerico"""
        with pytest.raises(ValueError, match="Il voto deve essere un numero intero tra 18 e 30"):
            valida_voto("abc")
            
    def test_voto_decimale(self):
        """Test validazione voto decimale (non supportato)"""
        with pytest.raises(ValueError, match="Il voto deve essere un numero intero tra 18 e 30"):
            valida_voto("24.5")
            
    def test_voto_vuoto(self):
        """Test validazione voto stringa vuota"""
        with pytest.raises(ValueError, match="Il voto deve essere un numero intero tra 18 e 30"):
            valida_voto("")


class TestLeggiStudentiDaFile:
    """Test per la funzione leggi_studenti_da_file"""
    
    def test_lettura_file_valido(self):
        """Test lettura file JSON valido"""
        studenti_test = [
            {"matricola": "123", "nome": "Mario", "cognome": "Rossi", "voti": [24, 26]},
            {"matricola": "456", "nome": "Lucia", "cognome": "Bianchi", "voti": [28, 30]}
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump(studenti_test, f, ensure_ascii=False, indent=2)
            temp_path = f.name
            
        try:
            risultato = leggi_studenti_da_file(temp_path)
            assert risultato == studenti_test
        finally:
            os.unlink(temp_path)
            
    def test_file_non_esistente(self):
        """Test lettura file non esistente"""
        with patch('builtins.print') as mock_print:
            risultato = leggi_studenti_da_file("/path/che/non/esiste.json")
            assert risultato == []
            mock_print.assert_called_with("ℹ️ File not found. Starting with empty registry.")
            
    def test_file_json_invalido(self):
        """Test lettura file con JSON non valido"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            f.write("{ invalid json content")
            temp_path = f.name
            
        try:
            with patch('builtins.print') as mock_print:
                risultato = leggi_studenti_da_file(temp_path)
                assert risultato == []
                mock_print.assert_called_with("❌ Error: Invalid JSON format in file.")
        finally:
            os.unlink(temp_path)


class TestSalvaStudentiSuFile:
    """Test per la funzione salva_studenti_su_file"""
    
    def test_salvataggio_corretto(self):
        """Test salvataggio corretto di studenti"""
        studenti_test = [
            {"matricola": "123", "nome": "Mario", "cognome": "Rossi", "voti": [24, 26]}
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name
            
        try:
            risultato = salva_studenti_su_file(temp_path, studenti_test)
            assert risultato == True
            
            # Verifica che il file sia stato salvato correttamente
            with open(temp_path, 'r', encoding='utf-8') as f:
                dati_salvati = json.load(f)
            assert dati_salvati == studenti_test
        finally:
            os.unlink(temp_path)
            
    def test_salvataggio_errore_permessi(self):
        """Test salvataggio con errore di permessi"""
        studenti_test = [{"matricola": "123", "nome": "Mario", "cognome": "Rossi"}]
        
        with patch('builtins.print') as mock_print:
            risultato = salva_studenti_su_file("/root/file_non_scrivibile.json", studenti_test)
            assert risultato == False
            # Verifica che sia stato stampato un messaggio di errore
            mock_print.assert_called()
            assert "❌ Errore nel salvataggio del file:" in str(mock_print.call_args)


class TestTrovaStudentePerMatricola:
    """Test per la funzione trova_studente_per_matricola"""
    
    @pytest.fixture(autouse=True)
    def setup_method(self):
        """Setup dati di test"""
        self.studenti_test = [
            {"matricola": "123", "nome": "Mario", "cognome": "Rossi", "voti": [24, 26]},
            {"matricola": "456", "nome": "Lucia", "cognome": "Bianchi", "voti": [28, 30]},
            {"matricola": "789", "nome": "Giuseppe", "cognome": "Verdi", "voti": []}
        ]
    
    def test_trova_studente_esistente(self):
        """Test ricerca studente esistente"""
        studente = trova_studente_per_matricola(self.studenti_test, "456")
        assert studente is not None
        assert studente["nome"] == "Lucia"
        assert studente["cognome"] == "Bianchi"
        
    def test_trova_studente_non_esistente(self):
        """Test ricerca studente non esistente"""
        studente = trova_studente_per_matricola(self.studenti_test, "999")
        assert studente is None
        
    def test_trova_studente_lista_vuota(self):
        """Test ricerca in lista vuota"""
        studente = trova_studente_per_matricola([], "123")
        assert studente is None


class TestMatricolaEsiste:
    """Test per la funzione matricola_esiste"""
    
    @pytest.fixture(autouse=True)
    def setup_method(self):
        """Setup dati di test"""
        self.studenti_test = [
            {"matricola": "123", "nome": "Mario", "cognome": "Rossi"},
            {"matricola": "456", "nome": "Lucia", "cognome": "Bianchi"}
        ]
    
    def test_matricola_esistente(self):
        """Test verifica matricola esistente"""
        assert matricola_esiste(self.studenti_test, "123") == True
        
    def test_matricola_non_esistente(self):
        """Test verifica matricola non esistente"""
        assert matricola_esiste(self.studenti_test, "999") == False
        
    def test_matricola_lista_vuota(self):
        """Test verifica matricola in lista vuota"""
        assert matricola_esiste([], "123") == False


class TestStampaStudenti:
    """Test per la funzione stampa_studenti"""
    
    def test_stampa_lista_vuota(self):
        """Test stampa lista studenti vuota"""
        with patch('builtins.print') as mock_print:
            stampa_studenti([])
            mock_print.assert_called_with("\n📋 Nessuno studente presente nel registro.")
            
    def test_stampa_studenti_con_voti(self):
        """Test stampa studenti con voti"""
        studenti_test = [
            {"matricola": "123", "nome": "Mario", "cognome": "Rossi", "voti": [24, 26, 28]},
            {"matricola": "456", "nome": "Lucia", "cognome": "Bianchi", "voti": [30]}
        ]
        
        with patch('builtins.print') as mock_print:
            stampa_studenti(studenti_test)
            
            # Verifica che siano state fatte le chiamate di print corrette
            calls = mock_print.call_args_list
            assert len(calls) >= 4  # Header + separator + 2 studenti
            
            # Verifica il contenuto di alcune chiamate
            assert "Lista studenti (2 studenti):" in str(calls[0])
            assert "[123] Mario Rossi - Media: 26.00 (3 voti)" in str(calls[2])
            assert "[456] Lucia Bianchi - Media: 30.00 (1 voti)" in str(calls[3])
            
    def test_stampa_studenti_senza_voti(self):
        """Test stampa studenti senza voti"""
        studenti_test = [
            {"matricola": "123", "nome": "Mario", "cognome": "Rossi", "voti": []}
        ]
        
        with patch('builtins.print') as mock_print:
            stampa_studenti(studenti_test)
            
            calls = mock_print.call_args_list
            assert "[123] Mario Rossi - Media: 0.00 (0 voti)" in str(calls[2])
            
    def test_stampa_studenti_dati_mancanti(self):
        """Test stampa studenti con dati mancanti"""
        studenti_test = [
            {"matricola": "123"},  # Nome e cognome mancanti
            {"nome": "Lucia", "cognome": "Bianchi"}  # Matricola mancante
        ]
        
        with patch('builtins.print') as mock_print:
            stampa_studenti(studenti_test)
            
            calls = mock_print.call_args_list
            assert "[123] N/D N/D - Media: 0.00 (0 voti)" in str(calls[2])
            assert "[N/D] Lucia Bianchi - Media: 0.00 (0 voti)" in str(calls[3])


class TestStampaVotiStudente:
    """Test per la funzione stampa_voti_studente"""
    
    def test_stampa_voti_studente_esistente(self):
        """Test stampa voti per studente esistente"""
        studenti_test = [
            {"matricola": "123", "nome": "Mario", "cognome": "Rossi", "voti": [24, 26, 28, 30]}
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump(studenti_test, f, ensure_ascii=False, indent=2)
            temp_path = f.name
            
        try:
            with patch('builtins.print') as mock_print:
                stampa_voti_studente(temp_path, "123")
                
                calls = mock_print.call_args_list
                # Verifica alcune delle informazioni stampate
                output_text = ' '.join([str(call) for call in calls])
                assert "Mario Rossi" in output_text
                assert "24, 26, 28, 30" in output_text
                assert "Numero totale voti: 4" in output_text
                assert "Media: 27.00" in output_text
                assert "Voto minimo: 24" in output_text
                assert "Voto massimo: 30" in output_text
        finally:
            os.unlink(temp_path)
            
    def test_stampa_voti_studente_non_esistente(self):
        """Test stampa voti per studente non esistente"""
        studenti_test = [
            {"matricola": "123", "nome": "Mario", "cognome": "Rossi", "voti": [24]}
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump(studenti_test, f, ensure_ascii=False, indent=2)
            temp_path = f.name
            
        try:
            with patch('builtins.print') as mock_print:
                stampa_voti_studente(temp_path, "999")
                
                mock_print.assert_called_with("❌ Errore: Nessuno studente trovato con matricola 999")
        finally:
            os.unlink(temp_path)
            
    def test_stampa_voti_studente_senza_voti(self):
        """Test stampa voti per studente senza voti"""
        studenti_test = [
            {"matricola": "123", "nome": "Mario", "cognome": "Rossi", "voti": []}
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump(studenti_test, f, ensure_ascii=False, indent=2)
            temp_path = f.name
            
        try:
            with patch('builtins.print') as mock_print:
                stampa_voti_studente(temp_path, "123")
                
                calls = mock_print.call_args_list
                output_text = ' '.join([str(call) for call in calls])
                assert "Mario Rossi" in output_text
                assert "⚠️ Nessun voto registrato." in output_text
        finally:
            os.unlink(temp_path)
            
    def test_stampa_voti_file_vuoto(self):
        """Test stampa voti con file di registro vuoto"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump([], f)
            temp_path = f.name
            
        try:
            with patch('builtins.print') as mock_print:
                stampa_voti_studente(temp_path, "123")
                
                mock_print.assert_called_with("❌ Nessuno studente presente nel registro.")
        finally:
            os.unlink(temp_path)


class TestIntegrazione:
    """Test di integrazione per flussi completi"""
    
    def test_ciclo_completo_studente(self):
        """Test ciclo completo: salva -> leggi -> trova -> modifica -> salva"""
        studenti_iniziali = [
            {"matricola": "123", "nome": "Mario", "cognome": "Rossi", "voti": [24]}
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name
            
        try:
            # 1. Salva studenti iniziali
            assert salva_studenti_su_file(temp_path, studenti_iniziali) == True
            
            # 2. Leggi studenti dal file
            studenti_letti = leggi_studenti_da_file(temp_path)
            assert len(studenti_letti) == 1
            assert studenti_letti[0]["nome"] == "Mario"
            
            # 3. Trova studente
            studente_trovato = trova_studente_per_matricola(studenti_letti, "123")
            assert studente_trovato is not None
            
            # 4. Aggiungi voto
            studente_trovato["voti"].append(28)
            
            # 5. Salva modifiche
            assert salva_studenti_su_file(temp_path, studenti_letti) == True
            
            # 6. Verifica modifiche
            studenti_aggiornati = leggi_studenti_da_file(temp_path)
            assert len(studenti_aggiornati[0]["voti"]) == 2
            assert 28 in studenti_aggiornati[0]["voti"]
            
        finally:
            os.unlink(temp_path)
            
    def test_gestione_matricole_duplicate(self):
        """Test gestione matricole duplicate"""
        studenti = [
            {"matricola": "123", "nome": "Mario", "cognome": "Rossi", "voti": []},
            {"matricola": "456", "nome": "Lucia", "cognome": "Bianchi", "voti": []}
        ]
        
        # Test matricola esistente
        assert matricola_esiste(studenti, "123") == True
        assert matricola_esiste(studenti, "456") == True
        
        # Test matricola non esistente
        assert matricola_esiste(studenti, "789") == False
        
        # Test aggiunta matricola nuova
        nuovo_studente = {"matricola": "789", "nome": "Giuseppe", "cognome": "Verdi", "voti": []}
        studenti.append(nuovo_studente)
        assert matricola_esiste(studenti, "789") == True


class TestValidazioneInput:
    """Test per la validazione degli input dell'utente"""
    
    def test_validazione_matricola_vuota(self):
        """Test validazione matricola vuota durante aggiunta studente"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump([], f)  # File vuoto
            temp_path = f.name
            
        try:
            # Simula input: matricola vuota -> matricola valida -> nome -> cognome -> nessun voto
            with patch('builtins.input', side_effect=['', '123', 'Mario', 'Rossi', '']):
                with patch('builtins.print') as mock_print:
                    aggiungi_studente(temp_path)
                    
                    # Verifica che sia stato mostrato l'errore per matricola vuota
                    calls = [str(call) for call in mock_print.call_args_list]
                    assert any("⚠️ La matricola è vuota. Riprova." in call for call in calls)
                    
                    # Verifica che alla fine lo studente sia stato aggiunto
                    assert any("✅ Studente Mario Rossi aggiunto con successo" in call for call in calls)
        finally:
            os.unlink(temp_path)
            
    def test_validazione_matricola_duplicata(self):
        """Test validazione matricola duplicata"""
        studenti_esistenti = [
            {"matricola": "123", "nome": "Existing", "cognome": "Student", "voti": []}
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump(studenti_esistenti, f, ensure_ascii=False, indent=2)
            temp_path = f.name
            
        try:
            # Simula input: matricola esistente -> matricola nuova -> nome -> cognome -> nessun voto
            with patch('builtins.input', side_effect=['123', '456', 'Mario', 'Rossi', '']):
                with patch('builtins.print') as mock_print:
                    aggiungi_studente(temp_path)
                    
                    # Verifica che sia stato mostrato l'errore per matricola duplicata
                    calls = [str(call) for call in mock_print.call_args_list]
                    assert any("⚠️ La matricola  esiste già" in call for call in calls)
        finally:
            os.unlink(temp_path)
            
    def test_validazione_nome_vuoto(self):
        """Test validazione nome vuoto"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump([], f)
            temp_path = f.name
            
        try:
            # Simula input: matricola -> nome vuoto -> nome valido -> cognome -> nessun voto
            with patch('builtins.input', side_effect=['123', '', 'Mario', 'Rossi', '']):
                with patch('builtins.print') as mock_print:
                    aggiungi_studente(temp_path)
                    
                    # Verifica che sia stato mostrato l'errore per nome vuoto
                    calls = [str(call) for call in mock_print.call_args_list]
                    assert any("⚠️ Il nome non può essere vuoto. Riprova." in call for call in calls)
        finally:
            os.unlink(temp_path)
            
    def test_validazione_cognome_vuoto(self):
        """Test validazione cognome vuoto"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump([], f)
            temp_path = f.name
            
        try:
            # Simula input: matricola -> nome -> cognome vuoto -> cognome valido -> nessun voto
            with patch('builtins.input', side_effect=['123', 'Mario', '', 'Rossi', '']):
                with patch('builtins.print') as mock_print:
                    aggiungi_studente(temp_path)
                    
                    # Verifica che sia stato mostrato l'errore per cognome vuoto
                    calls = [str(call) for call in mock_print.call_args_list]
                    assert any("⚠️ Il cognome non può essere vuoto. Riprova." in call for call in calls)
        finally:
            os.unlink(temp_path)
            
    def test_validazione_voti_con_errori(self):
        """Test validazione voti con alcuni errori"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump([], f)
            temp_path = f.name
            
        try:
            # Simula input: matricola -> nome -> cognome -> voti misti (validi e non)
            with patch('builtins.input', side_effect=['123', 'Mario', 'Rossi', '24,invalid,30,17,25']):
                with patch('builtins.print') as mock_print:
                    aggiungi_studente(temp_path)
                    
                    calls = [str(call) for call in mock_print.call_args_list]
                    # Verifica che siano stati ignorati i voti non validi
                    assert any("Voto 'invalid' ignorato" in call for call in calls)
                    assert any("Voto '17' ignorato" in call for call in calls)
                    
                    # Verifica che lo studente sia stato aggiunto con i voti validi
                    studenti = leggi_studenti_da_file(temp_path)
                    assert len(studenti) == 1
                    assert studenti[0]["voti"] == [24, 30, 25]  # Solo i voti validi
        finally:
            os.unlink(temp_path)
            
    def test_validazione_spazi_in_input(self):
        """Test che gli spazi vengano rimossi correttamente dall'input"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump([], f)
            temp_path = f.name
            
        try:
            # Simula input con spazi extra
            with patch('builtins.input', side_effect=['  123  ', '  Mario  ', '  Rossi  ', '  24, 26 , 30  ']):
                aggiungi_studente(temp_path)
                    
                # Verifica che i dati siano stati salvati senza spazi extra
                studenti = leggi_studenti_da_file(temp_path)
                assert len(studenti) == 1
                assert studenti[0]["matricola"] == "123"
                assert studenti[0]["nome"] == "Mario"
                assert studenti[0]["cognome"] == "Rossi"
                assert studenti[0]["voti"] == [24, 26, 30]
        finally:
            os.unlink(temp_path)


class TestValidazioneInputAggiungiVoto:
    """Test per la validazione degli input nella funzione aggiungi_voto"""
    
    def test_aggiungi_voto_studente_non_esistente(self):
        """Test aggiunta voto a studente non esistente"""
        studenti_test = [
            {"matricola": "123", "nome": "Mario", "cognome": "Rossi", "voti": [24]}
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump(studenti_test, f, ensure_ascii=False, indent=2)
            temp_path = f.name
            
        try:
            # Simula input: matricola non esistente
            with patch('builtins.input', side_effect=['999']):
                with patch('builtins.print') as mock_print:
                    aggiungi_voto(temp_path)
                    
                    mock_print.assert_called_with("❌ Errore: Nessuno studente trovato con matricola 999")
        finally:
            os.unlink(temp_path)
            
    def test_aggiungi_voto_invalido(self):
        """Test aggiunta voto non valido"""
        studenti_test = [
            {"matricola": "123", "nome": "Mario", "cognome": "Rossi", "voti": [24]}
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump(studenti_test, f, ensure_ascii=False, indent=2)
            temp_path = f.name
            
        try:
            # Simula input: matricola valida -> voto non valido
            with patch('builtins.input', side_effect=['123', '17']):
                with patch('builtins.print') as mock_print:
                    aggiungi_voto(temp_path)
                    
                    calls = [str(call) for call in mock_print.call_args_list]
                    assert any("❌ Errore:" in call for call in calls)
        finally:
            os.unlink(temp_path)
            
    def test_aggiungi_voto_successo(self):
        """Test aggiunta voto con successo"""
        studenti_test = [
            {"matricola": "123", "nome": "Mario", "cognome": "Rossi", "voti": [24]}
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump(studenti_test, f, ensure_ascii=False, indent=2)
            temp_path = f.name
            
        try:
            # Simula input: matricola valida -> voto valido
            with patch('builtins.input', side_effect=['123', '28']):
                with patch('builtins.print') as mock_print:
                    aggiungi_voto(temp_path)
                    
                    calls = [str(call) for call in mock_print.call_args_list]
                    assert any("✅ Voto 28 aggiunto con successo a Mario Rossi" in call for call in calls)
                    
                    # Verifica che il voto sia stato effettivamente aggiunto
                    studenti = leggi_studenti_da_file(temp_path)
                    assert len(studenti[0]["voti"]) == 2
                    assert 28 in studenti[0]["voti"]
        finally:
            os.unlink(temp_path)
            
    def test_aggiungi_voto_file_vuoto(self):
        """Test aggiunta voto con file registro vuoto"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump([], f)
            temp_path = f.name
            
        try:
            with patch('builtins.print') as mock_print:
                aggiungi_voto(temp_path)
                
                mock_print.assert_called_with("❌ Nessuno studente presente nel registro.")
        finally:
            os.unlink(temp_path)


class TestValidazioneInputCancellaStudente:
    """Test per la validazione degli input nella funzione cancella_studente"""
    
    def test_cancella_studente_non_esistente(self):
        """Test cancellazione studente non esistente"""
        studenti_test = [
            {"matricola": "123", "nome": "Mario", "cognome": "Rossi", "voti": [24]}
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump(studenti_test, f, ensure_ascii=False, indent=2)
            temp_path = f.name
            
        try:
            # Simula input: matricola non esistente
            with patch('builtins.input', side_effect=['999']):
                with patch('builtins.print') as mock_print:
                    cancella_studente(temp_path)
                    
                    mock_print.assert_called_with("❌ Errore: Nessuno studente trovato con matricola 999")
        finally:
            os.unlink(temp_path)
            
    def test_cancella_studente_conferma_no(self):
        """Test cancellazione studente con conferma negativa"""
        studenti_test = [
            {"matricola": "123", "nome": "Mario", "cognome": "Rossi", "voti": [24]}
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump(studenti_test, f, ensure_ascii=False, indent=2)
            temp_path = f.name
            
        try:
            # Simula input: matricola valida -> conferma negativa
            with patch('builtins.input', side_effect=['123', 'n']):
                with patch('builtins.print') as mock_print:
                    cancella_studente(temp_path)
                    
                    mock_print.assert_called_with("Operazione annullata.")
                    
                    # Verifica che lo studente non sia stato cancellato
                    studenti = leggi_studenti_da_file(temp_path)
                    assert len(studenti) == 1
        finally:
            os.unlink(temp_path)
            
    def test_cancella_studente_conferma_si(self):
        """Test cancellazione studente con conferma positiva"""
        studenti_test = [
            {"matricola": "123", "nome": "Mario", "cognome": "Rossi", "voti": [24]}
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump(studenti_test, f, ensure_ascii=False, indent=2)
            temp_path = f.name
            
        try:
            # Simula input: matricola valida -> conferma positiva
            with patch('builtins.input', side_effect=['123', 's']):
                with patch('builtins.print') as mock_print:
                    cancella_studente(temp_path)
                    
                    calls = [str(call) for call in mock_print.call_args_list]
                    assert any("✅ Studente Mario Rossi rimosso con successo" in call for call in calls)
                    
                    # Verifica che lo studente sia stato cancellato
                    studenti = leggi_studenti_da_file(temp_path)
                    assert len(studenti) == 0
        finally:
            os.unlink(temp_path)
            
    def test_cancella_studente_file_vuoto(self):
        """Test cancellazione studente con file registro vuoto"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump([], f)
            temp_path = f.name
            
        try:
            with patch('builtins.print') as mock_print:
                cancella_studente(temp_path)
                
                mock_print.assert_called_with("❌ Nessuno studente presente nel registro.")
        finally:
            os.unlink(temp_path)
            
    def test_cancella_studente_conferma_varianti(self):
        """Test cancellazione studente con diverse varianti di conferma"""
        studenti_test = [
            {"matricola": "123", "nome": "Mario", "cognome": "Rossi", "voti": [24]}
        ]
        
        # Test con conferma 'S' maiuscola
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump(studenti_test, f, ensure_ascii=False, indent=2)
            temp_path = f.name
            
        try:
            with patch('builtins.input', side_effect=['123', 'S']):
                with patch('builtins.print') as mock_print:
                    cancella_studente(temp_path)
                    
                    calls = [str(call) for call in mock_print.call_args_list]
                    assert any("✅ Studente Mario Rossi rimosso con successo" in call for call in calls)
        finally:
            os.unlink(temp_path)


class TestValidazioneInputStampaVoti:
    """Test per la validazione degli input nella funzione stampa_voti_studente senza matricola"""
    
    def test_stampa_voti_input_matricola(self):
        """Test richiesta input matricola per stampa voti"""
        studenti_test = [
            {"matricola": "123", "nome": "Mario", "cognome": "Rossi", "voti": [24, 26, 28]}
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump(studenti_test, f, ensure_ascii=False, indent=2)
            temp_path = f.name
            
        try:
            # Simula input: matricola valida
            with patch('builtins.input', side_effect=['123']):
                with patch('builtins.print') as mock_print:
                    stampa_voti_studente(temp_path)  # Senza parametro matricola
                    
                    calls = [str(call) for call in mock_print.call_args_list]
                    output_text = ' '.join(calls)
                    assert "Mario Rossi" in output_text
                    assert "Media: 26.00" in output_text
        finally:
            os.unlink(temp_path)


class TestValidazioneInputEdgeCases:
    """Test per casi limite nella validazione degli input"""
    
    def test_input_con_caratteri_speciali(self):
        """Test input con caratteri speciali"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump([], f)
            temp_path = f.name
            
        try:
            # Test con caratteri speciali nel nome
            with patch('builtins.input', side_effect=['123', 'José María', 'García-López', '']):
                aggiungi_studente(temp_path)
                    
                studenti = leggi_studenti_da_file(temp_path)
                assert len(studenti) == 1
                assert studenti[0]["nome"] == "José María"
                assert studenti[0]["cognome"] == "García-López"
        finally:
            os.unlink(temp_path)
            
    def test_input_voti_con_spazi_e_virgole_extra(self):
        """Test input voti con formattazione irregolare"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump([], f)
            temp_path = f.name
            
        try:
            # Test con spazi e virgole extra nei voti
            with patch('builtins.input', side_effect=['123', 'Mario', 'Rossi', ' 24 , , 26 ,, 30 , ']):
                aggiungi_studente(temp_path)
                    
                studenti = leggi_studenti_da_file(temp_path)
                assert len(studenti) == 1
                assert studenti[0]["voti"] == [24, 26, 30]  # Virgole vuote ignorate
        finally:
            os.unlink(temp_path)
            
    def test_matricola_numerica_vs_stringa(self):
        """Test che la matricola sia gestita come stringa"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump([], f)
            temp_path = f.name
            
        try:
            # Test con matricola che inizia con zero
            with patch('builtins.input', side_effect=['0123', 'Mario', 'Rossi', '']):
                aggiungi_studente(temp_path)
                    
                studenti = leggi_studenti_da_file(temp_path)
                assert len(studenti) == 1
                assert studenti[0]["matricola"] == "0123"  # Mantiene lo zero iniziale
        finally:
            os.unlink(temp_path)

if __name__ == "__main__":
    """
    Esecuzione diretta dei test
    
    Per eseguire tutti i test:
        python test_registro_studenti.py
        
    Per eseguire test specifici:
        python -m pytest test_registro_studenti.py::TestCalcolaMedia -v
    """
    pytest.main([__file__, "-v"])
