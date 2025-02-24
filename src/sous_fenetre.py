import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, font
from src import var, db


#################################################
##### Chapitre                              #####
#################################################

##### Créer le chapitre #####
def fenetre_chapitre():
    bg_color = var.bg_frame_mid

    sous_fenetre = tk.Toplevel()
    sous_fenetre.title("Ajouter un chapitre")
    sous_fenetre.geometry("680x520")
    sous_fenetre.iconbitmap('src/logoSb.ico')
    sous_fenetre.configure(bg=bg_color)

    style = ttk.Style()
    style.configure("Custom.TFrame", background=bg_color)
    style.configure("TLabel", background=bg_color)
    style.configure("TButton", background=bg_color)

    frame = ttk.Frame(sous_fenetre, padding="10", style="Custom.TFrame")
    frame.pack(fill=tk.BOTH, expand=True)

    # Numéro
    ttk.Label(frame, text="Numéro:").grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
    input_numero = ttk.Entry(frame)
    input_numero.grid(row=0, column=1, sticky=tk.EW, pady=5, padx=5)

    # Nom
    ttk.Label(frame, text="Nom:").grid(row=0, column=2, sticky=tk.W, pady=5, padx=5)
    input_nom = ttk.Entry(frame)
    input_nom.grid(row=0, column=3, sticky=tk.EW, pady=5, padx=5)

    # Résumé
    ttk.Label(frame, text="Résumé:").grid(row=1, column=0, columnspan=4, sticky=tk.W, pady=5, padx=5)
    text_widget = tk.Text(frame, wrap="word", undo=True, height=20)
    text_widget.grid(row=2, column=0, columnspan=4, sticky=tk.NSEW, pady=5, padx=5)

    # Bouton de validation
    ttk.Button(frame, text="Valider",
               command=lambda: valider_nom_chapitre(input_nom, text_widget, input_numero, sous_fenetre)).grid(
        row=3, column=0, columnspan=4, pady=10)

    # Configuration des colonnes pour qu'elles s'étendent
    for i in range(4):
        frame.columnconfigure(i, weight=1)

    # Configuration des lignes pour qu'elles s'étendent
    frame.rowconfigure(2, weight=1)

    def valider_nom_chapitre(nom, text_widget, numero, fenetre):
        nom = nom.get()
        numero = numero.get()
        resume = text_widget.get("1.0", tk.END).strip()
        db.new_chapitre(nom, resume, numero)
        db.liste_chapitre()
        fenetre.destroy()

    sous_fenetre.mainloop()
##### Afficher le chapitre #####
def fenetre_chapitre_resume(id):
    bg_color = var.bg_frame_mid

    sous_fenetre = tk.Toplevel()
    sous_fenetre.title("Résumé")
    sous_fenetre.geometry("680x520")
    sous_fenetre.iconbitmap('src/logoSb.ico')
    sous_fenetre.configure(bg=bg_color)

    style = ttk.Style()
    style.configure("Custom.TFrame", background=bg_color)
    style.configure("TLabel", background=bg_color)
    style.configure("TButton", background=bg_color)

    frame = ttk.Frame(sous_fenetre, padding="10", style="Custom.TFrame")
    frame.pack(fill=tk.BOTH, expand=True)

    nom = db.lire("chapitre", id, "nom")
    resume = db.lire("chapitre", id, "resume")
    numero = db.lire("chapitre", id, "numero")

    # Numéro
    ttk.Label(frame, text="Numéro:").grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
    input_numero = ttk.Entry(frame)
    input_numero.grid(row=0, column=1, sticky=tk.EW, pady=5, padx=5)
    input_numero.insert(0, numero)

    # Nom
    ttk.Label(frame, text="Nom:").grid(row=0, column=2, sticky=tk.W, pady=5, padx=5)
    input_nom = ttk.Entry(frame)
    input_nom.grid(row=0, column=3, sticky=tk.EW, pady=5, padx=5)
    input_nom.insert(0, nom)

    # Résumé
    ttk.Label(frame, text="Résumé:").grid(row=1, column=0, columnspan=4, sticky=tk.W, pady=5, padx=5)
    text_widget = tk.Text(frame, wrap="word", undo=True, height=20)
    text_widget.grid(row=2, column=0, columnspan=4, sticky=tk.NSEW, pady=5, padx=5)
    text_widget.delete('1.0', tk.END)
    text_widget.insert(tk.END, resume)
    text_widget.mark_set(tk.INSERT, '1.0')
    text_widget.see(tk.INSERT)

    # Bouton de validation
    ttk.Button(frame, text="Mettre à jour",
               command=lambda: update_nom_chapitre(input_nom.get(), text_widget.get("1.0", tk.END), input_numero.get(),
                                                   id, sous_fenetre)).grid(
        row=3, column=0, columnspan=4, pady=10)

    # Configuration des colonnes pour qu'elles s'étendent
    for i in range(4):
        frame.columnconfigure(i, weight=1)

    # Configuration des lignes pour qu'elles s'étendent
    frame.rowconfigure(2, weight=1)

    def update_nom_chapitre(nom, resume, numero, id, fenetre):
        db.update_chapitre(nom, resume, numero, id)
        db.liste_chapitre()
        fenetre.destroy()

    sous_fenetre.mainloop()
def fenetre_chapitre_tout():

    bg_color = var.bg_frame_mid

    fenetre = tk.Toplevel()
    fenetre.title("Liste des chapitres")
    fenetre.geometry("800x600")
    fenetre.configure(bg=bg_color)

    style = ttk.Style()
    style.configure("Custom.TFrame", background=bg_color)
    style.configure("TLabel", background=bg_color)
    style.configure("TButton", background=bg_color)

    frame = ttk.Frame(fenetre, padding="10", style="Custom.TFrame")
    frame.pack(fill=tk.BOTH, expand=True)

    # Création d'un canvas avec scrollbar
    canvas = tk.Canvas(frame, bg=bg_color)
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas, style="Custom.TFrame")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Récupération des données de la base de données
    conn = sqlite3.connect(var.dossier_projet + '/dbchapitre')
    cursor = conn.cursor()
    cursor.execute("SELECT numero, nom, resume FROM chapitre ORDER BY numero")
    chapitres = cursor.fetchall()
    conn.close()

    # Affichage des chapitres
    for i, (numero, nom, resume) in enumerate(chapitres):
        ttk.Label(scrollable_frame, text=f"Chapitre {numero}", font=("TkDefaultFont", 12, "bold")).grid(row=i * 3,
                                                                                                        column=0,
                                                                                                        sticky="w",
                                                                                                        pady=(
                                                                                                        10, 0))
        ttk.Label(scrollable_frame, text=f"Nom: {nom}").grid(row=i * 3 + 1, column=0, sticky="w")
        text_widget = tk.Text(scrollable_frame, wrap="word", height=4, width=80)
        text_widget.insert(tk.END, resume)
        text_widget.config(state="disabled")
        text_widget.grid(row=i * 3 + 2, column=0, sticky="w", pady=(0, 10))

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    fenetre.mainloop()
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
        sous_fenetre.destroy()
        fen_perso("x")

    def ouvrir_personnage():
        selection = listperso.selection()
        if not selection:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner un personnage.")
            return

        personnage_id = listperso.item(selection[0])['values'][0]
        sous_fenetre.destroy()
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

##### Fenetre détail perso
def fen_perso(id):
    bg_color = var.bg_frame_mid  # Utilisation de la couleur de fond définie dans var

    sous_fenetre = tk.Toplevel()
    sous_fenetre.title("Détails du Personnage")
    sous_fenetre.geometry("500x600")
    sous_fenetre.configure(bg=bg_color)

    style = ttk.Style()
    style.configure("Custom.TFrame", background=bg_color)
    style.configure("TButton", background=bg_color)
    style.configure("TLabel", background=bg_color)
    # Ne pas modifier le style des Entry pour garder leur couleur par défaut

    # Créer le cadre pour les boutons en haut
    button_frame = ttk.Frame(sous_fenetre, style="Custom.TFrame")
    button_frame.pack(side="top", fill="x", padx=10, pady=10)

    # Créer un sous-frame pour centrer les boutons
    center_frame = ttk.Frame(button_frame, style="Custom.TFrame")
    center_frame.pack(expand=True)

    # Ajouter les boutons au sous-frame centré
    ttk.Button(center_frame, text="Sauvegarder", command=lambda: sauvegarder()).pack(side="left", padx=5)
    ttk.Button(center_frame, text="Annuler", command=lambda: annule()).pack(side="left", padx=5)

    main_frame = ttk.Frame(sous_fenetre, style="Custom.TFrame")
    main_frame.pack(fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(main_frame, bg=bg_color)
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas, style="Custom.TFrame")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    def creer_champ(label_text, row, widget_type=ttk.Entry):
        label = ttk.Label(scrollable_frame, text=label_text, style="TLabel")
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
        fenetre_perso()

    def annule():
        sous_fenetre.destroy()
        fenetre_perso()

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

#################################################
##### Lieux                                 #####
#################################################
def fen_lieux_liste():
    sous_fenetre = tk.Toplevel()
    sous_fenetre.title("Lieux")
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
    listperso = ttk.Treeview(frame, columns=("ID", "Nom", "Description", "Tag"), show="headings")
    for col, width in zip(listperso["columns"], [50, 100, 150, 150]):
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
                cursor.execute("SELECT * FROM lieux")
                rows = cursor.fetchall()

            listperso.delete(*listperso.get_children())
            for row in rows:
                listperso.insert("", "end", values=row)
        except sqlite3.Error as e:
            messagebox.showerror("Erreur de base de données", f"Impossible de récupérer les données : {e}")

    def nouveau_personnage():
        sous_fenetre.destroy()
        fen_lieux("x")


    def ouvrir_personnage():
        selection = listperso.selection()
        if not selection:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner un personnage.")
            return

        personnage_id = listperso.item(selection[0])['values'][0]
        sous_fenetre.destroy()
        fen_lieux(personnage_id)

    def supprimer_personnage():
        selection = listperso.selection()
        if not selection:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner un lieu à supprimer.")
            return

        personnage_id = listperso.item(selection[0])['values'][0]

        if messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir supprimer ce lieu ?"):
            try:
                with sqlite3.connect(var.dossier_projet + '/dbgene') as conn:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM lieux WHERE id=?", (personnage_id,))
                    conn.commit()

                remplir_treeview()
                messagebox.showinfo("Succès", "Le lieu a été supprimé avec succès.")
            except sqlite3.Error as e:
                messagebox.showerror("Erreur de base de données", f"Impossible de supprimer le personnage : {e}")

    def treeview_sort_column(tv, col, reverse):
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)
        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)
        tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))

    # Boutons
    ttk.Button(button_frame, text="Nouveau lieu", command=nouveau_personnage).pack(side=tk.LEFT, padx=(0, 5))
    ttk.Button(button_frame, text="Ouvrir", command=ouvrir_personnage).pack(side=tk.LEFT)
    ttk.Button(button_frame, text="Supprimer", command=supprimer_personnage).pack(side=tk.LEFT, padx=(5, 0))
    ttk.Button(button_frame, text="Rafraîchir", command=remplir_treeview).pack(side=tk.LEFT, padx=(5, 0))

    # Binding pour double-clic
    listperso.bind('<Double-1>', lambda e: ouvrir_personnage())

    # Remplir le Treeview à l'ouverture de la fenêtre
    remplir_treeview()

    sous_fenetre.mainloop()

##### Fenetre détail Lieux
def fen_lieux(id):
    bg_color = var.bg_frame_mid

    sous_fenetre = tk.Toplevel()
    sous_fenetre.title("Détails du lieu")
    sous_fenetre.geometry("500x500")
    sous_fenetre.configure(bg=bg_color)

    style = ttk.Style()
    style.configure("Custom.TFrame", background=bg_color)
    style.configure("TButton", background=bg_color)
    style.configure("TLabel", background=bg_color)

    # Créer le cadre pour les boutons en haut
    button_frame = ttk.Frame(sous_fenetre, style="Custom.TFrame")
    button_frame.pack(side="top", fill="x", padx=10, pady=10)

    # Créer un sous-frame pour centrer les boutons
    center_frame = ttk.Frame(button_frame, style="Custom.TFrame")
    center_frame.pack(expand=True)

    # Ajouter les boutons au sous-frame centré
    ttk.Button(center_frame, text="Sauvegarder", command=lambda: sauvegarder()).pack(side="left", padx=5)
    ttk.Button(center_frame, text="Annuler", command=lambda: annule()).pack(side="left", padx=5)

    main_frame = ttk.Frame(sous_fenetre, style="Custom.TFrame")
    main_frame.pack(fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(main_frame, bg=bg_color)
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas, style="Custom.TFrame")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    def creer_champ(label_text, row, widget_type=ttk.Entry):
        label = ttk.Label(scrollable_frame, text=label_text, style="TLabel")
        label.grid(row=row, column=0, sticky="w", pady=5, padx=5)
        widget = widget_type(scrollable_frame)
        widget.grid(row=row, column=1, sticky="ew", pady=5, padx=5)
        scrollable_frame.grid_columnconfigure(1, weight=1)
        return widget

    nom = creer_champ("Nom:", 0)
    desc = creer_champ("Description:", 1, widget_type=lambda parent: tk.Text(parent, height=20, wrap=tk.WORD))

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def sauvegarder():
        nom_val = nom.get()
        desc_val = desc.get("1.0", tk.END).strip()

        conn = sqlite3.connect(var.dossier_projet + '/dbgene')
        cursor = conn.cursor()

        if id == "x":
            cursor.execute('''
            INSERT INTO lieux (nom, desc)
            VALUES (?, ?)
            ''', (nom_val, desc_val))
        else:
            cursor.execute('''
            UPDATE lieux
            SET nom=?, desc=?
            WHERE id=?
            ''', (nom_val, desc_val, id))

        conn.commit()
        conn.close()
        sous_fenetre.destroy()
        fen_lieux_liste()

    def annule():
        sous_fenetre.destroy()
        fen_lieux_liste()

    def get_perso_data():
        conn = sqlite3.connect(var.dossier_projet + '/dbgene')
        cursor = conn.cursor()

        query = "SELECT nom, desc FROM lieux WHERE id=?"
        cursor.execute(query, (id,))
        data = cursor.fetchone()

        conn.close()
        return data

    data = get_perso_data()
    if data:
        nom.insert(0, data[0])
        desc.insert("1.0", data[1])
    else:
        print("Aucune donnée trouvée dans la table lieux")

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    scrollable_frame.bind("<Configure>", on_frame_configure)

    def on_canvas_configure(event):
        canvas.itemconfig(canvas.create_window((0, 0), window=scrollable_frame, anchor="nw"), width=event.width)

    canvas.bind("<Configure>", on_canvas_configure)

    sous_fenetre.mainloop()

#################################################
##### Parametres                            #####
#################################################
##### Parametres Police
def ouvrir_fenetre_parametres_edition():
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
##### Fenetre informations
def ouvrir_fenetre_parametres_information():
    sous_fenetre = tk.Toplevel()
    sous_fenetre.title("Informations")
    sous_fenetre.geometry("500x400")

    style = ttk.Style()
    style.configure("Custom.TFrame", background=var.bg_frame_mid)

    main_frame = ttk.Frame(sous_fenetre, style="Custom.TFrame", padding=10)
    main_frame.pack(fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(main_frame, bg=var.bg_frame_mid, highlightthickness=0)
    scrollable_frame = ttk.Frame(canvas, style="Custom.TFrame")

    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    def on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    canvas.bind_all("<MouseWheel>", on_mousewheel)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    def creer_champ(label_text, row, widget_type=ttk.Entry):
        label = ttk.Label(scrollable_frame, text=label_text, background=var.bg_frame_mid)
        label.grid(row=row, column=0, sticky="w", pady=5, padx=5)
        widget = widget_type(scrollable_frame)
        widget.grid(row=row, column=1, sticky="ew", pady=5, padx=5)
        scrollable_frame.grid_columnconfigure(1, weight=1)
        return widget

    titre = creer_champ("Titre:", 0)
    sous_titre = creer_champ("Sous Titre:", 1)
    auteur = creer_champ("Auteur:", 2)
    date = creer_champ("Date:", 3)
    resume = creer_champ("Résumé:", 4, widget_type=lambda parent: tk.Text(parent, height=4, wrap=tk.WORD))

    canvas.pack(side="left", fill="both", expand=True)

    # Le reste du code reste inchangé


    def sauvegarder():
        titre_val = titre.get()
        sous_titre_val = sous_titre.get()
        auteur_val = auteur.get()
        date_val = date.get()
        resume_val = resume.get("1.0", tk.END).strip()


        conn = sqlite3.connect(var.dossier_projet + '/dbgene')
        cursor = conn.cursor()


        cursor.execute('''
        UPDATE info
        SET titre=?, stitre=?, auteur=?, date=?, resume=?
        WHERE id=?
        ''', (titre_val, sous_titre_val, auteur_val, date_val, resume_val, 1))

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

        query = "SELECT titre, stitre, auteur, date, resume FROM info WHERE id=1"
        cursor.execute(query)
        data = cursor.fetchone()

        conn.close()
        return data
    data = get_perso_data()
    if data:
        titre.insert(0, data[0])
        sous_titre.insert(0, data[1])
        auteur.insert(0, data[2])
        date.insert(0, data[3])
        resume.insert("1.0", data[4])

    else:
        print("Aucune donnée trouvée dans la table perso")

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    scrollable_frame.bind("<Configure>", on_frame_configure)

    def on_canvas_configure(event):
        canvas.itemconfig(canvas.create_window((0, 0), window=scrollable_frame, anchor="nw"), width=event.width)

    canvas.bind("<Configure>", on_canvas_configure)

    sous_fenetre.mainloop()