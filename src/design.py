import tkinter as tk
from src import var, fct_main, export_pdf, export_docx, export_epub
from tkinter import font, messagebox
import src.sous_fenetre as sfenetre
from tkinter import ttk


def question_box(title, message):
    var = messagebox.askquestion(title, message)
    resp = False
    if var == "yes":
        resp = True
    else:
        resp = False
    return resp
#### Frame Haut ####
def creer_frame_haut(master):
    frame_haut = tk.Frame(master=master, height=50, bg=var.bg_frame_haut, padx=5, pady=5)
    frame_haut.pack(fill=tk.X)
    return frame_haut
#### Frame Main ####
def creer_frame_main(master):
    frame_main = tk.Frame(master=master, bg=var.bg_frame_mid, padx=5, pady=5)
    frame_main.pack(fill=tk.BOTH, expand=True)
    return frame_main
#### Frame Main ####
def creer_frame_bas(master):
    frame_bas = tk.Frame(master=master, width=25, height=25, bg=var.bg_frame_haut, padx=5, pady=5)
    frame_bas.pack(fill=tk.X)
    return frame_bas
#### Frame Main ####
def creer_sous_frames(frame_main):
    frame1 = tk.Frame(master=frame_main, bg=var.bg_frame_droit, padx=0, pady=0, width=100, relief=tk.SUNKEN)
    frame1.pack(fill=tk.BOTH, side=tk.LEFT)
    frame2 = tk.Frame(master=frame_main, bg=var.bg_frame_droit, padx=5, pady=5)
    frame2.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

    return frame1, frame2

def creer_bouton_haut():

    for widget in var.frame_haut.winfo_children():
        widget.destroy()
    frame_boutons = tk.Frame(var.frame_haut, bg=var.bg_frame_haut)
    frame_boutons.pack(expand=True)
    if var.nom != "":
        ttk.Button(frame_boutons, text="Résumé", command=lambda: sfenetre.fenetre_chapitre_tout(), width=10).pack(side="left", padx=2, pady=2)
        ttk.Button(frame_boutons, text="Personnages", command=sfenetre.fenetre_perso, width=10).pack(side="left", padx=2, pady=2)
        ttk.Button(frame_boutons, text="Lieux", command=sfenetre.fen_lieux_liste, width=10).pack(side="left", padx=2, pady=2)
    else:
        ttk.Button(frame_boutons, text="Nouveau projet", command=fct_main.projet_new, width=15).pack(side="left", padx=2, pady=2)
        ttk.Button(frame_boutons, text="Ouvrir projet", command=fct_main.open_projet, width=15).pack(side="left", padx=2, pady=2)

def creer_toolbar(parent):
    toolbar = tk.Frame(parent)
    toolbar.pack(side="top", fill="x")
    return toolbar

def creer_boutons_toolbar(toolbar, toggle_bold, toggle_italic, toggle_sl):
    bold_button = ttk.Button(toolbar, text="Gras", command=toggle_bold)
    bold_button.pack(side="left", padx=2, pady=2)
    italic_button = ttk.Button(toolbar, text="Italique", command=toggle_italic)
    italic_button.pack(side="left", padx=2, pady=2)
    sl_button = ttk.Button(toolbar, text="Sousligné", command=toggle_sl)
    sl_button.pack(side="left", padx=2, pady=2)
    return bold_button, italic_button, sl_button


def creer_zone_texte(parent):
    # Créer un cadre pour contenir le widget Text et la barre de défilement
    if hasattr(var.app_instance, 'text_widget') and var.app_instance.text_widget.winfo_exists():
        var.app_instance.text_widget.destroy()
    text_widget = tk.Text(parent, wrap="word", undo=True)
    text_widget.config(font=(var.param_police, int(var.param_taille)), padx=20, pady=0, spacing1=4, spacing2=4, spacing3=4)
    text_widget.pack(side="left", expand=True, fill="both")

    text_widget.tag_configure("line_spacing", spacing1=8, spacing2=8, spacing3=8)
    text_widget.tag_add("line_spacing", "1.0", "end")

    text_widget.tag_configure("bold", font=(var.param_police, int(var.param_taille), "bold"))
    text_widget.tag_configure("italic", font=(var.param_police, int(var.param_taille), "italic"))
    text_widget.tag_configure("underline", underline=True)

    return text_widget



def projet_new():
    fct_main.projet_new()

def rac_s(ev=None):
    fct_main.save_projet()

def projet_open():
    fct_main.open_projet()

def projet_save():
    return

def create_menu():
    menubar = tk.Menu()
    menu1 = tk.Menu(menubar, tearoff=0)
    menu1.add_command(label="Nouveau projet", command=projet_new)
    menu1.add_command(label="Ouvrir un Projet", command=projet_open)
    menu1.add_command(label="Sauvegarder  ctrl+s", command=rac_s)
    menubar.add_cascade(label="Fichier", menu=menu1)

    menu2 = tk.Menu(menubar, tearoff=0)
    menu2.add_command(label="Général", command=lambda: sfenetre.ouvrir_fenetre_parametres_edition())
    menu2.add_command(label="Informations", command=lambda: sfenetre.ouvrir_fenetre_parametres_information())
    if var.dossier_projet != "":
        menubar.add_cascade(label="Paramètres", menu=menu2)

    menu3 = tk.Menu(menubar, tearoff=0)
    menu3.add_command(label="PDF", command=lambda : export_pdf.export())
    menu3.add_command(label="Docx", command=lambda: export_docx.export_doc())
    menu3.add_command(label="Epub", command=lambda: export_epub.export())
    if var.dossier_projet != "":
        menubar.add_cascade(label="Export", menu=menu3)

    menubar.bind_all('<Control-s>', rac_s)

    return menubar
def creer_label_version(frame_bas):
    lab_version = tk.Label(master=frame_bas, bg=var.bg_frame_haut, text="ScryBook version :" + var.version)
    lab_version.grid(row=0, column=1, padx=5, pady=5)
    return lab_version

def configurer_tags_texte(text_widget):
    text_widget.tag_configure("bold", font=font.Font(weight="bold"))
    text_widget.tag_configure("italic", font=font.Font(slant="italic"))
#def update_label_nom(new_text):
#    var.lab_nom_projet.config(text=new_text)

