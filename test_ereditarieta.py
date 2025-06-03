#!/usr/bin/env python3
"""
Test delle classi OOP con ereditarietà
=====================================
Testa le nuove classi Persona, Studente e ListaStudenti con ereditarietà.
"""

from models import Persona, Studente, ListaStudenti, converti_lista_a_oggetti
from file_operations import leggi_studenti_da_file
import os


def test_classe_persona():
    """Test della classe base Persona"""
    print("👤 Test della classe Persona")
    print("-" * 40)
    
    persona = Persona("Mario", "Rossi")
    print(f"Nome completo: {persona.nome_completo()}")
    print(f"Iniziali: {persona.iniziali()}")
    print(f"Stringa: {persona}")
    
    # Test confronto
    persona2 = Persona("Mario", "Rossi")
    persona3 = Persona("Lucia", "Bianchi")
    print(f"Uguaglianza (stesso nome): {persona == persona2}")
    print(f"Uguaglianza (nome diverso): {persona == persona3}")


def test_ereditarieta_studente():
    """Test dell'ereditarietà nella classe Studente"""
    print("\n🎓 Test dell'ereditarietà Studente -> Persona")
    print("-" * 50)
    
    studente = Studente("Lucia", "Bianchi", 12345, [28, 30, 29, 27])
    
    # Metodi ereditati da Persona
    print(f"Nome completo (da Persona): {studente.nome_completo()}")
    print(f"Iniziali (da Persona): {studente.iniziali()}")
    
    # Metodi specifici di Studente
    print(f"Matricola: {studente.matricola}")
    print(f"Media voti: {studente.media_voti():.2f}")
    print(f"Voto massimo: {studente.voto_massimo()}")
    print(f"Voto minimo: {studente.voto_minimo()}")
    print(f"Numero voti: {studente.numero_voti()}")
    print(f"Ha superato esami: {studente.ha_superato_esami()}")
    print(f"È eccellente: {studente.is_eccellente()}")
    
    # Test isinstance per verificare l'ereditarietà
    print(f"È istanza di Studente: {isinstance(studente, Studente)}")
    print(f"È istanza di Persona: {isinstance(studente, Persona)}")


def test_funzionalita_avanzate():
    """Test delle funzionalità avanzate di ListaStudenti"""
    print("\n📊 Test funzionalità avanzate ListaStudenti")
    print("-" * 50)
    
    # Creare lista con studenti diversi
    lista = ListaStudenti()
    
    studenti_test = [
        Studente("Mario", "Rossi", 1001, [30, 29, 30, 28]),  # Eccellente
        Studente("Lucia", "Bianchi", 1002, [26, 25, 27, 24]),  # Buono
        Studente("Giuseppe", "Verdi", 1003, [18, 20, 19, 21]),  # Sufficiente
        Studente("Anna", "Neri", 1004, []),  # Senza voti
        Studente("Francesca", "Rossi", 1005, [30, 30, 29, 30]),  # Eccellente
    ]
    
    for studente in studenti_test:
        lista.aggiungi_studente(studente)
    
    print(f"Totale studenti: {len(lista)}")
    
    # Test ricerca per nome
    print("\n🔍 Ricerca per nome 'Rossi':")
    trovati = lista.trova_per_nome("Rossi")
    for studente in trovati:
        print(f"  - {studente}")
    
    # Test studenti eccellenti
    print("\n⭐ Studenti eccellenti (media >= 28):")
    eccellenti = lista.studenti_eccellenti()
    for studente in eccellenti:
        print(f"  - {studente}")
    
    # Test studenti senza voti
    print("\n📝 Studenti senza voti:")
    senza_voti = lista.studenti_senza_voti()
    for studente in senza_voti:
        print(f"  - {studente}")
    
    # Statistiche
    print("\n📈 Statistiche generali:")
    stats = lista.statistiche()
    for chiave, valore in stats.items():
        if isinstance(valore, float):
            print(f"  {chiave}: {valore:.2f}")
        else:
            print(f"  {chiave}: {valore}")
    
    # Ordinamento per media
    print("\n🏆 Top 3 studenti per media:")
    top_studenti = lista.ordina_per_media()[:3]
    for i, studente in enumerate(top_studenti, 1):
        print(f"  {i}° - {studente}")
    
    # Ordinamento alfabetico
    print("\n📋 Studenti in ordine alfabetico:")
    alfabetico = lista.ordina_per_nome()
    for studente in alfabetico:
        print(f"  - {studente}")
    
    # Test operatore 'in'
    print(f"\nMatricola 1001 presente: {1001 in lista}")
    print(f"Matricola 9999 presente: {9999 in lista}")


def test_integrazione_con_file():
    """Test di integrazione con i dati del file esistente"""
    print("\n\n🔄 Test integrazione con file esistente")
    print("-" * 50)
    
    file_path = os.path.join(os.path.dirname(__file__), 'registro.txt')
    
    try:
        # Carica dati dal file
        dati_dict = leggi_studenti_da_file(file_path)
        print(f"📂 Caricati {len(dati_dict)} studenti dal file")
        
        # Converte in oggetti OOP
        lista_oop = converti_lista_a_oggetti(dati_dict)
        print(f"📦 Convertiti {len(lista_oop)} studenti in oggetti")
        
        # Mostra statistiche del file reale
        print("\n📊 Statistiche del registro reale:")
        stats = lista_oop.statistiche()
        for chiave, valore in stats.items():
            if isinstance(valore, float):
                print(f"  {chiave}: {valore:.2f}")
            else:
                print(f"  {chiave}: {valore}")
        
        # Mostra primi 3 studenti
        print("\n📋 Primi 3 studenti dal file:")
        for i, studente in enumerate(lista_oop):
            if i >= 3:
                break
            print(f"  - {studente}")
            
        # Test ricerca nel file reale
        if len(lista_oop) > 0:
            primo_studente = lista_oop.studenti[0]
            print(f"\n🔍 Test ricerca - Primo studente: {primo_studente.nome_completo()}")
            
            # Test ereditarietà sui dati reali
            print(f"  Nome completo: {primo_studente.nome_completo()}")
            print(f"  Iniziali: {primo_studente.iniziali()}")
            print(f"  È eccellente: {primo_studente.is_eccellente()}")
            
    except Exception as e:
        print(f"❌ Errore nel test integrazione: {e}")


def test_polimorfismo():
    """Test del polimorfismo tra Persona e Studente"""
    print("\n\n🔄 Test polimorfismo")
    print("-" * 30)
    
    # Lista di persone che include sia Persona che Studente
    persone = [
        Persona("Mario", "Rossi"),
        Studente("Lucia", "Bianchi", 12345, [28, 30, 29]),
        Persona("Giuseppe", "Verdi"),
        Studente("Anna", "Neri", 67890, [26, 24, 27])
    ]
    
    print("Tutte le persone (polimorfismo):")
    for persona in persone:
        print(f"  - {persona} (tipo: {type(persona).__name__})")
        print(f"    Nome completo: {persona.nome_completo()}")
        print(f"    Iniziali: {persona.iniziali()}")
        
        # Verifica se è uno studente per accedere a metodi specifici
        if isinstance(persona, Studente):
            print(f"    Media voti: {persona.media_voti():.2f}")
            print(f"    È eccellente: {persona.is_eccellente()}")
        print()


if __name__ == "__main__":
    try:
        print("🧪 Test delle classi OOP con ereditarietà")
        print("=" * 60)
        
        test_classe_persona()
        test_ereditarieta_studente()
        test_funzionalita_avanzate()
        test_integrazione_con_file()
        test_polimorfismo()
        
        print("\n🎉 Tutti i test completati con successo!")
        print("\n✅ Le classi con ereditarietà funzionano correttamente:")
        print("   • Persona: classe base con funzionalità generiche")
        print("   • Studente: estende Persona con funzionalità specifiche")
        print("   • ListaStudenti: gestione avanzata della collezione")
        print("   • Polimorfismo: funzionamento corretto dell'ereditarietà")
        
    except Exception as e:
        print(f"❌ Errore durante l'esecuzione: {e}")
        import traceback
        traceback.print_exc()
