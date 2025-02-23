import ebooklib
from ebooklib import epub
import sqlite3
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import src.var as var


def create_epub(input_files, output_file, title, subtitle, author, resume):
    book = epub.EpubBook()

    # Métadonnées
    book.set_identifier('id123456')
    book.set_title(title)
    book.set_language('fr')
    book.add_author(author)

    # Styles CSS
    style = '''
    @namespace epub "http://www.idpf.org/2007/ops";

    body {
        font-family: Arial, sans-serif;
    }

    h1 {
        margin-top: 0;
        page-break-before: always;
    }

    p {
        margin-bottom: 0;
        page-break-inside: avoid;
    }
    '''

    nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
    book.add_item(nav_css)

    # Page de titre
    title_page = epub.EpubHtml(title='Page de titre', file_name='title.xhtml')
    title_page.content = f'<h1>{title}</h1><h2>{subtitle}</h2><p>Par {author}</p>'
    title_page.add_item(nav_css)
    book.add_item(title_page)

    # Sommaire
    toc = []

    # Contenu des chapitres
    for input_file, chapter_title in input_files:
        chapter = epub.EpubHtml(title=chapter_title, file_name=f'chap_{os.path.basename(input_file)}.xhtml')
        with open(input_file, 'r', encoding='utf-8') as file:
            content = file.read()

        # Nettoyage du contenu
        content = content.replace('</p>\n\n', '</p>\n')  # Supprime les lignes vides excessives entre les paragraphes

        chapter.set_content(f'<h1>{chapter_title}</h1>{content}')
        chapter.add_item(nav_css)
        book.add_item(chapter)
        toc.append(chapter)

    # Résumé
    resume_page = epub.EpubHtml(title='Résumé', file_name='resume.xhtml')
    resume_page.content = f'<h1>Résumé</h1><p>{resume}</p>'
    resume_page.add_item(nav_css)
    book.add_item(resume_page)

    # Ajout du sommaire et de la navigation
    book.toc = toc
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # Définir l'ordre des pages
    book.spine = ['nav', title_page] + toc + [resume_page]

    # Écrire le fichier EPUB
    epub.write_epub(output_file, book, {})


def get_file_paths_and_titles_from_database():
    conn = sqlite3.connect(var.dossier_projet + '/dbchapitre')
    cur = conn.cursor()
    cur.execute("SELECT id, nom FROM chapitre ORDER BY numero")
    results = cur.fetchall()
    conn.close()
    return [(os.path.join(var.dossier_projet, str(result[0])), result[1]) for result in results]


def select_files_and_create_epub():
    input_files = get_file_paths_and_titles_from_database()
    if not input_files:
        messagebox.showwarning("Attention", "Aucun fichier trouvé dans la base de données.")
        return

    # Créer une fenêtre Tkinter cachée
    root = tk.Tk()
    root.withdraw()

    # Demander à l'utilisateur où enregistrer le fichier EPUB
    output_file = filedialog.asksaveasfilename(
        defaultextension=".epub",
        filetypes=[("EPUB files", "*.epub")],
        title="Enregistrer le fichier EPUB"
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
        create_epub(input_files, output_file, title, subtitle, author, resume)
        messagebox.showinfo("Succès", f"Le fichier EPUB a été créé : {output_file}")
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur s'est produite lors de la création du fichier EPUB : {str(e)}")


def export():
    select_files_and_create_epub()

# Appel de la fonction d'export
# export()
