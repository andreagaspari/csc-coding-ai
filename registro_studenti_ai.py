"""
Student Registry - Management system for university students
===========================================================
This program implements a simple electronic registry that allows to:
- View the list of students with their grade averages
- Add new students
- Add grades to existing students

Data is saved in JSON format in a text file.
"""

import os
from menu import esegui_menu_principale

# Data file path configuration
# ---------------------------------------
# Gets the absolute path of the 'registro.txt' file in the same folder as the script
main_dir = os.path.dirname(__file__)
file_path = os.path.join(main_dir, 'registro.txt')

# Punto di ingresso dell'applicazione
if __name__ == "__main__":
    esegui_menu_principale(file_path)
