def temp_to_data(self):
    param = list(self.temp_arch.keys())[0]

    # init data_source: import_data + custom_data
    data_sources = [self.import_data, self.custom_data]

    for source in data_sources:
        if param in source:
            # delete dataframe if parameter name is changed
            if param != list(self.temp.keys())[0]:
                del source[param]
                source[list(self.temp.keys())[0]] = {}
            # write records in source
            records_to_source(self, source)
            break  # break when parameter is found


def records_to_source(self, source):
    # empty source dataframe
    for key in self.temp[list(self.temp.keys())[0]]:
        source[
            list(self.temp.keys())[0]
        ][key] = ["" for _ in range(len(self.temp[
            list(self.temp.keys())[0]
        ]["actual"]))]
    # temp to source
    for key, temp_list in self.temp[list(self.temp.keys())[0]].items():
        for i, value in enumerate(temp_list):
            source[
                list(self.temp.keys())[0]
            ][key][i] = self.core.convert_seperator(value)
