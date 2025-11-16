import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout


class Gui:
    def __init__(self, app):
        self.app = app
        self.event = [
            "<MouseWheel>",
            "<Double-Button-1>",
            "<Return>",
            "<Configure>"
        ]
        self.i_edit = 0
        self.dat_entries = []  # Liste, um die Daten-Eingabefelder zu speichern

    def widgets(self):
        # delete checkboxes
        for self.app.widget in self.app.scrollable_frame.winfo_children():
            self.app.widget.destroy()
        self.app.data_store.widget_data.clear()

        if self.app.data_store.all_data != {}:
            for param, data in self.app.data_store.all_data.items():
                # new row
                self.app.row = tk.Frame(
                    self.app.scrollable_frame,
                    width=self.app.canvas.winfo_width())
                self.app.row.pack(fill="x", padx=5, pady=2)
                self.app.row.bind(
                    self.event[1],
                    lambda e,
                    p=param: self.app.events.on_edit(p)
                )

                # checkbox
                var = tk.BooleanVar(value=False)
                self.app.cb = tk.Checkbutton(
                    self.app.row,
                    variable=var,
                    anchor="w",
                    justify="left"
                )
                self.app.cb.pack(side="left")
                self.app.cb.bind(
                    self.event[1],
                    lambda e,
                    p=param: self.app.events.on_edit(p)
                )

                # entry for parameter name
                self.app.par_name = tk.Entry(self.app.row, width=25)
                self.app.par_name.insert(0, str(param))
                self.app.par_name.pack(
                    side="left",
                    padx=(10, 2),
                    expand='True',
                    fill='x'
                )
                self.app.par_name.bind(
                    self.event[1],
                    lambda e,
                    p=param: self.app.events.on_edit(p)
                )
                self.app.par_name.bind(
                    self.event[2],
                    lambda e,
                    p=param: self.app.events.on_input(p)
                )
                self.app.tol_frame = tk.Frame(self.app.row, width=10)
                self.app.tol_frame.pack(
                    side="left",
                    padx=(10, 2),
                    expand='True',
                    fill='x'
                )

                # label for lower tolerance
                self.app.tol_low_label = tk.Label(
                    self.app.tol_frame,
                    text="untere Tol.:"
                )
                self.app.tol_low_label.pack(side="left", padx=(10, 2))
                self.app.tol_low_label.bind(
                    self.event[1],
                    lambda e,
                    p=param: self.app.events.on_edit(p)
                )

                # entry for lower tolerance
                self.app.tol_low = tk.Entry(self.app.tol_frame, width=10)
                self.app.tol_low.insert(0, str(
                    self.app.data_store.all_data[param]["lower tol."][0]
                ))
                self.app.tol_low.pack(side="left", padx=(10, 2), expand='True')
                self.app.tol_low.bind(
                    self.event[1],
                    lambda e,
                    p=param: self.app.events.on_edit(p)
                )
                self.app.tol_low.bind(
                    self.event[2],
                    lambda e,
                    p=param: self.app.events.on_input(p)
                )

                # label for upper tolerance
                self.app.tol_up_label = tk.Label(
                    self.app.tol_frame,
                    text="obere Tol.:"
                )
                self.app.tol_up_label.pack(
                    side="left",
                    padx=(10, 2)
                )
                self.app.tol_up_label.bind(
                    self.event[1],
                    lambda e,
                    p=param: self.app.events.on_edit(p)
                )

                # entry for upper tolerance
                self.app.tol_up = tk.Entry(self.app.tol_frame, width=6)
                self.app.tol_up.insert(0, str(
                    self.app.data_store.all_data[param]["upper tol."][0]
                ))
                self.app.tol_up.pack(side="left", padx=(10, 20), expand='True')
                self.app.tol_up.bind(
                    self.event[1],
                    lambda e,
                    p=param: self.app.events.on_edit(p)
                )
                self.app.tol_up.bind(
                    self.event[2],
                    lambda e,
                    p=param: self.app.events.on_input(p)
                )

                # delete-button
                self.app.remove_btn = tk.Button(
                    self.app.tol_frame,
                    text="✕",
                    command=lambda p=param: self.app.events.on_del(p),
                    width=2,
                    relief='flat',
                    bg='white',
                    fg='red',
                    font=("Arial", 10, "bold"),
                    padx=0, pady=0
                )
                self.app.remove_btn.pack(side='right', padx=(2, 0))

                # option-button
                self.app.options_btn = tk.Button(
                    self.app.tol_frame,
                    text="⋮",  # U+22EE Vertical Ellipsis
                    command=lambda p=param: self.app.events.on_options(p),
                    width=2,
                    relief='flat',
                    bg='white',
                    fg='black',
                    font=("Arial", 10),
                    padx=0, pady=0
                )
                self.app.options_btn.pack(side='right', padx=(0, 2))

                # save data in self.widget_data
                self.app.data_store.widget_data[param] = {
                    "var": var,
                    "par_name": self.app.par_name,
                    "tol_low": self.app.tol_low,
                    "tol_up": self.app.tol_up
                }

            self.app.canvas.bind_all(
                self.event[0],
                lambda e: self.app.events.on_mousewheel(e, self.app.canvas)
            )

    def navigation_bar(self):
        while self.app.navigation_layout.count():
            if self.app.navigation_layout.takeAt(0).widget():
                self.app.navigation_layout.widget().deleteLater()

        if self.app.data_store.all_data != {}:
            for param, data in self.app.data_store.all_data.items():
                # layout for row frame
                self.app.row_layout = QHBoxLayout()

                # new row frame for every parameter
                self.app.row_frame = QWidget()
                self.app.row_frame.setLayout(self.app.row_layout)

                # label for param
                self.app.param_label = QLabel(param)
                self.param_label.setStyleSheet(
                    "color: #333333;\
                    font-weight: bold;\
                    font-size: 14px;"
                )

                # option button
                self.option_btn = QPushButton()
                self.option_btn.clicked.connect(self.app.events.on_options)

                # delete button
                self.del_btn = QPushButton()
                self.del_btn.clicked.connect(self.app.events.on_del)

                # add content to row layout
                self.app.row_layout.addWidget(self.app.param_label)
                self.app.row_layout.addStretch()
                self.app.row_layout.addWidget(self.app.option_btn)
                self.app.row_layout.addWidget(self.app.del_btn)

                # add row frame to navigation bar
                self.app.navigation_layout.addWidget(self.app.row_frame)

    def plot_all_data(self):
        idx = "pos. nr."
        for param, df_dict in self.app.data_store.all_data.items():
            self.app.plt_frame = ttk.Frame(self.app.notebook)
            self.app.notebook.add(self.app.plt_frame, text=param)

            # page 1: Plot
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(
                df_dict.get(idx, []),
                [float(str(x).replace(",", "."))
                    for x in df_dict.get("actual", [])],
                label="actual", marker="o"
            )
            plt.plot(
                df_dict.get(idx, []),
                [float(str(x).replace(",", "."))
                    for x in df_dict.get("nominal", [])],
                label="nominal", linestyle="-", color="green"
            )
            plt.plot(
                df_dict.get(idx, []),
                [n + u for n, u in zip(
                    [float(str(x).replace(",", "."))
                        for x in df_dict.get("nominal", [])],
                    [float(str(x).replace(",", "."))
                        for x in df_dict.get("upper tol.", [])]
                    )],
                label="upper tol.", linestyle="-", color="red"
            )
            plt.plot(
                df_dict.get(idx, []),
                [n + l for n, l in zip(
                    [float(str(x).replace(",", "."))
                        for x in df_dict.get("nominal", [])],
                    [float(str(x).replace(",", "."))
                        for x in df_dict.get("lower tol.", [])]
                    )],
                label="lower tol.", linestyle="-", color="red"
            )
            plt.title(f"chart: {param}")
            plt.xlabel("pos. nr.")
            plt.ylabel("value")
            plt.legend()
            plt.grid(True)
            plt.xticks(df_dict.get(idx, []), rotation=45)
            plt.tight_layout()

            # Plot in Tkinter-Canvas einbetten
            self.app.canvas = FigureCanvasTkAgg(
                fig,
                master=self.app.plt_frame
            )
            self.app.canvas.draw()
            self.app.canvas.get_tk_widget().pack(fill="both", expand=True)

            plt.close(fig)

    def select_dir(self):
        # dialog to choose directory
        directory = filedialog.askdirectory(
            parent=self.app.root,
            title="Ordner auswählen"
        )
        return directory

    def selection_window(self, data_source):
        # init selected
        selected = []

        # Dummy-Auswahlmöglichkeiten (z. B. Datenfelder)
        options = data_source.keys()

        # Zwischenspeicher für Auswahl
        selection_vars = {}

        # Neues Fenster für die Auswahl
        self.app.gui.win = tk.Toplevel(
            self.app.root,
            bg="white",
            highlightbackground="grey",
            highlightthickness=2
        )
        self.app.gui.win.overrideredirect(True)
        self.app.gui.win.geometry(
            f"250x132+"
            f"{self.app.root.winfo_rootx()+self.app.root.winfo_width()-250}+"
            f"{self.app.root.winfo_rooty()+50}"
        )

        self.app.gui.fr = tk.Frame(self.app.gui.win, bg="white")
        self.app.gui.fr.pack(padx=10, pady=10, fill="both", expand=True)

        self.app.gui.fr_canvas = tk.Frame(self.app.gui.fr, bg="white")
        self.app.gui.fr_canvas.pack(fill="both", expand=True)

        # Scrollbarer Bereich
        self.app.gui.canvas = tk.Canvas(
            self.app.gui.fr_canvas, height=70,
            bg="white",
            highlightthickness=0,
            bd=0
        )
        self.app.gui.scrollable_fr = tk.Frame(self.app.gui.canvas, bg="white")
        self.app.gui.canvas.bind_all(
            self.event[0],
            lambda e: self.app.events.on_mousewheel(e, self.app.gui.canvas)
        )

        # Fenster ID merken
        win_id = self.app.gui.canvas.create_window(
            (0, 0),
            window=self.app.gui.scrollable_fr,
            anchor="nw"
        )

        # Scrollable-Frame an Canvas-Breite anpassen
        self.app.gui.scrollable_fr.bind(
            self.event[3],
            lambda e: self.app.gui.canvas.itemconfig(
                win_id,
                width=getattr(e, "width", 0)
            )
        )

        self.app.gui.scrollable_fr.bind(
            self.event[3],
            lambda e: self.app.gui.canvas.configure(
                scrollregion=self.app.gui.canvas.bbox("all")
            )
        )

        self.app.gui.canvas.pack(side="left", fill="both", expand=True)

        # Checkbuttons erzeugen
        for opt in options:
            self.app.gui.row = tk.Frame(self.app.gui.scrollable_fr, bg="white")
            self.app.gui.row.pack(
                side="top",
                fill="x",
                expand=True,
                padx=20,
                pady=2
            )
            var = tk.BooleanVar()
            self.app.gui.chk = tk.Checkbutton(self.app.gui.row, text=opt, variable=var, bg="white")
            self.app.gui.chk.pack(side="left")
            selection_vars[opt] = var

        self.app.gui.fr_button = tk.Frame(
            self.app.gui.fr,
            height=12,
            bg="white"
        )
        self.app.gui.fr_button.pack(fill="x", pady=(5, 0))

        def confirm():
            nonlocal selected
            try:
                selected = [
                    opt for opt, var in selection_vars.items() if var.get()
                ]

            finally:
                self.app.gui.canvas.unbind_all(self.event[0])
                self.app.gui.win.destroy()

        self.app.gui.button = tk.Button(
            self.app.gui.fr_button,
            text="OK",
            command=confirm
        )
        self.app.gui.button.pack(side="bottom")

        self.app.gui.canvas.configure(scrollregion=self.app.gui.canvas.bbox("all"))

        self.app.gui.win.wait_window()

        return selected

    def option_menu(self, p):
        # gen menu
        self.app.gui.menu = tk.Menu(self.app.root, tearoff=0)

        # duplicate df
        self.app.gui.menu.add_command(
            label="Duplizieren",
            command=lambda: self.app.events.on_duplicate(p)
        )

        # transform df to mean of dfs
        self.app.gui.menu.add_command(
            label="Mittelwert",
            command=lambda: self.app.events.on_mean(p)
        )

        # restore df
        self.app.gui.menu.add_command(
            label="Wiederherstellen",
            command=lambda: self.app.events.on_restore()
        )

        # get cursor porsition
        try:
            x = self.app.root.winfo_pointerx()
            y = self.app.root.winfo_pointery()
            self.app.gui.menu.tk_popup(x, y)
        finally:
            self.app.gui.menu.grab_release()

    def edit_window(self, p):
        self.app.gui.i_edit = 0
        self.dat_entries = []

        self.app.gui.root = tk.Toplevel(self.app.root)
        self.app.gui.root.title(f"Edit {p}")
        self.app.gui.root.geometry("1200x400")
        self.app.gui.root.protocol(
            "WM_DELETE_WINDOW",
            lambda: self.app.gui.root.destroy()
        )

        self.app.gui.frame = tk.Frame(self.app.gui.root)
        self.app.gui.frame.pack(fill="both", expand=True)

        self.app.gui.helper_frame = tk.Frame(self.app.gui.frame)
        self.app.gui.helper_frame.pack(fill="both", expand=True)

        # scrollable frame
        self.app.gui.canvas = tk.Canvas(self.app.gui.helper_frame)
        self.app.gui.scrollable_frame = tk.Frame(self.app.gui.canvas)

        self.app.gui.canvas.bind_all(
            self.event[0],
            self.app.events.on_mousewheel
        )

        # get window id
        window_id = self.app.gui.canvas.create_window(
            (0, 0),
            window=self.app.gui.scrollable_frame,
            anchor="nw"
        )

        self.app.gui.scrollable_frame.bind(
            self.event[3],
            lambda e: self.app.gui.canvas.configure(scrollregion=self.app.gui.canvas.bbox("all"))
        )

        # Scrollable-Frame an Canvas-Breite anpassen
        self.app.gui.canvas.bind(
            self.event[3],
            lambda event: self.app.gui.canvas.itemconfig(
                window_id,
                width=event.width
                )
        )

        self.app.gui.canvas.pack(
            side="left",
            fill="both",
            padx=(10, 10),
            expand=True
        )

        self.app.gui.scrollable_frame.grid_rowconfigure(
            0,
            weight=1,
            uniform="equal"
        )

        self.app.gui.par_label = tk.Label(
            self.app.gui.scrollable_frame,
            text="Pos Nr."
        )
        self.app.gui.par_label.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=10,
            pady=2
        )

        self.app.gui.actual_label = tk.Label(
            self.app.gui.scrollable_frame,
            text="Messwert"
        )
        self.app.gui.actual_label.grid(
            row=0,
            column=1,
            sticky="ew",
            padx=10,
            pady=2
        )

        self.app.gui.nominal_label = tk.Label(
            self.app.gui.scrollable_frame,
            text="Sollwert"
        )
        self.app.gui.nominal_label.grid(
            row=0,
            column=2,
            sticky="ew",
            padx=10,
            pady=2
        )

        self.app.gui.upper_tol_label = tk.Label(
            self.app.gui.scrollable_frame,
            text="obere Tol."
        )
        self.app.gui.upper_tol_label.grid(
            row=0,
            column=3,
            sticky="ew",
            padx=10,
            pady=2
        )

        self.app.gui.lower_tol_label = tk.Label(
            self.app.gui.scrollable_frame,
            text="untere Tol."
        )
        self.app.gui.lower_tol_label.grid(
            row=0,
            column=4,
            sticky="ew",
            padx=10,
            pady=2
        )

        for col in range(5):
            self.app.gui.scrollable_frame.grid_columnconfigure(
                col,
                weight=1,
                uniform="equal"
            )

        self.app.gui.footer_fr = tk.Frame(self.app.gui.frame)
        self.app.gui.footer_fr.pack(pady=(10, 10))

        self.app.gui.add_button = tk.Button(
            self.app.gui.footer_fr,
            text="Datensatz hinzufügen",
            command=lambda: self.app.events.on_edit_add()
        )
        self.app.gui.add_button.pack(side="left", padx=10)

        self.app.gui.del_button = tk.Button(
            self.app.gui.footer_fr,
            text="Datensatz entfernen",
            command=lambda: self.app.events.on_edit_del()
        )
        self.app.gui.del_button.pack(side="left", padx=10)

        self.app.gui.confirm_button = tk.Button(
            self.app.gui.footer_fr,
            text="Datenreihe importieren",
            command=lambda: self.app.events.on_edit_accept()
        )
        self.app.gui.confirm_button.pack(side="left", padx=10)

        # add entrys for records in temp
        param = list(self.app.data_store.temp.keys())[0]

        num_rows = len(self.app.data_store.temp[param]["actual"])

        for _ in range(num_rows):
            self.app.gui.add_edit_entry()

        for i, row_entries in enumerate(self.app.gui.dat_entries):
            row_data = [
                self.app.data_store.temp[param]["pos. nr."][i],
                self.app.data_store.temp[param]["actual"][i],
                self.app.data_store.temp[param]["nominal"][i],
                self.app.data_store.temp[param]["upper tol."][i],
                self.app.data_store.temp[param]["lower tol."][i],
            ]

            for j, entry in enumerate(row_entries):
                entry.delete(0, tk.END)
                entry.insert(0, row_data[j])

        self.app.gui.root.mainloop()

    def add_edit_entry(self):
        row_entries = []

        for i in range(5):
            dat_entry = tk.Entry(self.app.gui.scrollable_frame)
            if i == 0:
                dat_entry.insert(
                    0,
                    f"Pos. xxx-0{self.app.gui.i_edit+1}" if self.app.gui.i_edit+1 <= 9 else f"Pos. xxx-{self.app.gui.i_edit+1}"
                )
            elif i == 1:
                dat_entry.insert(0, "0.0")
            elif i == 2:
                dat_entry.insert(0, "0.0")
            elif i == 3:
                dat_entry.insert(0, "0.015")
            elif i == 4:
                dat_entry.insert(0, "-0.015")

            dat_entry.grid(
                row=self.app.gui.i_edit + 1,
                column=i,
                sticky="ew",
                padx=10,
                pady=2
            )

            dat_entry.bind(
                "<KeyRelease>",
                lambda event,
                entry=dat_entry: self.app.core.get_edit_data()
            )

            row_entries.append(dat_entry)

        self.app.gui.dat_entries.append(row_entries)
        self.app.gui.i_edit += 1

    def del_edit_entry(self):
        if self.app.gui.dat_entries:
            last_row = self.app.gui.dat_entries.pop()
            for entry in last_row:
                entry.destroy()
            self.app.gui.i_edit -= 1
