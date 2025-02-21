import os
import sqlite3
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import tkinter as tk
from tkinter import filedialog
import src.var as var
import src.fct_main as fct_main


def create_doc(input_files, output_file, title):
    doc = Document()

    # Styles
    styles = doc.styles

    # Modifier les styles existants au lieu d'en créer de nouveaux
    title_style = styles['Title']
    title_style.font.size = Pt(24)
    title_style.font.bold = True
    title_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER

    heading1_style = styles['Heading 1']
    heading1_style.font.size = Pt(18)
    heading1_style.font.bold = True
    heading1_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER

    heading2_style = styles['Heading 2']
    heading2_style.font.size = Pt(14)
    heading2_style.font.bold = True

    # Page de titre
    doc.add_paragraph(title, style='Title')
    doc.add_page_break()

    # Sommaire (espace réservé)
    doc.add_paragraph("Table des matières", style='Title')
    doc.add_paragraph("(La table des matières sera générée automatiquement)")
    doc.add_page_break()

    # Contenu des chapitres
    for input_file, chapter_title in input_files:
        doc.add_paragraph(chapter_title, style='Heading 1')

        with open(input_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        for line in lines:
            if line.strip():
                if line.startswith('##'):  # Sous-titre
                    subtitle = line.strip('#').strip()
                    doc.add_paragraph(subtitle, style='Heading 2')
                elif line.startswith('#'):  # Titre de section (ignoré car déjà traité)
                    pass
                else:
                    doc.add_paragraph(line.strip())
            else:
                doc.add_paragraph()  # Ligne vide

        doc.add_page_break()

    # Sauvegarde du document
    doc.save(output_file)

def get_file_paths_and_titles_from_database():
    conn = sqlite3.connect(var.dossier_projet + '/dbchapitre')
    cur = conn.cursor()
    cur.execute("SELECT id, nom FROM chapitre ORDER BY numero")
    results = cur.fetchall()
    conn.close()
    return [(os.path.join(var.dossier_projet, str(result[0])), result[1]) for result in results]

def select_files_and_create_doc():
    # Obtenir les chemins des fichiers et les titres depuis la base de données
    input_files = get_file_paths_and_titles_from_database()

    if not input_files:
        print("Aucun fichier trouvé dans la base de données.")
        return

    # Sélectionner l'emplacement et le nom du fichier DOC de sortie
    output_file = filedialog.asksaveasfilename(defaultextension=".docx", filetypes=[("Fichiers Word", "*.docx")])
    if not output_file:
        return

    # Utiliser var.nom comme titre
    title = var.nom

    # Créer le DOC
    create_doc(input_files, output_file, title)
    fct_main.alert(f"Le fichier DOC a été créé : {output_file}")

def export():
    # Créer une fenêtre Tkinter (elle sera cachée)
    root = tk.Tk()
    root.withdraw()

    # Appeler la fonction pour sélectionner l'emplacement de sortie et créer le DOC
    select_files_and_create_doc()

# Appel de la fonction d'export
# export()  # Décommentez cette ligne si vous voulez que l'export se fasse automatiquement à l'exécution du script
