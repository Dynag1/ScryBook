import os
import shutil


def copy_src_folder():
    # Chemin vers le dossier dist/ScryBook
    dist_path = os.path.join('dist', 'ScryBook')

    # Chemin vers le dossier src dans dist/ScryBook
    src_path_internal = os.path.join(dist_path, '_internal\src')
    print(src_path_internal)
    # Chemin vers le nouveau dossier src au même niveau que l'exécutable
    src_path_external = os.path.join('dist\ScryBook', 'src')
    print(src_path_external)
    # Vérifier si le dossier src existe dans dist/ScryBook
    if os.path.exists(src_path_internal):
        # Copier le dossier src au même niveau que l'exécutable
        if os.path.exists(src_path_external):
            shutil.rmtree(src_path_external)
        shutil.copytree(src_path_internal, src_path_external)
        print("Le dossier 'src' a été copié avec succès.")
    else:
        print("Le dossier 'src' n'a pas été trouvé dans le dossier de distribution.")


if __name__ == "__main__":
    copy_src_folder()
