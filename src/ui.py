"""
Interfaccia utente per il registro studenti
==========================================
Gestisce l'interfaccia a menu e l'interazione con l'utente.
"""

from typing import List
from src.data_manager import FileManager
from src.student_service import StudentService, stampa_studenti, stampa_voti_studente
from src.pdf_exporter import PDFExporter
from src.utils import valida_voto, valida_matricola, valida_nome
from src.config import DEFAULT_DATA_PATH


class MenuUI:
    """Interfaccia utente a menu per il registro studenti"""
    
    def __init__(self, data_file_path: str = None):
        """
        Inizializza l'interfaccia utente.
        
        Args:
            data_file_path: Percorso del file dati (opzionale)
        """
        if data_file_path:
            from pathlib import Path
            self.file_manager = FileManager(Path(data_file_path))
        else:
            self.file_manager = FileManager()
        
        self.student_service = StudentService(self.file_manager)
        self.pdf_exporter = PDFExporter()
    
    def mostra_menu(self):
        """Visualizza il menu delle opzioni disponibili"""
        print("\nCosa vuoi fare?")
        print("[1] 📋 Stampa lista studenti")
        print("[2] ➕ Aggiungi studente")
        print("[3] 📝 Aggiungi voto")
        print("[4] 🗑️  Cancella studente")
        print("[5] 📊 Visualizza voti di uno studente")
        print("[6] 📥 Esporta lista studenti in PDF")
        print("[7] 📈 Visualizza statistiche")
        print("[8] 🔍 Cerca studente per nome")
        print("[0] 👋 Esci")
    
    def esegui_menu_principale(self):
        """Esegue il loop principale del menu"""
        print("🎓 Benvenuto nel Sistema di Gestione Registro Studenti")
        print("=" * 55)
        
        while True:
            try:
                self.mostra_menu()
                scelta = input("Scelta: ").strip()

                if scelta == "1":
                    self._visualizza_lista_studenti()
                elif scelta == "2":
                    self._aggiungi_studente()
                elif scelta == "3":
                    self._aggiungi_voto()
                elif scelta == "4":
                    self._cancella_studente()
                elif scelta == "5":
                    self._stampa_voti_studente()
                elif scelta == "6":
                    self._esporta_pdf()
                elif scelta == "7":
                    self._visualizza_statistiche()
                elif scelta == "8":
                    self._cerca_studente()
                elif scelta == "0":
                    print("👋 Grazie per aver usato il Sistema di Gestione Registro Studenti!")
                    break
                else:
                    print("⚠️ Scelta non valida. Riprova.")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Uscita forzata. Arrivederci!")
                break
            except Exception as e:
                print(f"❌ Errore inaspettato: {e}")
                print("🔄 Riprova con un'operazione diversa.")
    
    def _visualizza_lista_studenti(self):
        """Visualizza la lista di tutti gli studenti"""
        try:
            studenti = self.student_service.ottieni_tutti_studenti()
            
            if not studenti:
                print("\n📋 Nessuno studente presente nel registro.")
                return
            
            # Converti in formato dizionario per compatibilità
            studenti_dict = [s.to_dict() for s in studenti]
            stampa_studenti(studenti_dict)
            
        except Exception as e:
            print(f"❌ Errore nella visualizzazione degli studenti: {e}")
    
    def _aggiungi_studente(self):
        """Aggiunge un nuovo studente"""
        try:
            print("\n➕ Aggiunta nuovo studente")
            print("-" * 30)
            
            # Richiesta matricola unica
            while True:
                matricola = input("Numero di matricola: ").strip()
                try:
                    valida_matricola(matricola)
                    if not self.student_service.trova_studente_per_matricola(matricola):
                        break
                    print(f"⚠️ La matricola {matricola} esiste già. Inserisci una matricola diversa.")
                except ValueError as e:
                    print(f"⚠️ {e}")

            # Richiesta nome obbligatorio
            while True:
                nome = input("Nome: ").strip()
                try:
                    nome = valida_nome(nome)
                    break
                except ValueError as e:
                    print(f"⚠️ {e}")

            # Richiesta cognome obbligatorio
            while True:
                cognome = input("Cognome: ").strip()
                try:
                    cognome = valida_nome(cognome)
                    break
                except ValueError as e:
                    print(f"⚠️ {e}")

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

            # Aggiunge lo studente
            if self.student_service.aggiungi_studente(matricola, nome, cognome, voti):
                if voti:
                    print(f"\n✅ Studente {nome} {cognome} aggiunto con successo con {len(voti)} voti.")
                else:
                    print(f"\n✅ Studente {nome} {cognome} aggiunto con successo (nessun voto iniziale).")
            else:
                print("❌ Errore nell'aggiunta dello studente.")
                
        except Exception as e:
            print(f"❌ Errore nell'aggiunta dello studente: {e}")
    
    def _aggiungi_voto(self):
        """Aggiunge un voto a uno studente esistente"""
        try:
            studenti = self.student_service.ottieni_tutti_studenti()

            if not studenti:
                print("❌ Nessuno studente presente nel registro.")
                return

            matricola_input = input("Inserisci il numero di matricola: ").strip()
            studente = self.student_service.trova_studente_per_matricola(matricola_input)

            if not studente:
                print(f"❌ Errore: Nessuno studente trovato con matricola {matricola_input}")
                return

            voto_input = input("Inserisci il nuovo voto: ").strip()
            
            if self.student_service.aggiungi_voto_studente(matricola_input, voto_input):
                voto_valido = valida_voto(voto_input)
                print(f"✅ Voto {voto_valido} aggiunto con successo a {studente.nome} {studente.cognome}.")
            else:
                print("❌ Errore nell'aggiunta del voto.")
                
        except ValueError as e:
            print(f"❌ Errore: {e}")
        except Exception as e:
            print(f"❌ Errore nell'aggiunta del voto: {e}")
    
    def _cancella_studente(self):
        """Cancella uno studente esistente dal registro"""
        try:
            studenti = self.student_service.ottieni_tutti_studenti()
            
            if not studenti:
                print("❌ Nessuno studente presente nel registro.")
                return
            
            matricola_input = input("Inserisci il numero di matricola dello studente da cancellare: ").strip()
            studente = self.student_service.trova_studente_per_matricola(matricola_input)
            
            if not studente:
                print(f"❌ Errore: Nessuno studente trovato con matricola {matricola_input}")
                return
            
            nome_completo = studente.nome_completo()
            
            conferma = input(f"Sei sicuro di voler cancellare lo studente {nome_completo}? (s/n): ").strip().lower()
            if conferma != 's':
                print("Operazione annullata.")
                return
            
            if self.student_service.rimuovi_studente(matricola_input):
                print(f"✅ Studente {nome_completo} rimosso con successo dal registro.")
            else:
                print("❌ Errore nella cancellazione dello studente.")
                
        except Exception as e:
            print(f"❌ Errore nella cancellazione dello studente: {e}")
    
    def _stampa_voti_studente(self):
        """Stampa i voti di uno studente specifico"""
        try:
            studenti = self.student_service.ottieni_tutti_studenti()
            
            if not studenti:
                print("❌ Nessuno studente presente nel registro.")
                return
            
            matricola_input = input("Inserisci il numero di matricola: ").strip()
            
            # Converti in formato dizionario per compatibilità
            studenti_dict = [s.to_dict() for s in studenti]
            stampa_voti_studente(studenti_dict, matricola_input)
            
        except Exception as e:
            print(f"❌ Errore nella visualizzazione dei voti: {e}")
    
    def _esporta_pdf(self):
        """Esporta la lista studenti in PDF"""
        try:
            studenti = self.student_service.ottieni_tutti_studenti()
            
            if not studenti:
                print("❌ Nessuno studente presente nel registro. Impossibile creare il PDF.")
                return
            
            nome_file = input("Inserisci il nome del file PDF (o premi INVIO per nome predefinito): ").strip() or None
            
            # Converti in formato dizionario
            studenti_dict = [s.to_dict() for s in studenti]
            
            # Esporta
            file_path = self.pdf_exporter.esporta_lista_studenti(studenti_dict, nome_file)
            
            print(f"✅ PDF creato con successo: {file_path}")
            print(f"📄 Contiene {len(studenti)} studenti")
            
        except Exception as e:
            print(f"❌ Errore nella creazione del PDF: {e}")
    
    def _visualizza_statistiche(self):
        """Visualizza le statistiche del registro"""
        try:
            stats = self.student_service.ottieni_statistiche()
            
            print("\n📈 Statistiche del Registro")
            print("-" * 40)
            print(f"📊 Totale studenti: {stats['totale_studenti']}")
            print(f"📝 Studenti con voti: {stats['studenti_con_voti']}")
            print(f"📋 Studenti senza voti: {stats['studenti_senza_voti']}")
            print(f"🌟 Studenti eccellenti: {stats['studenti_eccellenti']}")
            
            if stats['studenti_con_voti'] > 0:
                print(f"📊 Media generale: {stats['media_generale']:.2f}")
                print(f"🏆 Media più alta: {stats['media_più_alta']:.2f}")
                print(f"📉 Media più bassa: {stats['media_più_bassa']:.2f}")
                print(f"👨‍🎓 Migliore studente: {stats['migliore_studente']}")
            
        except Exception as e:
            print(f"❌ Errore nella visualizzazione delle statistiche: {e}")
    
    def _cerca_studente(self):
        """Cerca studenti per nome/cognome"""
        try:
            nome = input("Inserisci il nome da cercare: ").strip()
            if not nome:
                print("⚠️ Il nome non può essere vuoto.")
                return
            
            cognome = input("Inserisci il cognome da cercare (opzionale): ").strip() or None
            
            studenti_trovati = self.student_service.cerca_studenti_per_nome(nome, cognome)
            
            if not studenti_trovati:
                print("❌ Nessuno studente trovato con i criteri specificati.")
                return
            
            print(f"\n🔍 Trovati {len(studenti_trovati)} studenti:")
            print("-" * 50)
            
            for studente in studenti_trovati:
                print(f"  {studente}")
            
        except Exception as e:
            print(f"❌ Errore nella ricerca: {e}")


# Funzioni di compatibilità con il codice esistente
def mostra_menu():
    """Funzione di compatibilità per mostrare il menu"""
    menu = MenuUI()
    menu.mostra_menu()


def esegui_menu_principale(file_path: str):
    """
    Funzione di compatibilità per eseguire il menu principale.
    
    Args:
        file_path: Percorso del file dati
    """
    menu = MenuUI(file_path)
    menu.esegui_menu_principale()
