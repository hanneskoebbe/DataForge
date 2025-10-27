def gen_import_data(self, data):
    self.import_data = {}

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
            if param not in self.import_data:
                self.import_data[param] = {
                    "pos. nr.": [],
                    "actual": [],
                    "nominal": [],
                    "upper tol.": [],
                    "lower tol.": [],
                }

            self.import_data[param]["pos. nr."].append(part_no)
            self.import_data[param]["actual"].append(row["Actual"])
            self.import_data[param]["nominal"].append(row["Nominal"])
            self.import_data[param]["upper tol."].append("0.015")
            self.import_data[param]["lower tol."].append("-0.015")
