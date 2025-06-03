"""
Menu principale del registro studenti
====================================
Gestisce l'interfaccia utente e la navigazione.
"""

from student_operations import (
    visualizza_lista_studenti, aggiungi_studente, aggiungi_voto,
    cancella_studente, stampa_voti_studente
)
from pdf_export import salva_lista_studenti_pdf


def mostra_menu():
    """Visualizza il menu delle opzioni disponibili."""
    print("\nCosa vuoi fare?")
    print("[1] 📋 Stampa lista studenti")
    print("[2] ➕ Aggiungi studente")
    print("[3] 📝 Aggiungi voto")
    print("[4] 🗑️  Cancella studente")
    print("[5] 📊 Visualizza voti di uno studente")
    print("[6] 📥 Esporta lista studenti in PDF")
    print("[0] 👋 Esci")


def esegui_menu_principale(file_path: str):
    """
    Esegue il loop principale del menu.
    
    Args:
        file_path: Percorso del file dati
    """
    print("🎓 Benvenuto nel Sistema di Gestione Registro Studenti")
    print("=" * 55)
    
    while True:
        mostra_menu()
        scelta = input("Scelta: ").strip()

        if scelta == "1":
            visualizza_lista_studenti(file_path)
        elif scelta == "2":
            aggiungi_studente(file_path)
        elif scelta == "3":
            aggiungi_voto(file_path)
        elif scelta == "4":
            cancella_studente(file_path)
        elif scelta == "5":
            stampa_voti_studente(file_path)
        elif scelta == "6":
            nome_file = input("Inserisci il nome del file PDF (o premi INVIO per nome predefinito): ").strip() or None
            salva_lista_studenti_pdf(file_path, nome_file)
        elif scelta == "0":
            print("👋 Uscita dal programma. Arrivederci!")
            break
        else:
            print("❌ Scelta non valida. Riprova.")
