# rc/hook-questionnaire.py

import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules, copy_metadata

# Inclure le dossier "fichier" à la racine de l'exécutable
datas = []
fichier_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')  # Chemin relatif à l'emplacement du hook

if os.path.exists(fichier_dir):
    for root, dirs, files in os.walk(fichier_dir):
        for f in files:
            source = os.path.join(root, f)
            # Destination : place directement à la racine
            destination = os.path.join('.', os.path.relpath(source, fichier_dir))
            datas.append((source, destination))
for d in dirs:
    source_dir = os.path.join(root, d)
    destination_dir = os.path.join('.', os.path.relpath(source_dir, fichier_dir))
    # Ajouter un tuple avec l'indicateur "binaire" (le 3ème élément) pour indiquer un répertoire
    datas.append((source_dir, destination_dir, 'BINARY'))  #Le chemin vers le sous-répertoire

# Collecter les données pour les dépendances déclarées dans requirements.txt
hiddenimports = []
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'requirements.txt'), 'r') as f: #Ajout du path requirement.txt
    for line in f:
        package = line.strip().split("==")[0]
        try:
            hiddenimports += collect_submodules(package)
            datas += copy_metadata(package)
        except ModuleNotFoundError:
            print(f"Module not found: {package}.  Make sure it is installed.")

# Spécifiez manuellement les modules cachés si nécessaire
hiddenimports += ['urllib3.util.selectors', 'urllib3.contrib.pyopenssl']
