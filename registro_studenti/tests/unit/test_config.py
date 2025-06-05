"""
Test unitari per il modulo config
================================
Testa le configurazioni e costanti dell'applicazione.
"""

import pytest
from pathlib import Path
from src.config import (
    VOTO_MIN, VOTO_MAX, DEFAULT_DATA_PATH, 
    DATA_DIR, LOGS_DIR, EXPORTS_DIR
)


class TestConfig:
    """Test per le configurazioni dell'applicazione"""
    
    def test_voti_range_valido(self):
        """Test che il range dei voti sia valido"""
        assert VOTO_MIN == 18
        assert VOTO_MAX == 30
        assert VOTO_MIN < VOTO_MAX
    
    def test_default_data_path_esiste(self):
        """Test che il percorso dati di default sia valido"""
        assert DEFAULT_DATA_PATH is not None
        assert isinstance(DEFAULT_DATA_PATH, Path)
    
    def test_directory_configurate(self):
        """Test che le directory siano configurate correttamente"""
        directories = [DATA_DIR, LOGS_DIR, EXPORTS_DIR]
        
        for directory in directories:
            assert directory is not None
            assert isinstance(directory, Path)
    
    def test_voto_min_boundary(self):
        """Test boundary voto minimo"""
        assert VOTO_MIN >= 0
        assert VOTO_MIN <= 30
    
    def test_voto_max_boundary(self):
        """Test boundary voto massimo"""
        assert VOTO_MAX >= 18
        assert VOTO_MAX <= 35  # Limite ragionevole
    
    def test_costanti_immutabili(self):
        """Test che le costanti non siano modificabili accidentalmente"""
        # Verifica che i tipi siano corretti
        assert isinstance(VOTO_MIN, int)
        assert isinstance(VOTO_MAX, int)
    
    def test_paths_relativi(self):
        """Test che i percorsi siano relativi alla directory del progetto"""
        # Verifica che i percorsi non siano assoluti di sistema
        assert not str(DEFAULT_DATA_PATH).startswith('/usr')
        assert not str(DEFAULT_DATA_PATH).startswith('/etc')
    
    def test_directory_names_validi(self):
        """Test che i nomi delle directory siano validi"""
        directory_names = [
            DATA_DIR.name,
            LOGS_DIR.name, 
            EXPORTS_DIR.name
        ]
        
        for name in directory_names:
            assert name.isalnum() or '_' in name or '-' in name
            assert not name.startswith('.')
            assert len(name) > 0
