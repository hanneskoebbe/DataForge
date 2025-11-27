import sys
from tkinter import messagebox
import copy
from datetime import datetime
from dataforge.data_store import DataEntry
import pandas as pd


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

    def on_start_new(self):
        # get name and directory from dialog
        name, directory = self.app.gui.f_new_dialog("New File")

        names = [name, "custom"]
        source = ["_init_", "custom"]
        dir_ = [directory, None]
        crtd = [None, None]
        data = [{},{}]

        # init all_data
        for i, src in enumerate(source):
            self.app.core.init_data(names[i], src, dir_[i], crtd[i], data[i])

        # save file
        self.app.core.f_save(name, directory)

        # main page
        for _, entry in self.app.data_store.all_data.items():
            if '_init_' in entry.source:
                self.app.workspace_stack.setCurrentIndex(0)

        print(self.app.data_store.all_data)

    def on_start_open(self):
        # get name and directory from dialog
        name, directory = self.app.gui.f_open_dialog("Open")

        # open file
        self.app.core.f_open(name, directory)

        # main page and update gui
        for _, entry in self.app.data_store.all_data.items():
            if '_init_' in entry.source:
                self.app.workspace_stack.setCurrentIndex(0)
                self.app.gui.navigation_bar()
        print("Opend...")

    def on_start_save(self):
        name = list(self.app.data_store.all_data.keys())[0]
        directory = self.app.data_store.all_data[name].directory

        self.app.core.f_save(name, directory)
        self.app.workspace_stack.setCurrentIndex(0)
        print("Saved")

    def on_start_save_as(self):
         # get name and directory from dialog
        name, directory = self.app.gui.f_new_dialog("Save as")

        # write name, directory in all_data
        self.app.core.change_init(name, directory)

        # save all data
        self.app.core.f_save(name, directory)
        self.app.workspace_stack.setCurrentIndex(0)
        print("Saved")

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

        # update gui
        self.app.gui.navigation_bar()

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

#neu
    def on_edit_data(self, p):
        self.app.workspace_stack.setCurrentIndex(1)

        self.app.core.get_temp(p)

        self.app.gui.edit_page(p)

#neu
    def on_data_changed(self, entry, row, col):
        # update temp
        self.app.core.record_to_temp(entry, row, col)

        # update all_data
        self.app.core.temp_to_all_data()

#neu
    def on_edit_add(self, p):
        # add record in temp
        self.app.core.temp_add_record(p)

        # update all_data
        self.app.core.temp_to_all_data()

        # update data table
        self.app.gui.gen_data_table(p)

#neu
    def on_edit_del(self,p):
        self.app.gui.i_edit =-1

        # del record in temp
        self.app.core.temp_del_record(p)

        # update all_data
        self.app.core.temp_to_all_data()

        # update data table
        self.app.gui.gen_data_table(p)

#neu
    def on_edit_confirm(self, p):
        self.app.workspace_stack.setCurrentIndex(0)

        self.app.gui.content_header(p)

        self.app.gui.content_plot_df(p)

#neu
    def on_df_selected(self, p):
        self.app.core.get_temp(p)

        self.app.gui.content_header(p)

        self.app.gui.content_plot_df(p)

    def on_options(self, p, widget, pos):
        self.app.gui.option_menu(p, widget, pos)

    def on_del(self, p):
        self.app.core.get_temp(p)

        self.app.data_store.arch[p] = copy.deepcopy(self.app.data_store.temp[p])

        print(self.app.data_store.temp)

        for entry in self.app.data_store.all_data.values():
            if p in entry.df:
                del entry.df[p]

        # set file save status on false
        self.app.core.file_saved = False

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
