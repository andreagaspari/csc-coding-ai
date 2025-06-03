"""
Esportazione PDF per il registro studenti
========================================
Gestisce la creazione di report PDF.
"""

import os
from datetime import datetime
from typing import List, Dict
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from utils import calcola_media
from file_operations import leggi_studenti_da_file


def salva_lista_studenti_pdf(percorso_file: str, nome_file_pdf: str = None):
    """
    Salva la lista degli studenti in formato PDF con una tabella formattata.
    
    Args:
        percorso_file: Percorso completo del file JSON dei dati
        nome_file_pdf: Nome del file PDF da creare (opzionale)
    """
    studenti = leggi_studenti_da_file(percorso_file)
    
    if not studenti:
        print("❌ Nessuno studente presente nel registro. Impossibile creare il PDF.")
        return
    
    if nome_file_pdf is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_file_pdf = f"registro_studenti_{timestamp}.pdf"
    
    if not nome_file_pdf.endswith('.pdf'):
        nome_file_pdf += '.pdf'
    
    cartella_file = os.path.dirname(percorso_file)
    percorso_pdf = os.path.join(cartella_file, nome_file_pdf)
    
    try:
        doc = SimpleDocDocument(percorso_pdf, pagesize=A4)
        elements = []
        
        # Stili
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=1
        )
        
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Normal'],
            fontSize=12,
            spaceAfter=20,
            alignment=1
        )
        
        # Titolo e data
        title = Paragraph("📋 Registro Elettronico Studenti", title_style)
        elements.append(title)
        
        data_creazione = datetime.now().strftime("%d/%m/%Y alle %H:%M")
        subtitle = Paragraph(f"Generato il {data_creazione}", subtitle_style)
        elements.append(subtitle)
        elements.append(Spacer(1, 20))
        
        # Dati tabella
        data = [['Matricola', 'Nome', 'Cognome', 'N° Voti', 'Media']]
        
        for studente in studenti:
            matricola = studente.get("matricola", "N/D")
            nome = studente.get("nome", "N/D")
            cognome = studente.get("cognome", "N/D")
            voti = studente.get("voti", [])
            num_voti = len(voti)
            media = calcola_media(voti)
            
            data.append([
                matricola, nome, cognome, str(num_voti), f"{media:.2f}"
            ])
        
        # Tabella
        table = Table(data, colWidths=[1.2*inch, 1.5*inch, 1.5*inch, 0.8*inch, 0.8*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.beige, colors.lightgrey]),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 30))
        
        # Statistiche
        total_studenti = len(studenti)
        studenti_con_voti = len([s for s in studenti if s.get("voti", [])])
        media_generale = calcola_media([v for s in studenti for v in s.get("voti", [])])
        
        stats_style = ParagraphStyle('Stats', parent=styles['Normal'], fontSize=10, spaceAfter=10)
        stats_text = f"""
        <b>Statistiche Generali:</b><br/>
        • Totale studenti: {total_studenti}<br/>
        • Studenti con voti: {studenti_con_voti}<br/>
        • Media generale: {media_generale:.2f}<br/>
        """
        
        stats = Paragraph(stats_text, stats_style)
        elements.append(stats)
        
        doc.build(elements)
        
        print(f"✅ Lista studenti salvata con successo in: {percorso_pdf}")
        print(f"📊 {total_studenti} studenti esportati nel PDF")
        
    except Exception as e:
        print(f"❌ Errore durante la creazione del PDF: {e}")
