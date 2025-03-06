import tkinter as tk
from tkinter import ttk, Menu
import language_tool_python


class TextCorrector:
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.tool = language_tool_python.LanguageTool('fr')
        self.matches = []

        # Configuration du tag pour les erreurs
        self.text_widget.tag_configure("erreur", background="green", foreground="white")

        # Lier le clic droit à l'ouverture du menu de correction
        self.text_widget.bind("<Button-3>", self.show_correction_menu)

    def detecter_et_surligner_erreurs(self):
        texte = self.text_widget.get("1.0", tk.END).strip()
        if not texte:
            return "Aucun texte à vérifier."

        self.text_widget.tag_remove("erreur", "1.0", tk.END)
        self.matches = self.tool.check(texte)

        for match in self.matches:
            start_index = f"1.0+{match.offset}c"
            end_index = f"1.0+{match.offset + match.errorLength}c"
            self.text_widget.tag_add("erreur", start_index, end_index)

        return f"{len(self.matches)} erreurs détectées."

    def show_correction_menu(self, event):
        index = self.text_widget.index(f"@{event.x},{event.y}")
        tags = self.text_widget.tag_names(index)

        if "erreur" in tags:
            menu = Menu(self.text_widget, tearoff=0)
            for match in self.matches:
                start_index = f"1.0+{match.offset}c"
                end_index = f"1.0+{match.offset + match.errorLength}c"
                if self.text_widget.compare(start_index, "<=", index) and self.text_widget.compare(index, "<",
                                                                                                   end_index):
                    if match.replacements:
                        for replacement in match.replacements:
                            menu.add_command(label=replacement, command=lambda r=replacement, s=start_index,
                                                                               e=end_index: self.apply_correction(r, s,
                                                                                                                  e))
                    else:
                        menu.add_command(label="Pas de suggestion", state="disabled")
                    menu.add_separator()
                    menu.add_command(label=f"Erreur : {match.message}", state="disabled")
                    break
            if not menu.index("end"):  # Si le menu est vide
                menu.add_command(label="Aucune suggestion disponible", state="disabled")
            menu.add_separator()
            menu.add_command(label="Ignorer", command=lambda: self.ignore_error(index))

            menu.post(event.x_root, event.y_root)

    def apply_correction(self, replacement, start, end):
        self.text_widget.delete(start, end)
        self.text_widget.insert(start, replacement)
        self.text_widget.tag_remove("erreur", start, f"{start}+{len(replacement)}c")
        self.detecter_et_surligner_erreurs()  # Rafraîchir les erreurs après correction

    def ignore_error(self, index):
        start = self.text_widget.index(f"{index} linestart")
        end = self.text_widget.index(f"{index} lineend")
        self.text_widget.tag_remove("erreur", start, end)



def check_errors():
    result = corrector.detecter_et_surligner_erreurs()
    result_label.config(text=result)



