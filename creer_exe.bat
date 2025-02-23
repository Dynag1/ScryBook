@echo off
REM Change le répertoire courant vers celui du fichier .bat
cd /d "%~dp0"

REM Affiche le répertoire courant pour confirmation
echo Répertoire courant : %CD%

REM Exécute PyInstaller pour créer l'exécutable
pyinstaller --noconsole --icon=src/logoSb.ico --add-data "src:src" --hidden-import=pkg_resources.py2_warn --additional-hooks-dir=. --name=ScryBook --add-data "post_build.py:." ScryBook.py -y

REM Exécute le script post-build
python post_build.py

REM Pause pour voir les résultats
pause
