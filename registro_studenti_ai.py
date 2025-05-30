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
from datetime import datetime  # Module for date and time operations
from reportlab.lib.pagesizes import letter, A4  # PDF page sizes
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

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
    except FileNotFoundError:
        print("ℹ️ File not found. Starting with empty registry.")
        return []  # Returns an empty list if file doesn't exist
    except json.JSONDecodeError:
        print("❌ Error: Invalid JSON format in file.")
        return []  # Returns an empty list in case of JSON error


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
    if not studenti:
        print("\n📋 Nessuno studente presente nel registro.")
        return
        
    print(f"\n📋 Lista studenti ({len(studenti)} studenti):")
    print("-" * 60)
    for studente in studenti:
        matricola = studente.get("matricola", "N/D")  # 'N/D' is the default value if the key doesn't exist
        nome = studente.get("nome", "N/D")
        cognome = studente.get("cognome", "N/D")
        voti = studente.get("voti", [])  # Empty list if the key doesn't exist
        media = calcola_media(voti)
        num_voti = len(voti)
        print(f"[{matricola}] {nome} {cognome} - Media: {media:.2f} ({num_voti} voti)")  # Formatting with f-string


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
          * Student ID must be unique
          * Grades are optional but must be integers between 18 and 30 if provided
        - Uses while loops to repeatedly request data until
          it is provided correctly
        - Each student is represented as a dictionary with standardized keys
    """
    # Carica i dati attuali per verificare le matricole esistenti
    studenti = leggi_studenti_da_file(percorso_file)
    
    # PHASE 1: Data collection with validation
    # ----------------------------------------
    
    # Request mandatory and unique student ID
    while True:
        matricola = input("Numero di matricola: ").strip()  # .strip() removes leading and trailing spaces
        if not matricola:
            print("⚠️ La matricola è vuota. Riprova.")
            continue
        if matricola_esiste(studenti, matricola):
            print(f"⚠️ La matricola {matricola} esiste già. Inserisci una matricola diversa.")
            continue
        break  # Exits the loop if the student ID is valid and unique

    # Request mandatory first name
    while True:
        nome = input("Nome: ").strip()
        if nome:
            break
        print("⚠️ Il nome non può essere vuoto. Riprova.")

    # Request mandatory last name
    while True:
        cognome = input("Cognome: ").strip()
        if cognome:
            break
        print("⚠️ Il cognome non può essere vuoto. Riprova.")
    
    # Request and validation of grades (now optional)
    voti = []
    voti_input = input("Inserisci i voti separati da virgole (es. 24,26,30) o premi INVIO per saltare: ").strip()
    
    if voti_input:  # Se l'utente ha inserito dei voti
        try:
            # Process each grade
            for v in voti_input.split(","):
                voto_str = v.strip()
                if voto_str:  # Ignore empty strings
                    try:
                        voto = valida_voto(voto_str)
                        voti.append(voto)
                    except ValueError as e:
                        print(f"⚠️ Voto '{voto_str}' ignorato: {e}")
        except Exception as e:
            print(f"⚠️ Errore nel processare i voti: {e}")
            voti = []

    # PHASE 2: Data creation and saving
    # ---------------------------------

    # Create the new student as dictionary
    nuovo_studente = {
        "matricola": matricola,
        "nome": nome,
        "cognome": cognome,
        "voti": voti
    }

    # Add the new student to the list
    studenti.append(nuovo_studente)

    # Save the updated file
    if salva_studenti_su_file(percorso_file, studenti):
        if voti:
            print(f"\n✅ Studente {nome} {cognome} aggiunto con successo con {len(voti)} voti.")
        else:
            print(f"\n✅ Studente {nome} {cognome} aggiunto con successo (nessun voto iniziale).")
    else:
        print("❌ Errore nel salvataggio dello studente.")


def aggiungi_voto(percorso_file: str):
    """
    Aggiunge un voto a uno studente esistente identificato per matricola.
    
    Args:
        percorso_file: Percorso completo del file dati
        
    Note:
        - Cerca lo studente tramite la matricola usando la funzione dedicata
        - Valida il voto inserito usando la funzione di validazione centralizzata
        - Usa il metodo setdefault() per gestire il caso in cui lo studente non abbia già voti
    """
    # Carica i dati attuali
    studenti = leggi_studenti_da_file(percorso_file)

    if not studenti:
        print("❌ Nessuno studente presente nel registro.")
        return

    # Richiesta della matricola
    matricola_input = input("Inserisci il numero di matricola: ").strip()

    # Ricerca dello studente con la matricola inserita
    studente_trovato = trova_studente_per_matricola(studenti, matricola_input)

    # Verifica se lo studente è stato trovato
    if not studente_trovato:
        print(f"❌ Errore: Nessuno studente trovato con matricola {matricola_input}")
        return

    # Richiesta e validazione del nuovo voto
    voto_input = input("Inserisci il nuovo voto: ").strip()
    try:
        voto = valida_voto(voto_input)
    except ValueError as e:
        print(f"❌ Errore: {e}")
        return

    # Aggiunta del voto all'elenco
    studente_trovato.setdefault("voti", []).append(voto)

    # Salvataggio nel file
    if salva_studenti_su_file(percorso_file, studenti):
        print(f"✅ Voto {voto} aggiunto con successo a {studente_trovato['nome']} {studente_trovato['cognome']}.")
    else:
        print("❌ Errore nel salvataggio del voto.")


def cancella_studente(percorso_file: str):
    """
    Cancella uno studente esistente dal registro identificandolo per matricola.
    
    Args:
        percorso_file: Percorso completo del file dati
        
    Note:
        - Cerca lo studente tramite la matricola usando la funzione dedicata
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
    studente_trovato = trova_studente_per_matricola(studenti, matricola_input)
    
    # Verifica se lo studente è stato trovato
    if not studente_trovato:
        print(f"❌ Errore: Nessuno studente trovato con matricola {matricola_input}")
        return
    
    # Ottieni i dati dello studente per la conferma
    nome_completo = f"{studente_trovato.get('nome', 'N/D')} {studente_trovato.get('cognome', 'N/D')}"
    
    # Chiedi conferma prima di procedere
    conferma = input(f"Sei sicuro di voler cancellare lo studente {nome_completo}? (s/n): ").strip().lower()
    if conferma != 's':
        print("Operazione annullata.")
        return
    
    # Rimuovi lo studente dalla lista
    studenti.remove(studente_trovato)

    # Salvataggio nel file
    if salva_studenti_su_file(percorso_file, studenti):
        print(f"✅ Studente {nome_completo} rimosso con successo dal registro.")
    else:
        print("❌ Errore nel salvataggio dopo la cancellazione.")

# Funzione per stampare la lista voti di uno studente
def stampa_voti_studente(percorso_file: str, matricola: str = None):
    """
    Stampa i voti di uno studente identificato dalla matricola.
    
    Args:
        percorso_file: Percorso completo del file dati
        matricola: Matricola dello studente di cui stampare i voti (opzionale)
        
    Note:
        - Se matricola non è fornita, la richiede all'utente
        - Cerca lo studente tramite la matricola usando la funzione dedicata
        - Se lo studente non esiste, mostra un messaggio di errore
        - Se esiste, stampa i suoi voti formattati con statistiche
    """
    studenti = leggi_studenti_da_file(percorso_file)
    
    if not studenti:
        print("❌ Nessuno studente presente nel registro.")
        return

    # Se la matricola non è fornita, la richiediamo
    if matricola is None:
        matricola = input("Inserisci il numero di matricola: ").strip()
    
    studente_trovato = trova_studente_per_matricola(studenti, matricola)

    if not studente_trovato:
        print(f"❌ Errore: Nessuno studente trovato con matricola {matricola}")
        return

    nome_completo = f"{studente_trovato['nome']} {studente_trovato['cognome']}"
    voti = studente_trovato.get("voti", [])
    
    print(f"\n📊 Dettaglio voti per {nome_completo} (Matricola: {matricola})")
    print("-" * 50)
    
    if not voti:
        print("⚠️ Nessun voto registrato.")
    else:
        print(f"Voti registrati: {', '.join(map(str, voti))}")
        print(f"Numero totale voti: {len(voti)}")
        print(f"Media: {calcola_media(voti):.2f}")
        print(f"Voto minimo: {min(voti)}")
        print(f"Voto massimo: {max(voti)}")


def salva_lista_studenti_pdf(percorso_file: str, nome_file_pdf: str = None):
    """
    Salva la lista degli studenti in formato PDF con una tabella formattata.
    
    Args:
        percorso_file: Percorso completo del file JSON dei dati
        nome_file_pdf: Nome del file PDF da creare (opzionale)
        
    Note:
        - Se nome_file_pdf non è fornito, usa un nome predefinito con timestamp
        - Crea una tabella con matricola, nome, cognome, numero voti e media
        - Aggiunge intestazione e data di creazione
        - Gestisce il caso di lista vuota
    """
    studenti = leggi_studenti_da_file(percorso_file)
    
    if not studenti:
        print("❌ Nessuno studente presente nel registro. Impossibile creare il PDF.")
        return
    
    # Se non viene fornito un nome file, crea uno con timestamp
    if nome_file_pdf is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_file_pdf = f"registro_studenti_{timestamp}.pdf"
    
    # Assicurati che abbia estensione .pdf
    if not nome_file_pdf.endswith('.pdf'):
        nome_file_pdf += '.pdf'
    
    # Percorso completo del file PDF
    cartella_file = os.path.dirname(percorso_file)
    percorso_pdf = os.path.join(cartella_file, nome_file_pdf)
    
    try:
        # Crea il documento PDF
        doc = SimpleDocTemplate(percorso_pdf, pagesize=A4)
        elements = []
        
        # Stili
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=1  # Centrato
        )
        
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Normal'],
            fontSize=12,
            spaceAfter=20,
            alignment=1  # Centrato
        )
        
        # Titolo
        title = Paragraph("📋 Registro Elettronico Studenti", title_style)
        elements.append(title)
        
        # Data di creazione
        data_creazione = datetime.now().strftime("%d/%m/%Y alle %H:%M")
        subtitle = Paragraph(f"Generato il {data_creazione}", subtitle_style)
        elements.append(subtitle)
        
        # Spazio
        elements.append(Spacer(1, 20))
        
        # Prepara i dati per la tabella
        # Intestazione
        data = [['Matricola', 'Nome', 'Cognome', 'N° Voti', 'Media']]
        
        # Dati degli studenti
        for studente in studenti:
            matricola = studente.get("matricola", "N/D")
            nome = studente.get("nome", "N/D")
            cognome = studente.get("cognome", "N/D")
            voti = studente.get("voti", [])
            num_voti = len(voti)
            media = calcola_media(voti)
            
            data.append([
                matricola,
                nome,
                cognome,
                str(num_voti),
                f"{media:.2f}"
            ])
        
        # Crea la tabella
        table = Table(data, colWidths=[1.2*inch, 1.5*inch, 1.5*inch, 0.8*inch, 0.8*inch])
        
        # Stile della tabella
        table.setStyle(TableStyle([
            # Intestazione
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            
            # Righe dei dati
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.beige, colors.lightgrey]),
            
            # Bordi
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        elements.append(table)
        
        # Spazio
        elements.append(Spacer(1, 30))
        
        # Statistiche riassuntive
        total_studenti = len(studenti)
        studenti_con_voti = len([s for s in studenti if s.get("voti", [])])
        media_generale = calcola_media([v for s in studenti for v in s.get("voti", [])])
        
        stats_style = ParagraphStyle(
            'Stats',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=10
        )
        
        stats_text = f"""
        <b>Statistiche Generali:</b><br/>
        • Totale studenti: {total_studenti}<br/>
        • Studenti con voti: {studenti_con_voti}<br/>
        • Media generale: {media_generale:.2f}<br/>
        """
        
        stats = Paragraph(stats_text, stats_style)
        elements.append(stats)
        
        # Genera il PDF
        doc.build(elements)
        
        print(f"✅ Lista studenti salvata con successo in: {percorso_pdf}")
        print(f"📊 {total_studenti} studenti esportati nel PDF")
        
    except Exception as e:
        print(f"❌ Errore durante la creazione del PDF: {e}")


def salva_studenti_su_file(percorso_file: str, studenti: List[Dict]) -> bool:
    """
    Salva la lista di studenti nel file JSON.
    
    Args:
        percorso_file: Percorso completo del file dati
        studenti: Lista di studenti da salvare
        
    Returns:
        bool: True se il salvataggio è riuscito, False altrimenti
    """
    try:
        with open(percorso_file, "w", encoding="utf-8") as file:
            json.dump(studenti, file, ensure_ascii=False, indent=2)
        return True
    except (IOError, OSError) as e:
        print(f"❌ Errore nel salvataggio del file: {e}")
        return False


def trova_studente_per_matricola(studenti: List[Dict], matricola: str) -> Dict:
    """
    Trova uno studente nella lista tramite matricola.
    
    Args:
        studenti: Lista di studenti in cui cercare
        matricola: Matricola dello studente da trovare
        
    Returns:
        Dict: Dizionario dello studente trovato, None se non trovato
    """
    return next((s for s in studenti if s.get("matricola") == matricola), None)


def matricola_esiste(studenti: List[Dict], matricola: str) -> bool:
    """
    Verifica se una matricola esiste già nella lista studenti.
    
    Args:
        studenti: Lista di studenti in cui cercare
        matricola: Matricola da verificare
        
    Returns:
        bool: True se la matricola esiste, False altrimenti
    """
    return any(s.get("matricola") == matricola for s in studenti)


def valida_voto(voto_str: str) -> int:
    """
    Valida e converte una stringa di voto in intero.
    
    Args:
        voto_str: Stringa contenente il voto da validare
        
    Returns:
        int: Voto validato, solleva ValueError se non valido
        
    Raises:
        ValueError: Se il voto non è valido (non numerico o fuori dal range 18-30)
    """
    try:
        voto = int(voto_str.strip())
        if not 18 <= voto <= 30:
            raise ValueError(f"Il voto deve essere compreso tra 18 e 30, ricevuto: {voto}")
        return voto
    except ValueError:
        raise ValueError("Il voto deve essere un numero intero tra 18 e 30")

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
    print("🎓 Benvenuto nel Sistema di Gestione Registro Studenti")
    print("=" * 55)
    
    while True:
        # Visualizza il menù delle opzioni
        print("\nCosa vuoi fare?")
        print("[1] 📋 Stampa lista studenti")
        print("[2] ➕ Aggiungi studente")
        print("[3] 📝 Aggiungi voto")
        print("[4] 🗑️  Cancella studente")
        print("[5] 📊 Visualizza voti di uno studente")
        print("[6] 📥 Esporta lista studenti in PDF")
        print("[0] 👋 Esci")
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
        elif scelta == "5":
            stampa_voti_studente(file_path)
        elif scelta == "6":
            # Esportazione della lista studenti in PDF
            nome_file = input("Inserisci il nome del file PDF (o premi INVIO per nome predefinito): ").strip() or None
            salva_lista_studenti_pdf(file_path, nome_file)
        elif scelta == "0":
            print("👋 Uscita dal programma. Arrivederci!")
            break  # Esce dal ciclo while e termina il programma
        else:
            print("❌ Scelta non valida. Riprova.")
