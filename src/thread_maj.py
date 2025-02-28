import traceback
import webbrowser
import os
import urllib3
import xmltodict

from src import var, design

def getxml():
    try:
        url = var.site + "/ScryBook/changelog.xml"
        http = urllib3.PoolManager(cert_reqs='CERT_NONE')
        response = http.request('GET', url)
        data = xmltodict.parse(response.data)
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
        print(f"Clé manquante dans le XML : {e}")
    except Exception as e:
        print(f"Erreur dans recupDerVer : {e}")
    return None


def testVersion():
    version = recupDerVer()
    if version is None:
        print("Unable to retrieve the latest version")
        return

    current_version = ''.join(var.version.split('.'))

    if int(current_version) < int(version):
        val = design.question_box(_('Mise à jour'),
                                  f_('Une mise à jour vers la version {version} est disponible. \n Voulez vous la télécharger ?'))
        if val:
            webbrowser.open(var.site + '/ScryBook/ScryBook_Setup.exe')
            os._exit(0)

def main():
    try:
        testVersion()
    except Exception as e:
        print(f"Error in main: {e}")


