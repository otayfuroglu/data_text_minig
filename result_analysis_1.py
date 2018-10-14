# -*- coding:utf-8 -*-

import pandas as pd
import numpy as np

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def save_to_exel(df, file_name):
	writer = pd.ExcelWriter("%s.xlsx"%file_name, engine='xlsxwriter')
	df.to_excel(writer, sheet_name='Sheet1')
	writer.save()


df_data_sa = pd.read_excel("all_MOF_SA_extract_paral.xlsx")
df_data_pv = pd.read_excel("all_MOF_PV_extract_paral.xlsx")

def clean_name_for_sa(df_data_sa):

    # MOF ismi olmayanları (*IDK* or *NO_MOF_data*) eledik
    clean_name_mof_sa = df_data_sa.loc[df_data_sa["MOF Name"] != "*IDK*"]
    non_clean_name_mof_sa_1 = df_data_sa.loc[df_data_sa["MOF Name"] == "*IDK*"]
    
    # clean too long name
    clean_name_mof_sa = clean_name_mof_sa.loc[clean_name_mof_sa["MOF Name"].str.count("") <= 40]
    non_clean_name_mof_sa_2 = clean_name_mof_sa.loc[clean_name_mof_sa["MOF Name"].str.count("") > 40]

    total_non_clean_names_sa = pd.concat([non_clean_name_mof_sa_1, non_clean_name_mof_sa_2])

    # reset index
    clean_name_mof_sa = clean_name_mof_sa.reset_index(drop=True)

    # celan "% , (nm).." vs. from the mof name
    mof_names = clean_name_mof_sa["MOF Name"]
    i = 0
    for mof_name in mof_names:
        if "%" in mof_name:
            total_non_clean_names_sa = total_non_clean_names_sa.append(clean_name_mof_sa.loc[[i]],
                                                     ignore_index=True)
            clean_name_mof_sa = clean_name_mof_sa.drop(i)
        elif "(nm)" in mof_name or "error" in mof_name:
            total_non_clean_names_sa = total_non_clean_names_sa.append(clean_name_mof_sa.loc[[i]],
                                                     ignore_index=True)
            clean_name_mof_sa = clean_name_mof_sa.drop(i)

        elif mof_name[0] == "." or mof_name[-1] == "." or mof_name[0] == ":" or mof_name[-1] == "." \
                or mof_name[0] == "/" or mof_name[-1] == "/" or mof_name[0] == "-" or mof_name[-1] == "-" \
                or mof_name[0] == "•" or mof_name[-1] == "•" or mof_name[0] == "~" or mof_name[-1] == "~":

            total_non_clean_names_sa = total_non_clean_names_sa.append(clean_name_mof_sa.loc[[i]],
                                                     ignore_index=True)
            clean_name_mof_sa = clean_name_mof_sa.drop(i)
        i += 1


    
    # sadece BET olanlar
    bet_name_mof_sa = clean_name_mof_sa.loc[clean_name_mof_sa["Type"] == "BET"]
    # sadece Langmuir olanlar
    lang_name_mof_sa = clean_name_mof_sa.loc[clean_name_mof_sa["MOF Name"] == "Langmuir"]

    return clean_name_mof_sa.reset_index(drop=True), total_non_clean_names_sa.reset_index(drop=True)


#save_to_exel(clean_name_for_sa(df_data_sa)[1], "non_celan_names_SA_1")

def clean_values_sa(clean_and_non_clean_name_mof):

    """clean the anything excepted for digit and dot. And clean a value is bigger than 20
     return clean and bug df file"""


    clean_value_name_mof = clean_and_non_clean_name_mof[0]
    non_clean_value = clean_and_non_clean_name_mof[1]

    values_clean = clean_value_name_mof["Value"]

    #clean the anything excepted for digit and dot.
    i = 0
    for value in values_clean:
        value = str(value)
        result = ''.join([item for item in value.replace(".", "") if not item.isdigit()])
        if len(result) != 0:
            non_clean_value = non_clean_value.append(clean_value_name_mof.loc[[i]],
                                                     ignore_index=True)  # list teki gibi değil = ile assign etmelisin
            clean_value_name_mof = clean_value_name_mof.drop(i)

        elif float(value) > 50000:
            non_clean_value = non_clean_value.append(clean_value_name_mof.loc[[i]], ignore_index=True)
            clean_value_name_mof = clean_value_name_mof.drop(i)

        elif float(value) < 10:
            non_clean_value = non_clean_value.append(clean_value_name_mof.loc[[i]], ignore_index=True)
            clean_value_name_mof = clean_value_name_mof.drop(i)

        i += 1

    return clean_value_name_mof.reset_index(drop=True), non_clean_value.reset_index(drop=True)


def clean_name_for_pv(df_data_pv):
    """clean MOF names"""

    #MOF ismi olmayanları (*IDK* or *NO_MOF_data*) eledik
    clean_name_mof_pv = df_data_pv.loc[df_data_pv["MOF Name"] != "*IDK*"]
    clean_name_mof_pv = clean_name_mof_pv.loc[clean_name_mof_pv["MOF Name"] != "*NO_MOF_data*"]

    # MOF ismi olmayanlar(*IDK* or *NO_MOF_data*)
    non_clean_names1 = df_data_pv.loc[df_data_pv["MOF Name"] == "*NO_MOF_data*"]
    non_clean_names2 = df_data_pv.loc[df_data_pv["MOF Name"] == "*IDK*"]

    # clean too long name
    clean_name_mof_pv = clean_name_mof_pv.loc[clean_name_mof_pv["MOF Name"].str.count("") <= 40]

    # non clean too long name
    non_clean_names3 = df_data_pv.loc[df_data_pv["MOF Name"].str.count("") > 40]

    tatal_non_clean_names = pd.concat([non_clean_names1, non_clean_names2, non_clean_names3])

    # reset index
    clean_name_mof_pv = clean_name_mof_pv.reset_index(drop=True)

    # celan "% , (nm).." vs. from the mof name
    mof_names = clean_name_mof_pv["MOF Name"]
    i = 0
    for mof_name in mof_names:
        if "%" in mof_name:
            tatal_non_clean_names = tatal_non_clean_names.append(clean_name_mof_pv.loc[[i]],
                                                     ignore_index=True)
            clean_name_mof_pv = clean_name_mof_pv.drop(i)
        elif "(nm)" in mof_name or "error" in mof_name:
            tatal_non_clean_names = tatal_non_clean_names.append(clean_name_mof_pv.loc[[i]],
                                                     ignore_index=True)
            clean_name_mof_pv = clean_name_mof_pv.drop(i)

        elif mof_name[0] == "." or mof_name[-1] == "." or mof_name[0] == ":" or mof_name[-1] == "." \
                or mof_name[0] == "/" or mof_name[-1] == "/"or mof_name[0] == "-" or mof_name[-1] == "-" \
                or mof_name[0] == "•" or mof_name[-1] == "•" or mof_name[0] == "~" or mof_name[-1] == "~" :
            tatal_non_clean_names = tatal_non_clean_names.append(clean_name_mof_pv.loc[[i]],
                                                     ignore_index=True)
            clean_name_mof_pv = clean_name_mof_pv.drop(i)
        i += 1

    return clean_name_mof_pv.reset_index(drop=True), tatal_non_clean_names.reset_index(drop=True)


def clean_values_pv(clean_and_non_clean_name_mof):

    """clean the anything excepted for digit and dot. And clean a value is bigger than 20
     return clean and bug df file

     input = clean_and_non_clean_name_mof (included clean and non_clean name mof as dataframe in tuple )
     output = cleaned and non cleaned dataframe in tuple """


    clean_value_name_mof = clean_and_non_clean_name_mof[0]
    non_clean_value = clean_and_non_clean_name_mof[1]

    values_clean = clean_value_name_mof["Value"]

    #clean the anything excepted for digit and dot.
    i = 0
    for value in values_clean:
        result = ''.join([item for item in value.replace(".", "") if not item.isdigit()])
        if len(result) != 0:
            non_clean_value = non_clean_value.append(clean_value_name_mof.loc[[i]],
                                                     ignore_index=True)  # list teki gibi değil = ile assign etmelisin
            clean_value_name_mof = clean_value_name_mof.drop(i)

        elif float(value) > 20:
            non_clean_value = non_clean_value.append(clean_value_name_mof.loc[[i]], ignore_index=True)
            clean_value_name_mof = clean_value_name_mof.drop(i)

        elif float(value) < 0.1:
            non_clean_value = non_clean_value.append(clean_value_name_mof.loc[[i]], ignore_index=True)
            clean_value_name_mof = clean_value_name_mof.drop(i)
        i += 1


    return clean_value_name_mof.reset_index(drop=True), non_clean_value.reset_index(drop=True)


def drop_duplicates(df):

    """removed dublicateis from pandas dataframe """

    non_dublicates = df[["MOF Name", "Value", "DOI"]].drop_duplicates()
    df = df.loc[non_dublicates.index].reset_index(drop=True)

    return df

def merge_dub_names(df):

    """Aynı MOF isiminde birden fazla değer var ise en büyük değeri alır"""
    df = df[["MOF Name", "Value", "DOI"]]
    df_merge = df.astype(str).groupby("MOF Name").agg(";".join)

    for i, row in df_merge.iterrows(): # for the iteration data frame as row

        values = row["Value"].split(";")
        dois = row["DOI"].split(";")
        max_value = max(values)

        idex_max_value = values.index(max_value)

        df_merge.loc[i]["Value"] = max_value
        df_merge.loc[i]["DOI"] = dois[idex_max_value]

    return df_merge

def abtain_sa_pv(cleaned_sa, cleaned_pv):
    """create two column have came from pv and sa data beside MOF name and DOI"""

    df = pd.concat([cleaned_sa, cleaned_pv])
    df = df.astype(str).groupby("MOF Name").agg(";".join)
    df = df[df['Value'].str.contains(";", regex=False, case=False, na=False)] # value stununda ";"  içeren satırları getir

    df = df.join(df["Value"].str.split(';', expand=True).add_prefix("Value").fillna(np.nan)) # ";" dan bölerek iki ayrı sütün oluşturur ve boşluklara null ekler
    df = df.join(df["DOI"].str.split(';', expand=True).add_prefix("DOI").fillna(np.nan))
    df = df.drop(columns=["Value", "DOI"]).reset_index()

    labels = ["MOF Name", "Value_SA(m2/g)", "Value_PV(cm3/g)", "DOI_SA", "DOI_PV"]

    df.columns = labels # remane columns of dataframe

    return df#.reset_index(drop=True)


def cleaned_pv():
    pv = clean_values_pv(clean_name_for_pv(df_data_pv))
    non_dublicates_pv = drop_duplicates(pv[0])
    merge_names_pv = merge_dub_names(non_dublicates_pv)

    return merge_names_pv

def cleaned_sa():
    df_sa_bet = df_data_sa.loc[df_data_sa['Type'] == "BET"]
    sa = clean_values_sa(clean_name_for_sa(df_sa_bet))
    non_dublicates_sa = drop_duplicates(sa[0])
    merge_names_sa = merge_dub_names(non_dublicates_sa)

    return merge_names_sa



save_to_exel(abtain_sa_pv(cleaned_sa(), cleaned_pv()), "betSA_PV_")