import re
import json
import os
import language_tool_python

class correction:
    def __init__(self, text_widget, spell, menu_correction, fichier_mots_ignores='mots_ignores.json'):
        self.text_widget = text_widget
        self.menu_correction = menu_correction
        self.fichier_mots_ignores = fichier_mots_ignores
        self.mots_a_ignorer = self.charger_mots_ignores()
        self.tool = language_tool_python.LanguageTool('fr')
        print("languagetool")

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
        matches = self.tool.check(contenu)

        self.text_widget.tag_remove("erreur", "1.0", "end")

        for match in matches:
            if match.ruleId != 'MORFOLOGIK_RULE_FR_FR':
                debut = f"1.0+{match.offset}c"
                fin = f"1.0+{match.offset + match.errorLength}c"
                self.text_widget.tag_add("erreur", debut, fin)

    def obtenir_mot_a_index(self, index):
        ligne, col = map(int, index.split('.'))
        ligne_texte = self.text_widget.get(f"{ligne}.0", f"{ligne}.end")
        contenu = self.text_widget.get("1.0", "end-1c")
        offset = len(self.text_widget.get("1.0", f"{ligne}.0")) + col
        matches = self.tool.check(contenu)
        for match in matches:
            if match.offset <= offset < match.offset + match.errorLength:
                return contenu[match.offset:match.offset + match.errorLength]
        return None

    def afficher_menu_correction(self, event):
        index = self.text_widget.index(f"@{event.x},{event.y}")
        mot = self.obtenir_mot_a_index(index)

        if mot:
            contenu = self.text_widget.get("1.0", "end-1c")
            matches = self.tool.check(contenu)
            for match in matches:
                if contenu[match.offset:match.offset + match.errorLength] == mot:
                    self.menu_correction.delete(0, 'end')
                    for correction in match.replacements:
                        self.menu_correction.add_command(label=correction,
                                                         command=lambda c=correction: self.appliquer_correction(index, mot, c))
                    self.menu_correction.add_separator()
                    self.menu_correction.add_command(label=_("Ignorer ce mot"),
                                                     command=lambda: self.ajouter_mot_a_ignorer(mot))
                    self.menu_correction.post(event.x_root, event.y_root)
                    break

    def appliquer_correction(self, index, ancien_mot, nouveau_mot):
        ligne, col = map(int, index.split('.'))
        ligne_texte = self.text_widget.get(f"{ligne}.0", f"{ligne}.end")
        nouvelle_ligne = ligne_texte.replace(ancien_mot, nouveau_mot, 1)
        self.text_widget.delete(f"{ligne}.0", f"{ligne}.end")
        self.text_widget.insert(f"{ligne}.0", nouvelle_ligne)
        self.verifier_orthographe()