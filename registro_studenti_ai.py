"""
Student Registry - Management system for university students
===========================================================
This program implements a simple electronic registry that allows to:
- View the list of students with their grade averages
- Add new students
- Add grades to existing students

Data is saved in JSON format in a text file.
"""

import os  # Module to interact with the operating system
import json  # Module to work with data in JSON format (JavaScript Object Notation)
from typing import List, Dict  # Type annotations to improve code readability

# Data file path configuration
# ---------------------------------------
# Gets the absolute path of the 'registro.txt' file in the same folder as the script
# __file__ is a special variable that contains the path of the current file
main_dir = os.path.dirname(__file__)  # Gets the directory containing the script
file_path = os.path.join(main_dir, 'registro.txt')  # Composes the complete file path


def leggi_studenti_da_file(percorso_file: str) -> List[Dict]:
    """
    Reads the JSON file and returns the list of students as a list of dictionaries.
    
    Args:
        percorso_file: Complete path of the JSON file to read
        
    Returns:
        List[Dict]: List of dictionaries, each representing a student
                   Returns empty list in case of error
    
    Note:
        - Uses encoding='utf-8' to correctly handle special characters
        - Handles two possible exceptions:
          * FileNotFoundError: when the file doesn't exist
          * JSONDecodeError: when the file exists but doesn't contain valid JSON
    """
    try:
        with open(percorso_file, encoding='utf-8') as file:  # 'with' ensures the file is closed
            return json.load(file)  # Converts JSON into Python data structure
    except (json.JSONDecodeError, FileNotFoundError):
        print("❌ Error in JSON file or file not found.")
        return []  # Returns an empty list in case of error


def calcola_media(voti: List[float]) -> float:
    """
    Calculates the arithmetic mean of a list of numeric grades.
    
    Args:
        voti: List of grades to calculate the average from
        
    Returns:
        float: Average calculated with decimal precision, 0.0 if there are no valid grades
        
    Note:
        - Filters only numeric values (integers or decimals) from the list
        - Uses list comprehension to create a new filtered list
        - Checks that the list is not empty before calculating the average
    """
    # Filtra solo i valori numerici (interi o float) dalla lista dei voti
    voti_validi = [v for v in voti if isinstance(v, (int, float))]
    if not voti_validi:
        # Se non ci sono voti validi, restituisce 0.0 come media
        return 0.0
    # Calcola la media aritmetica dei voti validi
    return sum(voti_validi) / len(voti_validi)

def stampa_studenti(studenti: List[Dict]):
    """
    Prints on screen the list of students with their data.
    
    Args:
        studenti: List of dictionaries, each representing a student
        
    Note:
        - For each student shows: student ID, first name, last name and grade average
        - Uses the .get() method of dictionaries which allows to specify
          a default value ('N/D' = Not Available) if the key doesn't exist
        - Formats the average with two decimals using f-string syntax {media:.2f}
    """
    print("\nStudent list:")
    for studente in studenti:
        matricola = studente.get("matricola", "N/D")  # 'N/D' is the default value if the key doesn't exist
        nome = studente.get("nome", "N/D")
        cognome = studente.get("cognome", "N/D")
        voti = studente.get("voti", [])  # Empty list if the key doesn't exist
        media = calcola_media(voti)
        print(f"[{matricola}] {nome} {cognome} - Grade average: {media:.2f}")  # Formatting with f-string


def esegui_processo(percorso_file: str):
    """
    Main function that reads students from the file and displays them on screen.
    
    Args:
        percorso_file: Complete path of the data file
        
    Note:
        - This function combines two operations:
          1. Reading data from file
          2. Displaying the data
        - It's an example of function composition: a function that uses others
    """
    studenti = leggi_studenti_da_file(percorso_file)  # First reads the data
    stampa_studenti(studenti)  # Then displays it


def aggiungi_studente(percorso_file: str):
    """
    Adds a new student by requesting data via input and saving it to the file.
    
    Args:
        percorso_file: Complete path of the data file
        
    Note:
        - The function implements input data validation:
          * The student ID, first name, and last name fields are mandatory
          * Grades must be integers between 18 and 30
        - Uses while loops to repeatedly request data until
          it is provided correctly
        - Each student is represented as a dictionary with standardized keys
    """
    # PHASE 1: Data collection with validation
    # ----------------------------------------
    
    # Request mandatory student ID
    while True:
        matricola = input("Student ID: ").strip()  # .strip() removes leading and trailing spaces
        if matricola:
            break  # Exits the loop if the student ID is not empty
        print("⚠️ Student ID cannot be empty. Try again.")

    # Request mandatory first name
    while True:
        nome = input("First name: ").strip()
        if nome:
            break
        print("⚠️ First name cannot be empty. Try again.")

    # Request mandatory last name
    while True:
        cognome = input("Last name: ").strip()
        if cognome:
            break
        print("⚠️ Last name cannot be empty. Try again.")    # Request and validation of grades
    voti_input = input("Enter grades separated by commas (e.g. 24,26,30): ")
    try:
        # List comprehension with multiple conditions:
        # 1. Splits the input based on commas
        # 2. For each value, removes leading and trailing spaces
        # 3. Verifies that it consists only of digits
        # 4. Verifies that it is in the 18-30 range
        # 5. Converts to integer
        voti = [
            int(v.strip()) 
            for v in voti_input.split(",") 
            if v.strip().isdigit() and 18 <= int(v.strip()) <= 30
        ]
    except ValueError:
        voti = []  # In case of error, initialize with empty list

    # Verify that there is at least one valid grade
    if not voti:
        print("⚠️ No valid grades entered (must be between 18 and 30). Student not added.")
        return  # Terminates the function without adding the student

    # PHASE 2: Data creation and saving
    # ---------------------------------

    # Create the new student as dictionary
    nuovo_studente = {
        "matricola": matricola,
        "nome": nome,
        "cognome": cognome,
        "voti": voti
    }

    # Load current students and add the new one
    studenti = leggi_studenti_da_file(percorso_file)
    studenti.append(nuovo_studente)  # Adds the new student to the existing list

    # Save the updated file
    with open(percorso_file, "w", encoding="utf-8") as file:
        # ensure_ascii=False allows saving non-ASCII characters (e.g. accented letters)
        # indent=2 formats JSON with 2-space indentation for better readability
        json.dump(studenti, file, ensure_ascii=False, indent=2)

    # Confirmation to user
    print(f"\n✅ Student {nome} {cognome} successfully added.")


def aggiungi_voto(percorso_file: str):
    """
    Aggiunge un voto a uno studente esistente identificato per matricola.
    
    Args:
        percorso_file: Percorso completo del file dati
        
    Note:
        - Cerca lo studente tramite la matricola usando la funzione next() con un generatore
        - Valida il voto inserito assicurandosi che sia un intero tra 18 e 30
        - Usa il metodo setdefault() per gestire il caso in cui lo studente non abbia già voti
    """
    # Carica i dati attuali
    studenti = leggi_studenti_da_file(percorso_file)

    # Richiesta della matricola
    matricola_input = input("Inserisci il numero di matricola: ").strip()

    # Ricerca dello studente con la matricola inserita
    # La funzione next() prende:
    # - Un generatore (espressione che produce valori uno alla volta)
    # - Un valore di default (None) da restituire se il generatore è vuoto
    studente_trovato = next((s for s in studenti if s.get("matricola") == matricola_input), None)

    # Verifica se lo studente è stato trovato
    if not studente_trovato:
        print(f"❌ Errore: Nessuno studente trovato con matricola {matricola_input}")
        return  # Esce dalla funzione    # Richiesta e validazione del nuovo voto
    voto_input = input("Inserisci il nuovo voto: ").strip()
    try:
        voto = int(voto_input)  # Converte l'input in numero intero
        if not 18 <= voto <= 30:  # Verifica il range consentito
            raise ValueError  # Genera un'eccezione se il voto non è nel range
    except ValueError:
        print("❌ Errore: Il voto deve essere un numero intero tra 18 e 30.")
        return  # Esce dalla funzione

    # Aggiunta del voto all'elenco
    # setdefault() restituisce il valore della chiave se esiste o crea la chiave
    # con il valore di default specificato (lista vuota in questo caso)
    studente_trovato.setdefault("voti", []).append(voto)

    # Salvataggio nel file
    with open(percorso_file, "w", encoding="utf-8") as file:
        json.dump(studenti, file, ensure_ascii=False, indent=2)

    # Conferma all'utente
    print(f"✅ Voto {voto} aggiunto con successo a {studente_trovato['nome']} {studente_trovato['cognome']}.")


def cancella_studente(percorso_file: str):
    """
    Cancella uno studente esistente dal registro identificandolo per matricola.
    
    Args:
        percorso_file: Percorso completo del file dati
        
    Note:
        - Cerca lo studente tramite la matricola
        - Richiede conferma prima di procedere con la cancellazione
        - Aggiorna il file JSON dopo la cancellazione
    """
    # Carica i dati attuali
    studenti = leggi_studenti_da_file(percorso_file)
    
    # Se non ci sono studenti nel registro
    if not studenti:
        print("❌ Nessuno studente presente nel registro.")
        return
    
    # Richiesta della matricola
    matricola_input = input("Inserisci il numero di matricola dello studente da cancellare: ").strip()
    
    # Ricerca dello studente con la matricola inserita
    studente_index = None
    for index, studente in enumerate(studenti):
        if studente.get("matricola") == matricola_input:
            studente_index = index
            break
    
    # Verifica se lo studente è stato trovato
    if studente_index is None:
        print(f"❌ Errore: Nessuno studente trovato con matricola {matricola_input}")
        return
    
    # Ottieni i dati dello studente per la conferma
    studente = studenti[studente_index]
    nome_completo = f"{studente.get('nome', 'N/D')} {studente.get('cognome', 'N/D')}"
    
    # Chiedi conferma prima di procedere
    conferma = input(f"Sei sicuro di voler cancellare lo studente {nome_completo}? (s/n): ").strip().lower()
    if conferma != 's':
        print("Operazione annullata.")
        return
    
    # Rimuovi lo studente dalla lista
    studente_rimosso = studenti.pop(studente_index)

    # Salvataggio nel file
    with open(percorso_file, "w", encoding="utf-8") as file:
        json.dump(studenti, file, ensure_ascii=False, indent=2)

    # Conferma all'utente
    print(f"✅ Studente {nome_completo} rimosso con successo dal registro.")

# Funzione per stampare la lista voti di uno studente
def stampa_voti_studente(percorso_file: str, matricola: str):
    """
    Stampa i voti di uno studente identificato dalla matricola.
    
    Args:
        percorso_file: Percorso completo del file dati
        matricola: Matricola dello studente di cui stampare i voti
        
    Note:
        - Cerca lo studente tramite la matricola
        - Se lo studente non esiste, mostra un messaggio di errore
        - Se esiste, stampa i suoi voti formattati
    """
    studenti = leggi_studenti_da_file(percorso_file)
    studente_trovato = next((s for s in studenti if s.get("matricola") == matricola), None)

    if not studente_trovato:
        print(f"❌ Errore: Nessuno studente trovato con matricola {matricola}")
        return

    voti = studente_trovato.get("voti", [])
    if not voti:
        print(f"⚠️ Lo studente {studente_trovato['nome']} {studente_trovato['cognome']} non ha voti registrati.")
    else:
        print(f"Voti per {studente_trovato['nome']} {studente_trovato['cognome']}: {', '.join(map(str, voti))}")


# Menù principale del programma
if __name__ == "__main__":
    """
    Punto di ingresso dell'applicazione.
    
    Note:
        - La condizione if __name__ == "__main__": garantisce che questo codice venga eseguito solo 
          quando lo script viene avviato direttamente e non quando viene importato
        - Il menù utilizza un ciclo while infinito (interrotto solo dall'opzione di uscita)
        - Ogni opzione chiama la funzione corrispondente passando il percorso del file dati
    """
    while True:
        # Visualizza il menù delle opzioni
        print("\nCosa vuoi fare?")
        print("[1] Stampa lista studenti")
        print("[2] Aggiungi studente")
        print("[3] Aggiungi voto")
        print("[4] Cancella studente")
        print("[0] Esci")
        scelta = input("Scelta: ").strip()

        # Gestione delle diverse opzioni tramite if-elif-else
        if scelta == "1":
            esegui_processo(file_path)
        elif scelta == "2":
            aggiungi_studente(file_path)
        elif scelta == "3":
            aggiungi_voto(file_path)
        elif scelta == "4":
            cancella_studente(file_path)
        elif scelta == "0":
            print("👋 Uscita dal programma.")
            break  # Esce dal ciclo while e termina il programma
        else:
            print("❌ Scelta non valida. Riprova.")
