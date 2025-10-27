def get_data(self):
    # get param
    param = list(self.temp.keys())[0]

    # count records
    n0 = len(self.temp[list(self.temp.keys())[0]]["actual"])

    keys = ["pos. nr.", "actual", "nominal", "upper tol.", "lower tol."]

    # delete temp
    del self.temp[list(self.temp.keys())[0]]

    # init temp as dictionary
    self.temp[self.widget_data[param]["par_name"].get()] = {}

    for key in keys:
        self.temp[
            self.widget_data[param]["par_name"].get()
        ][key] = ["" for _ in range(n0)]
        for i in range(n0):
            if key == "pos. nr." or key == "actual" or key == "nominal":
                self.temp[
                    self.widget_data[param]["par_name"].get()
                ][key][i] = self.temp_arch[param][key][i]
            elif key == "upper tol.":
                self.temp[
                    self.widget_data[param]["par_name"].get()
                ][key][i] = self.widget_data[param]["tol_up"].get()
            elif key == "lower tol.":
                self.temp[
                    self.widget_data[param]["par_name"].get()
                ][key][i] = self.widget_data[param]["tol_low"].get()
