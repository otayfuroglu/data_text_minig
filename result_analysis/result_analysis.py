# -*- coding:utf-8 -*-

import pandas as pd
import numpy as np

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from collections import Counter

#from  ccdc.io import EntryReader, CrystalReader
#from ccdc.search import TextNumericSearch


def save_to_exel(df, file_name):
	writer = pd.ExcelWriter("%s.xlsx"%file_name, engine='xlsxwriter')
	df.to_excel(writer, sheet_name='Sheet1')
	writer.save()


df_data_sa = pd.read_csv("../all_SA_extract.csv")
df_data_pv = pd.read_csv("../all_PV_extract.csv")

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

    #mof name 'in basinda ve sonundaki istenmeyen karakterleri siliyoruz
    for ch in [".", ":", "/", "-", "~", "•", "#", "‚"]:
        clean_name_mof_sa["MOF Name"] = clean_name_mof_sa["MOF Name"].map(lambda x:
                                                                          x[0].replace("%s" %ch, "")
                                                                          + x[1:-1]
                                                                          + x[-1].replace("%s" %ch, ""))
    # celan "% , (nm).." vs. from the mof name
    mof_names = clean_name_mof_sa["MOF Name"]
    i = 0
    for mof_name in mof_names:
        #sadece rakam içeren mof nameleri ignore ettik
        result = ''.join([item for item in mof_name.replace("-", "") if not item.isdigit()])
        if len(result) == 0:
            total_non_clean_names_sa = total_non_clean_names_sa.append(clean_name_mof_sa.loc[[i]],
                                                     ignore_index=True)
            clean_name_mof_sa = clean_name_mof_sa.drop(i)
        i += 1

    #    if "%" in mof_name: 
    #        total_non_clean_names_sa = total_non_clean_names_sa.append(clean_name_mof_sa.loc[[i]],
    #                                                 ignore_index=True)
    #        clean_name_mof_sa = clean_name_mof_sa.drop(i)
    #    elif "(nm)" in mof_name or "error" in mof_name:
    #        total_non_clean_names_sa = total_non_clean_names_sa.append(clean_name_mof_sa.loc[[i]],
    #                                                 ignore_index=True)
    #        clean_name_mof_sa = clean_name_mof_sa.drop(i)
    return clean_name_mof_sa.reset_index(drop=True), total_non_clean_names_sa.reset_index(drop=True)

#clean_name_for_sa(df_data_sa)[0].to_csv("clean_sa.csv")

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

#clean_values_sa(clean_name_for_sa(df_data_sa))[0].to_csv("clean_sa.csv")

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

    for ch in [".", ":", "/", "-", "~", "•", "#", "‚"]:
        clean_name_mof_pv["MOF Name"] = clean_name_mof_pv["MOF Name"].map(lambda x:
                                                                          x[0].replace("%s" %ch, "")
                                                                          + x[1:-1]
                                                                          + x[-1].replace("%s" %ch, ""))
    # celan "% , (nm).." vs. from the mof name
    mof_names = clean_name_mof_pv["MOF Name"]
    i = 0
    for mof_name in mof_names:
        #sadece rakam içeren mof nameleri ignore ettik
        result = ''.join([item for item in mof_name.replace("-", "") if not item.isdigit()])
        if len(result) == 0:
            tatal_non_clean_names = tatal_non_clean_names.append(clean_name_mof_pv.loc[[i]],
                                                     ignore_index=True)
            clean_name_mof_pv = clean_name_mof_pv.drop(i)
        i += 1

    #    if "%" in mof_name:
    #        tatal_non_clean_names = tatal_non_clean_names.append(clean_name_mof_pv.loc[[i]],
    #                                                 ignore_index=True)
    #        clean_name_mof_pv = clean_name_mof_pv.drop(i)
    #    elif "(nm)" in mof_name or "error" in mof_name:
    #        tatal_non_clean_names = tatal_non_clean_names.append(clean_name_mof_pv.loc[[i]],
    #                                                 ignore_index=True)
    #        clean_name_mof_pv = clean_name_mof_pv.drop(i)
    #    i += 1

    return clean_name_mof_pv.reset_index(drop=True), tatal_non_clean_names.reset_index(drop=True)

#clean_name_for_pv(df_data_pv)[0].to_csv("clean_pv.csv")

def clean_values_pv(clean_and_non_clean_name_mof):

    """
    clean the anything excepted for digit and dot. And clean a value is bigger than 20
    return clean and bug df file

    input = clean_and_non_clean_name_mof (included clean and non_clean name mof as dataframe in tuple )
    output = cleaned and non cleaned dataframe in tuple
     """

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

#clean_values_pv(clean_name_for_pv(df_data_pv))[0].to_csv("clean_pv.csv")

def drop_duplicates(df):

    """removed dublicateis from pandas dataframe """

    non_dublicates = df[["MOF Name", "Value", "DOI"]].drop_duplicates()
    df = df.loc[non_dublicates.index].reset_index(drop=True)
    return df

def merge_dub_names_sa(df):

    """Aynı MOF isiminde birden fazla değer var ise en büyük değeri alır"""
    df = df[["MOF Name", "Value", "DOI"]]
    df_merge = df.astype(str).groupby("MOF Name").agg(";".join)

    for i, row in df_merge.iterrows(): # for the iteration data frame as row

        ls_values = row["Value"].split(";")
        ls_values_appr = [int(str(int(float(item)))[:-1]+"0") for item in ls_values]
        freq_values = Counter(ls_values_appr)

        if len(freq_values.values()) != len(ls_values): # eğer bu şart geçerli ise bir değrden enaz iki tane var
            most_freq_value = [key for key, value in freq_values.items()\
                               if value == max(freq_values.values())]
            target_value = most_freq_value[0]
            idex_target_value = ls_values_appr.index(target_value)
        else:
            target_value = max(ls_values)
            idex_target_value = ls_values.index(target_value)


        dois = row["DOI"].split(";")


        df_merge.loc[i]["Value"] = target_value
        df_merge.loc[i]["DOI"] = dois[idex_target_value]

    return df_merge

def merge_dub_names_pv(df):

    """Aynı MOF isiminde birden fazla değer var ise en büyük değeri alır"""
    df = df[["MOF Name", "Value", "DOI"]]
    df_merge = df.astype(str).groupby("MOF Name").agg(";".join)

    for i, row in df_merge.iterrows(): # for the iteration data frame as row

        ls_values = row["Value"].split(";")
        ls_values_appr = [float(str(float(item))[:-1]+"0") for item in ls_values]
        freq_values = Counter(ls_values_appr)

        if len(freq_values.values()) != len(ls_values): # eğer bu şart geçerli ise bir değrden enaz iki tane var
            most_freq_value = [key for key, value in freq_values.items()\
                               if value == max(freq_values.values())]
            target_value = most_freq_value[0]
            idex_target_value = ls_values_appr.index(target_value)
        else:
            target_value = max(ls_values)
            idex_target_value = ls_values.index(target_value)


        dois = row["DOI"].split(";")


        df_merge.loc[i]["Value"] = target_value
        df_merge.loc[i]["DOI"] = dois[idex_target_value]
    return df_merge

def cacl_density(doi):
    print doi
    query = TextNumericSearch()
    query.add_doi(doi)
    hits = query.search()

    ref_codes = []
    for hit in  hits:
        ref_codes.append(hit.identifier)

    csd_crystal_reader = CrystalReader('CSD')

    if len(ref_codes) == 0:
	density = 1
    else:
	crystal = csd_crystal_reader.crystal(ref_codes[0])
	density = crystal.calculated_density
    return "%.3f" %density

def obtain_sa_pv(cleaned_sa, cleaned_pv):
    df_merge = pd.merge(cleaned_sa, cleaned_pv, how="left", left_on="MOF Name", right_on="MOF Name")
    #drop rows of Pandas DataFrame whose value in certain columns is NaN
    df_merge = df_merge[np.isfinite(df_merge["Value_y"].astype(float))]
    return df_merge


def abtain_sa_pv_density(cleaned_sa, cleaned_pv):
   #create two column have came from pv and sa data beside MOF name and DOI

    df = pd.concat([cleaned_sa, cleaned_pv])
    df = df.astype(str).groupby("MOF Name").agg(";".join)
    df = df[df['Value'].str.contains(";", regex=False, case=False, na=False)] # value sutununda ";"  içeren satırları getir

    df = df.join(df["Value"].str.split(';', expand=True).add_prefix("Value").fillna(np.nan)) # her bir cell'i ";" dan bölerek iki ayrı sütün oluşturur ve boşluklara null ekler
    df = df.join(df["DOI"].str.split(';', expand=True).add_prefix("DOI").fillna(np.nan))

    sa_pv = df.drop(columns=["Value", "DOI"]).reset_index()

    labels = ["MOF Name", "Value_SA(m2/g)", "Value_PV(cm3/g)", "DOI_SA", "DOI_PV"]
    sa_pv.columns = labels # remane columns of dataframe

    # DENSITY eklendi!!
    sa_pv.insert(loc=1, column="Density", value=map(cacl_density, sa_pv["DOI_PV"]))

    return sa_pv

def calc_H2_up_core(sa, pv, density):

    sa = float(sa)  # g/m2
    pv = float(pv) / 1000000.0  # m3/g
    #c = 0.021  # H2 g/m2 --> proportionslity canstant linking SA
    #ph2 = 11.5 * 1000  # g/m3 (77 K and 35 bar)

    h2_up_per_gram = "%.3f" %((0.0000210 * sa + 0.0115 * pv)*100)
    h2_up_per_volume = "%.3f" % (((0.0000210 * sa + 0.0115 * pv) * density)*10)

    return h2_up_per_gram, h2_up_per_volume


def calc_H2_up(sa_pv_dens_data):

    sa_pv_dens_data.insert(loc=4, column="H2_UP (w/W %)",
                           value=[value[0] for value in (map(calc_H2_up_core,
                                                             sa_pv_dens_data["Value_SA(m2/g)"],
                                                             sa_pv_dens_data["Value_PV(cm3/g)"],
                                                             sa_pv_dens_data["Density"]))])

    sa_pv_dens_data.insert(loc=5, column="H2_UP (w/L %)",
                           value=[value[1] for value in (map(calc_H2_up_core,
                                                             sa_pv_dens_data["Value_SA(m2/g)"],
                                                             sa_pv_dens_data["Value_PV(cm3/g)"],
                                                             sa_pv_dens_data["Density"]))])

    return sa_pv_dens_data

def cleaned_pv():
    pv = clean_values_pv(clean_name_for_pv(df_data_pv))
    non_dublicates_pv = drop_duplicates(pv[0])
    merge_names_pv = merge_dub_names_pv(non_dublicates_pv)

    return merge_names_pv

def cleaned_sa():
    # SA için sadece BET alıyoruz. Langmiur SA eledik
    df_sa_bet = df_data_sa.loc[df_data_sa['Type'] == "BET"]
    sa = clean_values_sa(clean_name_for_sa(df_sa_bet))
    non_dublicates_sa = drop_duplicates(sa[0])
    merge_names_sa = merge_dub_names_sa(non_dublicates_sa)

    return merge_names_sa

cleaned_sa = cleaned_sa()
#cleaned_sa.to_csv("final_cleaned_sa.csv")
cleaned_pv = cleaned_pv()
#cleaned_pv.to_csv("final_cleaned_pv.csv")
obtain_sa_pv(cleaned_sa, cleaned_pv).to_csv("all_merged_sa_pv.csv")

#sa_pv_dens_data = abtain_sa_pv_density(cleaned_sa, cleaned_pv)
#calc_H2_up(sa_pv_data)

#save_to_exel(calc_H2_up(sa_pv_dens_data), "betSA_PV_H2_up_3")
