import logging
import os
import threading
import time
import tkinter as tk
from pathlib import Path
from threading import Thread
from tkinter import filedialog
from tkinter.messagebox import showinfo
from src import var, design, db, sous_fenetre


#####################################################
##### Divers                                   #####
#####################################################
##### Logs #####
def logs(log):
    logging.config.fileConfig('src/logger.ini', disable_existing_loggers=False)
    logger = logging.getLogger(__name__)
    logger.error(log, exc_info=True)
##### Alert #####
def alert(message):
    showinfo("alerte", message)
#####################################################
##### Projet                                    #####
#####################################################
##### Créer le dossier du projet #####
def creer_dossier(nom):
    chemin_dossier = os.getcwd() + "\\" + nom
    dossier = Path(chemin_dossier)
    if not dossier.exists():
        dossier.mkdir(parents=True, exist_ok=True)

##### Nouveau Projet #####
def projet_new():
    if var.dossier_projet != "":
        close_projet()
    chemin_fichier = filedialog.asksaveasfilename(
        defaultextension=".sb",
        filetypes=[("Fichiers texte", "*.sb")],
        title="Enregistrer le fichier"
    )

    if chemin_fichier:
        chemin_dossier, nom_fichier_complet = os.path.split(chemin_fichier)
        nom_fichier = os.path.splitext(nom_fichier_complet)[0]
        if os.path.exists(chemin_fichier):
            alert(_("Le projet existe déjà"))
        else:
            with open(chemin_fichier, 'w', encoding='utf-8') as fichier:
                fichier.write(f"path = {chemin_dossier}\n"
                              f"nom = {nom_fichier}")
                # Création du nouveau dossier
                nouveau_dossier = os.path.join(chemin_dossier, nom_fichier)
                try:
                    os.makedirs(nouveau_dossier, exist_ok=True)
                except OSError as e:
                    print(f"Erreur lors de la création du dossier : {e}")
            db.creer_table_chapitre(chemin_dossier+"/"+nom_fichier+"/")
            db.creer_table_gene(chemin_dossier+"/"+nom_fichier+"/")
            alert(_("Le projet "+nom_fichier+" à bien été crée"))
            open_projet()
    else:
        alert(_("Opération annulée."))

##### Ouvrir un projet #####
def open_projet():
    if var.dossier_projet != "":
        close_projet()
    chemin_fichier = filedialog.askopenfilename(
        title=_("Sélectionner un fichier .sb"),
        filetypes=[(_("Fichiers SB"), "*.sb"), (_("Tous les fichiers"), "*.*")]
    )
    if chemin_fichier:
        variables = {}
        with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
            for ligne in fichier:
                ligne = ligne.strip()
                if ligne and '=' in ligne:
                    cle, valeur = ligne.split('=', 1)
                    variables[cle.strip()] = valeur.strip()
        for cle, valeur in variables.items():
            if cle == 'path':
                var.path = valeur
            elif cle == 'nom':
                var.nom = valeur

        def fct():
            var.dossier_projet = var.path+"/"+var.nom
            db.creer_table_gene(var.dossier_projet)
            db.creer_table_chapitre(var.dossier_projet)
            var.app_instance.update_titre()

            db.liste_chapitre()
            var.param_police = db.tab_param_lire("police")
            var.param_taille = db.tab_param_lire("taille")
            var.save_time = int(db.tab_param_lire("save_time"))
            var.info_auteur = db.tab_info_lire("auteur")
            var.info_date = db.tab_info_lire("date")
            var.info_resume = db.tab_info_lire("resume")
            var.app_instance.ouvrir_fichier()
        fct()
        thread = threading.Thread(target=enregistrement_auto)
        thread.start()

##### Enregistrement auto #####
def enregistrement_auto(tk=None):
    tourne = True
    while tourne == True:
        if var.dossier_projet == "":
            tourne = False
            Thread.curentThread.join()
        if var.save_time == 0:
            print("Stop save")
            tourne  =False
        threading.Thread(target=save_projet()).start()
        print("save")
        time.sleep(var.save_time)

def close_projet():
    var.dossier_projet = ""
    var.nom = ""
    var.app_instance.update_titre()
    design.creer_bouton_haut()
    design.create_menu()
    var.param_police = "Helvetica"
    var.param_taille = "10"
    var.save_time = 0
    var.info_auteur = ""
    var.info_date = ""
    var.info_resume = ""
    var.app_instance.update_text_widget()
    var.app_instance.update_menu()
    var.app_instance.update_txt_resume()
    for item in var.app_instance.list_chapitre.get_children():
        var.app_instance.list_chapitre.delete(item)
#####################################################
##### Chapitre                                  #####
#####################################################
##### Sauvegarder le chapitre #####
def save_projet():
    if var.chapitre != "":
        def get_formatted_content(self):
            import tkinter as tk

            content = []
            for index in range(1, int(self.index(tk.END).split('.')[0])):
                line_start = f"{index}.0"
                line_end = f"{index}.end"
                line = self.get(line_start, line_end)
                formatted_line = ""

                # Récupération des balises d'alignement au début de la ligne
                alignment_tags = [tag for tag in self.tag_names(line_start)
                                  if tag in ("left", "right", "center", "justify")]
                alignment = alignment_tags[0] if alignment_tags else None

                # Formatage des caractères
                for i, char in enumerate(line):
                    char_index = f"{index}.{i}"
                    tags = self.tag_names(char_index)

                    # Applique les styles de texte
                    if "bold" in tags and "italic" in tags and "underline" in tags:
                        formatted_line += f"<b><i><u>{char}</u></i></b>"
                    elif "bold" in tags and "italic" in tags:
                        formatted_line += f"<b><i>{char}</i></b>"
                    elif "bold" in tags and "underline" in tags:
                        formatted_line += f"<b><u>{char}</u></b>"
                    elif "italic" in tags and "underline" in tags:
                        formatted_line += f"<i><u>{char}</u></i>"
                    elif "bold" in tags:
                        formatted_line += f"<b>{char}</b>"
                    elif "italic" in tags:
                        formatted_line += f"<i>{char}</i>"
                    elif "underline" in tags:
                        formatted_line += f"<u>{char}</u>"
                    else:
                        formatted_line += char

                # Ajoute l'alignement si nécessaire
                if alignment:
                    formatted_line = f'<div style="text-align: {alignment};">{formatted_line}</div>'

                content.append(formatted_line)

            return "\n".join(content).rstrip('\n')

        with open(var.dossier_projet+"/"+var.chapitre, "w", encoding='utf-8') as f:
            content = get_formatted_content(var.app_instance.text_widget)
            f.write(content)


import tkinter as tk
from tkinter import ttk
import os
from PIL import Image, ImageTk
import uuid


def save_projet_image():
    if var.chapitre != "":
        # Créer une fenêtre de progression
        progress_window = tk.Toplevel()
        progress_window.title("Sauvegarde en cours")
        progress_bar = ttk.Progressbar(progress_window, length=300, mode='determinate')
        progress_bar.pack(pady=10)
        progress_label = tk.Label(progress_window, text="Sauvegarde en cours...")
        progress_label.pack(pady=5)

        try:
            content = get_formatted_content_image(var.app_instance.text_widget, progress_bar, progress_label)

            # Créer un dossier pour les images si nécessaire
            images_folder = os.path.join(var.dossier_projet, "images")
            os.makedirs(images_folder, exist_ok=True)

            # Sauvegarder le contenu texte
            with open(os.path.join(var.dossier_projet, var.chapitre), "w", encoding='utf-8') as f:
                f.write(content)

            progress_label.config(text="Sauvegarde terminée!")
        except Exception as e:
            print({str(e)})
            progress_label.config(text=f"Erreur: {str(e)}")
        finally:
            progress_window.after(2000, progress_window.destroy)

def get_formatted_content_image(text_widget, progress_bar, progress_label):
    content = []
    total_chars = int(text_widget.index(tk.END).split('.')[0])
    progress_bar['maximum'] = total_chars

    # Obtenir tous les indices d'images
    image_indices = text_widget.image_names()

    current_index = "1.0"
    while text_widget.compare(current_index, "<", tk.END):
        if current_index in image_indices:
            # C'est une image
            image = text_widget.image_cget(current_index, "image")
            img_filename = save_image(image)
            print(image)
            if img_filename:
                content.append(f"<IMG>{img_filename}</IMG>")
            current_index = text_widget.index(f"{current_index}+1c")
        else:
            # C'est du texte
            next_image_index = next((idx for idx in image_indices if text_widget.compare(idx, ">", current_index)),
                                    tk.END)
            text_chunk = text_widget.get(current_index, next_image_index)
            formatted_chunk = format_text_chunk(text_widget, current_index, text_chunk)
            content.append(formatted_chunk)
            current_index = next_image_index

        # Mise à jour de la barre de progression
        progress_line = int(text_widget.index(current_index).split('.')[0])
        progress_bar['value'] = progress_line
        progress_label.config(text=f"Sauvegarde en cours... {progress_line}/{total_chars} lignes")
        progress_bar.update()

    return ''.join(content)

def format_text_chunk(text_widget, start_index, text_chunk):
    formatted_chunk = ""
    for i, char in enumerate(text_chunk):
        char_index = text_widget.index(f"{start_index}+{i}c")
        tags = text_widget.tag_names(char_index)
        formatted_char = format_char(char, tags)
        formatted_chunk += formatted_char
    return formatted_chunk

def format_char(char, tags):
    # Appliquer les styles de mise en forme (gras, italique, souligné)
    if "bold" in tags and "italic" in tags and "underline" in tags:
        formatted_char = f"<b><i><u>{char}</u></i></b>"
    elif "bold" in tags and "italic" in tags:
        formatted_char = f"<b><i>{char}</i></b>"
    elif "bold" in tags and "underline" in tags:
        formatted_char = f"<b><u>{char}</u></b>"
    elif "italic" in tags and "underline" in tags:
        formatted_char = f"<i><u>{char}</u></i>"
    elif "bold" in tags:
        formatted_char = f"<b>{char}</b>"
    elif "italic" in tags:
        formatted_char = f"<i>{char}</i>"
    elif "underline" in tags:
        formatted_char = f"<u>{char}</u>"
    else:
        formatted_char = char

    # Appliquer les styles d'alignement (gauche, droite, centré, justifié)
    if "align-left" in tags:
        return f'<div style="text-align: left;">{formatted_char}</div>'
    elif "align-right" in tags:
        return f'<div style="text-align: right;">{formatted_char}</div>'
    elif "align-center" in tags:
        return f'<div style="text-align: center;">{formatted_char}</div>'
    elif "align-justify" in tags:
        return f'<div style="text-align: justify;">{formatted_char}</div>'

    # Retourner le texte formaté sans alignement si aucun alignement n'est spécifié
    return formatted_char

def save_image(image):
    try:
        images_folder = os.path.join(var.dossier_projet, "images")
        os.makedirs(images_folder, exist_ok=True)
        image_filename = f"image_{uuid.uuid4().hex[:8]}.png"
        png_path = os.path.join(images_folder, image_filename)

        # Convertir l'image en objet PIL Image
        if isinstance(image, str):
            # Si c'est un chemin de fichier
            image_pil = Image.open(image)
        elif isinstance(image, tk.PhotoImage):
            # Si c'est un PhotoImage Tkinter
            image_pil = Image.new("RGBA", (image.width(), image.height()))
            image_pil.paste(Image.frombytes("RGBA", (image.width(), image.height()), image.get()), (0, 0))
        elif isinstance(image, ImageTk.PhotoImage):
            # Si c'est un PhotoImage de PIL
            image_pil = ImageTk.getimage(image)
        elif isinstance(image, Image.Image):
            # Si c'est déjà un objet PIL Image
            image_pil = image
        else:
            raise ValueError("Type d'image non pris en charge")

        # Redimensionner l'image
        max_size = (800, 800)
        image_pil.thumbnail(max_size, Image.LANCZOS)

        # Sauvegarder l'image
        image_pil.save(png_path, "PNG", optimize=True)

        print(f"Image sauvegardée : {png_path}")
        return image_filename
    except Exception as e:
        print(f"Erreur lors de la sauvegarde de l'image : {str(e)}")
        return None

##### Nouveau Chapitre #####
def nouveau_chapitre():
    sous_fenetre.fenetre_chapitre()
##### Ouvrir un projet
def apply_formatted_content(text_widget, content):

    # Configuration des tags AVANT l'insertion du texte
    text_widget.tag_configure("left", justify=tk.LEFT)
    text_widget.tag_configure("right", justify=tk.RIGHT)
    text_widget.tag_configure("center", justify=tk.CENTER)
    #text_widget.tag_configure("justify", justify=tk.JUSTIFY)


    # Efface le contenu actuel
    text_widget.delete('1.0', tk.END)

    for line in content.split('\n'):
        alignment = None
        clean_line = line

        # Détection de l'alignement
        if line.startswith('<div style="text-align:'):
            if 'left' in line:
                alignment = "left"
            elif 'right' in line:
                alignment = "right"
            elif 'center' in line:
                alignment = "center"
            elif 'justify' in line:
                alignment = "justify"
            clean_line = line.split('>', 1)[1].replace('</div>', '')  # Nettoie la ligne

        # Début de la ligne actuelle
        line_start = text_widget.index(tk.INSERT)

        # Insertion du texte
        _insert_formatted_text(text_widget, clean_line)

        # Application de l'alignement sur toute la ligne
        if alignment:
            line_end = text_widget.index(f"{line_start} lineend")
            text_widget.tag_add(alignment, line_start, line_end)

def _insert_formatted_text(text_widget, line):
    in_bold = in_italic = in_underline = False
    i = 0

    while i < len(line):
        if line[i:].startswith('<b>'):
            in_bold, i = True, i + 3
        elif line[i:].startswith('</b>'):
            in_bold, i = False, i + 4
        elif line[i:].startswith('<i>'):
            in_italic, i = True, i + 3
        elif line[i:].startswith('</i>'):
            in_italic, i = False, i + 4
        elif line[i:].startswith('<u>'):
            in_underline, i = True, i + 3
        elif line[i:].startswith('</u>'):
            in_underline, i = False, i + 4
        else:
            # Insertion caractère par caractère avec tags
            pos = text_widget.index(tk.INSERT)
            text_widget.insert(tk.INSERT, line[i])
            if in_bold: text_widget.tag_add("bold", pos, tk.INSERT)
            if in_italic: text_widget.tag_add("italic", pos, tk.INSERT)
            if in_underline: text_widget.tag_add("underline", pos, tk.INSERT)
            i += 1

    text_widget.insert(tk.INSERT, '\n')  # Saut de ligne final

def ouvrir_chapitre(id):
    var.chapitre = id
    try:
        if not os.path.exists(var.dossier_projet + "/" + id):
            with open(var.dossier_projet + "/" + id, 'w', encoding='utf-8') as f:
                f.write("")
        with open(var.dossier_projet + "/" + id, 'r', encoding='utf-8') as f:
            contenu = f.read()

        var.app_instance.update_text_widget()
        apply_formatted_content(var.app_instance.text_widget, contenu)
        resume = db.lire("chapitre", id, "resume")
        var.app_instance.update_txt_resume()
        var.app_instance.txt_resume.insert(1.0, resume)
    except Exception as e:
        tk.messagebox.showerror(_("Erreur"), _("Impossible d'ouvrir le fichier : ")+str(e))

##### Supprimer le chapite #####
def delete_chapitre(id, chapitre):
    chemin_fichier = var.dossier_projet+"/"+id
    try:
        os.remove(chemin_fichier)
        print(f_("Le fichier '{chemin_fichier}' a été supprimé avec succès."))
    except FileNotFoundError:
        print(f_("Le fichier '{chemin_fichier}' n'existe pas."))
    except PermissionError:
        print(f_("Pas de permission pour supprimer le fichier '{chemin_fichier}'."))
    except Exception as e:
        print(f"Une erreur s'est produite lors de la suppression du fichier : {str(e)}")
    db.effacer(id, "chapitre")
    db.liste_chapitre()
