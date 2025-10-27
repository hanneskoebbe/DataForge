import pandas as pd
import os as os


def gen_raw_excel_data(dir):
    data = {}
    i = 0
    name_list = get_name_list(dir)
    for i, name in name_list:
        # skip temporary excel files
        if name.startswith('~$'):
            print(f"Achtung Excel mit dem Namen {name} geöffnet!")
            continue
        # gen os path
        os_dir = os.path.join(dir, name)
        data[i] = pd.read_excel(os_dir)
        i += 1
    return data


def get_name_list(dir):
    name_list = [
        f for f in os.listdir(dir) if f.lower().endswith(('.xlsx', '.xls'))
        ]
    return name_list
