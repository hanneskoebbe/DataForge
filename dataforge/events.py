import sys
from tkinter import messagebox
import copy
from datetime import datetime


class Events:
    def __init__(self, app):
        self.app = app

    def on_closing(self, window):
        window.destroy()
        sys.exit()

    def on_mousewheel(self, event, canvas):
        if event.delta:
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        elif event.num == 4:
            canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            canvas.yview_scroll(1, "units")

    def on_import(self):
        # dialog to choose directory
        import_dir = self.app.gui.select_dir()

        # quit if no directory is choosen
        if not import_dir:
            messagebox.showinfo("Abbruch", "Kein Ordner ausgewählt.")
            return

        # get raw data from directory
        raw_data = self.app.core.gen_raw_import_data(import_dir)

        # quit if no data in directory
        if not raw_data:
            messagebox.showwarning(
                "Keine Daten", "Keine gültigen Excel-Dateien gefunden."
            )
            return

        # gen import_data from raw_data
        self.app.data_store.import_data = self.app.core.gen_import_data(raw_data)

        # gen all_data
        self.app.core.gen_all_data()

        # update gui
        self.app.core.widgets()

    def on_export(self):
        # empty sel_params
        sel_params = []

        # gen sel_params
        for param, widgets in self.app.data_store.widget_data.items():
            if widgets["var"].get():
                sel_params.append(param)

        # empty export_data
        self.app.data_store.export_data = {}

        # check if a parameter is selected
        if sel_params != []:
            # gen export_data
            for key, value in self.app.data_store.all_data.items():
                for param in sel_params:
                    if key == param:
                        self.app.data_store.export_data[key] = copy.deepcopy(value)

            # get export directory
            export_dir = self.app.gui.select_dir()

            # export pdf from export_data
            self.app.core.plot_to_pdf(
                export_dir,
                self.app.core.tool_number(export_dir)
            )

    def on_add_par(self):
        # gen custom name for parameter
        self.app.data_store.custom_id += 1
        param_name = f"Custom_{self.app.data_store.custom_id:02d}"

        # write empty directory in custom_data
        self.app.data_store.all_data["custom"].df[param_name] = {
            "pos. nr.": [],
            "actual": [],
            "nominal": [],
            "lower tol.": [],
            "upper tol.": []
        }

        # define default values
        self.app.data_store.all_data["custom"].df[param_name]["pos. nr."].append("Pos. xxx-01")
        self.app.data_store.all_data["custom"].df[param_name]["actual"].append(0.0)
        self.app.data_store.all_data["custom"].df[param_name]["nominal"].append(0.0)
        self.app.data_store.all_data["custom"].df[param_name]["lower tol."].append(-0.015)
        self.app.data_store.all_data["custom"].df[param_name]["upper tol."].append(0.015)

        # generate all_data
        #self.app.core.gen_all_data()
        print(self.app.data_store.all_data)

        # update gui
        self.app.gui.navigation_bar()

        print(self.app.data_store.all_data)

    def on_input(self, p):
        # get temp for parameter
        self.app.core.get_temp(p)

        # write data from gui into temp
        self.app.core.get_data()

        # write temp into imp_data or custom_data
        self.app.core.temp_to_data()

        # update all_data
        self.app.core.gen_all_data()

        # update gui
        self.app.gui.widgets()

    def on_edit(self, p):
        self.app.core.get_temp(p)

        self.app.gui.edit_window(p)

    def on_edit_add(self):
        self.app.gui.add_edit_entry()

        self.app.core.get_edit_data()

    def on_edit_del(self):
        self.app.gui.del_edit_entry()

        self.app.core.get_edit_data()

    def on_edit_accept(self):
        self.app.core.get_edit_data()

        self.app.core.edit_data_to_data()

        self.app.core.gen_all_data()

        self.app.gui.canvas.unbind_all("<MouseWheel>")

        self.app.gui.root.destroy()

    def on_options(self, p, widget, pos):
        self.app.gui.option_menu(p, widget, pos)

    def on_del(self, p):
        self.app.core.get_temp(p)

        self.app.data_store.arch[p] = copy.deepcopy(self.app.data_store.temp[p])

        print(self.app.data_store.temp)

        for entry in self.app.data_store.all_data.values():
            if p in entry.df:
                del entry.df[p]

        # self.app.core.gen_all_data()

        # self.app.gui.widgets()
        self.app.gui.navigation_bar()

    def on_duplicate(self, p):
        # new parameter name
        p_ = f"{p}_copy"

        # get temp
        self.app.core.get_temp(p)

        # duplicate dataframe
        self.app.data_store.custom_data[p_] = copy.deepcopy(self.app.data_store.temp[p])

        # gen all_data
        self.app.core.gen_all_data()

        # update gui
        self.app.gui.widgets()

    def on_mean(self, p):
        # select parameter
        selected = self.app.gui.selection_window(self.app.data_store.all_data)

        if len(selected) >= 2:
            # get temp
            self.app.core.get_temp(p)

            # gen mean_data and write into temp in temp_data
            self.app.core.gen_mean_data(p, selected)

            # write temp in import_data/custom_data
            self.app.core.temp_to_data()

            # gen all_data
            self.app.core.gen_all_data()

            # update gui
            self.app.gui.widgets()

    def on_restore(self):
        # select parameter
        selected = self.app.gui.selection_window(self.app.data_store.arch)

        # restor dataframe if a parameter is selected
        if selected != []:
            self.app.core.restore_df(selected)

            self.app.core.gen_all_data()

            self.app.gui.widgets()
