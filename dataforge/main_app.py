import tkinter as tk
from PyQt6.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QLabel, QPushButton, QScrollArea, QStackedWidget, QMenu, QStyle
from PyQt6.QtGui import QIcon, QRegion, QPixmap
from PyQt6.QtCore import Qt, QSize, QRect
from tkinter import ttk
from dataforge.gui import Gui
from dataforge.events import Events
from dataforge.core import Core
from dataforge.data_store import DataStore, DataEntry


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.gui = Gui(self)
        self.events = Events(self)
        self.data_store = DataStore()
        self.core = Core(self)
        self.run()
        self.workspace_stack.setCurrentIndex(2)

    def run(self):
        self.setWindowTitle("DataForge")

        # central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # main frame -> vertical layout
        self.main_frame = QVBoxLayout(self.central_widget)

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

        # start button menu
        self.start_menu = QMenu(self.start_btn)

        # options for start menu
        self.start_open = self.start_menu.addAction(
            self.start_menu.style().standardIcon(QStyle.StandardPixmap.SP_DialogOpenButton),
            "Open..."
        )
        self.start_new = self.start_menu.addAction(
            self.start_menu.style().standardIcon(QStyle.StandardPixmap.SP_FileIcon),
            "New project"
        )
        self.start_save = self.start_menu.addAction(
            self.start_menu.style().standardIcon(QStyle.StandardPixmap.SP_DialogSaveButton),
            "Save"
        )
        self.start_save_as = self.start_menu.addAction(
            self.start_menu.style().standardIcon(QStyle.StandardPixmap.SP_DialogSaveButton),
            "Save as..."
        )

        # actions for start menu
        self.start_open.triggered.connect(self.events.on_start_open)
        self.start_new.triggered.connect(self.events.on_start_new)
        self.start_save.triggered.connect(self.events.on_start_save)
        self.start_save_as.triggered.connect(self.events.on_start_save_as)

        #
        self.start_btn.clicked.connect(
            lambda: self.start_menu.exec(
                self.start_btn.mapToGlobal(self.start_btn.rect().bottomLeft())
            )
        )

        self.menu_layout.addWidget(self.start_btn)
        self.menu_layout.addStretch()

        # workspace -> stacked widget (main page, edit page, ..., empty start page)
        self.workspace_stack = QStackedWidget()

        # main page
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
        self.content_frame.setStyleSheet("background: #FDFDFD")
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

        # edit page
        self.page_edit = QWidget()
        self.page_edit.setStyleSheet("background: #EEEEEE;")
        self.page_edit_layout = QVBoxLayout(self.page_edit)
        self.page_edit_layout.setContentsMargins(0, 0, 0, 0)

        # start page -> empty (shown when app is started and no project is opend)
        self.page_start = QWidget()
        self.page_start.setStyleSheet("background: #EEEEEE;")

        # add content to workspace
        self.workspace_stack.addWidget(self.page_main)
        self.workspace_stack.addWidget(self.page_edit)
        self.workspace_stack.addWidget(self.page_start)

        # add content to main_frame
        self.main_frame.addWidget(self.menu_frame)
        self.main_frame.addWidget(self.workspace_stack)

        self.showMaximized()
