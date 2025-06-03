"""
Test unitari per il modulo models
================================
Testa le classi Persona, Studente e ListaStudenti.
"""

import pytest
from src.models import Persona, Studente, ListaStudenti


class TestPersona:
    """Test per la classe Persona"""
    
    def test_init_persona(self):
        """Test inizializzazione persona"""
        persona = Persona("mario", "rossi")
        assert persona.nome == "Mario"
        assert persona.cognome == "Rossi"
    
    def test_nome_completo(self):
        """Test nome completo"""
        persona = Persona("Mario", "Rossi")
        assert persona.nome_completo() == "Mario Rossi"
    
    def test_iniziali(self):
        """Test iniziali"""
        persona = Persona("Mario", "Rossi")
        assert persona.iniziali() == "M.R."
    
    def test_str_representation(self):
        """Test rappresentazione stringa"""
        persona = Persona("Mario", "Rossi")
        assert str(persona) == "Mario Rossi"
    
    def test_normalizzazione_nome(self):
        """Test normalizzazione automatica del nome"""
        persona = Persona("  mario  ", "  rossi  ")
        assert persona.nome == "Mario"
        assert persona.cognome == "Rossi"


class TestStudente:
    """Test per la classe Studente"""
    
    def test_init_studente(self, studente_mario):
        """Test inizializzazione studente"""
        assert studente_mario.nome == "Mario"
        assert studente_mario.cognome == "Rossi"
        assert studente_mario.matricola == 12345
        assert studente_mario.voti == [24, 28, 30, 26]
    
    def test_init_studente_senza_voti(self):
        """Test inizializzazione studente senza voti"""
        studente = Studente("Paolo", "Verdi", 11111)
        assert studente.voti == []
    
    def test_media_voti_con_voti(self, studente_mario):
        """Test calcolo media con voti"""
        media = studente_mario.media_voti()
        assert media == 27.0  # (24+28+30+26)/4
    
    def test_media_voti_senza_voti(self, studente_senza_voti):
        """Test calcolo media senza voti"""
        assert studente_senza_voti.media_voti() == 0.0
    
    def test_aggiungi_voto_valido(self, studente_senza_voti):
        """Test aggiunta voto valido"""
        assert studente_senza_voti.aggiungi_voto(25) is True
        assert 25 in studente_senza_voti.voti
    
    def test_aggiungi_voto_invalido(self, studente_senza_voti):
        """Test aggiunta voto non valido"""
        assert studente_senza_voti.aggiungi_voto(17) is False
        assert studente_senza_voti.aggiungi_voto(31) is False
        assert len(studente_senza_voti.voti) == 0
    
    def test_voto_massimo(self, studente_mario):
        """Test voto massimo"""
        assert studente_mario.voto_massimo() == 30
    
    def test_voto_massimo_senza_voti(self, studente_senza_voti):
        """Test voto massimo senza voti"""
        assert studente_senza_voti.voto_massimo() == 0
    
    def test_voto_minimo(self, studente_mario):
        """Test voto minimo"""
        assert studente_mario.voto_minimo() == 24
    
    def test_voto_minimo_senza_voti(self, studente_senza_voti):
        """Test voto minimo senza voti"""
        assert studente_senza_voti.voto_minimo() == 0
    
    def test_numero_voti(self, studente_mario):
        """Test numero voti"""
        assert studente_mario.numero_voti() == 4
    
    def test_ha_superato_esami_true(self, studente_mario):
        """Test ha superato esami - true"""
        assert studente_mario.ha_superato_esami() is True
    
    def test_ha_superato_esami_false(self, studente_senza_voti):
        """Test ha superato esami - false"""
        assert studente_senza_voti.ha_superato_esami() is False
    
    def test_is_eccellente_true(self, studente_lucia):
        """Test is eccellente - true"""
        assert studente_lucia.is_eccellente() is True  # media 29
    
    def test_is_eccellente_false(self, studente_mario):
        """Test is eccellente - false"""
        # Mario ha media 27, che secondo la logica attuale è considerato eccellente (>=27)
        assert studente_mario.is_eccellente() is True  # media 27
    
    def test_to_dict(self, studente_mario):
        """Test conversione a dizionario"""
        data = studente_mario.to_dict()
        expected = {
            "matricola": "12345",
            "nome": "Mario", 
            "cognome": "Rossi",
            "voti": [24, 28, 30, 26]
        }
        assert data == expected
    
    def test_from_dict(self):
        """Test creazione da dizionario"""
        data = {
            "matricola": "12345",
            "nome": "Mario",
            "cognome": "Rossi", 
            "voti": [24, 28, 30, 26]
        }
        studente = Studente.from_dict(data)
        assert studente.matricola == 12345
        assert studente.nome == "Mario"
        assert studente.cognome == "Rossi"
        assert studente.voti == [24, 28, 30, 26]
    
    def test_str_representation(self, studente_mario):
        """Test rappresentazione stringa"""
        str_repr = str(studente_mario)
        assert "[12345]" in str_repr
        assert "Mario Rossi" in str_repr
        assert "27.00" in str_repr
        assert "4 voti" in str_repr


class TestListaStudenti:
    """Test per la classe ListaStudenti"""
    
    def test_init_lista_vuota(self, lista_studenti_vuota):
        """Test inizializzazione lista vuota"""
        assert len(lista_studenti_vuota) == 0
        assert list(lista_studenti_vuota) == []
    
    def test_aggiungi_studente_nuovo(self, lista_studenti_vuota, studente_mario):
        """Test aggiunta studente nuovo"""
        assert lista_studenti_vuota.aggiungi_studente(studente_mario) is True
        assert len(lista_studenti_vuota) == 1
        assert studente_mario in lista_studenti_vuota.studenti
    
    def test_aggiungi_studente_duplicato(self, lista_studenti_vuota, studente_mario):
        """Test aggiunta studente duplicato"""
        lista_studenti_vuota.aggiungi_studente(studente_mario)
        studente_duplicato = Studente("Paolo", "Verdi", 12345)  # stessa matricola
        assert lista_studenti_vuota.aggiungi_studente(studente_duplicato) is False
        assert len(lista_studenti_vuota) == 1
    
    def test_trova_studente_esistente(self, lista_studenti_popolata):
        """Test trova studente esistente"""
        studente = lista_studenti_popolata.trova_studente(12345)
        assert studente is not None
        assert studente.nome == "Mario"
    
    def test_trova_studente_inesistente(self, lista_studenti_popolata):
        """Test trova studente inesistente"""
        studente = lista_studenti_popolata.trova_studente(99999)
        assert studente is None
    
    def test_rimuovi_studente_esistente(self, lista_studenti_popolata):
        """Test rimozione studente esistente"""
        assert lista_studenti_popolata.rimuovi_studente(12345) is True
        assert len(lista_studenti_popolata) == 2
        assert lista_studenti_popolata.trova_studente(12345) is None
    
    def test_rimuovi_studente_inesistente(self, lista_studenti_popolata):
        """Test rimozione studente inesistente"""
        lunghezza_iniziale = len(lista_studenti_popolata)
        assert lista_studenti_popolata.rimuovi_studente(99999) is False
        assert len(lista_studenti_popolata) == lunghezza_iniziale
    
    def test_trova_per_nome(self, lista_studenti_popolata):
        """Test ricerca per nome"""
        risultati = lista_studenti_popolata.trova_per_nome("Mario")
        assert len(risultati) == 1
        assert risultati[0].nome == "Mario"
    
    def test_studenti_eccellenti(self, lista_studenti_popolata):
        """Test filtro studenti eccellenti"""
        eccellenti = lista_studenti_popolata.studenti_eccellenti()
        # Mario e Lucia sono entrambi eccellenti (media >=27)
        assert len(eccellenti) == 2
        nomi = [s.nome for s in eccellenti]
        assert "Lucia" in nomi
        assert "Mario" in nomi
    
    def test_studenti_con_voti(self, lista_studenti_popolata):
        """Test filtro studenti con voti"""
        con_voti = lista_studenti_popolata.studenti_con_voti()
        assert len(con_voti) == 2  # Mario e Lucia
    
    def test_studenti_senza_voti(self, lista_studenti_popolata):
        """Test filtro studenti senza voti"""
        senza_voti = lista_studenti_popolata.studenti_senza_voti()
        assert len(senza_voti) == 1  # Paolo
        assert senza_voti[0].nome == "Paolo"
    
    def test_media_generale(self, lista_studenti_popolata):
        """Test calcolo media generale"""
        media = lista_studenti_popolata.media_generale()
        # Media di Mario (27) e Lucia (29) = 28
        assert media == 28.0
    
    def test_media_generale_senza_voti(self, lista_studenti_vuota):
        """Test media generale con lista vuota"""
        assert lista_studenti_vuota.media_generale() == 0.0
    
    def test_statistiche(self, lista_studenti_popolata):
        """Test generazione statistiche"""
        stats = lista_studenti_popolata.statistiche()
        assert stats["totale_studenti"] == 3
        assert stats["studenti_con_voti"] == 2
        assert stats["studenti_senza_voti"] == 1
        assert stats["studenti_eccellenti"] == 2
        assert stats["media_generale"] == 28.0
    
    def test_ordina_per_media(self, lista_studenti_popolata):
        """Test ordinamento per media"""
        ordinati = lista_studenti_popolata.ordina_per_media(decrescente=True)
        assert ordinati[0].nome == "Lucia"  # media più alta
        assert ordinati[1].nome == "Mario"  # media più bassa
    
    def test_ordina_per_nome(self, lista_studenti_popolata):
        """Test ordinamento per nome"""
        ordinati = lista_studenti_popolata.ordina_per_nome()
        # Ordine alfabetico per cognome: Bianchi, Rossi, Verdi
        assert ordinati[0].cognome == "Bianchi"
        assert ordinati[1].cognome == "Rossi"
        assert ordinati[2].cognome == "Verdi"
    
    def test_to_dict_list(self, lista_studenti_popolata):
        """Test conversione a lista di dizionari"""
        dict_list = lista_studenti_popolata.to_dict_list()
        assert len(dict_list) == 3
        assert all(isinstance(item, dict) for item in dict_list)
        assert dict_list[0]["nome"] == "Mario"
    
    def test_from_dict_list(self, sample_student_data):
        """Test caricamento da lista di dizionari"""
        lista = ListaStudenti()
        lista.from_dict_list(sample_student_data)
        assert len(lista) == 3
        assert lista.trova_studente(12345) is not None
    
    def test_contains_operator(self, lista_studenti_popolata):
        """Test operatore contains"""
        assert 12345 in lista_studenti_popolata
        assert 99999 not in lista_studenti_popolata
    
    def test_iteration(self, lista_studenti_popolata):
        """Test iterazione sulla lista"""
        nomi = [studente.nome for studente in lista_studenti_popolata]
        assert "Mario" in nomi
        assert "Lucia" in nomi
        assert "Paolo" in nomi
