import docx
from docx.enum.style import WD_STYLE_TYPE
from docx.shared import Pt
import sqlite3
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import src.var as var


def create_doc(input_files, output_file, title, subtitle, author, resume):
    doc = docx.Document()

    # Utiliser les styles existants ou les créer si nécessaire
    def get_or_create_style(name, base_style='Normal'):
        if name not in doc.styles:
            style = doc.styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH)
            style.base_style = doc.styles[base_style]
        return doc.styles[name]

    title_style = get_or_create_style('Title')
    title_style.font.size = Pt(24)
    title_style.font.bold = True

    subtitle_style = get_or_create_style('Subtitle')
    subtitle_style.font.size = Pt(18)
    subtitle_style.font.italic = True

    heading1_style = get_or_create_style('Heading 1')
    heading1_style.font.size = Pt(16)
    heading1_style.font.bold = True

    toc_style = get_or_create_style('TOC 1')
    toc_style.font.size = Pt(12)

    # Page de titre
    doc.add_paragraph(title, style='Title')
    doc.add_paragraph(subtitle, style='Subtitle')
    doc.add_paragraph(f"Par {author}")

    doc.add_page_break()

    # Sommaire
    doc.add_paragraph("Sommaire", style='Title')
    for _, chapter_title in input_files:
        doc.add_paragraph(chapter_title, style='TOC 1')

    doc.add_page_break()

    # Contenu des chapitres
    for input_file, chapter_title in input_files:
        doc.add_heading(chapter_title, level=1)

        with open(input_file, 'r', encoding='utf-8') as file:
            content = file.read()

        # Ajouter le contenu du chapitre
        for paragraph in content.split('\n'):
            if paragraph.strip():
                doc.add_paragraph(paragraph.strip())

        doc.add_page_break()

    # Résumé
    doc.add_heading("Résumé", level=1)
    doc.add_paragraph(resume)

    # Sauvegarder le document
    doc.save(output_file)


def get_file_paths_and_titles_from_database():
    conn = sqlite3.connect(var.dossier_projet + '/dbchapitre')
    cur = conn.cursor()
    cur.execute("SELECT id, nom FROM chapitre ORDER BY numero")
    results = cur.fetchall()
    conn.close()
    return [(os.path.join(var.dossier_projet, str(result[0])), result[1]) for result in results]


def export_doc():
    input_files = get_file_paths_and_titles_from_database()
    if not input_files:
        messagebox.showwarning("Attention", "Aucun fichier trouvé dans la base de données.")
        return

    root = tk.Tk()
    root.withdraw()

    output_file = filedialog.asksaveasfilename(
        defaultextension=".docx",
        filetypes=[("Word Document", "*.docx")],
        title="Enregistrer le fichier Word"
    )

    if not output_file:
        messagebox.showinfo("Information", "Opération annulée.")
        return

    title = var.nom

    conn = sqlite3.connect(var.dossier_projet + '/dbgene')
    cur = conn.cursor()
    cur.execute("SELECT stitre, auteur, resume FROM info WHERE id=1")
    result = cur.fetchone()
    conn.close()

    subtitle = result[0] if result else "Sous-titre par défaut"
    author = result[1] if result else "Auteur inconnu"
    resume = result[2] if result and len(result) > 2 else "Résumé non disponible"

    try:
        create_doc(input_files, output_file, title, subtitle, author, resume)
        messagebox.showinfo("Succès", f"Le fichier Word a été créé : {output_file}")
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur s'est produite lors de la création du fichier Word : {str(e)}")



