import os
import sqlite3
from ebooklib import epub
import src.var as var
import src.fct_main as fct_main
import tkinter as tk
from tkinter import filedialog


def get_chapters_from_database():
    conn = sqlite3.connect(os.path.join(var.dossier_projet, 'dbchapitre'))
    cur = conn.cursor()
    cur.execute("SELECT id, nom, numero FROM chapitre ORDER BY numero")
    chapters = cur.fetchall()
    conn.close()
    return chapters


def text_files_to_epub(output_file, title, author):
    book = epub.EpubBook()
    book.set_identifier('id123456')
    book.set_title(title)
    book.set_language('fr')
    book.add_author(author)

    chapters = []
    db_chapters = get_chapters_from_database()

    for chapter_id, chapter_title, chapter_number in db_chapters:
        file_path = os.path.join(var.dossier_projet, str(chapter_id))

        if not os.path.exists(file_path):
            print(f"Attention : Le fichier pour le chapitre {chapter_title} n'existe pas.")
            continue

        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read().strip()

        chapter = epub.EpubHtml(title=chapter_title, file_name=f'chap_{chapter_number}.xhtml')
        chapter.content = f'<h1>{chapter_title}</h1>'
        chapter.content += ''.join(f'<p>{p.strip()}</p>' for p in content.split('\n\n\n') if p.strip())

        book.add_item(chapter)
        chapters.append(chapter)

    book.toc = [(epub.Section('Chapitres'), chapters)]
    book.spine = ['nav'] + chapters
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    css_content = 'body { margin: 5%; }'
    nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=css_content)
    book.add_item(nav_css)

    epub.write_epub(output_file, book, {})


def export():
    root = tk.Tk()
    root.withdraw()

    output_file = filedialog.asksaveasfilename(defaultextension=".epub", filetypes=[("Fichiers EPUB", "*.epub")])
    if not output_file:
        return

    title = var.nom
    author = "Auteur"  # Modifiez selon vos besoins

    text_files_to_epub(output_file, title, author)
    fct_main.alert(f"Le fichier EPUB a été créé : {output_file}")

# export_epub()  # Décommentez pour exécuter l'export automatiquement
