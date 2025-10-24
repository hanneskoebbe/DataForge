import pandas as pd
import math

def gen_temp_data(sel_param, lower_tol, upper_tol, data):
    temp_data={}
    i_sel=find_index(sel_param,data)

    # i_par=0
    # i_df=0
    for i_par, param in enumerate(sel_param):
        temp_data[i_par]={}
        if i_sel[i_par] is None:
            continue
        for i_df, df in data.items():
            temp_data[i_par][i_df]=df.iloc[i_sel[i_par],0:5]
            temp_data[i_par][i_df].index = ["pos. nr.","actual", "nominal", "upper tol.", "lower tol."]
            temp_data[i_par][i_df]["pos. nr."]=df.iloc[6,5]
            temp_data[i_par][i_df]["lower tol."]=lower_tol[param]
            temp_data[i_par][i_df]["upper tol."]=upper_tol[param]
    # i_par=i_par+1
    return temp_data

def find_index(sel_param,data):
    i_sel=[]
    for param in sel_param:
            # Spaltenindex im ersten DataFrame suchen
        try:
            i_sel.append(data[0].index[data[0][data[0].columns[0]] == param][0])
        except KeyError:
            print(f"Parameter '{param}' nicht gefunden.")
            i_sel.append(None)
    return i_sel
