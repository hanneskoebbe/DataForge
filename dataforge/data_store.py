class Data:
    def __init__(self):
        self.widget_data = {}
        self.import_data = {}
        self.custom_data = {}
        self.all_data = {}
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
        self.temp_arch = {}
        self.export_data = {}
        self.mean_data = {}
