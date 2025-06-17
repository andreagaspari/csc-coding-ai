# ui_tkinter.py
# Interfaccia grafica per il quiz usando tkinter
import tkinter as tk
from tkinter import messagebox

class QuizUI:
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.root.title('Quiz')
        self.root.geometry('400x600')
        self.current_frame = None
        self.show_home()

    def clear_frame(self):
        # Ferma qualsiasi timer attivo prima di cancellare il frame
        self.stop_timer()
        
        if self.current_frame:
            # Rimuovi tutti i widget figlio prima di distruggere il frame
            for widget in self.current_frame.winfo_children():
                widget.destroy()
            self.current_frame.destroy()
            self.current_frame = None

    def show_home(self):
        self.clear_frame()
        frame = tk.Frame(self.root)
        frame.pack(expand=True, fill='both')
        tk.Label(frame, text='BENVENUTO AL QUIZ', font=('Arial', 20)).pack(pady=30)
        tk.Label(frame, text='SCEGLI LA DIFFICOLTÀ', font=('Arial', 14)).pack(pady=10)
        btn_frame = tk.Frame(frame)
        btn_frame.pack(pady=30)
        tk.Button(btn_frame, text='FACILE', width=10, height=2, command=lambda: self.controller.start_quiz('facile')).pack(side='left', padx=10)
        tk.Button(btn_frame, text='MEDIO', width=10, height=2, command=lambda: self.controller.start_quiz('medio')).pack(side='left', padx=10)
        tk.Button(btn_frame, text='DIFFICILE', width=10, height=2, command=lambda: self.controller.start_quiz('difficile')).pack(side='left', padx=10)
        self.current_frame = frame

    def show_question(self, domanda, risposte, punteggio, tempo, on_risposta, on_salta, on_exit):
        # Prima di tutto, fermiamo il timer precedente se esiste
        self.stop_timer()
        
        self.clear_frame()
        frame = tk.Frame(self.root)
        frame.pack(expand=True, fill='both')
        top_frame = tk.Frame(frame)
        top_frame.pack(fill='x', pady=5)
        tk.Button(top_frame, text='ESCI', command=on_exit).pack(side='left', padx=5)
        tk.Label(top_frame, text=f'Punteggio: {punteggio}', font=('Arial', 12)).pack(side='right', padx=5)
        
        # Timer frame con barra colorata e testo in sovraimpressione
        timer_frame = tk.Frame(frame)
        timer_frame.pack(fill='x', padx=20, pady=5)
        
        # Canvas per il timer con altezza aumentata
        timer_bar = tk.Canvas(timer_frame, height=30, bg='white')
        timer_bar.pack(fill='x')
        
        # Crea rettangolo verde e testo in sovraimpressione
        bar = timer_bar.create_rectangle(0, 0, 400, 30, fill='green')
        self.timer_text = timer_bar.create_text(200, 15, text=f'{tempo}s', fill='black', 
                                               font=('Arial', 12, 'bold'))
        
        tk.Label(frame, text=domanda, font=('Arial', 14), wraplength=350).pack(pady=10)
        btns = []
        for idx, risposta in enumerate(risposte):
            b = tk.Button(frame, text=risposta, width=30, height=2, 
                          command=lambda i=idx, btn=btns: self._handle_answer(on_risposta, i))
            b.pack(pady=5)
            btns.append(b)
        skip_btn = tk.Button(frame, text='SALTA', command=lambda: self._handle_skip(on_salta))
        skip_btn.pack(pady=15)
        self.current_frame = frame

        # Timer animato
        self._timer_running = True
        self._timer_elapsed = 0
        self._timer_update(timer_bar, bar, tempo, on_salta, btns, skip_btn)

    def _timer_update(self, timer_bar, bar, tempo, on_salta, btns, skip_btn):
        if not hasattr(self, '_timer_running') or not self._timer_running:
            return
        
        # Verifica se il widget esiste ancora
        try:
            if not timer_bar.winfo_exists():
                self._timer_running = False
                return
        except:
            self._timer_running = False
            return
            
        max_width = 400
        interval = 100  # ms
        if self._timer_elapsed >= tempo:
            self._timer_running = False
            for b in btns:
                try:
                    b.config(state='disabled')
                except:
                    pass
            try:
                skip_btn.config(state='disabled')
            except:
                pass
            on_salta()
            return
        
        # Calcola la percentuale di tempo rimanente e il colore corrispondente
        percentuale = 1 - (self._timer_elapsed / tempo)
        width = int(max_width * percentuale)
        secondi_rimasti = int(tempo - self._timer_elapsed)
        
        # Scegli il colore in base al tempo rimanente
        if percentuale > 0.60:  # Più del 60% del tempo rimanente: verde
            color = "green"
        elif percentuale > 0.30:  # Tra 30% e 60% del tempo rimanente: giallo
            color = "yellow"
        else:  # Meno del 30% del tempo rimanente: rosso
            color = "red"
        
        try:
            # Aggiorna la barra di tempo: dimensione e colore
            timer_bar.coords(bar, 0, 0, width, 30)
            timer_bar.itemconfig(bar, fill=color)
            
            # Aggiorna il testo al centro della barra
            timer_bar.itemconfig(self.timer_text, text=f'{secondi_rimasti}s')
            
            self._timer_elapsed += interval / 1000
            self._timer_job = self.root.after(interval, self._timer_update, timer_bar, bar, tempo, on_salta, btns, skip_btn)
        except:
            self._timer_running = False

    def _handle_answer(self, on_risposta, idx):
        self.stop_timer()
        on_risposta(idx)
        
    def _handle_skip(self, on_salta):
        self.stop_timer()
        on_salta()

    def stop_timer(self):
        self._timer_running = False
        if hasattr(self, '_timer_job'):
            try:
                self.root.after_cancel(self._timer_job)
            except:
                pass

    def show_recap(self, punteggio, dettagli, on_save, on_exit, on_resume):
        self.clear_frame()
        frame = tk.Frame(self.root, bg='white')
        frame.pack(expand=True, fill='both')
        
        # Titolo
        tk.Label(frame, text='IL TUO PUNTEGGIO', font=('Arial', 16, 'bold'), bg='white').pack(pady=20)
        
        # Punteggio grande
        tk.Label(frame, text=str(punteggio), font=('Arial', 32, 'bold'), bg='white').pack(pady=10)
        
        # Statistiche con icone
        stats_frame = tk.Frame(frame, bg='white')
        stats_frame.pack(pady=10)
        
        # Estrai i numeri dal dettaglio
        import re
        numeri = re.findall(r'\d+', dettagli)
        if len(numeri) >= 3:
            corrette = int(numeri[0])
            errate = int(numeri[1])
            saltate = int(numeri[2])
            
            # Mostra statistiche con icone
            tk.Label(stats_frame, text="✓", font=('Arial', 14), fg='green', bg='white').grid(row=0, column=0, padx=5)
            tk.Label(stats_frame, text=str(corrette), font=('Arial', 12), bg='white').grid(row=0, column=1, padx=5)
            
            tk.Label(stats_frame, text="✗", font=('Arial', 14), fg='red', bg='white').grid(row=0, column=2, padx=5)
            tk.Label(stats_frame, text=str(errate), font=('Arial', 12), bg='white').grid(row=0, column=3, padx=5)
            
            tk.Label(stats_frame, text="→", font=('Arial', 14), fg='blue', bg='white').grid(row=0, column=4, padx=5)
            tk.Label(stats_frame, text=str(saltate), font=('Arial', 12), bg='white').grid(row=0, column=5, padx=5)
        
        # Label con istruzioni per le iniziali
        tk.Label(frame, text="Inserisci le tue iniziali (3 lettere):", font=('Arial', 12), bg='white').pack(pady=(20, 5))
        
        # Frame con trattini
        mask_frame = tk.Frame(frame, bg='white')
        mask_frame.pack(pady=5)
        
        # Crea tre Entry box da un carattere, simili a trattini
        entries = []
        for i in range(3):
            e = tk.Entry(mask_frame, width=2, font=('Arial', 12), justify='center')
            e.grid(row=0, column=i, padx=5)
            e.config(highlightthickness=0, bd=0, bg='white')
            # Disegna un trattino sotto ogni casella
            underscore = tk.Label(mask_frame, text="__", font=('Arial', 12), bg='white')
            underscore.grid(row=1, column=i, padx=5)
            entries.append(e)
            
            # Aggiungi validazione per permettere solo lettere
            e.bind('<KeyRelease>', lambda event, idx=i, ent=entries: self._validate_letter(event, idx, entries))
        
        # Metti il focus sulla prima casella
        entries[0].focus_set()
        
        # Bottoni per salvare, uscire o riprendere
        tk.Button(frame, text='Salva il tuo risultato', 
                  command=lambda: on_save(''.join([e.get().upper() for e in entries])),
                  width=20).pack(pady=10)
        
        btn_frame = tk.Frame(frame, bg='white')
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text='ESCI', width=10, command=on_exit).pack(side='left', padx=10)
        tk.Button(btn_frame, text='RIPRENDI', width=10, command=on_resume).pack(side='left', padx=10)
        
        self.current_frame = frame

    def _validate_letter(self, event, idx, entries):
        """Valida l'input per accettare solo lettere e gestisce il passaggio tra campi"""
        entry = event.widget
        c = entry.get()
        
        # Mantiene solo lettere (e un carattere alla volta)
        if c and (not c.isalpha() or len(c) > 1):
            entry.delete(0, tk.END)
            entry.insert(0, c[-1] if c and c[-1].isalpha() else '')
        
        # Converti automaticamente in maiuscolo
        if c and c.isalpha():
            entry.delete(0, tk.END)
            entry.insert(0, c.upper())
        
        # Passa al campo successivo se ne ho inserito uno
        if c and idx < len(entries) - 1:
            entries[idx + 1].focus_set()

    def run(self):
        self.root.mainloop()
