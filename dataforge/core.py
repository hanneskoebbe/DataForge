import copy
import json
import csv
import numpy as np
import pandas as pd
import os as os
import matplotlib.pyplot as plt
from dataforge.data_store import DataEntry
from matplotlib.backends.backend_pdf import PdfPages
from datetime import date


class Core:
    def __init__(self, app):
        self.app = app
        self.file_saved = False
        self.tolerance = ["lower tol.", "upper tol."]
        self.keys = ["pos. nr.", "actual", "nominal", "lower tol.", "upper tol."]

    def init_data(self, name, src, dir, crtd, data):      
        self.app.data_store.all_data[name] = DataEntry(
            source=src,
            directory=dir,
            created=crtd,
            df=data
        )

    def f_save(self, name, dir):
        # file path
        file_path = os.path.join(dir)

        if name.endswith(".txt"):
            with open(file_path, 'w') as f:
                for key, entry in self.app.data_store.all_data.items():
                    f.write(f"Key: {key}\n")
                    f.write(f"Source: {entry.source}\n")
                    f.write(f"Directory: {entry.directory}\n")
                    f.write(f"Created: {entry.created}\n")
                    f.write(f"DF:\n{json.dumps(entry.df, indent=4)}\n")
                    self.app.core.file_saved = True
        elif name.endswith(".csv"):
            with open(file_path, 'w', newline='') as f:
                writer = csv.writer(f)
                
                # Write the header row
                writer.writerow(["Key", "Source", "Directory", "Created", "DataFrame"])
                
                # Write the data rows
                for key, entry in self.app.data_store.all_data.items():
                    # Convert DataFrame (df) to a string or JSON format for CSV storage
                    df_json = json.dumps(entry.df, indent=4) if entry.df else ''
                    writer.writerow([key, entry.source, entry.directory, entry.created, df_json])

                self.app.core.file_saved = True

    def f_open(self, name, dir):
        # Construct the full file path
        file_path = os.path.join(dir)

        if name.endswith(".txt"):
            with open(file_path, 'r') as f:
                df = {}
                row = None
                key = None
                df_key = None
                df_entry = None
                row_key = None

                for line in f:
                    line = line.strip()
                    if line.startswith("Key:"):
                        if key:
                            self.app.core.init_data(key, src, dir, crtd, df[key]) # Store before starting a new one
                        key = line.split(":")[1].strip()  # Extract key
                        df[key]={}
                    elif line.startswith("Source:"):
                        src = line.split("Source:")[1].strip()
                    elif line.startswith("Directory:"):
                        dir_val = line.split("Directory:")[1].strip()
                        dir = None if dir_val == "None" else dir_val
                    elif line.startswith("Created:"):
                        crtd_val = line.split("Created:")[1].strip()
                        crtd = None if crtd_val == "None" else crtd_val
                    else:
                        if line.endswith(": {"):
                            if df_key and df_entry:
                                df[key][df_key] = df_entry # Store the previous df_entry before starting a new one
                                if row_key and row:
                                    df_entry[row_key] = row
                                    row = None
                            df_key = json.loads(line.split(":")[0].strip()) # Extract key
                            df[key][df_key] = {}
                            df_entry = {}
                        elif line.endswith(": ["):
                            if row_key and row:
                                df_entry[row_key] = row
                            row_key = json.loads(line.split(":")[0].strip())  # Extract key
                            row = []
                        elif not line.startswith("]") and not line.startswith("DF:") and not line.startswith("{") and not line.startswith("}"):
                            row.append(json.loads(line.strip().rstrip(",")))
                if df_key and df_entry: # Store the last df_entry
                    df_entry[row_key] = row
                    df[key][df_key] = df_entry
                if key:  # Store the last one
                    self.app.core.init_data(key, src, dir, crtd, df[key])
        elif name.endswith(".csv"):
            with open(file_path, 'r') as f:
                key = None
                reader = csv.reader(f)
                headers = next(reader)  # Skip header row
                df = {}
                for row in reader:
                    if key:
                        self.app.core.init_data(key, src, dir, crtd, df)
                    key, src, directory, created, df_json = row
                    dir = directory or None
                    crtd = created or None
                    df = json.loads(df_json) if df_json else {}  # Deserialize the DataFrame (JSON)
                if key:
                    self.app.core.init_data(key, src, dir, crtd, df)

    def gen_raw_excel_data(self, dir):
        data = {}
        i = 0
        name_list = self.app.core.get_name_list(dir)
        for name in name_list:
            # skip temporary excel files
            if name.startswith('~$'):
                print(f"Achtung Excel mit dem Namen {name} geöffnet!")
                continue
            # gen os path
            os_dir = os.path.join(dir, name)
            data[i] = pd.read_excel(os_dir)
            i += 1
        return data

    def get_name_list(self, dir):
        name_list = [
            f for f in os.listdir(dir) if f.lower().endswith(('.xlsx', '.xls'))
            ]
        return name_list

    def gen_import_data(self, data):
        self.app.data_store.import_data = {}

        for _, df in data.items():
            # clean dataframe
            df_clean = df.iloc[12:].reset_index(drop=True)
            df_clean.columns = df.iloc[11]

            # identify dataframe
            part_no = df.iloc[6]["Unnamed: 5"]

            # gen import_data
            for _, row in df_clean.iterrows():
                param = row["Characteristic"]

                # default
                if param not in self.app.data_store.import_data:
                    self.app.data_store.import_data[param] = {
                        "pos. nr.": [],
                        "actual": [],
                        "nominal": [],
                        "upper tol.": [],
                        "lower tol.": [],
                    }

                self.app.data_store.import_data[param]["pos. nr."].append(part_no)
                self.app.data_store.import_data[param]["actual"].append(row["Actual"])
                self.app.data_store.import_data[param]["nominal"].append(row["Nominal"])
                self.app.data_store.import_data[param]["upper tol."].append("0.015")
                self.app.data_store.import_data[param]["lower tol."].append("-0.015")

    def gen_all_data(self):
        # reset all_data
        self.app.data_store.all_data = {}

        data_source = [
            self.app.data_store.import_data,
            self.app.data_store.custom_data
        ]

        # add to all_data if not empty
        for source in data_source:
            for key, value in source.items():
                self.app.data_store.all_data[key] = copy.deepcopy(value)

        # sort all_data alphabetically
        self.app.data_store.all_data = dict(sorted(
            self.app.data_store.all_data.items(),
            key=lambda item: item[0].lower())
        )

    def get_data(self):
        # get param
        param = list(self.app.data_store.temp.keys())[0]

        # count records
        n0 = len(self.app.data_store.temp[list(self.app.data_store.temp.keys())[0]]["actual"])

        keys = ["pos. nr.", "actual", "nominal", "upper tol.", "lower tol."]

        # delete temp
        del self.app.data_store.temp[list(self.app.data_store.temp.keys())[0]]

        # init temp as dictionary
        self.app.data_store.temp[self.app.data_store.widget_data[param]["par_name"].get()] = {}

        for key in keys:
            self.app.data_store.temp[
                self.app.data_store.widget_data[param]["par_name"].get()
            ][key] = ["" for _ in range(n0)]
            for i in range(n0):
                if key == "pos. nr." or key == "actual" or key == "nominal":
                    self.app.data_store.temp[
                        self.app.data_store.widget_data[param]["par_name"].get()
                    ][key][i] = self.app.data_store.temp_arch[param][key][i]
                elif key == "upper tol.":
                    self.app.data_store.temp[
                        self.app.data_store.widget_data[param]["par_name"].get()
                    ][key][i] = self.app.data_store.widget_data[param]["tol_up"].get()
                elif key == "lower tol.":
                    self.app.data_store.temp[
                        self.app.data_store.widget_data[param]["par_name"].get()
                    ][key][i] = self.app.data_store.widget_data[param]["tol_low"].get()

    def get_temp(self, p):
        # reset temp
        self.app.data_store.temp = {}

        # reset temp_arch
        self.app.data_store.temp_arch = {}

        # check if parameter exists
        if not any(p in entry.df for entry in self.app.data_store.all_data.values()):
            print(f"Parameter '{p}' nicht in all_data gefunden.")
            return

        for entry in self.app.data_store.all_data.values():
            if p in entry.df:
                # write directory from all_data to temp for parameter
                self.app.data_store.temp[p] = copy.deepcopy(
                    entry.df[p]
                )

                # write temp into temp archive to not lose temp while changing it
                self.app.data_store.temp_arch[p] = copy.deepcopy(
                    entry.df[p]
                )

    def temp_to_data(self):
        param = list(self.app.data_store.temp_arch.keys())[0]

        # init data_source: import_data + custom_data
        data_sources = [
            self.app.data_store.import_data,
            self.app.data_store.custom_data
        ]

        for source in data_sources:
            if param in source:
                # delete dataframe if parameter name is changed
                if param != list(self.app.data_store.temp.keys())[0]:
                    del source[param]
                    source[list(self.app.data_store.temp.keys())[0]] = {}
                # write records in source
                self.app.core.records_to_source(source)
                break  # break when parameter is found

    def records_to_source(self, source):
        # empty source dataframe
        for key in self.app.data_store.temp[list(self.app.data_store.temp.keys())[0]]:
            source[
                list(self.app.data_store.temp.keys())[0]
            ][key] = ["" for _ in range(len(self.app.data_store.temp[
                list(self.app.data_store.temp.keys())[0]
            ]["actual"]))]
        # temp to source
        for key, temp_list in self.app.data_store.temp[list(self.app.data_store.temp.keys())[0]].items():
            for i, value in enumerate(temp_list):
                source[
                    list(self.app.data_store.temp.keys())[0]
                ][key][i] = self.app.core.convert_seperator(value)

    def convert_seperator(self, value):
        # replace comma with point
        if isinstance(value, str):
            value = value.replace(",", ".")
        # try to convert string to float
        try:
            value = float(value)
        except (ValueError, TypeError):
            pass  # record is still a string (pos. nr.)
        return value

    def get_edit_data(self):
        param = list(self.app.data_store.temp.keys())[0]

        keys = ["pos. nr.", "actual", "nominal", "upper tol.", "lower tol."]

        self.app.data_store.temp[param] = {}

        for key in keys:
            self.app.data_store.temp[param][key] = ["" for _ in range(self.app.gui.i_edit)]

        for i, entry in enumerate(self.app.gui.dat_entries):
            for j, key in enumerate(keys):
                self.app.data_store.temp[param][key][i] = entry[j].get()

    def edit_data_to_data(self):
        param = list(self.app.data_store.temp.keys())[0]

        # find source in import_data and custom_data
        data_sources = [
            self.app.data_store.import_data,
            self.app.data_store.custom_data
        ]

        for source in data_sources:
            if param in source:
                for key, temp_list in self.app.data_store.temp[param].items():
                    new = []
                    for value in temp_list:
                        # convert seperator
                        value = self.app.core.convert_seperator(value)
                        new.append(value)
                    source[param][key] = new
                break  # break when parameter is found

 # neu
    def temp_add_record(self, p):
        for key in self.app.core.keys:
            if key == "pos. nr.":
                self.app.data_store.temp[p][key].append(f"Pos. xxx-{self.app.gui.i_edit+1:02d}")
            elif key == "actual":
                self.app.data_store.temp[p][key].append("0.0")
            elif key == "nominal":
                self.app.data_store.temp[p][key].append("0.0")
            elif key == "lower tol.":
                self.app.data_store.temp[p][key].append("-0.015")
            elif key == "upper tol.":
                self.app.data_store.temp[p][key].append("0.015")

# neu
    def temp_del_record(self, p):
        for key in self.app.core.keys:
            del self.app.data_store.temp[p][key][self.app.gui.i_edit]

# neu
    def record_to_temp(self, entry, row, col):
        param = list(self.app.data_store.temp.keys())[0]
        
        self.app.data_store.temp[param][self.app.core.keys[col]][row] = self.app.core.convert_seperator(entry.text())

    def temp_to_all_data(self):
        param = list(self.app.data_store.temp.keys())[0]

        for data in self.app.data_store.all_data.values():
            for p in data.df:
                if p == param:
                    data.df[p] = self.app.data_store.temp[p]
        
        # set file save status on false
        self.app.core.file_saved = False

    def gen_mean_data(self, p, selected):
        self.app.data_store.mean_data = {}

        for par in selected:
            self.app.data_store.mean_data[par] = copy.deepcopy(self.app.data_store.all_data[par])

        n_0 = len(self.app.data_store.mean_data[selected[0]]['actual'])

        for par in selected:
            if len(self.app.data_store.mean_data[par]['actual']) != n_0:
                print("Abbruch: unterschiedliche Anzahl an Datensätzen")
                return

        print("Anzahl datensätze immer gleich!")

        tol_value = ["", ""]

        for i, tol in enumerate(self.tolerance):
            tol_value[i] = self.app.data_store.temp[p][tol][0]

        self.app.core.mean_to_temp(p, selected, n_0, tol_value)

    def mean_to_temp(self, p, selected, n_0, tol_value):
        keys = self.app.data_store.temp[p].keys()

        for key in keys:
            if key == "pos. nr.":
                self.app.data_store.temp[p][key] = [""] * n_0
                for i in range(n_0):
                    self.app.data_store.temp[p][key][i] = self.app.data_store.mean_data[selected[0]][key][i]
            elif key == "actual" or key == "nominal":
                self.app.data_store.temp[p][key] = [0.0] * n_0
                for i in range(n_0):
                    self.app.data_store.temp[p][key][i] = round(
                        np.mean([self.app.data_store.mean_data[par][key][i] for par in self.app.data_store.mean_data]), 7
                    )
            elif key == self.tolerance[0]:
                self.app.data_store.temp[p][key] = [tol_value[0]] * n_0
            elif key == self.tolerance[1]:
                self.app.data_store.temp[p][key] = [tol_value[1]] * n_0

    def restore_df(self, selected):
        for key in selected:
            self.app.data_store.custom_data[key] = copy.deepcopy(self.app.data_store.arch[key])
            del self.app.data_store.arch[key]

    def plot_to_pdf(self, output_path, tool_number):
        idx = "pos. nr."
        name = f"{date.today().isoformat()}_{tool_number}_evaluation.pdf"

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with PdfPages(os.path.join(output_path, name)) as pdf:
            for param, df_dict in self.app.data_store.export_data.items():
                # page 1: Plot
                plt.figure(figsize=(10, 6))
                plt.plot(
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
                pdf.savefig()
                plt.close()

                # page 2: Rohdaten-Tabelle
                df_export = pd.DataFrame(df_dict).T  # DataFrame aus den Series
                _, ax = plt.subplots(figsize=(10, len(df_export) * 0.5 + 1))
                ax.axis('off')
                table = ax.table(
                    cellText=df_export.values,
                    rowLabels=df_export.index,
                    loc='center',
                    cellLoc='center'
                )
                table.auto_set_font_size(False)
                table.set_fontsize(8)
                table.scale(1.2, 1.2)
                plt.title(f"raw data: {param}")
                plt.tight_layout()
                pdf.savefig()
                plt.close()
