import pandas as pd
import os as os

def import_data(dir):
    data={}
    i=0
    name_list=get_name_list(dir)
    for name in name_list:
        if name.startswith('~$'):
            print(f"Achtung Excel mit dem Namen {name} geöffnet!")
            continue
        os_dir=os.path.join(dir,name)
        print(os_dir)
        data[i]=pd.read_excel(os_dir)
        i=i+1
    return data

def get_name_list(dir):
    name_list=[f for f in os.listdir(dir) if f.lower().endswith(('.xlsx', '.xls'))]
    print(name_list)
    return name_list