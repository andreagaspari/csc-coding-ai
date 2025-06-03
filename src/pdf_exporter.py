"""
Esportazione PDF per il registro studenti
========================================
Gestisce la creazione di report PDF.
"""

import os
from datetime import datetime
from typing import List, Dict
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from src.config import EXPORTS_DIR
from src.utils import calcola_media, genera_nome_file_timestamp


class PDFExporter:
    """Gestisce l'esportazione in PDF del registro studenti"""
    
    def __init__(self, output_dir: Path = None):
        """
        Inizializza l'esportatore PDF.
        
        Args:
            output_dir: Directory di output per i PDF
        """
        self.output_dir = output_dir or EXPORTS_DIR
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Configura gli stili personalizzati per il PDF"""
        # Stile per il titolo
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=20,
            spaceAfter=30,
            alignment=1,  # Centrato
            textColor=colors.darkblue
        )
        
        # Stile per i sottotitoli
        self.subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            textColor=colors.darkgreen
        )
    
    def esporta_lista_studenti(self, studenti: List[Dict], nome_file: str = None) -> Path:
        """
        Esporta la lista degli studenti in formato PDF.
        
        Args:
            studenti: Lista di studenti da esportare
            nome_file: Nome del file PDF (opzionale)
            
        Returns:
            Path: Percorso del file PDF creato
        """
        if nome_file is None:
            nome_file = genera_nome_file_timestamp("registro_studenti", "pdf")
        elif not nome_file.endswith('.pdf'):
            nome_file += '.pdf'
        
        file_path = self.output_dir / nome_file
        
        # Assicura che la directory esista
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Crea il documento PDF
        doc = SimpleDocTemplate(str(file_path), pagesize=A4)
        story = []
        
        # Titolo del documento
        title = Paragraph("📋 Registro Elettronico Studenti", self.title_style)
        story.append(title)
        
        # Data di generazione
        now = datetime.now()
        date_str = now.strftime("%d/%m/%Y alle %H:%M")
        subtitle = Paragraph(f"Generato il {date_str}", self.styles['Normal'])
        story.append(subtitle)
        story.append(Spacer(1, 20))
        
        if not studenti:
            # Se non ci sono studenti
            no_data = Paragraph("Nessuno studente presente nel registro.", self.styles['Normal'])
            story.append(no_data)
        else:
            # Crea la tabella degli studenti
            self._aggiungi_tabella_studenti(story, studenti)
            story.append(Spacer(1, 20))
            
            # Aggiungi statistiche
            self._aggiungi_statistiche(story, studenti)
        
        # Genera il PDF
        doc.build(story)
        
        return file_path
    
    def _aggiungi_tabella_studenti(self, story: List, studenti: List[Dict]):
        """Aggiunge la tabella degli studenti al PDF"""
        # Intestazioni della tabella
        headers = ['Matricola', 'Nome', 'Cognome', 'N° Voti', 'Media']
        
        # Dati della tabella
        table_data = [headers]
        
        for studente in studenti:
            matricola = studente.get('matricola', 'N/D')
            nome = studente.get('nome', 'N/D')
            cognome = studente.get('cognome', 'N/D')
            voti = studente.get('voti', [])
            num_voti = len(voti)
            media = calcola_media(voti)
            
            row = [
                matricola,
                nome,
                cognome,
                str(num_voti),
                f"{media:.2f}" if media > 0 else "N/D"
            ]
            table_data.append(row)
        
        # Crea la tabella
        table = Table(table_data, colWidths=[1.2*inch, 1.5*inch, 1.5*inch, 0.8*inch, 0.8*inch])
        
        # Stile della tabella
        table.setStyle(TableStyle([
            # Intestazione
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            
            # Contenuto
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            
            # Bordi
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            
            # Righe alternate
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ]))
        
        story.append(table)
    
    def _aggiungi_statistiche(self, story: List, studenti: List[Dict]):
        """Aggiunge le statistiche al PDF"""
        subtitle = Paragraph("📊 Statistiche Generali", self.subtitle_style)
        story.append(subtitle)
        
        # Calcola statistiche
        totale_studenti = len(studenti)
        studenti_con_voti = [s for s in studenti if s.get('voti', [])]
        studenti_senza_voti = totale_studenti - len(studenti_con_voti)
        
        stats_text = f"• Totale studenti: {totale_studenti}<br/>"
        stats_text += f"• Studenti con voti: {len(studenti_con_voti)}<br/>"
        stats_text += f"• Studenti senza voti: {studenti_senza_voti}<br/>"
        
        if studenti_con_voti:
            medie = [calcola_media(s.get('voti', [])) for s in studenti_con_voti]
            media_generale = sum(medie) / len(medie)
            media_massima = max(medie)
            media_minima = min(medie)
            
            # Trova il migliore studente
            migliore = max(studenti_con_voti, key=lambda s: calcola_media(s.get('voti', [])))
            nome_migliore = f"{migliore.get('nome', '')} {migliore.get('cognome', '')}"
            
            stats_text += f"• Media generale: {media_generale:.2f}<br/>"
            stats_text += f"• Media più alta: {media_massima:.2f}<br/>"
            stats_text += f"• Media più bassa: {media_minima:.2f}<br/>"
            stats_text += f"• Migliore studente: {nome_migliore}<br/>"
            
            # Studenti eccellenti (media >= 27)
            eccellenti = [s for s in studenti_con_voti if calcola_media(s.get('voti', [])) >= 27]
            stats_text += f"• Studenti eccellenti (≥27): {len(eccellenti)}"
        
        stats_paragraph = Paragraph(stats_text, self.styles['Normal'])
        story.append(stats_paragraph)


# Funzione di compatibilità con il codice esistente
def salva_lista_studenti_pdf(percorso_file: str, nome_file_pdf: str = None):
    """
    Funzione di compatibilità per salvare la lista studenti in PDF.
    
    Args:
        percorso_file: Percorso del file JSON con i dati
        nome_file_pdf: Nome del file PDF da creare
    """
    try:
        from src.data_manager import leggi_studenti_da_file
        
        # Leggi i dati degli studenti
        studenti = leggi_studenti_da_file(percorso_file)
        
        if not studenti:
            print("❌ Nessuno studente presente nel registro. Impossibile creare il PDF.")
            return
        
        # Crea l'esportatore
        exporter = PDFExporter()
        
        # Esporta in PDF
        file_path = exporter.esporta_lista_studenti(studenti, nome_file_pdf)
        
        print(f"✅ PDF creato con successo: {file_path}")
        print(f"📄 Contiene {len(studenti)} studenti")
        
        # Prova ad aprire il file (se su Linux/Mac)
        import subprocess
        import platform
        
        try:
            if platform.system() == "Linux":
                subprocess.run(["xdg-open", str(file_path)], check=False)
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", str(file_path)], check=False)
            elif platform.system() == "Windows":
                os.startfile(str(file_path))
        except Exception:
            pass  # Non bloccare se non riesce ad aprire il file
            
    except Exception as e:
        print(f"❌ Errore nella creazione del PDF: {e}")
