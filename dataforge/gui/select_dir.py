import tkinter as tk
from tkinter import filedialog


def select_dir():
    # Hauptfenster erstellen, aber nicht anzeigen
    root = tk.Tk()
    root.withdraw()

    # Dialog zur Ordnerauswahl
    directory = filedialog.askdirectory(title="Ordner auswählen")

    # Ergebnis anzeigen
    print("Ausgewählter Ordner:", directory)
    return dir
