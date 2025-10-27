import copy


def get_temp(self, p):
    # check if parameter exists
    if p not in self.all_data:
        print(f"Parameter '{p}' nicht in all_data gefunden.")
        return

    # reset temp
    self.temp = {}

    # write directory from all_data to temp for parameter
    self.temp[p] = copy.deepcopy(self.all_data[p])

    # write temp into temp archive to not lose temp while changing it
    self.temp_arch[p] = copy.deepcopy(self.temp[p])
