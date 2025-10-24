import pandas as pd

def gen_import_data(data, params):
    imp_data = {}

    for report_idx, df in data.items():
        # Überschrift befindet sich immer in Zeile 11
        df_clean = df.iloc[12:].reset_index(drop=True)
        df_clean.columns = df.iloc[11]

        # "Part No." aus Zeile 6, Spalte "Unnamed: 5"
        part_no = df.iloc[6]["Unnamed: 5"]

        for _, row in df_clean.iterrows():
            param = row["Characteristic"]

            if param not in imp_data:
                imp_data[param] = {
                    "pos. nr.": [],
                    "actual": [],
                    "nominal": [],
                    "upper tol.": [],
                    "lower tol.": [],
                }

            imp_data[param]["pos. nr."].append(part_no)
            imp_data[param]["actual"].append(row["Actual"])
            imp_data[param]["nominal"].append(row["Nominal"])
            imp_data[param]["upper tol."].append("0.015")
            imp_data[param]["lower tol."].append("-0.015")

    return imp_data


# import pandas as pd

# def gen_import_data(data, params):
#     temp_data={}
    
#     #for i_par in enumerate(params):
#         #for i_df, df in data:
#             #print(i_df,df)
#             #temp_data[i_par][i_df]=df.iloc[i_par,0:5]
#             #temp_data[i_par][i_df].index = ["pos. nr.","actual", "nominal", "upper tol.", "lower tol."]
#             #temp_data[i_par][i_df]["pos. nr."]=df.iloc[6,5]
#             # temp_data[i_par][i_df]["lower tol."]=lower_tol[param]
#             # temp_data[i_par][i_df]["upper tol."]=upper_tol[param]

#     return temp_data
