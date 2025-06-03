"""
Configurazione dell'applicazione
===============================
Contiene le configurazioni centrali per il sistema.
"""

import os
from pathlib import Path

# Configurazioni file
DEFAULT_DATA_FILE = "registro.txt"
DEFAULT_PDF_NAME = "registro_studenti"

# Configurazioni validazione
VOTO_MIN = 18
VOTO_MAX = 30

# Configurazioni paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
EXPORTS_DIR = PROJECT_ROOT / "exports"
LOGS_DIR = PROJECT_ROOT / "logs"

# Assicura che le directory esistano
DATA_DIR.mkdir(exist_ok=True)
EXPORTS_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# Path del file dati predefinito
DEFAULT_DATA_PATH = DATA_DIR / DEFAULT_DATA_FILE
