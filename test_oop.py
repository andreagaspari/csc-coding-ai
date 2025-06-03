#!/usr/bin/env python3
# Test semplice delle classi OOP

import sys
import os

# Aggiungi la directory corrente al path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from models import Studente, ListaStudenti
    
    print("🎓 Test Classi OOP - Sistema Registro Studenti")
    print("=" * 50)
    
    # Test 1: Creazione studente
    print("\n1️⃣ Test creazione studente:")
    studente1 = Studente("Mario", "Rossi", 12345, [24, 26, 28])
    print(f"   Creato: {studente1}")
    print(f"   Media: {studente1.media_voti():.2f}")
    
    # Test 2: Aggiunta voto
    print("\n2️⃣ Test aggiunta voto:")
    print(f"   Voti prima: {studente1.voti}")
    risultato = studente1.aggiungi_voto(30)
    print(f"   Aggiunto voto 30: {risultato}")
    risultato = studente1.aggiungi_voto(35)  # Voto non valido
    print(f"   Tentativo voto 35: {risultato}")
    print(f"   Voti dopo: {studente1.voti}")
    print(f"   Nuova media: {studente1.media_voti():.2f}")
    
    # Test 3: Lista studenti
    print("\n3️⃣ Test lista studenti:")
    lista = ListaStudenti()
    studente2 = Studente("Lucia", "Bianchi", 67890, [28, 30])
    studente3 = Studente("Giuseppe", "Verdi", 11111)
    
    print(f"   Aggiunto Mario: {lista.aggiungi_studente(studente1)}")
    print(f"   Aggiunto Lucia: {lista.aggiungi_studente(studente2)}")
    print(f"   Aggiunto Giuseppe: {lista.aggiungi_studente(studente3)}")
    
    # Tentativo duplicato
    studente_dup = Studente("Anna", "Neri", 12345)
    print(f"   Tentativo duplicato (12345): {lista.aggiungi_studente(studente_dup)}")
    
    print(f"   Totale studenti: {len(lista)}")
    
    # Test 4: Ricerca
    print("\n4️⃣ Test ricerca studente:")
    trovato = lista.trova_studente(67890)
    if trovato:
        print(f"   Trovato: {trovato}")
    else:
        print("   Studente non trovato")
    
    # Test 5: Conversione
    print("\n5️⃣ Test conversione:")
    dict_list = lista.to_dict_list()
    print(f"   Convertiti {len(dict_list)} studenti in dizionari")
    print(f"   Primo studente come dict: {dict_list[0]}")
    
    # Test 6: Iterazione
    print("\n6️⃣ Test iterazione:")
    print("   Lista completa:")
    for i, studente in enumerate(lista, 1):
        print(f"     {i}. {studente}")
    
    print("\n✅ Tutti i test completati con successo!")
    print("🎉 Le classi OOP sono funzionanti!")
    
except Exception as e:
    print(f"❌ Errore durante i test: {e}")
    import traceback
    traceback.print_exc()
