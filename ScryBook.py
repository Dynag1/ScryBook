import os
import threading
import tkinter as tk
from tkinter import ttk, Menu
import tkinter.font as tkFont
from src import var, design, fct_main, sous_fenetre, thread_maj, verif_ortho, db
from textblob import TextBlob
from src.verif_ortho import CorrectionOrthographique
from spellchecker import SpellChecker
import re
import gettext
import locale
global app_instance
app_instance = None
def quitter():
    os._exit(0)

class main:

    def __init__(self, master):
        chemin_repertoire = os.getcwd()
        var.path_dossier = chemin_repertoire
        db.creer_table_param()
        try:
            # Obtenir la langue du système

            var.langue = db.tab_param_lire("langue")
            gettext.find("ScryBook")
            traduction = gettext.translation(var.langue, localedir='src/locale', languages=[var.langue])
            traduction.install()
            print(traduction)
        except:
            gettext.install('ScryBook')
            print("error")
        global app_instance
        self.master = master
        var.app_instance = self
        master.title(var.nom)
        master.geometry("800x600")
        master.iconbitmap('src/logoSb.ico')
        master.title("ScryBook")
        #master.state('zoomed')
        thread = threading.Thread(target=thread_maj.main())
        thread.start()
        fct_main.creer_dossier("Projets")
        var.frame_haut = design.creer_frame_haut(master)
        self.frame_main = design.creer_frame_main(master)
        self.frame_bas = design.creer_frame_bas(master)
        self.frame1, self.frame2 = design.creer_sous_frames(self.frame_main)

        self.lab_nom_projet = tk.Label(master=self.frame1, bg=var.bg_frame_haut, text=var.nom, height=2, anchor='w')

        # Assurez-vous que la colonne s'étende
        self.frame1.columnconfigure(0, weight=1)

        design.creer_bouton_haut()
        self.but_chapitre = ttk.Button(self.frame1, text=_("Nouveau chapitre"), command=fct_main.nouveau_chapitre).grid(row=2, column=0, padx=5, pady=5)

        self.list_chapitre = design.creer_list_chapitre(self.frame1)

        # Liaison des événements
        self.list_chapitre.bind('<ButtonRelease-1>', self.item_selected)
        self.list_chapitre.bind('<Button-3>', self.right_clic)
        self.list_chapitre.bind('<Double-1>', lambda e: self.resume())

        self.txt_resume = design.creer_zone_text_resume(self.frame1)

        self.toolbar = design.creer_toolbar(self.frame2)
        self.bold_button, self.italic_button, self.sl_button, self.corrige = design.creer_boutons_toolbar(self.toolbar, self.toggle_bold, self.toggle_italic, self.toggle_sl, self.verifier_orthographe)
        self.text_widget = design.creer_zone_texte(self.frame2)
        self.text_widget.tag_configure("erreur", foreground="red")



        self.spell = SpellChecker(language=var.langue)

        self.text_widget.bind("<space>", self.verifier_orthographe)
        self.text_widget.bind("<Return>", self.verifier_orthographe)

        self.menu_correction = tk.Menu(self.master, tearoff=0)
        self.lab_version = design.creer_label_version(self.frame_bas)
        self.menubar = design.create_menu()
        self.master.config(menu=self.menubar)
        design.configurer_tags_texte(self.text_widget)

        # Créer le menu de correction
        self.menu_correction = tk.Menu(self.master, tearoff=0)

        # Initialiser le vérificateur d'orthographe
        self.spell = SpellChecker(language=var.langue)

        # Initialiser la classe de correction orthographique
        self.correcteur = CorrectionOrthographique(self.text_widget, self.spell, self.menu_correction)

        # Lier les événements
        self.text_widget.bind('<KeyRelease>', self.correcteur.verifier_orthographe)
        self.text_widget.bind('<Button-3>', self.correcteur.afficher_menu_correction)

        # Configurer le tag pour les erreurs
        self.text_widget.tag_configure("erreur", foreground="red", underline=True)
    def langue(self):
        try:
            var.langue = db.tab_param_lire("langue")
        except:
            var.langue = "en"
        print(var.langue)
    def verifier_orthographe(self):
        self.correcteur = CorrectionOrthographique(self.text_widget, self.spell, self.menu_correction)
    def update_text_widget(self):
        self.langue()
        try:
            gettext.find("ScryBook")
            traduction = gettext.translation(var.langue, localedir='src/locale', languages=[var.langue])
            traduction.install()
            print(traduction)
        except:
            gettext.install('ScryBook')
            print("error")
        if hasattr(var, 'text_widget') and var.text_widget is not None:
            self.text_widget.destroy()
        self.text_widget = design.creer_zone_texte(self.frame2)
        self.text_widget.pack(fill=tk.BOTH, expand=True)
        self.text_widget.tag_configure("erreur", foreground="red")

        # Créer le menu de correction
        self.menu_correction = tk.Menu(self.master, tearoff=0)

        # Initialiser le vérificateur d'orthographe
        self.spell = SpellChecker(language=var.langue)

        # Initialiser la classe de correction orthographique
        self.correcteur = CorrectionOrthographique(self.text_widget, self.spell, self.menu_correction)

        # Lier les événements
        self.text_widget.bind('<KeyRelease>', self.correcteur.verifier_orthographe)
        self.text_widget.bind('<Button-3>', self.correcteur.afficher_menu_correction)

        # Configurer le tag pour les erreurs
        self.text_widget.tag_configure("erreur", foreground="red", underline=True)
    def update_txt_resume(self):
        if hasattr(var, 'txt_resume') and var.txt_resume is not None:
            self.txt_resume.destroy()
        self.txt_resume = design.creer_zone_text_resume(self.frame1)
    def update_menu(self):
        if self.menubar is not None:
            self.menubar.destroy()
        self.menubar = design.create_menu()
        self.master.config(menu=self.menubar)
    def update_titre(self):
        if self.lab_nom_projet is not None:
            self.lab_nom_projet.destroy()
        # Créez une police en gras
        bold_font = tkFont.Font(weight="bold")

        # Définissez une largeur fixe pour le label (en pixels)
        label_width = 150  # Ajustez cette valeur selon vos besoins

        self.lab_nom_projet = tk.Label(
            master=self.frame1,
            bg=var.bg_frame_haut,
            text=var.nom,
            #height="auto",
            anchor='center',
            font=bold_font,
            wraplength=label_width,  # Permet le retour à la ligne automatique
            justify='center'  # Centre le texte sur plusieurs lignes
        )
        self.lab_nom_projet.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

        # Assurez-vous que la colonne s'étende
        self.frame1.columnconfigure(0, weight=1)
    def toggle_bold(self):
        current_font = tk.font.Font(font=self.text_widget["font"])
        self.text_widget.tag_configure("bold", font=(current_font.actual("family"), current_font.actual("size"), "bold"))

        try:
            if self.text_widget.tag_ranges("sel"):
                current_tags = self.text_widget.tag_names("sel.first")
                if "bold" in current_tags:
                    self.text_widget.tag_remove("bold", "sel.first", "sel.last")
                else:
                    self.text_widget.tag_add("bold", "sel.first", "sel.last")
        except tk.TclError:
            pass
    def toggle_italic(self):
        current_font = tk.font.Font(font=self.text_widget["font"])
        self.text_widget.tag_configure("italic",
                                      font=(current_font.actual("family"), current_font.actual("size"), "italic"))

        try:
            if self.text_widget.tag_ranges("sel"):
                current_tags = self.text_widget.tag_names("sel.first")
                if "italic" in current_tags:
                    self.text_widget.tag_remove("italic", "sel.first", "sel.last")
                else:
                    self.text_widget.tag_add("italic", "sel.first", "sel.last")
        except tk.TclError:
            pass
    def toggle_sl(self):
        current_font = tk.font.Font(font=self.text_widget["font"])
        self.text_widget.tag_configure("underline", font=(current_font.actual("family"), current_font.actual("size")),
                                      underline=True)

        try:
            if self.text_widget.tag_ranges("sel"):
                current_tags = self.text_widget.tag_names("sel.first")
                if "underline" in current_tags:
                    self.text_widget.tag_remove("underline", "sel.first", "sel.last")
                else:
                    self.text_widget.tag_add("underline", "sel.first", "sel.last")
        except tk.TclError:
            pass
    def item_selected(self, event):
        fct_main.save_projet()
        selected_item = self.list_chapitre.selection()
        result = self.list_chapitre.item(selected_item)["values"]
        try:
            id = str(result[0])
            var.chapitre = id
        except Exception as e:
            print(e)
        fct_main.ouvrir_chapitre(id)
    def right_clic(self, event):
        # create a popup menu
        selected_item = self.list_chapitre.selection()[0]

        rowID = self.list_chapitre.identify('item', event.x, event.y)
        if rowID:
            self.list_chapitre.selection_set(rowID)
            self.list_chapitre.focus_set()
            self.list_chapitre.focus(rowID)

            self.menu_tree = tk.Menu(self.master, tearoff=0)
            self.menu_tree.add_separator()
            self.menu_tree.add_command(label="Résumé", command=self.resume)
            self.menu_tree.add_command(label="Effacer", command=self.delete)
            self.menu_tree.post(event.x_root, event.y_root)
        else:
            pass
    def resume(self):
        sous_fenetre.fenetre_chapitre_resume(var.chapitre)
    def delete(self):
        print("effacer"+var.chapitre)
        id = var.chapitre
        fct_main.delete_chapitre(id, "chapitre")
    def reload_all(self):
        self.master.destroy()
        var.chapitre = ""
        var.path_dossier = ""
        var.app_instance = ""
        var.projet_en_cours = ""
        var.nom = ""
        var.dossier_projet = ""
        root = tk.Tk()
        page_principale = main(root)
        root.protocol("WM_DELETE_WINDOW", quitter)
        root.mainloop()

root = tk.Tk()
page_principale = main(root)
root.protocol("WM_DELETE_WINDOW", quitter)
root.mainloop()