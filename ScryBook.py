import os
import threading
import tkinter as tk
from tkinter import ttk, Menu
import tkinter.font as tkFont
from src import var, design, fct_main, sous_fenetre, thread_maj, verif_ortho, db, languagetool
from textblob import TextBlob
from src.verif_ortho import CorrectionOrthographique
from src.languagetool import correction
from spellchecker import SpellChecker
import re
import gettext
import locale
from tkinter import filedialog
from PIL import Image, ImageTk


global app_instance
app_instance = None
def quitter():
    os._exit(0)
class main:
    def __init__(self, master):
        chemin_repertoire = os.getcwd()
        var.path_dossier = chemin_repertoire
        db.creer_table_param()
            # Obtenir la langue du système
        self.get_theme()
        self.get_lang()
        global app_instance
        self.master = master
        var.app_instance = self
        master.title(var.nom)
        master.geometry("800x600")
        master.iconbitmap('src/logoSb.ico')
        master.title("ScryBook")
        #master.state('zoomed')
        threading.Thread(target=thread_maj.main()).start()

        fct_main.creer_dossier("Projets")
        var.frame_haut = design.creer_frame_haut(master)
        self.frame_main = design.creer_frame_main(master)
        self.frame_bas = design.creer_frame_bas(master)
        self.frame1, self.frame2 = design.creer_sous_frames(self.frame_main)
        self.lab_nom_projet = tk.Label(master=self.frame1, bg=var.bg_frame_haut, text=var.nom, height=2, anchor='w')
        self.frame1.columnconfigure(0, weight=1)
        design.creer_bouton_haut()

        self.but_chapitre = ttk.Button(self.frame1, text=_("Nouveau chapitre"), command=fct_main.nouveau_chapitre).grid(row=2, column=0, padx=5, pady=5)
        self.list_chapitre = design.creer_list_chapitre(self.frame1)
        self.list_chapitre.bind('<ButtonRelease-1>', self.item_selected)
        self.list_chapitre.bind('<Button-3>', self.right_clic)
        self.list_chapitre.bind('<Double-1>', lambda e: self.resume())
        self.txt_resume = design.creer_zone_text_resume(self.frame1)

        self.toolbar = design.creer_toolbar(self.frame2)
        self.bold_button, self.italic_button, self.sl_button, self.corrige, self.inserer_image = design.creer_boutons_toolbar(self.toolbar, self.toggle_bold, self.toggle_italic, self.toggle_sl, self.correcteur, self.inserer_image)

        self.create_tooltip(self.inserer_image, "Ceci est un message d'aide")

        self.text_widget = design.creer_zone_texte(self.frame2)
        self.lab_version = design.creer_label_version(self.frame_bas)
        design.create_menu(self.master)

        self.menu_correction = tk.Menu(self.master, tearoff=0)
        self.spell = SpellChecker(language=var.langue)
        self.text_widget.tag_configure("erreur", foreground="red", underline=True)

#############################################################################
##### Langue                                                            #####
#############################################################################
##### Définir la langue
    def langue(self):
        try:
            var.langue = db.tab_param_lire("langue")
        except:
            var.langue = "en"
##### Récupérer le fichier langue
    def get_lang(self):
        try:
            var.langue = db.tab_param_lire("langue")
            gettext.find("ScryBook")
            traduction = gettext.translation(var.langue, localedir='src/locale', languages=[var.langue])
            traduction.install()
        except:
            gettext.install('ScryBook')
            print("error")

#############################################################################
##### Correcteur                                                        #####
#############################################################################
##### Correcteur d'orthographe
    def correcteur(self, text_widget, spell, menu_correction):
        print('11')
        #correcteur = languagetool.correcteur(self.text_widget, spell, self.menu_correction)
        self.correcteur = CorrectionOrthographique(self.text_widget, self.spell, self.menu_correction)
        #thread = threading.Thread(target=self.correcteur())
        #thread.start()

#############################################################################
##### Widget Texte                                                      #####
#############################################################################
##### MAJ Widget Texte
    def update_text_widget(self):
        self.langue()
        try:
            gettext.find("ScryBook")
            traduction = gettext.translation(var.langue, localedir='src/locale', languages=[var.langue])
            traduction.install()
        except:
            gettext.install('ScryBook')
            print("error")
        if hasattr(var, 'text_widget') and var.text_widget is not None:
            self.text_widget.destroy()
        self.text_widget = design.creer_zone_texte(self.frame2)
        self.text_widget.pack(fill=tk.BOTH, expand=True)
        self.text_widget.tag_configure("erreur", foreground="red")
        self.text_widget.tag_configure("tag_txt", foreground=var.txt_police)
        self.text_widget.tag_add("tag_txt", "1.0", "end")
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

    def create_tooltip(self, widget, text):
        tooltip = None

        def show_tooltip(event=None):
            nonlocal tooltip
            x, y, _, _ = widget.bbox("insert")
            x += widget.winfo_rootx() + 25
            y += widget.winfo_rooty() + 20

            tooltip = tk.Toplevel(widget)
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{x}+{y}")

            label = ttk.Label(tooltip, text=text, background="#ffffe0", relief="solid", borderwidth=1)
            label.pack()

        def hide_tooltip(event=None):
            nonlocal tooltip
            if tooltip:
                tooltip.destroy()
                tooltip = None
##### Txt Mise en gras
    def toggle_bold(self):
        current_font = tk.font.Font(font=self.text_widget["font"])
        self.text_widget.tag_configure("bold",
                                       font=(current_font.actual("family"), current_font.actual("size"), "bold"))

        try:
            if self.text_widget.tag_ranges("sel"):
                current_tags = self.text_widget.tag_names("sel.first")
                if "bold" in current_tags:
                    self.text_widget.tag_remove("bold", "sel.first", "sel.last")
                else:
                    self.text_widget.tag_add("bold", "sel.first", "sel.last")
        except tk.TclError:
            pass
    def ouvrir_fichier(self):
        design.create_menu(self.master)
        design.creer_bouton_haut()
        self.update_text_widget()
        self.update_menu()


##### Txt Mise en Italique
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
##### TxtMise en surlignage
    def toggle_sl(self):
        current_font = tk.font.Font(font=self.text_widget["font"])
        self.text_widget.tag_configure("underline",
                                       font=(current_font.actual("family"), current_font.actual("size")),
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
##### Insérer image
    def inserer_image(self):
        # Ouvrir une boîte de dialogue pour choisir un fichier image
        chemin_fichier = filedialog.askopenfilename(
            title="Choisir une image",
            filetypes=[("Images", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )

        if chemin_fichier:
            try:
                # Ouvrir l'image avec PIL
                image_pil = Image.open(chemin_fichier)

                # Redimensionner l'image si nécessaire (par exemple, max 300x300 pixels)
                image_pil.thumbnail((300, 300))

                # Convertir l'image PIL en PhotoImage Tkinter
                image_tk = ImageTk.PhotoImage(image_pil)

                # Obtenir la position actuelle du curseur
                position_curseur = self.text_widget.index(tk.INSERT)

                # Insérer l'image à la position du curseur
                self.text_widget.insert(position_curseur, " ")  # Insérer un espace avant l'image
                self.text_widget.image_create(position_curseur + " +1c", image=image_tk)
                self.text_widget.insert(tk.INSERT, "\n")  # Insérer un saut de ligne après l'image
                self.text_widget.images = {}
                self.text_widget.images[position_curseur] = image_tk

                # Garder une référence à l'image pour éviter qu'elle ne soit supprimée par le garbage collector
                if not hasattr(self.text_widget, 'images'):
                    self.text_widget.images = {}
                self.text_widget.images[position_curseur] = image_tk

                print(f"Image insérée à la position {position_curseur} : {chemin_fichier}")
            except Exception as e:
                print(f"Erreur lors de l'insertion de l'image : {e}")

    #############################################################################
##### Ouvrir projet                                                     #####
#############################################################################
    def update_txt_resume(self):
        if hasattr(var, 'txt_resume') and var.txt_resume is not None:
            self.txt_resume.destroy()
        self.txt_resume = design.creer_zone_text_resume(self.frame1)
        self.txt_resume.tag_configure("tag_txt", foreground=var.txt_police)
        self.txt_resume.tag_add("tag_txt", "1.0", "end")


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
            bg=var.txt_fond,  # Utilisation de var.txt_fond pour le fond
            fg=var.txt_police,  # Utilisation de var.txt_police pour le texte
            text=var.nom,
            anchor='center',
            font=bold_font,
            wraplength=label_width,  # Permet le retour à la ligne automatique
            justify='center'  # Centre le texte sur plusieurs lignes
        )
        self.lab_nom_projet.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

        # Assurez-vous que la colonne s'étende
        self.frame1.columnconfigure(0, weight=1)

#############################################################################
##### Chapitre                                                          #####
#############################################################################
    def item_selected(self, event):
        id = ""
        threading.Thread(target=fct_main.save_projet()).start()
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

    def get_theme(self):
        theme_colors = {
            "clair": {
                "bg_frame_haut": "#9a9a9a",
                "bg_frame_mid": "#c8c8c8",
                "bg_frame_droit": "#c8c8c8",
                "bg_but": "#c8c8c8",
                "txt_fond": "#ffffff",
                "txt_police": "#000000"
            },
            "sombre": {
                "bg_frame_haut": "#494949",
                "bg_frame_mid": "#7c7b7b",
                "bg_frame_droit": "#7c7b7b",
                "bg_but": "#7c7b7b",
                "txt_fond": "#292929",
                "txt_police": "#ffffff"
            },
            "bleu": {
                "bg_frame_haut": "#327ec6",
                "bg_frame_mid": "#9dc3e7",
                "bg_frame_droit": "#9dc3e7",
                "bg_but": "#327ec6",
                "txt_fond": "#ffffff",
                "txt_police": "#000000"
            },
            "vert": {
                "bg_frame_haut": "#4c925e",
                "bg_frame_mid": "#9de7b0",
                "bg_frame_droit": "#9de7b0",
                "bg_but": "#4c925e",
                "txt_fond": "#9de7b0",
                "txt_police": "#000000"
            }
        }

        theme = db.tab_param_lire("theme")
        if theme in theme_colors:
            for key, value in theme_colors[theme].items():
                setattr(var, key, value)



root = tk.Tk()
page_principale = main(root)
root.protocol("WM_DELETE_WINDOW", quitter)
root.mainloop()