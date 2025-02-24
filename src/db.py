import sqlite3
import src.fct_main as fct_main
import src.var as var
import tkinter as tk
########################################
##### Chapitres                    #####
########################################
##### Créer la table des chapitres #####
def creer_table_chapitre(chemin):
    # Connexion à la base de données (elle sera créée si elle n'existe pas)
    conn = sqlite3.connect(chemin + '/dbchapitre')

    # Création d'un objet curseur pour exécuter les commandes SQL
    cursor = conn.cursor()

##### Table chapitre
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='chapitre'")
    table_existe = cursor.fetchone()

    if not table_existe:
        # Création de la table si elle n'existe pas
        cursor.execute('''CREATE TABLE chapitre (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            numero TEXT NOT NULL,
            resume TEXT NOT NULL
        )''')
    else:
        # Vérification et ajout des colonnes manquantes si la table existe déjà
        colonnes_existantes = [row[1] for row in cursor.execute("PRAGMA table_info(chapitre)").fetchall()]

        if 'nom' not in colonnes_existantes:
            cursor.execute("ALTER TABLE chapitre ADD COLUMN nom TEXT NOT NULL DEFAULT ''")

        if 'numero' not in colonnes_existantes:
            cursor.execute("ALTER TABLE chapitre ADD COLUMN numero TEXT NOT NULL DEFAULT ''")

        if 'resume' not in colonnes_existantes:
            cursor.execute("ALTER TABLE chapitre ADD COLUMN resume TEXT NOT NULL DEFAULT ''")

    # Validation des changements et fermeture de la connexion
    conn.commit()
    conn.close()
##### Nouveau Chapitre #####
def new_chapitre(nom, resume, numero):
    conn = sqlite3.connect(var.dossier_projet+"/dbchapitre")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chapitre (nom, resume, numero) VALUES (?, ?, ?)", (nom, resume, numero))
    conn.commit()
    conn.close()
    liste_chapitre()
##### Mise à jour chapitre #####
def update_chapitre(nom, resume, numero, id):
    conn = sqlite3.connect(var.dossier_projet+"/dbchapitre")
    cursor = conn.cursor()
    cursor.execute("UPDATE chapitre SET nom = ?, resume = ?, numero = ? WHERE id = ?", (nom, resume, numero, id))
    conn.commit()
    conn.close()
    liste_chapitre()
##### Lister les chapitres #####
def liste_chapitre():
    # Connexion à la base de données
    global cursor
    try:
        conn = sqlite3.connect(var.dossier_projet+"/dbchapitre")
        cursor = conn.cursor()
    except Exception as e:
        fct_main.logs(e)
    # Récupération des données
    try:
        cursor.execute("SELECT * FROM chapitre ORDER BY numero")
        donnees = cursor.fetchall()
    except Exception as e:
        print(e)
    # Insertion des données dans le Treeview
    for item in var.list_chapitre.get_children():
        var.list_chapitre.delete(item)
    for ligne in donnees:
        valeurs_reordonnees = (ligne[0], ligne[2], ligne[1])
        var.list_chapitre.insert("", tk.END, values=valeurs_reordonnees)

    # Fermeture de la connexion
    conn.close()
##### Effacer un chapitre #####
def effacer(id, type):
    if type == "chapitre":
        try:
            conn = sqlite3.connect(var.dossier_projet + "/dbchapitre")
            cursor = conn.cursor()
        except Exception as e:
            fct_main.logs(e)
        cursor.execute("DELETE FROM chapitre WHERE id = ?", (id,))

        # Validation des changements
        conn.commit()
        conn.close()
##### Lire #####
def lire(type, id, varia, curseur=None):
    if type == "chapitre":
        try:
            conn = sqlite3.connect(var.dossier_projet + "/dbchapitre")
            cursor = conn.cursor()
        except Exception as e:
            fct_main.logs(e)

        requete = "SELECT "+varia+" FROM chapitre WHERE id = ?"
        cursor.execute(requete, (id,))
        resultat = cursor.fetchone()
        if resultat:
            texte = str(resultat[0])

    return texte

def creer_table_gene(chemin):
    # Connexion à la base de données (la crée si elle n'existe pas)
    conn = sqlite3.connect(chemin+'/dbgene')
    cursor = conn.cursor()


    # Création des tables si elles n'existent pas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS perso (
            id INTEGER PRIMARY KEY AUTOINCREMENT
        )
        ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lieux (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT,
            desc TEXT
        )
        ''')

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS info (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titre TEXT,
                stitre TEXT,
                auteur TEXT,
                date TEXT,
                resume TEXT
            )
            ''')
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS param (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    police TEXT,
                    taille TEXT,
                    save_time
                )
                ''')

    # Définition des champs attendus pour chaque table
    champs_attendus = {
        'perso': {
            'alias': 'TEXT',
            'nom': 'TEXT',
            'prenom': 'TEXT',
            'sexe': 'TEXT',
            'age': 'INTEGER',
            'desc_phys': 'TEXT',
            'desc_global': 'TEXT',
            'skill': 'TEXT'
        },
        'lieux': {
            'nom': 'TEXT',
            'desc': 'TEXT'
        },
        'info': {
            'titre': 'TEXT',
            'stitre': 'TEXT',
            'auteur': 'TEXT',
            'date': 'TEXT',
            'resume': 'TEXT'
        },
        'param': {
            'police': 'TEXT',
            'taille': 'TEXT',
            'save_time': 'TEXT'
        }
    }

    # Vérification et ajout des champs manquants pour chaque table
    for table, champs in champs_attendus.items():
        cursor.execute(f"PRAGMA table_info({table})")
        colonnes_existantes = [colonne[1] for colonne in cursor.fetchall()]

        for champ, type_champ in champs.items():
            if champ not in colonnes_existantes:
                cursor.execute(f"ALTER TABLE {table} ADD COLUMN {champ} {type_champ}")
                print(f"Champ '{champ}' ajouté à la table '{table}'.")



    conn.commit()

    cursor.execute("SELECT EXISTS(SELECT 1 FROM info WHERE id=1)")
    row_exists = cursor.fetchone()[0]

    if not row_exists:
        # Insérer les données dans la table 'info' si la ligne n'existe pas
        cursor.execute("INSERT INTO info (auteur, date, resume) VALUES (?, ?, ?)", ("auteur", "date", "resume"))
    cursor.execute("SELECT EXISTS(SELECT 1 FROM param WHERE id=1)")
    row_exists1 = cursor.fetchone()[0]
    if not row_exists1:
        # Insérer les données dans la table 'param'
        cursor.execute("INSERT INTO param (police, taille, save_time) VALUES (?, ?, ?)", ("Helvetica", "12", "30"))

    conn.commit()
    conn.close()
    var.param_police = "Helvetica"
    var.param_taille = "12"
    print("Base de données 'dbgene' et tables mises à jour avec succès.")

def tab_gene_del(id, table):
    try:
        conn = sqlite3.connect(var.dossier_projet + '/dbgene')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM " + table + " WHERE id = ?", (id,))
        # Validation des changements
        conn.commit()
        conn.close()
    except Exception as e:
        fct_main.logs(e)
def tab_info_update(auteur, date, resume):
    try:
        conn = sqlite3.connect(var.dossier_projet + '/dbgene')
        cursor = conn.cursor()
        cursor.execute("UPDATE info SET auteur = ?, date = ?, resume = ? WHERE id = ?", (auteur, date, resume, 1))
        conn.commit()
        conn.close()
    except Exception as e:
        fct_main.logs(e)
def tab_param_update(police, taille, save):
    try:
        conn = sqlite3.connect(var.dossier_projet + '/dbgene')
        cursor = conn.cursor()
        cursor.execute("UPDATE param SET police = ?, taille = ?, save_time = ? WHERE id = '1'", (police, taille, save))
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        fct_main.logs(e)
def tab_param_lire(varia):
    try:
        conn = sqlite3.connect(var.dossier_projet + "/dbgene")
        cursor = conn.cursor()
        requete = "SELECT " + varia + " FROM param WHERE id = 1"
        cursor.execute(requete)
        result = cursor.fetchone()
        value = result[0]
    except Exception as e:
        print(e)
        fct_main.logs(e)
    return value
def tab_info_lire(varia):
    try:
        conn = sqlite3.connect(var.dossier_projet + "/dbgene")
        cursor = conn.cursor()
        requete = "SELECT " + varia + " FROM info WHERE id = 1"
        cursor.execute(requete)
        result = cursor.fetchone()
        value = result[0]
    except Exception as e:
        fct_main.logs(e)
    return value