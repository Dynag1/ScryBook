import os
import sqlite3
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
import tkinter as tk
from tkinter import filedialog
import src.var as var
import src.fct_main as fct_main

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for i, state in enumerate(self._saved_page_states):
            self.__dict__.update(state)
            self.draw_page_number(i + 1, num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_num, total_pages):
        if page_num > 2:  # Ne pas numéroter les deux premières pages
            self.setFont("Helvetica", 9)
            self.drawRightString(20*cm, 1*cm, f"{page_num - 2}")

class MyDocTemplate(SimpleDocTemplate):
    def __init__(self, *args, **kwargs):
        SimpleDocTemplate.__init__(self, *args, **kwargs)
        self.toc = TableOfContents()
        self.toc.levelStyles = [
            ParagraphStyle(name='TOCHeading1', fontSize=14, leading=16, firstLineIndent=0,
                           leftIndent=0, rightIndent=0, spaceBefore=5, spaceAfter=5,
                           endDots='.', dottedWidth=0.5*cm),
            ParagraphStyle(name='TOCHeading2', fontSize=12, leading=14, firstLineIndent=0.5*cm,
                           leftIndent=0.5*cm, rightIndent=0, spaceBefore=2, spaceAfter=2,
                           endDots='.', dottedWidth=0.5*cm)
        ]

    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph):
            text = flowable.getPlainText()
            style = flowable.style.name
            if style == 'CenteredChapterTitle':
                self.notify('TOCEntry', (0, text, self.page))
            elif style == 'Subtitle':
                self.notify('TOCEntry', (1, text, self.page))

def create_pdf(input_files, output_file, title):
    doc = MyDocTemplate(output_file, pagesize=A4,
                        leftMargin=2*cm, rightMargin=2*cm,
                        topMargin=2*cm, bottomMargin=2*cm)
    elements = []

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))

    title_style = ParagraphStyle(name='CenteredTitle', parent=styles['Title'],
                                 alignment=TA_CENTER,
                                 fontSize=24,
                                 spaceAfter=30)

    chapter_title_style = ParagraphStyle(name='CenteredChapterTitle', parent=styles['Heading1'],
                                         alignment=TA_CENTER,
                                         fontSize=18,
                                         spaceAfter=12)

    subtitle_style = ParagraphStyle(name='Subtitle', parent=styles['Heading2'],
                                    fontSize=14,
                                    spaceAfter=6)

    # Page de titre
    elements.append(Paragraph(title, title_style))
    elements.append(PageBreak())

    # Sommaire
    elements.append(Paragraph("Sommaire", title_style))
    elements.append(doc.toc)
    elements.append(PageBreak())

    # Contenu des chapitres
    for input_file, chapter_title in input_files:
        elements.append(Paragraph(chapter_title, chapter_title_style))
        elements.append(Spacer(1, 12))

        with open(input_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        for line in lines:
            if line.strip():
                if line.startswith('##'):  # Sous-titre
                    subtitle = line.strip('#').strip()
                    elements.append(Paragraph(subtitle, subtitle_style))
                    elements.append(Spacer(1, 6))
                elif line.startswith('#'):  # Titre de section (ignoré car déjà traité)
                    pass
                else:
                    elements.append(Paragraph(line.strip(), styles['Justify']))
            else:
                elements.append(Spacer(1, 6))  # Espace pour les lignes vides

        elements.append(PageBreak())

    # Génération du PDF avec le sommaire
    doc.multiBuild(elements, canvasmaker=NumberedCanvas)

def get_file_paths_and_titles_from_database():
    conn = sqlite3.connect(var.dossier_projet + '/dbchapitre')
    cur = conn.cursor()
    cur.execute("SELECT id, nom FROM chapitre ORDER BY numero")
    results = cur.fetchall()
    conn.close()
    return [(os.path.join(var.dossier_projet, str(result[0])), result[1]) for result in results]

def select_files_and_create_pdf():
    # Obtenir les chemins des fichiers et les titres depuis la base de données
    input_files = get_file_paths_and_titles_from_database()

    if not input_files:
        print("Aucun fichier trouvé dans la base de données.")
        return

    # Sélectionner l'emplacement et le nom du fichier PDF de sortie
    output_file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("Fichiers PDF", "*.pdf")])
    if not output_file:
        return

    # Utiliser var.nom comme titre
    title = var.nom

    # Créer le PDF
    create_pdf(input_files, output_file, title)
    fct_main.alert(f"Le fichier PDF a été créé : {output_file}")

def export():
    # Créer une fenêtre Tkinter (elle sera cachée)
    root = tk.Tk()
    root.withdraw()

    # Appeler la fonction pour sélectionner l'emplacement de sortie et créer le PDF
    select_files_and_create_pdf()

# Appel de la fonction d'export
# export()  # Décommentez cette ligne si vous voulez que l'export se fasse automatiquement à l'exécution du script
