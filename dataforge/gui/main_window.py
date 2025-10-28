import tkinter as tk


class MainAPP:
    def __init__(
            self,
            gui,
            events,
            core):
        self.gui = gui
        self.events = events
        self.core = core

        # var
        self.widget_data = {}
        self.import_data = {}
        self.all_data = {}

        self.setup_ui()

        self.widgets()

        self.root.mainloop()



        self.import_data = import_data
        self.extract_params = extract_params
        self.tool_number = tool_number
        self.gen_temp_data = gen_temp_data

        self.data = None
        self.temp_data = None
        self.params = []
        self.custom_params = []
        self.param_widgets = {}

        self.all_data = {}

        self.imp_data = {}

        self.custom_data = {}

        self.temp = {
            "temp": {
                "pos. nr.": [],
                "actual": [],
                "nominal": [],
                "tol_low": [],
                "tol_up": []
            },
        }

        self.arch = {}

        self.temp_arch = {}

        self.export_data = {}

        self.mean_data = {}

    def setup_ui(self):
        self.root = tk.Tk()
        self.root.title("DataForge")
        self.root.geometry("625x480")
        self.root.protocol("WM_DELETE_WINDOW", self.events.on_closing)

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
            anchor="nw")

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Scrollable-Frame an Canvas-Breite anpassen
        self.canvas.bind("<Configure>", lambda event: self.canvas.itemconfig(self.window_id, width=event.width))

        self.canvas.pack(side="left", fill="both", expand=True)

        # Button-Leiste
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=(10, 10))

        self.import_button = tk.Button(self.button_frame, text="Messberichte importieren", command=self.events.on_import)
        self.import_button.pack(side="left", padx=10)

        self.button_par = tk.Button(self.button_frame, text="Parameter hinzufuegen", command=self.events.on_add_par)
        self.button_par.pack(side="left", padx=10)

        self.export_button = tk.Button(self.button_frame, text="PDF exportieren", command=self.events.on_export)
        self.export_button.pack(side="left", padx=10)


class Gui:
    def __init__(self,
                 widgets,
                 select_dir):
        self.widgets = widgets
        self.select_dir = select_dir


class Events:
    def __init__(self,
                 on_closing,
                 on_mousewheel,
                 on_import,
                 on_export,
                 on_add_par):
        self.on_closing = on_closing
        self.on_mousewheel = on_mousewheel
        self.on_import = on_import
        self.on_export = on_export
        self.on_add_par = on_add_par


class Core:
    def __init__(self,
                 gen_raw_import_data,
                 gen_import_data,
                 gen_all_data,
                 get_temp,
                 get_data,
                 temp_to_data,
                 convert_seperator,
                 plot_to_pdf):
        self.gen_raw_import_data = gen_raw_import_data
        self.gen_import_data = gen_import_data
        self.gen_all_data = gen_all_data
        self.get_temp = get_temp
        self.get_data = get_data
        self.temp_to_data = temp_to_data
        self.convert_seperator = convert_seperator
        self.plot_to_pdf = plot_to_pdf
