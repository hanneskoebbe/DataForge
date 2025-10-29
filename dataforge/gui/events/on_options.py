import tkinter as tk


def on_option(self, p):
    self.get_temp(p)

    # Menü erstellen
    menu = tk.Menu(self.root, tearoff=0)
    menu.add_command(
        label="Duplizieren",
        command=lambda: self.on_duplicate(p)
    )
    menu.add_command(
        label="Mittelwert",
        command=lambda: self.on_mean(p)
    )
    menu.add_command(
        label="Wiederherstellen",
        command=lambda: self.on_restore
    )

    # Position des Mauszeigers abfragen (z. B. global aufrufen)
    try:
        x = self.root.winfo_pointerx()
        y = self.root.winfo_pointery()
        menu.tk_popup(x, y)
    finally:
        menu.grab_release()
