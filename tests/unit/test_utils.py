"""
Test unitari per il modulo utils
===============================
Testa le funzioni di utilità e validazione.
"""

import pytest
from src.utils import calcola_media, valida_voto, valida_matricola, valida_nome


class TestCalcolaMedia:
    """Test per la funzione calcola_media"""
    
    def test_calcola_media_voti_validi(self, voti_validi):
        """Test calcolo media con voti validi"""
        media = calcola_media(voti_validi)
        assert media == 24.75  # (18+24+27+30)/4
    
    def test_calcola_media_lista_vuota(self):
        """Test calcolo media con lista vuota"""
        assert calcola_media([]) == 0.0
    
    def test_calcola_media_con_float(self):
        """Test calcolo media con valori float"""
        voti = [18.5, 24.5, 27.0, 30.0]
        media = calcola_media(voti)
        assert media == 25.0
    
    def test_calcola_media_con_valori_misti(self):
        """Test calcolo media con valori misti"""
        voti = [18, 24.5, "invalid", 30, None]
        media = calcola_media(voti)
        # Deve considerare solo i valori numerici: (18+24.5+30)/3 = 24.17
        assert abs(media - 24.166666666666668) < 0.0001


class TestValidaVoto:
    """Test per la funzione valida_voto"""
    
    def test_valida_voto_valido_minimo(self):
        """Test validazione voto minimo valido"""
        assert valida_voto("18") == 18
    
    def test_valida_voto_valido_massimo(self):
        """Test validazione voto massimo valido"""
        assert valida_voto("30") == 30
    
    def test_valida_voto_valido_intermedio(self):
        """Test validazione voto intermedio valido"""
        assert valida_voto("25") == 25
    
    def test_valida_voto_troppo_basso(self):
        """Test validazione voto troppo basso"""
        with pytest.raises(ValueError, match="deve essere compreso tra 18 e 30"):
            valida_voto("17")
    
    def test_valida_voto_troppo_alto(self):
        """Test validazione voto troppo alto"""
        with pytest.raises(ValueError, match="deve essere compreso tra 18 e 30"):
            valida_voto("31")
    
    def test_valida_voto_non_numerico(self):
        """Test validazione voto non numerico"""
        with pytest.raises(ValueError, match="deve essere un numero"):
            valida_voto("abc")
    
    def test_valida_voto_stringa_vuota(self):
        """Test validazione stringa vuota"""
        with pytest.raises(ValueError, match="deve essere un numero"):
            valida_voto("")
    
    def test_valida_voto_con_spazi(self):
        """Test validazione voto con spazi"""
        assert valida_voto("  25  ") == 25


class TestValidaMatricola:
    """Test per la funzione valida_matricola"""
    
    def test_valida_matricola_valida(self):
        """Test validazione matricola valida"""
        assert valida_matricola("12345") == "12345"
    
    def test_valida_matricola_con_spazi(self):
        """Test validazione matricola con spazi"""
        assert valida_matricola("  12345  ") == "12345"
    
    def test_valida_matricola_troppo_corta(self):
        """Test validazione matricola troppo corta"""
        with pytest.raises(ValueError, match="deve essere di almeno 2 cifre"):
            valida_matricola("7")
    
    def test_valida_matricola_non_numerica(self):
        """Test validazione matricola non numerica"""
        with pytest.raises(ValueError, match="deve contenere solo numeri"):
            valida_matricola("abc123")
    
    def test_valida_matricola_vuota(self):
        """Test validazione matricola vuota"""
        with pytest.raises(ValueError, match="non può essere vuota"):
            valida_matricola("")
    
    def test_valida_matricola_negativa(self):
        """Test validazione matricola negativa"""
        with pytest.raises(ValueError, match="deve essere un numero positivo"):
            valida_matricola("-12345")


class TestValidaNome:
    """Test per la funzione valida_nome"""
    
    def test_valida_nome_valido(self):
        """Test validazione nome valido"""
        assert valida_nome("Mario") == "Mario"
    
    def test_valida_nome_con_spazi(self):
        """Test validazione nome con spazi"""
        assert valida_nome("  mario  ") == "Mario"
    
    def test_valida_nome_vuoto(self):
        """Test validazione nome vuoto"""
        with pytest.raises(ValueError, match="non può essere vuoto"):
            valida_nome("")
    
    def test_valida_nome_solo_spazi(self):
        """Test validazione nome solo spazi"""
        with pytest.raises(ValueError, match="non può essere vuoto"):
            valida_nome("   ")
    
    def test_valida_nome_troppo_corto(self):
        """Test validazione nome troppo corto"""
        with pytest.raises(ValueError, match="deve essere di almeno 2 caratteri"):
            valida_nome("A")
    
    def test_valida_nome_con_numeri(self):
        """Test validazione nome con numeri"""
        with pytest.raises(ValueError, match="deve contenere solo lettere"):
            valida_nome("Mario123")
    
    def test_valida_nome_con_caratteri_speciali(self):
        """Test validazione nome con caratteri speciali"""
        with pytest.raises(ValueError, match="deve contenere solo lettere"):
            valida_nome("Mario@")
    
    def test_valida_nome_con_apostrofo(self):
        """Test validazione nome con apostrofo (carattere valido)"""
        assert valida_nome("D'Angelo") == "D'Angelo"
    
    def test_valida_nome_troppo_lungo(self):
        """Test validazione nome troppo lungo"""
        nome_lungo = "A" * 51
        with pytest.raises(ValueError, match="non può superare i 50 caratteri"):
            valida_nome(nome_lungo)
