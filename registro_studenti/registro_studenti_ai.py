"""
Student Registry - Management system for university students
===========================================================
This program implements a simple electronic registry that allows to:
- View the list of students with their grade averages
- Add new students
- Add grades to existing students

Data is saved in JSON format in a text file.

Version 2.0 - New modular architecture
"""

import os
import sys

# Aggiungi src al path per importare i moduli
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.config import DEFAULT_DATA_PATH
from src.ui import MenuUI
from src.data_manager import FileManager
from src.student_service import StudentService
from src.pdf_exporter import PDFExporter

def main():
    """Punto di ingresso principale dell'applicazione"""
    try:
        # Inizializza e avvia l'interfaccia utente
        ui = MenuUI(str(DEFAULT_DATA_PATH))
        ui.esegui_menu_principale()
        
    except KeyboardInterrupt:
        print("\n\n👋 Applicazione interrotta dall'utente. Arrivederci!")
    except Exception as e:
        print(f"❌ Errore inaspettato: {e}")
        print("Per assistenza, controlla i log o contatta il supporto.")

# Punto di ingresso dell'applicazione
if __name__ == "__main__":
    main()
