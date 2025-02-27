import re
import json
import os

class CorrectionOrthographique:
    def __init__(self, text_widget, spell, menu_correction, fichier_mots_ignores='mots_ignores.json'):
        self.text_widget = text_widget
        self.spell = spell
        self.menu_correction = menu_correction
        self.fichier_mots_ignores = fichier_mots_ignores
        self.mots_a_ignorer = self.charger_mots_ignores()

    def charger_mots_ignores(self):
        if os.path.exists(self.fichier_mots_ignores):
            with open(self.fichier_mots_ignores, 'r', encoding='utf-8') as f:
                return set(json.load(f))
        return set()

    def sauvegarder_mots_ignores(self):
        with open(self.fichier_mots_ignores, 'w', encoding='utf-8') as f:
            json.dump(list(self.mots_a_ignorer), f, ensure_ascii=False)

    def ajouter_mot_a_ignorer(self, mot):
        mot_lower = mot.lower()
        self.mots_a_ignorer.add(mot_lower)
        self.sauvegarder_mots_ignores()

    def verifier_orthographe(self, event=None):
        contenu = self.text_widget.get("1.0", "end-1c")
        mots_avec_positions = re.finditer(
            r"(?i)\b(?:[ldnmtsjcç]')?[a-zàâäéèêëîïôöùûüç]+(?:[-']?[a-zàâäéèêëîïôöùûüç]+)*\b", contenu)

        self.text_widget.tag_remove("erreur", "1.0", "end")

        for match in mots_avec_positions:
            mot = match.group()
            mot_lower = mot.lower()

            if mot_lower in self.mots_a_ignorer:
                continue

            if "'" in mot:
                parties_mot = mot.split("'")
                if len(parties_mot) == 2 and parties_mot[0].lower() in ["l", "d", "j", "m", "n", "t", "s", "c", "qu"]:
                    continue

            if self.spell.unknown([mot]):
                debut = f"1.0+{match.start()}c"
                fin = f"1.0+{match.end()}c"
                self.text_widget.tag_add("erreur", debut, fin)

    def obtenir_mot_a_index(self, index):
        ligne, col = map(int, index.split('.'))
        ligne_texte = self.text_widget.get(f"{ligne}.0", f"{ligne}.end")
        for match in re.finditer(r"(?i)\b(?:[ldnmtsjcç]')?[a-zàâäéèêëîïôöùûüç]+(?:[-']?[a-zàâäéèêëîïôöùûüç]+)*\b",
                                 ligne_texte):
            if match.start() <= col < match.end():
                return match.group()
        return None

    def afficher_menu_correction(self, event):
        index = self.text_widget.index(f"@{event.x},{event.y}")
        mot = self.obtenir_mot_a_index(index)

        if mot:
            mot_lower = mot.lower()
            if mot_lower not in self.mots_a_ignorer:
                if self.spell.unknown([mot]):
                    corrections = self.spell.candidates(mot)
                    self.menu_correction.delete(0, 'end')
                    for correction in corrections:
                        self.menu_correction.add_command(label=correction,
                                                         command=lambda c=correction: self.appliquer_correction(index, mot, c))
                    self.menu_correction.add_separator()
                    self.menu_correction.add_command(label="Ignorer ce mot",
                                                     command=lambda: self.ajouter_mot_a_ignorer(mot))
                    self.menu_correction.post(event.x_root, event.y_root)

    def appliquer_correction(self, index, ancien_mot, nouveau_mot):
        ligne, col = map(int, index.split('.'))
        ligne_texte = self.text_widget.get(f"{ligne}.0", f"{ligne}.end")
        nouvelle_ligne = re.sub(r'\b' + re.escape(ancien_mot) + r'\b', nouveau_mot, ligne_texte, 1)
        self.text_widget.delete(f"{ligne}.0", f"{ligne}.end")
        self.text_widget.insert(f"{ligne}.0", nouvelle_ligne)
        self.verifier_orthographe()
