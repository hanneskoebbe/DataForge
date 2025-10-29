import copy
import datetime


def on_duplicate(self, p):
    p_ = f"{p}_copy_{datetime.now().strftime('%Y%m%d%H%M%S')}"

    for p in self.temp:
        self.custom_data[p_] = copy.deepcopy(self.temp[p])

    self.gen_all_data()

    self.widgets()
