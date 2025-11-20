import tkinter as tk
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QScrollArea, QStackedWidget
from PyQt6.QtGui import QIcon, QRegion, QPixmap
from PyQt6.QtCore import Qt, QSize, QRect
from tkinter import ttk
from dataforge.gui import Gui
from dataforge.events import Events
from dataforge.core import Core
from dataforge.data_store import DataStore


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.gui = Gui(self)
        self.events = Events(self)
        self.data_store = DataStore()
        self.core = Core(self)
        self.run2()
        self.workspace_stack.setCurrentIndex(0)

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

        # # main-menu frame
        # self.menu_frame = tk.Frame(self.root)
        # self.menu_frame.pack(side="top", fill="x")

        # self.start_button = tk.Button(self.menu_frame)
        # self.start_button.pack(text="Start", side="left")


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

        # # notebook
        # self.notebook = ttk.Notebook(self.root)
        # self.notebook.pack(fill="both", expand=True)
        # self.notebook.config(height=400)

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
            command=self.gui.plot_all_data
        )
        self.export_button.pack(side="left", padx=10)

        self.gui.widgets()
        self.gui.plot_all_data()
        self.root.mainloop()

    def run2(self):
        self.setWindowTitle("DataForge")

        # central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # main frame -> vertical layout
        self.main_frame = QVBoxLayout(central_widget)

        # menu bar -> horizontal layout
        self.menu_layout = QHBoxLayout()

        # frame for menu bar
        self.menu_frame = QWidget()
        self.menu_frame.setFixedHeight(80)
        self.menu_frame.setStyleSheet("background: #DEDEDE;")
        self.menu_frame.setLayout(self.menu_layout)

        # start button
        self.start_btn = QPushButton()
        self.start_btn.setFixedSize(60, 60)
        self.start_btn.setMask(
            QRegion(
                QRect(0, 0, 60, 60),
                QRegion.RegionType.Ellipse
            )
        )
        img = QPixmap("gui/img/start.png").scaled(
            640,
            640,
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )
        self.start_btn.setIcon(QIcon(img))
        self.start_btn.setIconSize(QSize(60, 60))
        self.start_btn.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent;
                border-radius: 30px;
            }
        """)

        def start_button_clicked():
            print("start test 123")

        self.start_btn.clicked.connect(start_button_clicked)

        self.menu_layout.addWidget(self.start_btn)
        self.menu_layout.addStretch()

        # workspace -> stacked widget (main page, edit page, ...)
        self.workspace_stack = QStackedWidget()

        # frame for workspace
        self.page_main = QWidget()
        self.page_main.setStyleSheet("background: #FFFFFF;")
        self.page_main_layout = QHBoxLayout(self.page_main)
        self.page_main_layout.setContentsMargins(0, 0, 0, 0)

        # navigation layout -> vertical
        self.navigation_layout = QVBoxLayout()
        self.navigation_layout.setSpacing(0)

        # frame for navigation bar
        self.navigation_frame = QWidget()
        self.navigation_frame.setStyleSheet("background: #000000")
        self.navigation_frame.setLayout(self.navigation_layout)

        # scrollable navigation frame
        self.nav_scroll = QScrollArea()
        self.nav_scroll.setWidgetResizable(True)
        self.nav_scroll.setWidget(self.navigation_frame)
        self.nav_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.nav_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # add parameter button
        self.add_btn = QPushButton("+")
        self.add_btn.setFixedSize(20, 20)
        self.add_btn.setStyleSheet(
                "background: #FFFFFF;\
                color: #000000;\
                font-weight: bold;\
                font-size: 14px;"
            )
        self.add_btn.clicked.connect(self.events.on_add_par)

        # add add_btn to navigation bar
        self.navigation_layout.addWidget(self.add_btn)
        self.navigation_layout.addStretch()

        # layout for content frame -> vertical
        self.content_layout = QVBoxLayout()
        self.content_layout.setSpacing(0)

        # frame for content
        self.content_frame = QWidget()
        self.content_frame.setStyleSheet("background: #EEEEEE")
        self.content_frame.setLayout(self.content_layout)

        # layout for content header -> horizontal
        self.content_header_layout = QHBoxLayout()

        # frame for content header
        self.content_header_frame = QWidget()
        self.content_header_frame.setLayout(self.content_header_layout)
        self.content_header_frame.setStyleSheet("background: #FFFFFF")

        # layout for content plot
        self.content_plot_layout = QHBoxLayout()

        # frame for content plot
        self.content_plot_frame = QWidget()
        self.content_plot_frame.setLayout(self.content_plot_layout)
        self.content_plot_frame.setStyleSheet("background: #000000")

        # scrollable plot frame
        self.plot_scroll = QScrollArea()
        self.plot_scroll.setWidgetResizable(True)
        self.plot_scroll.setWidget(self.content_plot_frame)

        # add content to layout
        self.content_layout.addWidget(self.content_header_frame, 1)
        self.content_layout.addWidget(self.plot_scroll, 9)

        # add content to main page layout
        self.page_main_layout.addWidget(self.nav_scroll, 1)
        self.page_main_layout.addWidget(self.content_frame, 9)

        self.page_edit = QWidget()
        self.page_edit.setStyleSheet("background: #EEEEEE;")
        self.page_edit_layout = QVBoxLayout(self.page_edit)
        self.page_edit_layout.setContentsMargins(0, 0, 0, 0)

        # add content to workspace
        self.workspace_stack.addWidget(self.page_main)
        self.workspace_stack.addWidget(self.page_edit)

        # add content to main_frame
        self.main_frame.addWidget(self.menu_frame)
        self.main_frame.addWidget(self.workspace_stack)

        self.showMaximized()
