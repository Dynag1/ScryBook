import sqlite3
import tkinter as tk
from tkinter import ttk, FALSE, TRUE, messagebox, font
import src.db as db
from src import var, fct_main


#################################################
##### Chapitre                              #####
#################################################

##### Créer le chapitre #####
def fenetre_chapitre():
    sous_fenetre = tk.Toplevel()
    sous_fenetre.title("Ajouter un chapitre")
    sous_fenetre.geometry("600x500")

    # Création d'un cadre principal avec padding
    main_frame = ttk.Frame(sous_fenetre, padding="20")
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Frame pour les entrées numéro et nom
    input_frame = ttk.Frame(main_frame)
    input_frame.pack(fill=tk.X, pady=(0, 20))

    # Numéro
    ttk.Label(input_frame, text="Numéro:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
    input_numero = ttk.Entry(input_frame, width=10)
    input_numero.grid(row=0, column=1, sticky=tk.W, padx=(0, 20))

    # Nom
    ttk.Label(input_frame, text="Nom:").grid(row=0, column=2, sticky=tk.W, padx=(0, 10))
    input_nom = ttk.Entry(input_frame)
    input_nom.grid(row=0, column=3, sticky=tk.EW)

    input_frame.columnconfigure(3, weight=1)

    # Résumé
    ttk.Label(main_frame, text="Résumé:").pack(anchor=tk.W, pady=(0, 5))
    text_widget = tk.Text(main_frame, wrap="word", undo=True, height=15)
    text_widget.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

    # Bouton de validation
    ttk.Button(main_frame, text="Valider",
               command=lambda: valider_nom_chapitre(input_nom, text_widget, input_numero, sous_fenetre)
              ).pack(pady=10)

    # Configurer l'expansion
    main_frame.columnconfigure(0, weight=1)
    main_frame.rowconfigure(1, weight=1)

##### Enregistrer le chapitre #####
def valider_nom_chapitre(nom, text_widget, numero, fenetre):
    nom = nom.get()
    numero = numero.get()
    resume = text_widget.get("1.0", tk.END).strip()
    db.new_chapitre(nom, resume, numero)
    db.liste_chapitre()
    fenetre.destroy()

##### Afficher le chapitre #####
def fenetre_chapitre_resume(id):
    sous_fenetre = tk.Toplevel()
    sous_fenetre.title("Résumé")
    sous_fenetre.geometry("680x520")
    sous_fenetre.iconbitmap('src/logoSb.ico')

    # Création d'un cadre pour organiser les widgets
    style = ttk.Style()
    style.configure("Custom.TFrame", background=var.bg_frame_mid)

    frame = ttk.Frame(sous_fenetre, padding="10", style="Custom.TFrame")
    frame.pack(fill=tk.BOTH, expand=True)
    nom = db.lire("chapitre", id, "nom")
    resume = db.lire("chapitre", id, "resume")
    numero = db.lire("chapitre", id, "numero")
    # Label "Nom"
    ttk.Label(frame, text="Numéro:").grid(row=0, column=0, sticky=tk.W, pady=5)
    # Champ de saisie pour le nom
    input_numero = ttk.Entry(frame)
    input_numero.grid(row=0, column=1, sticky=tk.EW, pady=5)
    input_numero.insert(0, numero)

    ttk.Label(frame, text="Résumé:").grid(row=1, column=0, columnspan=4, sticky=tk.W, pady=5)
    ttk.Label(frame, text="Nom:").grid(row=0, column=2, sticky=tk.W, pady=5)

    # Champ de saisie pour le nom
    input_nom = ttk.Entry(frame)
    input_nom.grid(row=0, column=3, sticky=tk.EW, pady=5)
    input_nom.insert(0, nom)
    ttk.Label(frame, text="Résumé:").grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=5)

    text_widget = (tk.Text(frame, wrap="word", undo=True))
    text_widget.grid(row=2, column=0, columnspan=2, pady=10)
    # Effacer tout le contenu existant
    text_widget.delete('1.0', tk.END)
    # Insérer le nouveau contenu
    text_widget.insert(tk.END, resume)
    # Déplacer le curseur au début du texte
    text_widget.mark_set(tk.INSERT, '1.0')
    text_widget.see(tk.INSERT)
    # Bouton de validation
    ttk.Button(frame, text="Mettre a jour", command=lambda: update_nom_chapitre(input_nom.get(), text_widget.get("1.0", tk.END), input_numero.get(), id, sous_fenetre)).grid(
        row=3, column=0, columnspan=2, pady=10)
##### Enregistrer le chapitre #####
def update_nom_chapitre(nom, resume, numero, id, fenetre):
    db.update_chapitre(nom, resume, numero, id)
    db.liste_chapitre()
    fenetre.destroy()
#################################################
##### Persos                                #####
#################################################

##### Fenetre liste persos
def fenetre_perso():
    sous_fenetre = tk.Toplevel()
    sous_fenetre.title("Personnages")
    sous_fenetre.geometry("600x500")
    sous_fenetre.iconbitmap('src/logoSb.ico')

    style = ttk.Style()
    style.configure("Custom.TFrame", background=var.bg_frame_mid)

    # Frame principal avec padding
    frame = ttk.Frame(sous_fenetre, style="Custom.TFrame", padding=10)
    frame.pack(fill=tk.BOTH, expand=True)

    # Frame pour les boutons
    button_frame = ttk.Frame(frame, style="Custom.TFrame")
    button_frame.grid(row=0, column=0, sticky='ew', pady=(0, 10))
    button_frame.columnconfigure(0, weight=1)

    # Créer et configurer le Treeview
    listperso = ttk.Treeview(frame, columns=("ID", "Alias", "Nom", "Prenom", "Sexe"), show="headings")
    for col, width in zip(listperso["columns"], [50, 100, 150, 150, 50]):
        listperso.column(col, width=width, stretch=tk.YES if col != "ID" else tk.NO)
        listperso.heading(col, text=col, command=lambda _col=col: treeview_sort_column(listperso, _col, False))

    # Ajouter des scrollbars
    scrolly = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=listperso.yview)
    scrollx = ttk.Scrollbar(frame, orient=tk.HORIZONTAL, command=listperso.xview)

    # Configurer le Treeview pour utiliser les scrollbars
    listperso.configure(yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)

    # Placer le Treeview et les scrollbars
    listperso.grid(row=1, column=0, sticky='nsew')
    scrolly.grid(row=1, column=1, sticky='ns')
    scrollx.grid(row=2, column=0, sticky='ew')

    # Configurer l'expansion du grid
    frame.grid_rowconfigure(1, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    def remplir_treeview():
        try:
            with sqlite3.connect(var.dossier_projet + '/dbgene') as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM perso")
                rows = cursor.fetchall()

            listperso.delete(*listperso.get_children())
            for row in rows:
                listperso.insert("", "end", values=row)
        except sqlite3.Error as e:
            messagebox.showerror("Erreur de base de données", f"Impossible de récupérer les données : {e}")

    def nouveau_personnage():
        fen_perso("x")

    def ouvrir_personnage():
        selection = listperso.selection()
        if not selection:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner un personnage.")
            return

        personnage_id = listperso.item(selection[0])['values'][0]
        fen_perso(personnage_id)

    def supprimer_personnage():
        selection = listperso.selection()
        if not selection:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner un personnage à supprimer.")
            return

        personnage_id = listperso.item(selection[0])['values'][0]

        if messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir supprimer ce personnage ?"):
            try:
                with sqlite3.connect(var.dossier_projet + '/dbgene') as conn:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM perso WHERE id=?", (personnage_id,))
                    conn.commit()

                remplir_treeview()
                messagebox.showinfo("Succès", "Le personnage a été supprimé avec succès.")
            except sqlite3.Error as e:
                messagebox.showerror("Erreur de base de données", f"Impossible de supprimer le personnage : {e}")

    def treeview_sort_column(tv, col, reverse):
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)
        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)
        tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))

    # Boutons
    ttk.Button(button_frame, text="Nouveau personnage", command=nouveau_personnage).pack(side=tk.LEFT, padx=(0, 5))
    ttk.Button(button_frame, text="Ouvrir", command=ouvrir_personnage).pack(side=tk.LEFT)
    ttk.Button(button_frame, text="Supprimer", command=supprimer_personnage).pack(side=tk.LEFT, padx=(5, 0))
    ttk.Button(button_frame, text="Rafraîchir", command=remplir_treeview).pack(side=tk.LEFT, padx=(5, 0))

    # Binding pour double-clic
    listperso.bind('<Double-1>', lambda e: ouvrir_personnage())

    # Remplir le Treeview à l'ouverture de la fenêtre
    remplir_treeview()

    sous_fenetre.mainloop()

##### Fenetre détail persos
def fen_perso(id):
    sous_fenetre = tk.Toplevel()
    sous_fenetre.title("Détails du Personnage")
    sous_fenetre.geometry("500x600")

    style = ttk.Style()
    style.configure("Custom.TFrame", background=var.bg_frame_mid)

    main_frame = ttk.Frame(sous_fenetre, style="Custom.TFrame")
    main_frame.pack(fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(main_frame, bg=var.bg_frame_mid)
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas, style="Custom.TFrame")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    def creer_champ(label_text, row, widget_type=ttk.Entry):
        label = ttk.Label(scrollable_frame, text=label_text, background=var.bg_frame_mid)
        label.grid(row=row, column=0, sticky="w", pady=5, padx=5)
        widget = widget_type(scrollable_frame)
        widget.grid(row=row, column=1, sticky="ew", pady=5, padx=5)
        scrollable_frame.grid_columnconfigure(1, weight=1)
        return widget

    alias = creer_champ("Alias:", 0)
    nom = creer_champ("Nom:", 1)
    prenom = creer_champ("Prénom:", 2)
    sexe = creer_champ("Sexe:", 3)
    age = creer_champ("Âge:", 4)
    desc_phys = creer_champ("Description physique:", 5, widget_type=lambda parent: tk.Text(parent, height=4, wrap=tk.WORD))
    desc_glob = creer_champ("Description globale:", 6, widget_type=lambda parent: tk.Text(parent, height=4, wrap=tk.WORD))
    skill = creer_champ("Compétences:", 7, widget_type=lambda parent: tk.Text(parent, height=4, wrap=tk.WORD))

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def sauvegarder():
        alias_val = alias.get()
        nom_val = nom.get()
        prenom_val = prenom.get()
        sexe_val = sexe.get()
        age_val = age.get()
        desc_phys_val = desc_phys.get("1.0", tk.END).strip()
        desc_glob_val = desc_glob.get("1.0", tk.END).strip()
        skill_val = skill.get("1.0", tk.END).strip()

        conn = sqlite3.connect(var.dossier_projet + '/dbgene')
        cursor = conn.cursor()

        if id == "x":
            cursor.execute('''
            INSERT INTO perso (alias, nom, prenom, sexe, age, desc_phys, desc_global, skill)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (alias_val, nom_val, prenom_val, sexe_val, age_val, desc_phys_val, desc_glob_val, skill_val))
        else:
            cursor.execute('''
            UPDATE perso
            SET alias=?, nom=?, prenom=?, sexe=?, age=?, desc_phys=?, desc_global=?, skill=?
            WHERE id=?
            ''', (alias_val, nom_val, prenom_val, sexe_val, age_val, desc_phys_val, desc_glob_val, skill_val, id))

        conn.commit()
        conn.close()
        sous_fenetre.destroy()

    button_frame = ttk.Frame(sous_fenetre, style="Custom.TFrame")
    button_frame.pack(side="bottom", fill="x", padx=10, pady=10)

    save_button = ttk.Button(button_frame, text="Sauvegarder", command=sauvegarder)
    save_button.pack(expand=True)

    def get_perso_data():
        conn = sqlite3.connect(var.dossier_projet + '/dbgene')
        cursor = conn.cursor()

        query = "SELECT alias, nom, prenom, sexe, age, desc_phys, desc_global, skill FROM perso WHERE id=? LIMIT 1"
        cursor.execute(query, (id,))
        data = cursor.fetchone()

        conn.close()
        return data
    data = get_perso_data()
    if data:
        alias.insert(0, data[0])
        nom.insert(0, data[1])
        prenom.insert(0, data[2])
        sexe.insert(0, data[3])
        age.insert(0, str(data[4]))
        desc_phys.insert("1.0", data[5])
        desc_glob.insert("1.0", data[6])
        skill.insert("1.0", data[7])
    else:
        print("Aucune donnée trouvée dans la table perso")

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    scrollable_frame.bind("<Configure>", on_frame_configure)

    def on_canvas_configure(event):
        canvas.itemconfig(canvas.create_window((0, 0), window=scrollable_frame, anchor="nw"), width=event.width)

    canvas.bind("<Configure>", on_canvas_configure)

    sous_fenetre.mainloop()

def ouvrir_fenetre_parametres():
    fenetre_param = tk.Toplevel()
    fenetre_param.title("Paramètres")
    fenetre_param.geometry("300x200")

    # Récupérer la liste des polices système
    polices_systeme = list(font.families())
    polices_systeme.sort()

    # Récupérer les valeurs actuelles de la police et de la taille depuis la base de données
    conn = sqlite3.connect(var.dossier_projet + "/dbgene")
    cursor = conn.cursor()
    cursor.execute("SELECT police, taille FROM param WHERE id = 1")
    result = cursor.fetchone()
    police_actuelle, taille_actuelle = result if result else ('', '12')
    conn.close()

    # Sélection de la police
    tk.Label(fenetre_param, text="Police :").pack(pady=5)
    var_police = tk.StringVar(value=police_actuelle)
    combo_police = ttk.Combobox(fenetre_param, textvariable=var_police, values=polices_systeme)
    combo_police.pack(pady=5)

    # Sélection de la taille
    tk.Label(fenetre_param, text="Taille :").pack(pady=5)
    tailles = list(range(10, 21))
    var_taille = tk.StringVar(value=taille_actuelle)
    combo_taille = ttk.Combobox(fenetre_param, textvariable=var_taille, values=tailles)
    combo_taille.pack(pady=5)

    # Bouton Sauvegarder
    def sauvegarder():
        var.param_police = var_police.get()
        var.param_taille = var_taille.get()
        db.tab_param_update(var_police.get(), var_taille.get())

        fenetre_param.destroy()

    tk.Button(fenetre_param, text="Sauvegarder", command=sauvegarder).pack(pady=10)

    # Modifier la taille de la police pour les listes déroulantes
    style = ttk.Style()
    style.configure("TCombobox", font=("TkDefaultFont", 12))
    fenetre_param.option_add("*TCombobox*Listbox.font", ("TkDefaultFont", 12))

    fenetre_param.mainloop()
