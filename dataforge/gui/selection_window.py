import tkinter as tk


def selection_window(self, data_source):
    # Dummy-Auswahlmöglichkeiten (z. B. Datenfelder)
    options = data_source.keys()

    # Zwischenspeicher für Auswahl
    selection_vars = {}

    # Neues Fenster für die Auswahl
    win = tk.Toplevel(
        self.root,
        bg="white",
        highlightbackground="grey",
        highlightthickness=2
    )
    win.overrideredirect(True)
    win.geometry(
        f"250x132+"
        f"{self.root.winfo_rootx()+self.root.winfo_width()-250}+"
        f"{self.root.winfo_rooty()+50}"
    )

    fr = tk.Frame(win, bg="white")
    fr.pack(padx=10, pady=10, fill="both", expand=True)

    fr_canvas = tk.Frame(fr, bg="white")
    fr_canvas.pack(fill="both", expand=True)

    # Scrollbarer Bereich
    canvas = tk.Canvas(
        fr_canvas, height=70,
        bg="white",
        highlightthickness=0,
        bd=0
    )
    scrollable_fr = tk.Frame(canvas, bg="white")

    canvas.bind_all("<MouseWheel>", lambda e: self.on_mousewheel(e, canvas))

    # Fenster ID merken
    win_id = canvas.create_window((0, 0), window=scrollable_fr, anchor="nw")

    # Scrollable-Frame an Canvas-Breite anpassen
    canvas.bind(
        "<Configure>",
        lambda event: canvas.itemconfig(win_id, width=event.width)
    )

    canvas.pack(side="left", fill="both", expand=True)

    # Checkbuttons erzeugen
    for opt in options:
        row = tk.Frame(scrollable_fr, bg="white")
        row.pack(side="top", fill="x", expand=True, padx=20, pady=2)
        var = tk.BooleanVar()
        chk = tk.Checkbutton(row, text=opt, variable=var, bg="white")
        chk.pack(side="left")
        selection_vars[opt] = var

    fr_button = tk.Frame(fr, height=12, bg="white")
    fr_button.pack(fill="x", pady=(5, 0))

    button = tk.Button(fr_button, text="OK", command=lambda: apply_selection)
    button.pack(side="bottom")

    canvas.configure(scrollregion=canvas.bbox("all"))

    def apply_selection():
        try:
            selected = [
                opt for opt, var in selection_vars.items() if var.get()
            ]
            return selected

        finally:
            canvas.unbind_all("<MouseWheel>")
            win.destroy()
