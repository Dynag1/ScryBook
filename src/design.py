import tkinter as tk
import webbrowser
from click import style
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
        ttk.Button(frame_boutons, text=_("Résumé"), command=lambda: sfenetre.fenetre_chapitre_tout(), width=10).pack(side="left", padx=2, pady=2)
        ttk.Button(frame_boutons, text=_("Personnages"), command=sfenetre.fenetre_perso, width=10).pack(side="left", padx=2, pady=2)
        ttk.Button(frame_boutons, text=_("Lieux"), command=sfenetre.fen_lieux_liste, width=10).pack(side="left", padx=2, pady=2)
    else:
        but_nouveau = (ttk.Button(frame_boutons, text=_("Nouveau projet"), command=fct_main.projet_new, width=15))
        but_nouveau.pack(side="left", padx=2, pady=2)
        var.app_instance.create_tooltip(but_nouveau, _("Créer un nouveau projet"))
        but_ouvrir = ttk.Button(frame_boutons, text=_("Ouvrir projet"), command=fct_main.open_projet, width=15)
        but_ouvrir.pack(side="left", padx=2, pady=2)
        var.app_instance.create_tooltip(but_ouvrir, _("Ouvrir un projet existant"))
def creer_list_chapitre(frame1):
    # Créer un style personnalisé
    style = ttk.Style()
    style.theme_use('default')  # Utiliser le thème par défaut comme base

    # Configurer le style pour le Treeview
    style.configure("Custom.Treeview",
                    background=var.txt_fond,
                    foreground=var.txt_police,
                    fieldbackground=var.txt_fond)

    # Configurer le style pour l'en-tête du Treeview
    style.configure("Custom.Treeview.Heading",
                    background=var.txt_fond,
                    foreground=var.txt_police)

    # Créer le Treeview avec le style personnalisé
    list_chapitre = ttk.Treeview(frame1, height=10, columns=("ID", "Numero", "Nom"),
                                 show="headings", style="Custom.Treeview")

    # Configuration des en-têtes
    list_chapitre.heading("ID", text=_("ID"))
    list_chapitre.heading("Numero", text=_("Numéro"))
    list_chapitre.heading("Nom", text=_("Nom"))

    # Configuration des colonnes
    list_chapitre.column("ID", width=0, stretch=tk.NO)
    list_chapitre.column("Numero", width=50, stretch=tk.NO)
    list_chapitre.column("Nom", width=100, stretch=tk.YES)

    # Positionnement du Treeview
    list_chapitre.grid(row=1, column=0, padx=5, pady=5)

    return list_chapitre
def creer_toolbar(parent):
    toolbar = tk.Frame(parent, bg=var.bg_frame_mid)  # Ajout de bg=var.txt_fond
    toolbar.pack(side="top", fill="x")
    return toolbar
def creer_boutons_toolbar(toolbar, toggle_bold, toggle_italic, toggle_sl, corrige, inserer_image):
    style = ttk.Style()
    style.configure('Black.TButton', foreground='white', background='black')
    bold_button = ttk.Button(toolbar, text=_("Gras"), command=toggle_bold, style='Black.TButton')
    bold_button.pack(side="left", padx=2, pady=2)
    italic_button = ttk.Button(toolbar, text=_("Italique"), command=toggle_italic)
    italic_button.pack(side="left", padx=2, pady=2)
    sl_button = ttk.Button(toolbar, text=_("Souligné"), command=toggle_sl)
    sl_button.pack(side="left", padx=2, pady=2)
    corrige_button = ttk.Button(toolbar, text=_("Corriger"), command=corrige)
    #corrige_button.pack(side="left", padx=2, pady=2)
    image_button = ttk.Button(toolbar, text=_("Image"), command=inserer_image)
    #image_button.pack(side="left", padx=2, pady=2)
    return bold_button, italic_button, sl_button, corrige, image_button
def creer_zone_texte(parent):
    # Créer un cadre pour contenir le widget Text et la barre de défilement
    if hasattr(var.app_instance, 'text_widget') and var.app_instance.text_widget.winfo_exists():
        var.app_instance.text_widget.destroy()
    text_widget = tk.Text(parent, wrap="word", undo=True, bg=var.txt_fond, fg=var.txt_police)  # Utilisation de var.txt_police
    text_widget.config(font=(var.param_police, int(var.param_taille)), padx=20, pady=0, spacing1=4, spacing2=4, spacing3=4)
    text_widget.pack(side="left", expand=True, fill="both")

    text_widget.tag_configure("line_spacing", spacing1=8, spacing2=8, spacing3=8)
    text_widget.tag_add("line_spacing", "1.0", "end")

    text_widget.tag_configure("bold", font=(var.param_police, int(var.param_taille), "bold"))
    text_widget.tag_configure("italic", font=(var.param_police, int(var.param_taille), "italic"))
    text_widget.tag_configure("underline", underline=True)

    # Configurer une balise pour le texte avec la couleur définie dans var.txt_police
    text_widget.tag_configure("couleur_texte", foreground=var.txt_police)
    text_widget.tag_add("couleur_texte", "1.0", "end")
    text_widget.tag_configure("justify", justify='center')
    text_widget.tag_add("justify", "1.0", "end")

    return text_widget
def creer_zone_text_resume(parent):
    if hasattr(var.app_instance, 'txt_resume') and var.app_instance.txt_resume.winfo_exists():
        var.app_instance.txt_resume.destroy()

    # Créer un cadre pour contenir le widget Text et la barre de défilement
    frame = tk.Frame(parent)
    frame.grid(row=3, column=0, padx=5, pady=5, sticky='nsew')

    # Configurer le redimensionnement du cadre
    parent.grid_rowconfigure(3, weight=1)
    parent.grid_columnconfigure(0, weight=0)  # Pas de redimensionnement horizontal

    # Créer le widget Text avec une largeur fixe de 18 caractères
    txt_resume = tk.Text(frame, wrap="word", width=18, undo=True, bg=var.txt_fond, fg=var.txt_police)
    txt_resume.tag_configure("couleur_texte", foreground=var.txt_police)
    txt_resume.tag_add("couleur_texte", "1.0", "end")
    txt_resume.grid(row=0, column=0, sticky='nsew')

    # Créer la barre de défilement verticale
    scrollbar = tk.Scrollbar(frame, orient="vertical", command=txt_resume.yview)
    scrollbar.grid(row=0, column=1, sticky='ns')

    # Configurer le widget Text pour utiliser la barre de défilement
    txt_resume.config(yscrollcommand=scrollbar.set)

    # Configurer le redimensionnement à l'intérieur du cadre
    frame.grid_rowconfigure(0, weight=1)  # Permet l'expansion verticale
    frame.grid_columnconfigure(0, weight=0)  # Pas de redimensionnement horizontal pour le Text
    frame.grid_columnconfigure(1, weight=0)  # Pas de redimensionnement pour la scrollbar

    return txt_resume
def projet_new():
    fct_main.projet_new()
def rac_s(ev=None):
    fct_main.save_projet_image()
def projet_open():
    fct_main.open_projet()
def projet_save():
    return
def create_menu(root):
    print("menu")
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TMenubar", background="blue")
    root.option_add('*Menu.Background', var.bg_frame_haut)
    root.option_add('*Menu.Foreground', var.txt_police)

    # Création de la barre de menu
    menubar = tk.Menu(root)
    root.config(menu=menubar)

    menu1 = tk.Menu(menubar, tearoff=0)
    menu1.add_command(label=_("Nouveau projet"), command=projet_new)
    menu1.add_command(label=_("Ouvrir un Projet"), command=projet_open)
    menu1.add_command(label=_("Fermer le projet"), command=lambda: fct_main.close_projet())
    menu1.add_command(label=_("Sauvegarder  ctrl+s"), command=rac_s)
    menubar.add_cascade(label=_("Fichier"), menu=menu1)

    menu2 = tk.Menu(menubar, tearoff=0)
    menu2.add_command(label=_("Général"), command=lambda: sfenetre.ouvrir_fenetre_parametres_edition())
    menu2.add_command(label=_("Informations"), command=lambda: sfenetre.ouvrir_fenetre_parametres_information())
    menubar.add_cascade(label=_("Paramètres"), menu=menu2)

    menu3 = tk.Menu(menubar, tearoff=0)
    menu3.add_command(label=_("PDF"), command=lambda : export_pdf.export())
    menu3.entryconfigure("PDF", state="disabled")
    menu3.add_command(label=_("Docx"), command=lambda: export_docx.exporter_textes_vers_docx())
    menu3.entryconfigure("Docx", state="disabled")
    menu3.add_command(label=_("Epub"), command=lambda: export_epub.exporter_textes_vers_epub())
    menu3.entryconfigure("Epub", state="disabled")
    menubar.add_cascade(label=_("Export"), menu=menu3)
    if var.dossier_projet != "":
        menu3.entryconfigure("PDF", state="normal")
        menu3.entryconfigure("Docx", state="normal")
        menu3.entryconfigure("Epub", state="normal")

    menu4 = tk.Menu(menubar, tearoff=0)
    menu4.add_command(label=_("Readme"), command=lambda: webbrowser.open('https://github.com/Dynag1/ScryBook/blob/master/README.md'))
    menu4.add_command(label=_("Changelog"), command=lambda: webbrowser.open('https://github.com/Dynag1/ScryBook/blob/master/Changelog.md'))
    menu4.add_command(label=_("Site internet"), command=lambda: webbrowser.open('https://prog.dynag.co'))
    menubar.add_cascade(label="?", menu=menu4)

    menubar.bind_all('<Control-s>', rac_s)

    return menubar
def creer_label_version(frame_bas):
    lab_version = tk.Label(master=frame_bas,
                           bg=var.txt_fond,  # Utilisation de var.txt_fond pour le fond
                           fg=var.txt_police,  # Utilisation de var.txt_police pour le texte
                           text=_("ScryBook version :") + var.version)
    lab_version.grid(row=0, column=1, padx=5, pady=5)
    return lab_version


