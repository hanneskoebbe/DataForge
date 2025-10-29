import copy


def on_remove(self, p):
    self.get_temp(p)

    for p in self.temp:
        self.arch[p] = copy.deepcopy(self.temp[p])

    data_sources = [self.import_data, self.custom_data]

    for source in data_sources:
        if p in source:
            del source[p]

    self.gen_all_data()

    self.widgets()
