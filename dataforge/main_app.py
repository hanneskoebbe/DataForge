import tkinter as tk
from dataforge.gui import Gui
from dataforge.events import Events
from dataforge.core import Core
from dataforge.data_store import DataStore


class MainApp:
    def __init__(self):
        super().__init__()
        self.gui = Gui(self)
        self.events = Events(self)
        self.data_store = DataStore()
        self.core = Core(self)
        self.run()

    def run(self):
        self.root = tk.Tk()
        self.root.title("DataForge")
        self.root.geometry("625x480")
        self.root.protocol(
            "WM_DELETE_WINDOW",
            lambda: self.events.on_closing(self.root)
        )

        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=20, pady=5, fill="both", expand=True)

        self.head_label = tk.Label(
            self.frame, text="Parameterliste:",
            font=("Arial", 20))
        self.head_label.pack(side="top", fill="x")

        # Scrollbarer Bereich
        self.canvas = tk.Canvas(self.frame, highlightthickness=0, bd=0)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.canvas.bind_all("<MouseWheel>", self.events.on_mousewheel)

        # Fenster ID merken
        self.window_id = self.canvas.create_window(
            (0, 0),
            window=self.scrollable_frame,
            anchor="nw"
        )

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Scrollable-Frame an Canvas-Breite anpassen
        self.scrollable_frame.bind(
            "<Configure>",
            lambda event: self.canvas.itemconfig(
                self.window_id,
                width=getattr(event, "width", 0)
            )
        )

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.pack(side="left", fill="both", expand=True)

        # Button-Leiste
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=(10, 10))

        self.import_button = tk.Button(
            self.button_frame,
            text="Messberichte importieren",
            command=self.events.on_import
        )
        self.import_button.pack(side="left", padx=10)

        self.button_par = tk.Button(
            self.button_frame,
            text="Parameter hinzufuegen",
            command=self.events.on_add_par
        )
        self.button_par.pack(side="left", padx=10)

        self.export_button = tk.Button(
            self.button_frame,
            text="PDF exportieren",
            command=self.events.on_export
        )
        self.export_button.pack(side="left", padx=10)

        self.gui.widgets()
        self.root.mainloop()
