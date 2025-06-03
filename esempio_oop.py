#!/usr/bin/env python3
"""
Esempio di utilizzo delle classi Studente e ListaStudenti
========================================================
Dimostra come utilizzare le nuove classi orientate agli oggetti
per gestire il registro studenti.
"""

from models import Studente, ListaStudenti, converti_lista_a_oggetti, converti_oggetti_a_lista
from file_operations import leggi_studenti_da_file, salva_studenti_su_file
import os


def esempio_base():
    """Esempio base di utilizzo delle classi"""
    print("🎓 Esempio di utilizzo delle classi Studente e ListaStudenti")
    print("=" * 60)
    
    # Creare una lista di studenti
    lista = ListaStudenti()
    print(f"📋 Lista creata. Numero studenti: {len(lista)}")
    
    # Creare alcuni studenti
    studente1 = Studente("Mario", "Rossi", 12345, [24, 26, 28])
    studente2 = Studente("Lucia", "Bianchi", 67890, [30, 29, 28])
    studente3 = Studente("Giuseppe", "Verdi", 11111)  # Senza voti iniziali
    
    # Aggiungere studenti alla lista
    print("\n➕ Aggiunta studenti...")
    print(f"Aggiunto Mario: {lista.aggiungi_studente(studente1)}")
    print(f"Aggiunto Lucia: {lista.aggiungi_studente(studente2)}")
    print(f"Aggiunto Giuseppe: {lista.aggiungi_studente(studente3)}")
    
    # Tentativo di aggiungere studente con matricola duplicata
    studente_duplicato = Studente("Anna", "Neri", 12345)
    print(f"Tentativo duplicato (matricola 12345): {lista.aggiungi_studente(studente_duplicato)}")
    
    print(f"\n📊 Numero totale studenti: {len(lista)}")
    
    # Mostrare tutti gli studenti
    print("\n📋 Lista completa studenti:")
    for studente in lista:
        print(f"  {studente}")
    
    # Cercare uno studente
    print("\n🔍 Ricerca studente con matricola 67890:")
    studente_trovato = lista.trova_studente(67890)
    if studente_trovato:
        print(f"  Trovato: {studente_trovato}")
        print(f"  Media voti: {studente_trovato.media_voti():.2f}")
    
    # Aggiungere un voto
    print("\n📝 Aggiunta voto a Giuseppe (matricola 11111):")
    giuseppe = lista.trova_studente(11111)
    if giuseppe:
        print(f"  Voti prima: {giuseppe.voti}")
        giuseppe.aggiungi_voto(27)
        giuseppe.aggiungi_voto(25)
        giuseppe.aggiungi_voto(35)  # Voto non valido
        print(f"  Voti dopo: {giuseppe.voti}")
        print(f"  Nuova media: {giuseppe.media_voti():.2f}")
    
    # Rimuovere uno studente
    print("\n🗑️ Rimozione studente con matricola 11111:")
    rimosso = lista.rimuovi_studente(11111)
    print(f"  Studente rimosso: {rimosso}")
    print(f"  Numero studenti rimasti: {len(lista)}")
    
    return lista


def esempio_integrazione_file():
    """Esempio di integrazione con il sistema di file esistente"""
    print("\n\n🔄 Esempio di integrazione con file esistente")
    print("=" * 60)
    
    # Percorso del file di registro
    file_path = os.path.join(os.path.dirname(__file__), 'registro.txt')
    
    # Leggere dati esistenti dal file
    print("📂 Caricamento dati dal file registro.txt...")
    dati_dict = leggi_studenti_da_file(file_path)
    print(f"   Caricati {len(dati_dict)} studenti dal file")
    
    # Convertire in oggetti
    lista_oop = converti_lista_a_oggetti(dati_dict)
    print(f"📦 Convertiti in oggetti: {len(lista_oop)} studenti")
    
    # Mostrare alcuni studenti come oggetti
    print("\n📋 Primi 3 studenti come oggetti:")
    for i, studente in enumerate(lista_oop):
        if i >= 3:
            break
        print(f"  {studente}")
    
    # Aggiungere un nuovo studente usando le classi
    print("\n➕ Aggiunta nuovo studente usando le classi...")
    nuovo_studente = Studente("Test", "Studente", 99999, [26, 28, 30])
    if lista_oop.aggiungi_studente(nuovo_studente):
        print(f"   Aggiunto: {nuovo_studente}")
    else:
        print("   Studente già esistente o errore")
    
    # Convertire di nuovo in formato dizionario
    dati_aggiornati = converti_oggetti_a_lista(lista_oop)
    
    # Salvare nel file (opzionale - commentato per sicurezza)
    # print("\n💾 Salvataggio dati aggiornati...")
    # if salva_studenti_su_file(file_path, dati_aggiornati):
    #     print("   Dati salvati con successo")
    # else:
    #     print("   Errore nel salvataggio")
    
    print(f"\n✅ Esempio completato. Lista finale: {len(lista_oop)} studenti")
    return lista_oop


def esempio_operazioni_avanzate():
    """Esempio di operazioni avanzate con le classi"""
    print("\n\n⚡ Operazioni avanzate")
    print("=" * 60)
    
    # Creare lista con diversi tipi di studenti
    lista = ListaStudenti()
    
    # Studenti con situazioni diverse
    studenti_test = [
        Studente("Eccellente", "Studente", 1001, [30, 30, 29, 30]),
        Studente("Bravo", "Studente", 1002, [28, 27, 29, 26]),
        Studente("Sufficiente", "Studente", 1003, [18, 20, 19, 21]),
        Studente("Senza", "Voti", 1004, []),
    ]
    
    for studente in studenti_test:
        lista.aggiungi_studente(studente)
    
    print("📊 Analisi statistiche:")
    print(f"   Totale studenti: {len(lista)}")
    
    # Calcolare statistiche
    medie = [s.media_voti() for s in lista if s.voti]
    if medie:
        print(f"   Media generale: {sum(medie) / len(medie):.2f}")
        print(f"   Media più alta: {max(medie):.2f}")
        print(f"   Media più bassa: {min(medie):.2f}")
    
    # Studenti per categoria
    studenti_con_voti = [s for s in lista if s.voti]
    studenti_senza_voti = [s for s in lista if not s.voti]
    
    print(f"   Studenti con voti: {len(studenti_con_voti)}")
    print(f"   Studenti senza voti: {len(studenti_senza_voti)}")
    
    # Trovare il migliore studente
    if studenti_con_voti:
        migliore = max(studenti_con_voti, key=lambda s: s.media_voti())
        print(f"   Migliore studente: {migliore}")


if __name__ == "__main__":
    try:
        # Eseguire tutti gli esempi
        lista1 = esempio_base()
        lista2 = esempio_integrazione_file()
        esempio_operazioni_avanzate()
        
        print("\n🎉 Tutti gli esempi completati con successo!")
        print("\n💡 Le classi Studente e ListaStudenti sono ora pronte per l'uso!")
        print("   È possibile integrarle gradualmente nel codice esistente.")
        
    except Exception as e:
        print(f"❌ Errore durante l'esecuzione degli esempi: {e}")
        import traceback
        traceback.print_exc()
