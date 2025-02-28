import sqlite3
from ebooklib import epub
import re
import os
import tkinter as tk
from tkinter import filedialog
from src import var, fct_main

def exporter_textes_vers_epub():
    # Connexion à la base de données
    conn = sqlite3.connect(var.dossier_projet + '/dbchapitre')
    cursor = conn.cursor()

    # Récupération des informations des chapitres
    cursor.execute("SELECT id, nom FROM chapitre ORDER BY numero")
    chapitres_db = cursor.fetchall()

    # Créer une fenêtre Tkinter (elle sera cachée)
    root = tk.Tk()
    root.withdraw()

    # Demander à l'utilisateur où enregistrer le fichier EPUB
    fichier_sortie = filedialog.asksaveasfilename(
        defaultextension=".epub",
        filetypes=[("EPUB files", "*.epub")],
        title="Enregistrer le fichier EPUB",
        initialfile=var.nom+".epub"
    )

    if not fichier_sortie:
        print("Exportation annulée.")
        return

    # Créer un nouveau livre EPUB
    livre = epub.EpubBook()
    livre.set_identifier('id123456')
    livre.set_title(var.nom)
    livre.set_language('fr')

    # Ajouter les métadonnées de l'auteur
    livre.add_author(var.info_auteur)

    # Créer la page de garde
    page_garde = epub.EpubHtml(title='Page de garde', file_name='page_garde.xhtml', lang='fr')
    contenu_page_garde = f'''
    <html>
    <head>
        <title>{var.nom}</title>
    </head>
    <body>
        <h1 style="text-align: center; margin-top: 30%;">{var.nom}</h1>
        <h2 style="text-align: center;">{var.info_stitre}</h2>
        <p style="text-align: center; margin-top: 20%;">Par {var.info_auteur}</p>
    </body>
    </html>
    '''
    page_garde.content = contenu_page_garde
    livre.add_item(page_garde)

    # Créer la page de sommaire
    sommaire = epub.EpubHtml(title='Sommaire', file_name='sommaire.xhtml', lang='fr')
    contenu_sommaire = '<h1>Sommaire</h1><ul>'

    chapitres = [page_garde, sommaire]
    toc = [
        epub.Link('page_garde.xhtml', 'Page de garde', 'page_garde'),
        epub.Link('sommaire.xhtml', 'Sommaire', 'sommaire')
    ]

    for id_chapitre, titre_chapitre in chapitres_db:
        nom_fichier = f"{id_chapitre}"
        chemin_fichier = os.path.join(var.dossier_projet, nom_fichier)

        if os.path.exists(chemin_fichier):
            with open(chemin_fichier, 'r', encoding='utf-8') as f:
                contenu = f.read().strip()

            # Ajouter le titre du chapitre au début du contenu
            contenu_traite = f'<h1>{titre_chapitre}</h1>'

            # Traiter le contenu ligne par ligne
            lignes = contenu.split('\n')
            for ligne in lignes:
                ligne = ligne.strip()
                if ligne:
                    # Regrouper les balises <b>, <u> et <i>
                    ligne = re.sub(r'<(/?)([bui])>(.*?)<(/?\2)>', r'<\1\2>\3', ligne)
                    ligne = re.sub(r'(<[bui]>)(.+?)(<\/[bui]>)', r'\1\2\3', ligne)

                    if ligne.startswith('# '):  # Titre de niveau 1
                        contenu_traite += f'<h2>{ligne[2:]}</h2>'
                    elif ligne.startswith('## '):  # Titre de niveau 2
                        contenu_traite += f'<h3>{ligne[3:]}</h3>'
                    else:
                        contenu_traite += f'<p>{ligne}</p>'
                else:
                    contenu_traite += '<br/>'

            # Supprimer les balises paragraphes vides et les sauts de ligne consécutifs
            contenu_traite = re.sub(r'<p>\s*</p>', '', contenu_traite)
            contenu_traite = re.sub(r'(<br/>){2,}', '<br/>', contenu_traite)

            chapitre = epub.EpubHtml(title=titre_chapitre, file_name=f'chap_{id_chapitre:02d}.xhtml', lang='fr')
            chapitre.content = f'<html><body>{contenu_traite}</body></html>'

            livre.add_item(chapitre)
            chapitres.append(chapitre)
            toc.append(epub.Link(f'chap_{id_chapitre:02d}.xhtml', titre_chapitre, f'chap{id_chapitre:02d}'))

            # Ajouter le chapitre au sommaire
            contenu_sommaire += f'<li><a href="chap_{id_chapitre:02d}.xhtml">{titre_chapitre}</a></li>'

    contenu_sommaire += '</ul>'
    sommaire.content = f'<html><body>{contenu_sommaire}</body></html>'
    livre.add_item(sommaire)

    livre.toc = tuple(toc)
    livre.spine = chapitres
    livre.add_item(epub.EpubNcx())
    livre.add_item(epub.EpubNav())

    try:
        epub.write_epub(fichier_sortie, livre, {})
        fct_main.alert(f_("Le fichier DOCX a été enregistré sous : {fichier_sortie}"))
    except Exception as e:
        fct_main.alert(f_("Une erreur est survenue : {e}"))

    # Fermer la connexion à la base de données
    conn.close()
