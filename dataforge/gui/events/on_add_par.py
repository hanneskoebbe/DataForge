from datetime import datetime


def on_add_par(self):
    # gen custom name for parameter
    param_name = f'Custom_{datetime.now().strftime("%Y%m%d%H%M%S")}'

    # write empty directory in custom_data
    self.custom_data[param_name] = {
        "pos. nr.": [],
        "actual": [],
        "nominal": [],
        "lower tol.": [],
        "upper tol.": []
    }

    # define default values
    self.custom_data[param_name]["pos. nr."].append("Pos. xxx-01")
    self.custom_data[param_name]["actual"].append(0.0)
    self.custom_data[param_name]["nominal"].append(0.0)
    self.custom_data[param_name]["lower tol."].append(-0.015)
    self.custom_data[param_name]["upper tol."].append(0.015)

    self.gen_all_data()

    self.widget()
