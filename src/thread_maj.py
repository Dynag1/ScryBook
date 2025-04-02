import traceback
import webbrowser
import os
import urllib3
import xmltodict
import tkinter as Tk
from src import var, design, tMaj
import requests
import subprocess

def getxml():
    try:
        print("maj1")
        url = var.site + "/ScryBook/changelog.xml"
        http = urllib3.PoolManager(cert_reqs='CERT_NONE')
        response = http.request('GET', url)
        data = xmltodict.parse(response.data)
        print("maj2")
        return data

    except Exception as e:
        print(f"Failed to parse xml from response: {traceback.format_exc()}")
        return None


def recupDerVer():
    try:
        xml = getxml()
        if xml is None:
            print("Impossible de récupérer les données XML")
            return None

        versions = xml["changelog"]["version"]
        if not versions:
            print("Aucune version trouvée dans le XML")
            return None

        latest_version = versions[0]["versio"]
        return ''.join(latest_version.split('.'))
    except KeyError as e:
        print("Clé manquante dans le XML : "+e)
    except Exception as e:
        print("Erreur dans recupDerVer : "+e)
    return None


def download_new_version(version):
    try:
        exe_url = f"{var.site}/ScryBook/ScryBook.exe"  # URL du fichier .exe à télécharger
        temp_path = os.path.join(os.getcwd(), "ScryBook_new.exe")  # Chemin temporaire pour la nouvelle version

        # Télécharger le fichier .exe
        response = requests.get(exe_url, stream=True)
        if response.status_code == 200:
            with open(temp_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
            print(f"Nouvelle version téléchargée : {temp_path}")
            return temp_path  # Retourner le chemin du fichier téléchargé
        else:
            print(f"Erreur lors du téléchargement : {response.status_code}")
            return None
    except Exception as e:
        print(f"Erreur dans download_new_version : {traceback.format_exc()}")
        return None


def launch_updater(new_exe_path):
    try:
        updater_path = os.path.join(os.getcwd(), "updater.exe")
        current_exe = os.path.join(os.getcwd(), "ScryBook.exe")

        # Lancer updater.exe avec les chemins en arguments
        subprocess.Popen([
            updater_path,
            new_exe_path,  # Chemin du .exe téléchargé
            current_exe  # Chemin du .exe à remplacer
        ], shell=False)

        os._exit(0)
    except Exception as e:
        print(f"Erreur lancement updater : {traceback.format_exc()}")


def testVersion():
    version = recupDerVer()
    if version is None:
        print("Unable to retrieve the latest version")
        return

    current_version = ''.join(var.version.split('.'))

    if int(current_version) < int(version):
        val = design.question_box(_('Mise à jour'),
                                  _('Une mise à jour vers la version '+version+' est disponible. \n Voulez vous la télécharger ?'))
        if val:
            new_exe_path = download_new_version(version)
            if new_exe_path:
                launch_updater(new_exe_path)


def main():
    try:
        testVersion()
    except Exception as e:
        print(f"Error in main: {e}")
