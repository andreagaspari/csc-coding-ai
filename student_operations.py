"""
Operazioni sugli studenti
========================
Contiene tutte le funzioni per gestire gli studenti (CRUD operations).
"""

from typing import List, Dict
from utils import calcola_media
from models import StudentModel, valida_voto
from file_operations import leggi_studenti_da_file, salva_studenti_su_file


def stampa_studenti(studenti: List[Dict]):
    """Stampa a schermo la lista degli studenti con i loro dati."""
    if not studenti:
        print("\n📋 Nessuno studente presente nel registro.")
        return
        
    print(f"\n📋 Lista studenti ({len(studenti)} studenti):")
    print("-" * 60)
    for studente in studenti:
        matricola = studente.get("matricola", "N/D")
        nome = studente.get("nome", "N/D")
        cognome = studente.get("cognome", "N/D")
        voti = studente.get("voti", [])
        media = calcola_media(voti)
        num_voti = len(voti)
        print(f"[{matricola}] {nome} {cognome} - Media: {media:.2f} ({num_voti} voti)")


def visualizza_lista_studenti(percorso_file: str):
    """Funzione principale che legge gli studenti dal file e li visualizza."""
    studenti = leggi_studenti_da_file(percorso_file)
    stampa_studenti(studenti)


def aggiungi_studente(percorso_file: str):
    """Aggiunge un nuovo studente richiedendo i dati tramite input."""
    studenti = leggi_studenti_da_file(percorso_file)
    
    # Richiesta matricola unica
    while True:
        matricola = input("Numero di matricola: ").strip()
        if not matricola:
            print("⚠️ La matricola è vuota. Riprova.")
            continue
        if StudentModel.matricola_exists(studenti, matricola):
            print(f"⚠️ La matricola {matricola} esiste già. Inserisci una matricola diversa.")
            continue
        break

    # Richiesta nome obbligatorio
    while True:
        nome = input("Nome: ").strip()
        if nome:
            break
        print("⚠️ Il nome non può essere vuoto. Riprova.")

    # Richiesta cognome obbligatorio
    while True:
        cognome = input("Cognome: ").strip()
        if cognome:
            break
        print("⚠️ Il cognome non può essere vuoto. Riprova.")
    
    # Richiesta voti opzionali
    voti = []
    voti_input = input("Inserisci i voti separati da virgole (es. 24,26,30) o premi INVIO per saltare: ").strip()
    
    if voti_input:
        try:
            for v in voti_input.split(","):
                voto_str = v.strip()
                if voto_str:
                    try:
                        voto = valida_voto(voto_str)
                        voti.append(voto)
                    except ValueError as e:
                        print(f"⚠️ Voto '{voto_str}' ignorato: {e}")
        except Exception as e:
            print(f"⚠️ Errore nel processare i voti: {e}")
            voti = []

    # Creazione e salvataggio nuovo studente
    nuovo_studente = StudentModel.create_student(matricola, nome, cognome, voti)
    studenti.append(nuovo_studente)

    if salva_studenti_su_file(percorso_file, studenti):
        if voti:
            print(f"\n✅ Studente {nome} {cognome} aggiunto con successo con {len(voti)} voti.")
        else:
            print(f"\n✅ Studente {nome} {cognome} aggiunto con successo (nessun voto iniziale).")
    else:
        print("❌ Errore nel salvataggio dello studente.")


def aggiungi_voto(percorso_file: str):
    """Aggiunge un voto a uno studente esistente."""
    studenti = leggi_studenti_da_file(percorso_file)

    if not studenti:
        print("❌ Nessuno studente presente nel registro.")
        return

    matricola_input = input("Inserisci il numero di matricola: ").strip()
    studente_trovato = StudentModel.find_student_by_matricola(studenti, matricola_input)

    if not studente_trovato:
        print(f"❌ Errore: Nessuno studente trovato con matricola {matricola_input}")
        return

    voto_input = input("Inserisci il nuovo voto: ").strip()
    try:
        voto = valida_voto(voto_input)
    except ValueError as e:
        print(f"❌ Errore: {e}")
        return

    studente_trovato.setdefault("voti", []).append(voto)

    if salva_studenti_su_file(percorso_file, studenti):
        print(f"✅ Voto {voto} aggiunto con successo a {studente_trovato['nome']} {studente_trovato['cognome']}.")
    else:
        print("❌ Errore nel salvataggio del voto.")


def cancella_studente(percorso_file: str):
    """Cancella uno studente esistente dal registro."""
    studenti = leggi_studenti_da_file(percorso_file)
    
    if not studenti:
        print("❌ Nessuno studente presente nel registro.")
        return
    
    matricola_input = input("Inserisci il numero di matricola dello studente da cancellare: ").strip()
    studente_trovato = StudentModel.find_student_by_matricola(studenti, matricola_input)
    
    if not studente_trovato:
        print(f"❌ Errore: Nessuno studente trovato con matricola {matricola_input}")
        return
    
    nome_completo = f"{studente_trovato.get('nome', 'N/D')} {studente_trovato.get('cognome', 'N/D')}"
    
    conferma = input(f"Sei sicuro di voler cancellare lo studente {nome_completo}? (s/n): ").strip().lower()
    if conferma != 's':
        print("Operazione annullata.")
        return
    
    studenti.remove(studente_trovato)

    if salva_studenti_su_file(percorso_file, studenti):
        print(f"✅ Studente {nome_completo} rimosso con successo dal registro.")
    else:
        print("❌ Errore nel salvataggio dopo la cancellazione.")


def stampa_voti_studente(percorso_file: str, matricola: str = None):
    """Stampa i voti di uno studente identificato dalla matricola."""
    studenti = leggi_studenti_da_file(percorso_file)
    
    if not studenti:
        print("❌ Nessuno studente presente nel registro.")
        return

    if matricola is None:
        matricola = input("Inserisci il numero di matricola: ").strip()
    
    studente_trovato = StudentModel.find_student_by_matricola(studenti, matricola)

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
