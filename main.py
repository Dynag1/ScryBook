import os
import sys
import requests
import subprocess
import time
from tkinter import Tk, messagebox


def telecharger_mise_a_jour(url, chemin_temporaire):
    """
    Télécharge le fichier de mise à jour dans un emplacement temporaire.
    """
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(chemin_temporaire, "wb") as fichier_temp:
            for chunk in response.iter_content(chunk_size=8192):
                fichier_temp.write(chunk)

        print(f"Fichier téléchargé avec succès : {chemin_temporaire}")
        return True
    except Exception as e:
        print(f"Erreur lors du téléchargement : {e}")
        return False


def afficher_message_mise_a_jour():
    """
    Affiche un message d'alerte avant la mise à jour.
    """
    root = Tk()
    root.withdraw()  # Cache la fenêtre principale
    messagebox.showinfo("Mise à jour", "Une nouvelle version est disponible. L'application va se mettre à jour.")
    root.destroy()


def lancer_updater(chemin_executable, chemin_temporaire):
    """
    Lance le script intermédiaire pour effectuer la mise à jour.
    """
    subprocess.Popen([sys.executable, "updater.py", chemin_executable, chemin_temporaire])
    sys.exit(0)


if __name__ == "__main__":
    # URL de la nouvelle version (remplacez par votre propre URL)
    url_fichier = "https://votre-serveur.com/nouvelle_version.exe"

    # Emplacement temporaire pour le fichier téléchargé
    chemin_temporaire = os.path.join(os.getcwd(), "temp_update.exe")

    # Afficher une alerte de mise à jour
    afficher_message_mise_a_jour()

    # Télécharger la nouvelle version
    if telecharger_mise_a_jour(url_fichier, chemin_temporaire):
        # Lancer le processus de mise à jour
        lancer_updater(sys.executable, chemin_temporaire)
