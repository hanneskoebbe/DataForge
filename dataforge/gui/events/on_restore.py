import copy


def on_restore(self):

    selected = self.selection_window(self.arch)

    if selected != []:
        for key in selected:
            self.custom_data[key] = copy.deepcopy(self.arch[key])
            del self.arch[key]
