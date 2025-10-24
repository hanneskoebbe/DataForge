import tkinter as tk
from tkinter import filedialog

def select_dir():
    # Hauptfenster erstellen, aber nicht anzeigen
    root = tk.Tk()
    root.withdraw()

    # Dialog zur Ordnerauswahl
    dir = filedialog.askdirectory(title="Ordner auswählen")

    # Ergebnis anzeigen
    print("Ausgewählter Ordner:", dir)
    return dir