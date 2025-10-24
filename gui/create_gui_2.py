import sys
import numpy as np
import pandas as pd
import tkinter as tk
import copy
from datetime import datetime
from tkinter import ttk
from tkinter import messagebox

class AppGUI2:
    def __init__(self, select_dir, import_data, extract_params, tool_number, gen_temp_data, gen_import_data, plot_to_pdf):
        self.select_dir = select_dir
        self.import_data = import_data
        self.extract_params = extract_params
        self.tool_number = tool_number
        self.gen_temp_data = gen_temp_data
        self.gen_import_data = gen_import_data
        self.plot_to_pdf = plot_to_pdf

        self.data = None
        self.temp_data = None
        self.params = []
        self.custom_params=[]
        self.param_widgets = {}
        self.i_cd=0
        
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

        self.temp_arch={}

        self.export_data = {}

        self.mean_data={}

        self.root = tk.Tk()
        self.root.title("Wer das liest ist doof!")
        self.root.geometry("625x600")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.setup_ui()
        self.root.mainloop()

    def on_closing(self):
        self.root.destroy()
        sys.exit()

    def setup_ui(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Scrollbarer Bereich
        self.canvas = tk.Canvas(self.frame)
        self.scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        # Fenster ID merken
        self.window_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Scrollable-Frame an Canvas-Breite anpassen
        self.canvas.bind("<Configure>", lambda event: self.canvas.itemconfig(self.window_id, width=event.width))
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Button-Leiste
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=(10, 10))

        self.import_button = tk.Button(self.button_frame, text="Messberichte importieren", command=self.on_import)
        self.import_button.pack(side="left", padx=10)

        self.button_par=tk.Button(self.button_frame, text="Parameter hinzufuegen", command=self.add_par)
        self.button_par.pack(side="left", padx=10)

        self.export_button = tk.Button(self.button_frame, text="PDF exportieren", command=self.on_export)
        self.export_button.pack(side="left", padx=10)

        self.gen_widget()

    def gen_widget(self):
        # Vorherige Checkboxen löschen
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.param_widgets.clear()

        self.temp_arch={}

        if self.all_data != {}:
            for param, data in self.all_data.items():  # <-- Nutze all_data
                row = tk.Frame(self.scrollable_frame, width=self.canvas.winfo_width())
                row.pack(fill="x", padx=5, pady=2)
                row.bind("<Double-Button-1>", lambda e, p=param: self.edit_data(p))

                var = tk.BooleanVar(value=data.get("checked", False))
                cb = tk.Checkbutton(row,  variable=var, anchor="w", justify="left")
                cb.pack(side="left")
                cb.bind("<Double-Button-1>", lambda e, p=param: self.edit_data(p))

                par_name = tk.Entry(row, width=25)
                par_name.insert(0, str(data.get("par_name", param)))
                par_name.pack(side="left", padx=(10, 2), expand='True', fill='x')
                par_name.bind("<Double-Button-1>", lambda e, p=param: self.edit_data(p))
                par_name.bind("<Return>", lambda e, p=param: self.on_input(p))
                #par_name.bind("<Return>", lambda e, p=param: self.gen_widget())

                tol_frame = tk.Frame(row, width=10)
                tol_frame.pack(side="left", padx=(10, 2), expand='True', fill='x')

                tol_low_label = tk.Label(tol_frame, text="untere Tol.:")
                tol_low_label.pack(side="left", padx=(10, 2))
                tol_low_label.bind("<Double-Button-1>", lambda e, p=param: self.edit_data(p))

                tol_low = tk.Entry(tol_frame, width=10)
                tol_low.insert(0, str(data["lower tol."][0]))
                tol_low.pack(side="left", padx=(10, 2), expand='True')
                tol_low.bind("<Double-Button-1>", lambda e, p=param: self.edit_data(p))
                tol_low.bind("<KeyRelease>", lambda e, p=param: self.on_input(p))
                tol_low.bind("<Return>", lambda e, p=param: self.gen_widget())

                tol_up_label = tk.Label(tol_frame, text="obere Tol.:")
                tol_up_label.pack(side="left", padx=(10, 2))
                tol_up_label.bind("<Double-Button-1>", lambda e, p=param: self.edit_data(p))

                tol_up = tk.Entry(tol_frame, width=6)
                tol_up.insert(0, str(data["upper tol."][0]))
                tol_up.pack(side="left", padx=(10, 20), expand='True')
                tol_up.bind("<Double-Button-1>", lambda e, p=param: self.edit_data(p))
                tol_up.bind("<KeyRelease>", lambda e, p=param: self.on_input(p))
                tol_up.bind("<Return>", lambda e, p=param: self.gen_widget())

                # Entfernen-Button mit 'x'
                remove_btn = tk.Button(
                    tol_frame,
                    text="✕",
                    command=lambda p=param: self.on_remove(p),
                    width=2,
                    relief='flat',
                    bg='white',
                    fg='red',
                    font=("Arial", 10, "bold"),
                    padx=0, pady=0
                )
                remove_btn.pack(side='right', padx=(2, 0))

                # Optionen-Button mit "⋮" (3 vertikale Punkte)
                options_btn = tk.Button(
                    tol_frame,
                    text="⋮",  # U+22EE Vertical Ellipsis
                    command=lambda p=param: self.on_options(p),
                    width=2,
                    relief='flat',
                    bg='white',
                    fg='black',
                    font=("Arial", 10),
                    padx=0, pady=0
                )
                options_btn.pack(side='right', padx=(0, 2))

                self.param_widgets[param] = {
                    "var": var,
                    "par_name": par_name,
                    "tol_low": tol_low,
                    "tol_up": tol_up
                }

    def on_import(self):
        import_dir = self.select_dir()
        if not import_dir:
            messagebox.showinfo("Abbruch", "Kein Ordner ausgewählt.")
            return

        self.label.config(text=f"Importiere aus:\n{import_dir}")
        self.data = self.import_data(import_dir)

        if not self.data:
            messagebox.showwarning("Keine Daten", "Keine gültigen Excel-Dateien gefunden.")
            return

        self.params = self.extract_params(self.data)

        self.imp_data = self.gen_import_data(self.data, self.params)

        self.gen_all_data()

        print(self.all_data)

        self.gen_widget()

    def on_export(self):
        sel_params = []

        for param, widgets in self.param_widgets.items():
            if widgets["var"].get():
                sel_params.append(param)

        print(sel_params)

        if sel_params != []:
            for key, value in self.all_data.items():
                for param in sel_params:
                    if key == param:
                        self.export_data[key] = copy.deepcopy(value)

            print(self.export_data)

            export_dir = self.select_dir()

            self.plot_to_pdf(self.export_data, export_dir, self.tool_number(export_dir))

    def add_par(self):
        param_name = f'Custom_{datetime.now().strftime("%Y%m%d%H%M%S")}'

        self.custom_data[param_name]={
            "pos. nr.": [], 
            "actual": [],
            "nominal": [],
            "lower tol.": [],
            "upper tol.": []
        }

        self.custom_data[param_name]["pos. nr."].append("Pos. xxx-01")
        self.custom_data[param_name]["actual"].append(0.0)
        self.custom_data[param_name]["nominal"].append(0.0)
        self.custom_data[param_name]["lower tol."].append(-0.015)
        self.custom_data[param_name]["upper tol."].append(0.015)

        self.i_cd = self.i_cd+1

        self.gen_all_data()

        self.gen_widget()

    def gen_all_data(self):
        print(self.all_data)
        # all_data leeren
        self.all_data = {}

        # custom_data hinzufügen, wenn vorhanden
        for source in [self.imp_data, self.custom_data]:
            for key, value in source.items():
                self.all_data[key] = copy.deepcopy(value)
        print(self.all_data)

    def on_input(self, p):
        self.get_temp(p)

        self.get_data()

        self.temp_to_data()

        self.gen_all_data()

        self.gen_widget()

    def get_data(self):
        param = list(self.temp.keys())[0]

        n0 = len(self.temp[list(self.temp.keys())[0]]["actual"])

        keys = ["pos. nr.", "actual", "nominal", "upper tol.", "lower tol."]

        del self.temp[list(self.temp.keys())[0]]
        self.temp[self.param_widgets[param]["par_name"].get()]={}

        for key in keys:
            self.temp[self.param_widgets[param]["par_name"].get()][key] = ["" for _ in range(n0)]
            for i in range(n0):
                if key == "pos. nr." or key == "actual" or key == "nominal":
                    self.temp[self.param_widgets[param]["par_name"].get()][key][i] = self.temp_arch[param][key][i]
                elif key == "upper tol.":
                    self.temp[self.param_widgets[param]["par_name"].get()][key][i] = self.param_widgets[param]["tol_up"].get()
                elif key == "lower tol.":
                    self.temp[self.param_widgets[param]["par_name"].get()][key][i] = self.param_widgets[param]["tol_low"].get()

    def get_temp(self, param):
        if param not in self.all_data:
            print(f"Parameter '{param}' nicht in all_data gefunden.")
            return
        
        # Temp-Container zurücksetzen
        self.temp = {}

        # Die Daten des angeklickten Parameters übernehmen
        self.temp[param] = copy.deepcopy(self.all_data[param])
        self.temp_arch[param] = copy.deepcopy(self.temp[param])

    def temp_to_data(self):
        param = list(self.temp_arch.keys())[0]

        # Datenquelle suchen: zuerst imp_data, dann custom_data
        data_sources = [self.imp_data, self.custom_data]

        for source in data_sources:
            if param in source:
                if param != list(self.temp.keys())[0]:
                    del source[param]
                    source[list(self.temp.keys())[0]]={}
                for key in self.temp[list(self.temp.keys())[0]]:
                    source[list(self.temp.keys())[0]][key] = ["" for _ in range(len(self.temp[list(self.temp.keys())[0]]["actual"]))]
                for key, temp_list in self.temp[list(self.temp.keys())[0]].items():
                    for i, value in enumerate(temp_list):
                        # Falls Komma statt Punkt: ersetzen
                        if isinstance(value, str):
                            value = value.replace(",", ".")

                        # Versuche in float zu konvertieren
                        try:
                            value = float(value)
                            # Falls ganzzahlig, konvertiere zu int
                            if value.is_integer():
                                value = int(value)
                        except (ValueError, TypeError):
                            pass  # bleibt string

                        source[list(self.temp.keys())[0]][key][i] = value
                break  # Parameter wurde gefunden → keine weitere Suche nötig

    def edit_data(self,param):
        self.get_temp(param)

        AppEDIT(self,param)

    def on_remove(self,p):
        print("on remove")
        self.get_temp(p)

        for p in self.temp:
            self.arch[p] = copy.deepcopy(self.temp[p])        

        data_sources = [self.imp_data, self.custom_data]

        for source in data_sources:
            if p in source:
                del source[p]

        self.gen_all_data()

        self.gen_widget()

    def on_options(self, p):
        print("on options")
        self.get_temp(p)
        print(self.temp)

        # Menü erstellen
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Duplizieren", command=lambda: self.on_duplicate(p))
        menu.add_command(label="Mittelwert", command=lambda: self.on_mean(p))
        menu.add_command(label="Wiederherstellen", command=lambda: self.on_restore(p))

        # Position des Mauszeigers abfragen (z. B. global aufrufen)
        try:
            x = self.root.winfo_pointerx()
            y = self.root.winfo_pointery()
            menu.tk_popup(x, y)
        finally:
            menu.grab_release()

    def on_duplicate(self, p):
        p_=f"{p}_copy_{datetime.now().strftime("%Y%m%d%H%M%S")}"
        
        for p in self.temp:
            self.custom_data[p_] = copy.deepcopy(self.temp[p])

        self.gen_all_data()

        self.gen_widget()

    def on_mean(self, p):
        self.root.update_idletasks()

        self.get_temp(p)

        keys = self.temp[p].keys()

        # Dummy-Auswahlmöglichkeiten (z. B. Datenfelder)
        options = self.all_data.keys()

        # Zwischenspeicher für Auswahl
        selection_vars = {}

        # Neues Fenster für die Auswahl
        win = tk.Toplevel(self.root, bg="white", highlightbackground="grey", highlightthickness=2)
        win.overrideredirect(True)
        win.title(f"Mittelwert bilden – {p}")
        win.geometry(f"225x132+{self.root.winfo_rootx()+self.root.winfo_width()-225}+{self.root.winfo_rooty()+50}")

        fr = tk.Frame(win, bg="white")
        fr.pack(padx=10, pady=10, fill="both", expand=True)
        
        fr_canvas = tk.Frame(fr, bg="white")
        fr_canvas.pack(fill="both", expand=True)

        # Scrollbarer Bereich
        canvas = tk.Canvas(fr_canvas, height=70, bg="white", highlightthickness=0, bd=0)
        scrollable_fr = tk.Frame(canvas, bg="white")

        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        canvas.bind_all("<MouseWheel>", on_mousewheel)  # Windows

        # Fenster ID merken
        win_id = canvas.create_window((0, 0), window=scrollable_fr, anchor="nw")

        # Scrollable-Frame an Canvas-Breite anpassen
        canvas.bind("<Configure>", lambda event: canvas.itemconfig(win_id, width=event.width))

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
        fr_button.pack(fill="x", pady=(5,0))

        def apply_selection():
            try:
                selected = [opt for opt, var in selection_vars.items() if var.get()]
                
                if selected != []:
                    self.mean_data={}

                    for par in selected:
                        self.mean_data[par]=copy.deepcopy(self.all_data[par])

                    n_0 = len(self.mean_data[selected[0]]['actual'])

                    for par in selected:
                        if len(self.mean_data[par]['actual']) != n_0:
                            print("Abbruch: Datenreihen haben unterschiedliche Anzahl an Datensätzen")
                            return

                    print("Anzahl datensätze immer gleich!")

                    if self.temp[p]["lower tol."] == 0:
                        lower_tol = self.temp[p]["lower tol."]
                    else:
                        lower_tol = self.temp[p]["lower tol."][0]

                    if self.temp[p]["upper tol."] == 0:
                        upper_tol = self.temp[p]["upper tol."]
                    else:
                        upper_tol = self.temp[p]["upper tol."][0]

                    for key in keys:
                        if key == "pos. nr.":
                            self.temp[p][key] = [""] * n_0
                            for i in range(n_0):
                                self.temp[p][key][i] = self.mean_data[selected[0]][key][i]
                        if key == "actual" or key == "nominal":
                            self.temp[p][key] = [0.0] * n_0
                            for i in range(n_0):
                                self.temp[p][key][i]=round(np.mean([self.mean_data[par][key][i] for par in self.mean_data]), 7)
                        if key == "lower tol.":
                            self.temp[p][key] = [lower_tol] * n_0
                        if key == "upper tol.":
                            self.temp[p][key] = [upper_tol] * n_0
                    self.temp_to_data()
                    self.gen_all_data()
                    self.gen_widget()

            finally:
                canvas.unbind_all("<MouseWheel>")
                win.destroy()

        win.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

        button=tk.Button(fr_button, text="OK", command=apply_selection)
        button.pack(side="bottom")
    
    def on_restore(self, p):
        print(p)

class AppEDIT:
    def __init__(self,app_gui,param):
        self.app_gui = app_gui
        self.param=param

        self.i_dat=0
        self.dat_entries = []  # Liste, um die Daten-Eingabefelder zu speichern

        self.root = tk.Toplevel(self.app_gui.root) 
        self.root.title("Daten Eingabe")
        self.root.geometry("1200x400")
        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)

        self.setup_ui()
        self.root.mainloop()

    def setup_ui(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill="both", expand=True)

        self.helper_frame = tk.Frame(self.frame)
        self.helper_frame.pack(fill="both", expand=True)

        # Scrollbarer Bereich
        self.canvas = tk.Canvas(self.helper_frame)
        self.scrollbar = tk.Scrollbar(self.helper_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        # Fenster ID merken
        self.window_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Scrollable-Frame an Canvas-Breite anpassen
        self.canvas.bind("<Configure>", lambda event: self.canvas.itemconfig(self.window_id, width=event.width))

        #self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", padx=(10,10), expand=True)
        self.scrollbar.pack(side="right", fill="y", expand=False)

        # Zeilen für die Labels und Eingabefelder direkt in der scrollbaren Fläche
        self.scrollable_frame.grid_rowconfigure(0, weight=1, uniform="equal")

        self.par_label = tk.Label(self.scrollable_frame, text="Pos Nr.")
        self.par_label.grid(row=0, column=0, sticky="ew", padx=10, pady=2)

        self.actual_label = tk.Label(self.scrollable_frame, text="Messwert")
        self.actual_label.grid(row=0, column=1, sticky="ew", padx=10, pady=2)

        self.nominal_label = tk.Label(self.scrollable_frame, text="Sollwert")
        self.nominal_label.grid(row=0, column=2, sticky="ew", padx=10, pady=2)

        self.upper_tol_label = tk.Label(self.scrollable_frame, text="obere Tol.")
        self.upper_tol_label.grid(row=0, column=3, sticky="ew", padx=10, pady=2)

        self.lower_tol_label = tk.Label(self.scrollable_frame, text="untere Tol.")
        self.lower_tol_label.grid(row=0, column=4, sticky="ew", padx=10, pady=2)
        
        for col in range(5):
            self.scrollable_frame.grid_columnconfigure(col, weight=1, uniform="equal")

        self.footer_fr=tk.Frame(self.frame)
        self.footer_fr.pack(pady=(10,10))

        self.add_button=tk.Button(self.footer_fr, text="Datensatz hinzufügen", command=lambda: self.on_add())
        self.add_button.pack(side="left", padx=10)

        self.del_button=tk.Button(self.footer_fr, text="Datensatz entfernen", command=lambda: self.on_del())
        self.del_button.pack(side="left", padx=10)

        self.confirm_button=tk.Button(self.footer_fr, text="Datenreihe importieren", command=lambda: self.on_accept())
        self.confirm_button.pack(side="left", padx=10)

        self.on_open()

    def on_open(self):
        param = list(self.app_gui.temp.keys())[0]  # z. B. "004_1" oder "Custom-Parameter-1"

        num_rows = len(self.app_gui.temp[param]["actual"])

        for _ in range(num_rows):
            self.add_entry()

        for i, row_entries in enumerate(self.dat_entries):
            row_data = [
                self.app_gui.temp[param]["pos. nr."][i],
                self.app_gui.temp[param]["actual"][i],
                self.app_gui.temp[param]["nominal"][i],
                self.app_gui.temp[param]["upper tol."][i],
                self.app_gui.temp[param]["lower tol."][i],
            ]

            for j, entry in enumerate(row_entries):
                    entry.delete(0, tk.END)
                    entry.insert(0, row_data[j])

    def add_entry(self):
        print("add")
        row_entries = []

        for i in range(5):
            dat_entry = tk.Entry(self.scrollable_frame)
            if i == 0:
                dat_entry.insert(0, f"Pos. xxx-0{self.i_dat+1}" if self.i_dat+1 <= 9 else f"Pos. xxx-{self.i_dat+1}")
            elif i == 1:
                dat_entry.insert(0, "0.0")
            elif i == 2:
                dat_entry.insert(0, "0.0")
            elif i == 3:
                dat_entry.insert(0, "0.015")
            elif i == 4:
                dat_entry.insert(0, "-0.015")

            dat_entry.grid(row=self.i_dat + 1, column=i, sticky="ew", padx=10, pady=2)

            dat_entry.bind("<KeyRelease>", lambda event, entry=dat_entry: self.get_data())

            row_entries.append(dat_entry)

        self.dat_entries.append(row_entries)
        self.i_dat += 1

    def del_entry(self):
        print("delete")
        if self.dat_entries:
            last_row = self.dat_entries.pop()
            for entry in last_row:
                entry.destroy()
            self.i_dat -= 1

    def on_add(self):
        self.add_entry()

        self.get_data()

    def on_del(self):
        self.del_entry()
        
        self.get_data()

    def on_accept(self):
        self.get_data()

        param = list(self.app_gui.temp.keys())[0]  # z. B. "Punktabstand_Punkt1"

        # Datenquelle suchen: zuerst imp_data, dann custom_data
        data_sources = [self.app_gui.imp_data, self.app_gui.custom_data]

        for source in data_sources:
            if param in source:
                for key in self.app_gui.temp[param]:
                    source[param][key] = ["" for _ in range(self.i_dat)]
                for key, temp_list in self.app_gui.temp[param].items():
                    for i, value in enumerate(temp_list):
                        # Falls Komma statt Punkt: ersetzen
                        if isinstance(value, str):
                            value = value.replace(",", ".")

                        # Versuche in float zu konvertieren
                        try:
                            value = float(value)
                            # Falls ganzzahlig, konvertiere zu int
                            if value.is_integer():
                                value = int(value)
                        except (ValueError, TypeError):
                            pass  # bleibt string

                        source[param][key][i] = value
                break  # Parameter wurde gefunden → keine weitere Suche nötig

        self.app_gui.gen_all_data()

        self.root.destroy()

    def get_data(self):
        param = list(self.app_gui.temp.keys())[0]  # z. B. "004_1" oder "Custom-Parameter-1"

        keys = ["pos. nr.", "actual", "nominal", "upper tol.", "lower tol."]

        self.app_gui.temp[param] = {}

        print("vor")
        print(self.app_gui.temp)

        for key in keys:
            self.app_gui.temp[param][key] = ["" for _ in range(self.i_dat)]

        for i, entry in enumerate(self.dat_entries):
            for j, key in enumerate(keys):
                self.app_gui.temp[param][key][i] = entry[j].get()

        print("nach")
        print(self.app_gui.temp)

class AppADD:
    def __init__(self, app_gui):
        self.app_gui = app_gui

        self.par_name = None
        self.par_type = None
        self.custom_data = []
        self.data = []

        self.root = tk.Tk()
        self.root.title("Parameter anlegen")
        self.root.geometry("600x300")

        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)

        self.setup_ui()

        self.root.mainloop()

    def setup_ui(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        self.par_label = tk.Label(self.frame, text="Bezeichnung:")
        self.par_label.pack(side="left", padx=(10, 2))

        self.par_name = tk.Entry(self.frame, width=20)
        self.par_name.insert(0, "unknown")
        self.par_name.pack(side="left", padx=(10, 2))

        self.par_type = ttk.Combobox(self.frame, values=["custom", "median"])
        self.par_type.set("custom")
        self.par_type.pack(side="left", padx=(10, 2))

        # Entferne hier den Aufruf von .get()!
        par_button = tk.Button(self.frame, text="Datenreihe anlegen", command=lambda: self.on_custom(self.par_name, self.par_type))
        par_button.pack(side="left", padx=(10, 2))

        def on_par_type_change(event):
            nonlocal par_button

            if par_button:
                par_button.destroy()
            if self.par_type.get() == "custom":
                par_button = tk.Button(self.frame, text="Datenreihe anlegen", command=lambda: self.on_custom())
            elif self.par_type.get() == "median":
                par_button = tk.Button(self.frame, text="Median definieren", command=lambda: self.on_median())
            
            par_button.pack(side="left", padx=(10, 2))
        
        # Bind für Combobox
        self.par_type.bind("<<ComboboxSelected>>", on_par_type_change)

    def on_custom(self):        
        root = tk.Tk()
        root.title("Daten Eingabe")
        root.geometry("600x400")

        # Treeview Tabelle initialisieren
        tree = ttk.Treeview(root, columns=("Pos", "Actual", "Nominal", "Upper Tol", "Lower Tol"), show="headings")
        tree.heading("Pos", text="Pos. Nr.")
        tree.heading("Actual", text="Actual")
        tree.heading("Nominal", text="Nominal")
        tree.heading("Upper Tol", text="Upper Tol.")
        tree.heading("Lower Tol", text="Lower Tol.")
        tree.insert("", "end", values=["", "", "", "", ""])
        tree.pack(padx=10, pady=10, fill="both", expand=True)

        # Eingabefelder und Labels
        pos_label = tk.Label(root, text="Pos. Nr.")
        pos_label.pack(pady=5)
        pos_entry = tk.Entry(root)
        pos_entry.pack(pady=5)

        actual_label = tk.Label(root, text="Actual")
        actual_label.pack(pady=5)
        actual_entry = tk.Entry(root)
        actual_entry.pack(pady=5)

        nominal_label = tk.Label(root, text="Nominal")
        nominal_label.pack(pady=5)
        nominal_entry = tk.Entry(root)
        nominal_entry.pack(pady=5)

        upper_tol_label = tk.Label(root, text="Upper Tol.")
        upper_tol_label.pack(pady=5)
        upper_tol_entry = tk.Entry(root)
        upper_tol_entry.pack(pady=5)

        lower_tol_label = tk.Label(root, text="Lower Tol.")
        lower_tol_label.pack(pady=5)
        lower_tol_entry = tk.Entry(root)
        lower_tol_entry.pack(pady=5)

    def on_median(self):
        print(self.par_name)
        print("xxx")
        print(self.par_type)
        AppEDIT(self)
