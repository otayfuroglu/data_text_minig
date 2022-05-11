# -*- coding:utf-8 -*-

import pandas as pd
import re
from ast import literal_eval #Extracting list from string

df_td_sa = pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/final_cleaned_sa.csv")
df_td_pv = pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/final_cleaned_pv.csv")
df_dm_sa_pv = pd.read_csv("/home/omert/Desktop/data_mining_mof/workspace/result_analysis/all_out_data_table_sa_n2_probe.csv")

df_dm_td_mofname_refcodes = pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/refcode_mofname_csd_text_01.csv")

df_dm_td_values = pd.DataFrame(columns = ["MOF_Name", "TD_Values", "DM_Values"])

k = 0
for i, row in df_dm_td_mofname_refcodes.iterrows():
    mof_name = row["MOF_Name"]
    refcodes = row["RefCode"].split(";")
    td_value = df_td_sa.loc[df_td_sa["MOF_Name"] == str(mof_name)]["Value"].to_list()
    if len(td_value) != 0:
        td_value = td_value[0]
    else:
        continue
    ls_dm_values = []
    for refcode in refcodes:
        dm_value =df_dm_sa_pv.loc[df_dm_sa_pv["RefCode"] == str(refcode)]["| ASA_m^2/g"].to_list()

        if len(dm_value) != 0:
            dm_value = dm_value[0]
            ls_dm_values.append(dm_value)
        else:
            continue
    print(sorted(ls_dm_values))
    if len(ls_dm_values) != 0:
        dm_value = sorted(ls_dm_values)[-1]
    else:
        continue
    df_dm_td_values.loc[k] = [mof_name, td_value, dm_value]
    k += 1

df_dm_td_values.to_csv("dm_td_values.csv")



