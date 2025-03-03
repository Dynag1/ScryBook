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
            design.creer_bouton_haut()
            db.liste_chapitre()
            design.create_menu()
            var.param_police = db.tab_param_lire("police")
            var.param_taille = db.tab_param_lire("taille")
            var.save_time = int(db.tab_param_lire("save_time"))
            var.info_auteur = db.tab_info_lire("auteur")
            var.info_date = db.tab_info_lire("date")
            var.info_resume = db.tab_info_lire("resume")
            var.app_instance.update_text_widget()
            var.app_instance.update_menu()
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
        save_projet()
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
        content = get_formatted_content(var.app_instance.text_widget)

        # Créer un dossier pour les images si nécessaire
        images_folder = os.path.join(var.dossier_projet, "images")
        os.makedirs(images_folder, exist_ok=True)

        with open(os.path.join(var.dossier_projet, var.chapitre), "w", encoding='utf-8') as f:
            f.write(content)


def get_formatted_content(text_widget):
    content = []
    image_count = 0
    for index in range(1, int(text_widget.index(tk.END).split('.')[0])):
        line_start = f"{index}.0"
        line_end = f"{index}.end"
        formatted_line = ""
        i = 0
        while True:
            char_index = f"{index}.{i}"
            if char_index == line_end:
                break
            tags = text_widget.tag_names(char_index)

            if "image" in tags:
                image = text_widget.image_cget(char_index, "image")
                if image:
                    # Générer un nom de fichier unique
                    image_filename = f"image_{uuid.uuid4().hex[:8]}"

                    # Sauvegarder l'image en PNG et JPG
                    save_image(image, image_filename)

                    # Ajouter le tag d'image dans le contenu
                    formatted_line += f"<IMG>{image_filename}</IMG>"
                    image_count += 1
                i += 1  # Les images sont considérées comme un seul caractère
            else:
                char = text_widget.get(char_index)
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
                i += 1
        content.append(formatted_line)
    print(f"Nombre d'images sauvegardées : {image_count}")
    return "\n".join(content).rstrip('\n')


def save_image(image, filename):
    images_folder = os.path.join(var.dossier_projet, "images")

    if isinstance(image, tk.PhotoImage):
        # Convertir PhotoImage en Image PIL
        image_pil = Image.new("RGBA", (image.width(), image.height()))
        image_pil.paste(Image.frombytes("RGBA", (image.width(), image.height()), image.get()), (0, 0))
    elif isinstance(image, ImageTk.PhotoImage):
        image_pil = image._PhotoImage__photo
    else:
        image_pil = image

    # Sauvegarder en PNG
    png_path = os.path.join(images_folder, f"{filename}.png")
    image_pil.save(png_path, "PNG")

    # Sauvegarder en JPG
    jpg_path = os.path.join(images_folder, f"{filename}.jpg")
    image_pil.convert("RGB").save(jpg_path, "JPEG")
##### Nouveau Chapitre #####
def nouveau_chapitre():
    sous_fenetre.fenetre_chapitre()
##### Ouvrir un projet
def apply_formatted_content(text_widget, content):
    #text_widget.delete('1.0', tk.END)  # Efface le contenu actuel
    lines = content.split('\n')
    for line in lines:
        start_index = text_widget.index(tk.INSERT)
        in_bold = False
        in_italic = False
        in_underline = False
        i = 0
        while i < len(line):
            if line[i:].startswith('<b>'):
                in_bold = True
                i += 3
            elif line[i:].startswith('</b>'):
                in_bold = False
                i += 4
            elif line[i:].startswith('<i>'):
                in_italic = True
                i += 3
            elif line[i:].startswith('</i>'):
                in_italic = False
                i += 4
            elif line[i:].startswith('<u>'):
                in_underline = True
                i += 3
            elif line[i:].startswith('</u>'):
                in_underline = False
                i += 4
            else:
                text_widget.insert(tk.INSERT, line[i])
                end_index = text_widget.index(tk.INSERT)
                if in_bold:
                    text_widget.tag_add("bold", start_index, end_index)
                if in_italic:
                    text_widget.tag_add("italic", start_index, end_index)
                if in_underline:
                    text_widget.tag_add("underline", start_index, end_index)
                start_index = end_index
                i += 1
        text_widget.insert(tk.INSERT, '\n')
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
        tk.messagebox.showerror(_("Erreur"), f_("Impossible d'ouvrir le fichier : {str(e)}"))
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
