import tkinter as tk
import pandas as pd
from tkinter import ttk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PyQt6.QtWidgets import (
    QDialog, QWidget, QVBoxLayout, QHBoxLayout, 
    QGridLayout, QLabel, QLineEdit, QPushButton,
    QScrollArea, QMenu
)
from PyQt6.QtCore import Qt


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

        # ===formatting===
        # self.main_bg
        # self.header_bg
        # self.nav_bg
        self.btn_frm = "background: #FDFDFD;\
            color: #000000;\
            font-weight: bold;\
            font-size: 14px;"

        self.header_labels_frm = "background: #EEEEEE;\
            color: #000000;\
            font-weight: bold;\
            font-size: 14px;"

        self.labels_frm = "background: #FFFFFF;\
            color: #000000;\
            font-weight: bold;\
            font-size: 14px;"

        self.entrys = "background: #FFFFFF;\
            color: #000000;\
            font-weight: bold;\
            font-size: 14px;"

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
            item = self.app.navigation_layout.takeAt(0)
            if item.widget() is not None:
                item.widget().deleteLater()

        if any(entry.df for entry in self.app.data_store.all_data.values()):
            for data in self.app.data_store.all_data.values():
                for param in data.df:
                    # layout for row frame
                    self.app.row_layout = QHBoxLayout()
                    self.app.row_layout.setSpacing(0)

                    # new row frame for every parameter
                    self.app.row_frame = QWidget()
                    self.app.row_frame.setLayout(self.app.row_layout)

                    # bind context menu on right click
                    self.app.row_frame.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
                    self.app.row_frame.customContextMenuRequested.connect(
                        lambda pos, p=param, frame=self.app.row_frame:
                            self.app.events.on_options(p, frame, pos)
                    )

                    # bind left click
                    self.app.row_frame.mousePressEvent = (
                        lambda e, p=param:
                            self.app.events.on_df_selected(p)
                            if e.button() == Qt.MouseButton.LeftButton else None
                    )

                    # label for param
                    self.app.param_label = QLabel(param)
                    self.app.param_label.setStyleSheet(self.app.gui.header_labels_frm)

                    # delete button
                    self.app.del_btn = QPushButton("X")
                    self.app.del_btn.setStyleSheet(self.app.gui.btn_frm)
                    self.app.del_btn.setFixedSize(20, 20)
                    self.app.del_btn.clicked.connect(
                        lambda checked=False, p=param: self.app.events.on_del(p)
                    )

                    # add content to row layout
                    self.app.row_layout.addWidget(self.app.param_label)
                    self.app.row_layout.addStretch()
                    self.app.row_layout.addWidget(self.app.del_btn)

                    # add row frame to navigation bar
                    self.app.navigation_layout.addWidget(self.app.row_frame)

        # add parameter button
        self.app.add_btn = QPushButton("+")
        self.app.add_btn.setFixedSize(20, 20)
        self.app.add_btn.setStyleSheet(self.app.gui.btn_frm)
        self.app.add_btn.clicked.connect(self.app.events.on_add_par)

        # add add_btn to navigation bar
        self.app.navigation_layout.addWidget(self.app.add_btn)
        self.app.navigation_layout.addStretch()

    def content_header(self, p):
        # ====header===
        for data in self.app.data_store.all_data.values():
            for param in data.df:
                if param == p:
                    minimum = pd.Series(data.df[p]["actual"]).min()
                    maximum = pd.Series(data.df[p]["actual"]).max()
                    sigma = pd.Series(data.df[p]["actual"]).std()
                    mean = pd.Series(data.df[p]["actual"]).mean()

        while self.app.content_header_layout.count():
            item = self.app.content_header_layout.takeAt(0)
            if item.widget() is not None:
                item.widget().deleteLater()

        # param layout -> vertical
        self.app.param_layout = QVBoxLayout()

        # param frame
        self.app.param_frame = QWidget()
        self.app.param_frame.setLayout(self.app.param_layout)

        # param title label
        self.app.content_param_label_title = QLabel("Parameter:")
        self.app.content_param_label_title.setStyleSheet(self.app.gui.header_labels_frm)

        # param label
        self.app.content_param_label = QLabel(p)
        self.app.content_param_label.setStyleSheet(self.app.gui.labels_frm)

        # add to param layout
        self.app.param_layout.addWidget(self.app.content_param_label_title)
        self.app.param_layout.addWidget(self.app.content_param_label)
        self.app.param_layout.addStretch()

        # min layout -> vertical
        self.app.min_layout = QVBoxLayout()

        # min frame
        self.app.min_frame = QWidget()
        self.app.min_frame.setLayout(self.app.min_layout)

        # min title label
        self.app.min_label_title = QLabel("Min:")
        self.app.min_label_title.setStyleSheet(self.app.gui.header_labels_frm)

        # min label
        self.app.min_label = QLabel(str(minimum))
        self.app.min_label.setStyleSheet(self.app.gui.labels_frm)

        # add to min layout
        self.app.min_layout.addWidget(self.app.min_label_title)
        self.app.min_layout.addWidget(self.app.min_label)
        self.app.min_layout.addStretch()

        # max layout -> vertical
        self.app.max_layout = QVBoxLayout()

        # max frame
        self.app.max_frame = QWidget()
        self.app.max_frame.setLayout(self.app.max_layout)

        # max title label
        self.app.max_label_title = QLabel("Max:")
        self.app.max_label_title.setStyleSheet(self.app.gui.header_labels_frm)

        # max label
        self.app.max_label = QLabel(str(maximum))
        self.app.max_label.setStyleSheet(self.app.gui.labels_frm)

        # add to max layout
        self.app.max_layout.addWidget(self.app.max_label_title)
        self.app.max_layout.addWidget(self.app.max_label)
        self.app.max_layout.addStretch()

        # sigma layout -> vertical
        self.app.sigma_layout = QVBoxLayout()

        # sigma frame
        self.app.sigma_frame = QWidget()
        self.app.sigma_frame.setLayout(self.app.sigma_layout)

        # sigma title label
        self.app.sigma_label_title = QLabel("Sigma:")
        self.app.sigma_label_title.setStyleSheet(self.app.gui.header_labels_frm)

        # sigma label
        self.app.sigma_label = QLabel(str(sigma))
        self.app.sigma_label.setStyleSheet(self.app.gui.labels_frm)

        # add to sigma layout
        self.app.sigma_layout.addWidget(self.app.sigma_label_title)
        self.app.sigma_layout.addWidget(self.app.sigma_label)
        self.app.sigma_layout.addStretch()

        # mean layout -> vertical
        self.app.mean_layout = QVBoxLayout()

        # mean frame
        self.app.mean_frame = QWidget()
        self.app.mean_frame.setLayout(self.app.mean_layout)

        # mean title label
        self.app.mean_label_title = QLabel("Mean:")
        self.app.mean_label_title.setStyleSheet(self.app.gui.header_labels_frm)

        # mean label
        self.app.mean_label = QLabel(str(mean))
        self.app.mean_label.setStyleSheet(self.app.gui.labels_frm)

        # add to mean layout
        self.app.mean_layout.addWidget(self.app.mean_label_title)
        self.app.mean_layout.addWidget(self.app.mean_label)
        self.app.mean_layout.addStretch()

        # add content to header
        self.app.content_header_layout.addWidget(self.app.param_frame, 2)
        self.app.content_header_layout.addWidget(self.app.min_frame, 2)
        self.app.content_header_layout.addWidget(self.app.max_frame, 2)
        self.app.content_header_layout.addWidget(self.app.sigma_frame, 2)
        self.app.content_header_layout.addWidget(self.app.mean_frame, 2)

    def content_plot_df(self, p):
        # ====plot===
        while self.app.content_plot_layout.count():
            item = self.app.content_plot_layout.takeAt(0)
            if item.widget() is not None:
                item.widget().deleteLater()

        idx = "pos. nr."

        for data in self.app.data_store.all_data.values():
            for param in data.df:
                if param == p:
                    df_dict = data.df[param]

        # matlpotlib figure + axis
        fig = Figure(figsize=(10, 6))
        ax = fig.add_subplot(111)

        # plot
        ax.plot(
            df_dict.get(idx, []),
            [float(str(x).replace(",", "."))
                for x in df_dict.get("actual", [])],
            label="actual", marker="o"
        )
        ax.plot(
            df_dict.get(idx, []),
            [float(str(x).replace(",", "."))
                for x in df_dict.get("nominal", [])],
            label="nominal", linestyle="-", color="green"
        )
        ax.plot(
            df_dict.get(idx, []),
            [n + u for n, u in zip(
                [float(str(x).replace(",", "."))
                    for x in df_dict.get("nominal", [])],
                [float(str(x).replace(",", "."))
                    for x in df_dict.get("upper tol.", [])]
                )],
            label="upper tol.", linestyle="-", color="red"
        )
        ax.plot(
            df_dict.get(idx, []),
            [n + l for n, l in zip(
                [float(str(x).replace(",", "."))
                    for x in df_dict.get("nominal", [])],
                [float(str(x).replace(",", "."))
                    for x in df_dict.get("lower tol.", [])]
                )],
            label="lower tol.", linestyle="-", color="red"
        )

        # format plot
        ax.set_title(f"chart: {p}")
        ax.set_xlabel("pos. nr.")
        ax.set_ylabel("value")
        ax.legend()
        ax.grid(True)
        ax.set_xticks(df_dict.get(idx, []))
        ax.tick_params(axis="x", rotation=45)
        fig.tight_layout()

        # Plot in Tkinter-Canvas einbetten
        self.app.plot_canvas = FigureCanvas(fig)
        self.app.content_plot_layout.addWidget(self.app.plot_canvas)

        self.app.plot_canvas.draw()
        
        # bind double mouseclick
        self.app.plot_canvas.mouseDoubleClickEvent = (
            lambda e, p_=param:
                self.app.events.on_edit_data(p_)
                if e.button() == Qt.MouseButton.LeftButton else None
        )

    def edit_page(self, p):
        while self.app.page_edit_layout.count():
            item = self.app.page_edit_layout.takeAt(0)
            if item.widget() is not None:
                item.widget().deleteLater()

        # header frame for title
        self.app.edit_header_frame = QWidget()
        self.app.edit_header_layout = QHBoxLayout(self.app.edit_header_frame)
        self.app.edit_header_frame.setStyleSheet(
            "color: #000000;\
            font-weight: bold;\
            font-size: 14px;"
        )

        # labels for header
        self.app.edit_id_label = QLabel("ID")
        self.app.edit_id_label.setStyleSheet(self.app.gui.header_labels_frm)

        self.app.edit_actual_label = QLabel("actual")
        self.app.edit_actual_label.setStyleSheet(self.app.gui.header_labels_frm)

        self.app.edit_nominal_label = QLabel("nominal")
        self.app.edit_nominal_label.setStyleSheet(self.app.gui.header_labels_frm)

        self.app.edit_low_tol_label = QLabel("lower tol.")
        self.app.edit_low_tol_label.setStyleSheet(self.app.gui.header_labels_frm)

        self.app.edit_upper_tol_label = QLabel("upper tol.")
        self.app.edit_upper_tol_label.setStyleSheet(self.app.gui.header_labels_frm)

        # add content to header layout
        self.app.edit_header_layout.addWidget(self.app.edit_id_label, 2)
        self.app.edit_header_layout.addWidget(self.app.edit_actual_label, 2)
        self.app.edit_header_layout.addWidget(self.app.edit_nominal_label, 2)
        self.app.edit_header_layout.addWidget(self.app.edit_low_tol_label, 2)
        self.app.edit_header_layout.addWidget(self.app.edit_upper_tol_label, 2)

        # data frame
        self.app.edit_data_frame = QWidget()
        self.app.edit_data_layout = QVBoxLayout(self.app.edit_data_frame)

        # data table
        self.app.edit_data_table = QWidget()
        self.app.edit_data_table_layout = QGridLayout(self.app.edit_data_table)

        self.app.edit_data_scroll = QScrollArea()
        self.app.edit_data_scroll.setWidgetResizable(True)
        self.app.edit_data_scroll.setWidget(self.app.edit_data_frame)

        # add content to data layout
        self.app.edit_data_layout.addWidget(self.app.edit_data_table)
        self.app.edit_data_layout.addStretch()

        # footer frame for buttons
        self.app.edit_footer_frame = QWidget()
        self.app.edit_footer_layout = QHBoxLayout(self.app.edit_footer_frame)

        self.app.add_btn = QPushButton("add")
        self.app.add_btn.setStyleSheet(self.app.gui.btn_frm)
        self.app.add_btn.clicked.connect(lambda: self.app.events.on_edit_add(p))

        self.app.del_btn = QPushButton("del")
        self.app.del_btn.setStyleSheet(self.app.gui.btn_frm)
        self.app.del_btn.clicked.connect(lambda: self.app.events.on_edit_del(p))

        self.app.confirm_btn = QPushButton("confirm")
        self.app.confirm_btn.setStyleSheet(self.app.gui.btn_frm)
        self.app.confirm_btn.clicked.connect(lambda: self.app.events.on_edit_confirm(p))

        self.app.edit_footer_layout.addWidget(self.app.add_btn, 1)
        self.app.edit_footer_layout.addWidget(self.app.del_btn, 1)
        self.app.edit_footer_layout.addStretch(10)
        self.app.edit_footer_layout.addWidget(self.app.confirm_btn, 1)

        # add content to page edit layout
        self.app.page_edit_layout.addWidget(self.app.edit_header_frame, 1)
        self.app.page_edit_layout.addWidget(self.app.edit_data_scroll, 8)
        self.app.page_edit_layout.addWidget(self.app.edit_footer_frame, 1)

        self.app.gui.gen_data_table(p)

    def gen_data_table(self, p):
        self.dat_entries = []
        self.app.gui.i_edit = 0

        # empty data table
        while self.app.edit_data_table_layout.count():
            item = self.app.edit_data_table_layout.takeAt(0)
            if item.widget() is not None:
                item.widget().deleteLater()

        # add entrys for records in temp
        num_rows = len(self.app.data_store.temp[p]["actual"])

        for i in range(num_rows):
            self.app.gui.add_edit_entry()

        for i, row_entries in enumerate(self.app.gui.dat_entries):
            row_data = [
                self.app.data_store.temp[p]["pos. nr."][i],
                self.app.data_store.temp[p]["actual"][i],
                self.app.data_store.temp[p]["nominal"][i],
                self.app.data_store.temp[p]["lower tol."][i],
                self.app.data_store.temp[p]["upper tol."][i]
            ]

            for j, entry in enumerate(row_entries):
                entry.clear()
                entry.setText(str(row_data[j]))

    def add_edit_entry(self):
        row_entries = []

        for i in range(5):
            self.app.dat_entry = QLineEdit()
            self.app.dat_entry.setStyleSheet(self.app.gui.entrys)
            # add content
            self.app.edit_data_table_layout.addWidget(
                self.app.dat_entry,
                self.app.gui.i_edit + 1,
                i
            )

            self.app.dat_entry.textChanged.connect(
                lambda _,
                    entry = self.app.dat_entry,
                    row = self.app.gui.i_edit,
                    col = i: self.app.events.on_data_changed(entry, row, col)
            )

            row_entries.append(self.app.dat_entry)

        self.app.gui.dat_entries.append(row_entries)
        self.app.gui.i_edit += 1

    def del_edit_entry(self):
        if self.app.gui.dat_entries:
            last_row = self.app.gui.dat_entries.pop()
            for entry in last_row:
                entry.destroy()
            self.app.gui.i_edit -= 1

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

    def option_menu(self, p, widget, pos):
        # gen menu
        self.app.gui.menu = QMenu(widget)

        # duplicate df
        self.app.gui.action_dup = self.app.gui.menu.addAction("Duplizieren")
        self.app.gui.action_dup.triggered.connect(
            lambda checked=False, p=p: self.app.events.on_duplicate(p)
        )

        # transform df to mean of dfs
        self.app.gui.action_mean = self.app.gui.menu.addAction("Mittelwert")
        self.app.gui.action_mean.triggered.connect(    
            lambda checked=False, p=p: self.app.events.on_mean(p)
        )

        # restore df
        self.app.gui.action_restore = self.app.gui.menu.addAction("Wiederherstellen")
        self.app.gui.action_restore.triggered.connect(
            lambda checked=False: self.app.events.on_restore()
        )

        # execution
        self.app.gui.menu.exec(widget.mapToGlobal(pos))

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
