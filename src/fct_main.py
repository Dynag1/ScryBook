import logging
import os
import threading
import time
import tkinter as tk
from pathlib import Path
from threading import Thread
from tkinter import filedialog
from tkinter.messagebox import showinfo
import src.var as var
import src.design as design
import src.db as db
import src.sous_fenetre as s_fenetre
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
    chemin_fichier = filedialog.asksaveasfilename(
        defaultextension=".sb",
        filetypes=[("Fichiers texte", "*.sb")],
        title="Enregistrer le fichier"
    )

    if chemin_fichier:
        chemin_dossier, nom_fichier_complet = os.path.split(chemin_fichier)
        nom_fichier = os.path.splitext(nom_fichier_complet)[0]
        if os.path.exists(chemin_fichier):
            alert("Le projet existe déjà")
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
            alert("Le projet "+nom_fichier+" à bien été crée")
            open_projet()
    else:
        alert("Opération annulée.")
##### Ouvrir un projet #####
def open_projet():
    chemin_fichier = filedialog.askopenfilename(
        title="Sélectionner un fichier .sb",
        filetypes=[("Fichiers SB", "*.sb"), ("Tous les fichiers", "*.*")]
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
        var.dossier_projet = var.path+"/"+var.nom
        db.creer_table_gene(var.dossier_projet)
        db.creer_table_chapitre(var.dossier_projet)
        update_label_nom(var.nom)
        design.creer_bouton_haut()
        db.liste_chapitre()
        thread = threading.Thread(target=enregistrement_auto)
        thread.start()
        print("Dossier "+var.dossier_projet)
##### Update le Nom du projet #####
def update_label_nom(new_text):
    var.lab_nom_projet.config(text=new_text)
##### Enregistrement auto #####
def enregistrement_auto(tk=None):
    tourne = True
    while tourne == True:
        if var.dossier_projet == "":
            tourne = False
            Thread.curentThread.join()
        save_projet()
        time.sleep(30)
#####################################################
##### Chapitre                                  #####
#####################################################
##### Sauvegarder le chapitre #####
def save_projet():
    print(var.chapitre)
    if var.chapitre != "":
        def get_formatted_content(self):
            content = []
            for index in range(1, int(self.index(tk.END).split('.')[0])):
                line_start = f"{index}.0"
                line_end = f"{index}.end"
                line = self.get(line_start, line_end)
                formatted_line = ""
                for i, char in enumerate(line):
                    char_index = f"{index}.{i}"
                    tags = self.tag_names(char_index)
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
                content.append(formatted_line)
            return "\n".join(content)

        with open(var.dossier_projet+"/"+var.chapitre, "w", encoding='utf-8') as f:
            content = get_formatted_content(var.text_widget)
            f.write(content)
            #f.write(var.text_widget.get_formatted_content(1.0, tk.END))
    print("save")
##### Nouveau Chapitre #####
def nouveau_chapitre():
    s_fenetre.fenetre_chapitre()
##### Ouvrir un projet
def ouvrir_chapitre(id):
    var.chapitre = id
    try:
        if not os.path.exists(var.dossier_projet+"/"+id):
            with open(var.dossier_projet+"/"+id, 'w', encoding='utf-8') as f:
                f.write("")
        with open(var.dossier_projet+"/"+id, 'r', encoding='utf-8') as f:
            contenu = f.read()
        var.text_widget.delete('1.0', tk.END)  # Efface le contenu actuel

        def apply_formatted_content(self, content):
            lines = content.split('\n')
            for line in lines:
                start_index = self.index(tk.INSERT)
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
                        self.insert(tk.INSERT, line[i])
                        end_index = self.index(tk.INSERT)
                        if in_bold:
                            self.tag_add("bold", start_index, end_index)
                        if in_italic:
                            self.tag_add("italic", start_index, end_index)
                        if in_underline:
                            self.tag_add("underline", start_index, end_index)
                        start_index = end_index
                        i += 1
                self.insert(tk.INSERT, '\n')

        #var.text_widget.insert(tk.END, contenu)  # Insère le nouveau contenu

    except Exception as e:
        tk.messagebox.showerror("Erreur", f"Impossible d'ouvrir le fichier : {str(e)}")
    apply_formatted_content(var.text_widget, contenu)
##### Supprimer le chapite #####
def delete_chapitre(id, chapitre):
    chemin_fichier = var.dossier_projet+"/"+id
    try:
        os.remove(chemin_fichier)
        print(f"Le fichier '{chemin_fichier}' a été supprimé avec succès.")
    except FileNotFoundError:
        print(f"Le fichier '{chemin_fichier}' n'existe pas.")
    except PermissionError:
        print(f"Pas de permission pour supprimer le fichier '{chemin_fichier}'.")
    except Exception as e:
        print(f"Une erreur s'est produite lors de la suppression du fichier : {str(e)}")
    db.effacer(id, "chapitre")
    db.liste_chapitre()
