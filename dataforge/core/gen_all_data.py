import copy


def gen_all_data(self):
    # empty all_data
    self.all_data = {}

    # add to all_data if not empty
    for source in [self.import_data, self.custom_data]:
        for key, value in source.items():
            self.all_data[key] = copy.deepcopy(value)

    # sort all_data alphabetically
    self.all_data = dict(sorted(
        self.all_data.items(),
        key=lambda item: item[0].lower()
        ))
