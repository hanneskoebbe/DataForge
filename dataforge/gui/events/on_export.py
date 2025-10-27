import copy


def on_export(self):
    # empty sel_params
    sel_params = []

    # gen sel_params
    for param, widgets in self.widget_data.items():
        if widgets["var"].get():
            sel_params.append(param)

    # empty export_data
    self.export_data = {}

    # check if a parameter is selected
    if sel_params != []:
        # gen export_data
        for key, value in self.all_data.items():
            for param in sel_params:
                if key == param:
                    self.export_data[key] = copy.deepcopy(value)

        # get export directory
        export_dir = self.select_dir()

        # export pdf from export_data
        self.plot_to_pdf(
            self.export_data,
            export_dir,
            self.tool_number(export_dir))
