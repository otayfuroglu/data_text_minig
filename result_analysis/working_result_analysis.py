# -*- coding:utf-8 -*-
import numpy as np
import pandas as pd
import re
from ast import literal_eval #Extracting list from string
from collections import Counter

def match_csd_text_mof_name():
    df_doi_refcode_mofname = pd.read_csv(
        "/home/omert/Desktop/mof_text_minig/in_output/mof_mining/mof_list/df_doi_refcode_mofname_allMOF_just.csv")

    df_sa_pv = pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/final_cleaned_sapv.csv", low_memory=False)
    #df_sa_pv = df_sa_pv.loc[df_sa_pv["MOF Name"] != "*IDK*"]
    #df_sa_pv = df_sa_pv.loc[df_sa_pv["MOF Name"] != "*NO_MOF_data*"]
    df_sa_pv = df_sa_pv.drop_duplicates(subset="MOF Name", keep="last")
    print(len(df_sa_pv))

    #print(literal_eval(df_doi_refcode_mofname["RefCode"][0]).values())
    mof_names = df_sa_pv["MOF Name"].to_list()

    df_refcode_mofname1_2 = pd.DataFrame(columns=["RefCode", "MOF_Name1", "MOF_Name2", "DOI1", "DOI2"])
    l = 0
    for i, row in df_doi_refcode_mofname.iterrows():
        j = 0
        for refcode, mof_names_1 in literal_eval(row["RefCode"]).items():
            for mof_name_1 in mof_names_1:
                k = 0
                for mof_name_2 in mof_names:
                    temp_mof_name_1 = re.sub("[^A-Za-z0-9]+", "", str(mof_name_1))
                    temp_mof_name_2 = re.sub("[^A-Za-z0-9]+", "", str(mof_name_2))
                    if temp_mof_name_1 == temp_mof_name_2:
                        doi1 = row["DOI"]
                        doi2 = df_sa_pv.iloc[k]["DOI"]
                        df_refcode_mofname1_2.loc[l] = [refcode, mof_name_1, mof_name_2, doi1, doi2]
                        l += 1
                    k += 1
                j += 1
    df_refcode_mofname1_2.to_csv("refcode_mofname_csd_text.csv")
#match_csd_text_mof_name()

def csd_mof_name():
    df_doi_refcode_mofname = pd.read_csv(
        "/home/omert/Desktop/mof_text_minig/in_output/mof_mining/mof_list/df_doi_refcode_mofname_allMOF_just.csv")
    df_refcode_mofname3 = pd.DataFrame(columns=["RefCode", "MOF_Name"])

    k = 0
    for i, row in df_doi_refcode_mofname.iterrows():
        for refcode, mof_names in literal_eval(row["RefCode"]).items():
            for mof_name_1 in mof_names:
                if len(mof_name_1) <= 12:
                    df_refcode_mofname3.loc[k] = [refcode, mof_name_1.replace("(", "").replace(")", "").replace(",", "")]
                    k +=1

           # print(refcode, " --> ",re.sub("[^A-Za-z0-9]+", "", mof_name_1[0]))
        #if i == 3:
        #    break
    df_refcode_mofname3 = df_refcode_mofname3.astype(str).groupby("MOF_Name").agg(";".join)
    df_refcode_mofname3.to_csv("refcode_mofnameJust_groupby_mofname.csv")

#df = pd.read_csv(
#    "/home/omert/Desktop/mof_text_minig/in_output/mof_mining/mof_list/df_all_mof_refcode_mofname.csv")
#print(len(df["MOFName"]))
#print(len(df.loc[df["MOFName"] == "()"]))
#print(len(df.loc[df["MOFName"].str.contains("is not in 2018 CSD database")]))

#refcode_mofname_csd_text_0 = pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/refcode_mofname_csd_text.csv")
#refcode_mofname_csd_text_0 = refcode_mofname_csd_text_0.drop_duplicates()
#refcode_mofname_csd_text_0 = refcode_mofname_csd_text_0[["MOF_Name", "RefCode"]].astype(str).groupby("MOF_Name").agg(";".join)
#refcode_mofname_csd_text_0.to_csv("refcode_mofname_csd_text_01.csv")

def match_csd_text_doimof_name():
    df_doi_refcode_mofname = pd.read_csv(
        "/home/omert/Desktop/mof_text_minig/in_output/mof_mining/mof_list/refcode2doi_mofname.csv")
    df_doi_refcode_mofname = df_doi_refcode_mofname.loc[df_doi_refcode_mofname["MOF_name"]  != "()"]
    print(len(df_doi_refcode_mofname))

    df_sa_pv = pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/clean_pv.csv", low_memory=False)
    #df_sa_pv = df_sa_pv.loc[df_sa_pv["MOF Name"] != "*IDK*"]
    #df_sa_pv = df_sa_pv.loc[df_sa_pv["MOF Name"] != "*NO_MOF_data*"]
    df_sa_pv = df_sa_pv[["MOF Name", "Type", "Value", "Unit", "Link", "DOI"]].drop_duplicates()
    print(len(df_sa_pv))

    #print(literal_eval(df_doi_refcode_mofname["RefCode"][0]).values())
    mof_names = df_sa_pv["MOF Name"].to_list()

    df_refcode_mofname1_2 = pd.DataFrame(columns=["RefCode", "MOF_Name1", "MOF_Name2", "DOI1", "DOI2"])
    l = 0
    for i, row in df_doi_refcode_mofname.iterrows():
        mof_name_1 = row["MOF_name"]
        j = 0
        k = 0
        for mof_name_2 in mof_names:
            temp_mof_name_1 = re.sub("[^A-Za-z0-9]+", "", str(mof_name_1))
            temp_mof_name_2 = re.sub("[^A-Za-z0-9]+", "", str(mof_name_2))
            doi1 = row["DOI"]
            doi2 = df_sa_pv.iloc[k]["DOI"]
            doi1_mof_name_1 = str(doi1) + temp_mof_name_1
            doi2_mof_name_2 = str(doi2) + temp_mof_name_2

            if doi1_mof_name_1 == doi2_mof_name_2:
                doi1 = row["DOI"]
                doi2 = df_sa_pv.iloc[k]["DOI"]
                df_refcode_mofname1_2.loc[l] = [refcode, mof_name_1, mof_name_2, doi1, doi2]
                l += 1
            k += 1
        j += 1
    df_refcode_mofname1_2.to_csv("refcode_doimofname_csd_text.csv")
#match_csd_text_doimof_name()


def match_csd_text_doi_doi():
    df_doi_refcode_mofname = pd.read_csv("./refcode2doi_new_mofname.csv")
    #df_doi_refcode_mofname = df_doi_refcode_mofname.loc[df_doi_refcode_mofname["MOF_name"]  != "()"]
    print(len(df_doi_refcode_mofname))

    df_sa_pv = pd.read_csv("./clean_sa_doi_new.csv", low_memory=False)
    #df_sa_pv = df_sa_pv.loc[df_sa_pv["MOF Name"] != "*IDK*"]
    #df_sa_pv = df_sa_pv.loc[df_sa_pv["MOF Name"] != "*NO_MOF_data*"]
    #df_sa_pv = df_sa_pv[["MOF Name", "Type", "Value", "Unit", "Link", "DOI"]].drop_duplicates()
    print(len(df_sa_pv))

    #print(literal_eval(df_doi_refcode_mofname["RefCode"][0]).values())

    df_refcode_mofname1_2 = pd.DataFrame(columns=["RefCode", "MOF_Name1", "MOF_Name2", "DOI1", "DOI2"])
    l = 0
    counter = 0
    #for i, row_1 in df_doi_refcode_mofname.iterrows():
    for doi1 in df_doi_refcode_mofname["DOI_new"]:
        #for j, row_2 in df_sa_pv.iterrows():
        for doi2 in df_sa_pv["DOI_new"]:
            #doi1 = row_1["DOI_new"]
            #doi2 = row_2["DOI_new"]
            if doi1 == doi2:
                #refcode = row_1["Ref_code"]
                #mof_name_1 = row_1["MOF_name"]
                #mof_name_2 = row_2["MOF Name"]
                #df_refcode_mofname1_2.loc[l] = [refcode, mof_name_1, mof_name_2, doi1, doi2]
                l += 1
                print("DONE")
        counter += 1
        #print(counter)
        #if counter == 100:
        #    break
    #df_refcode_mofname1_2.to_csv("refcode_doi_doi_csd_text.csv")
    print("eslesen;", l)

#match_csd_text_doi_doi()


def add_doi_new():

    df_sa_pv = pd.read_csv("/home/omert/Desktop/mof_text_minig/code/result_analysis/dm_clean_sa_pv_h2up_add_doi.csv",
                           low_memory=False)
    df_sa_pv = df_sa_pv.sort_values(by=["DOI", "| POAV_cm^3/g"])
    #df_sa_pv = df_sa_pv.loc[df_sa_pv["MOF Name"] != "*IDK*"]
    #df_sa_pv = df_sa_pv.loc[df_sa_pv["MOF Name"] != "*NO_MOF_data*"]
    #print(literal_eval(df_doi_refcode_mofname["RefCode"][0]).values())

    #df_refcode_mofname1_2 = pd.DataFrame(columns=["RefCode", "MOF_Name1", "MOF_Name2", "DOI1", "DOI2"])
    l = 0
    doi_now = 0
    doi2 = 0
    a = 1
    b = 1
    dois= []
    alph_num_mof_name = []
    for i, row_1 in df_sa_pv.iterrows():
        doi_pre = row_1["DOI"]
        #alph_num_mof_name.append(re.sub("[^A-Za-z0-9]+", "", str(row_1["MOF Name"])))
        ##value düzeltme
        #try:
        #    df_sa_pv.loc[i:, ["Value"]] = float(re.sub("[^0-9.]+", "", str(row_1["Value"])))
        #except:
        #    try:
        #        df_sa_pv.loc[i:, ["Value"]] = float(re.sub("[^0-9.]+", "", str(row_1["Value"]))[:4])
        #    except:
        #        df_sa_pv.loc[i:, ["Value"]] = 0
        #
        if  doi_pre == doi_now:
            doi1 = doi_pre + "_" + str(a)
            a += 1
        else:
            doi1 = doi_pre
            a = 1
        doi_now = doi_pre
        dois.append(doi1)
    df_sa_pv["DOI_new"] = dois
    #df_sa_pv["MOF_Name_alphnum"] = alph_num_mof_name
    df_sa_pv.to_csv("dm_clean_doi_pv_sorted.csv")

#add_doi_new()

def merge_df():

    df_sa_pv = pd.read_csv("/home/omert/Desktop/mof_text_minig/code/result_analysis/refcode2doi_mofname.csv",
                           low_memory=False)

    df_dm_sa_pv= pd.read_csv("/home/omert/Desktop/data_mining_mof/workspace/result_analysis/all_sa_pv_h2Up_table_h2_n2_probe_for_clean_sorted_byH2up.csv",
                             low_memory=False)
    df_dm_sa_pv["RefCode"] = df_dm_sa_pv["RefCode"].str.replace("_stripped", "")
    print(df_dm_sa_pv.head())
    df_merge = pd.merge(df_sa_pv, df_dm_sa_pv, how="left", left_on="Ref_code", right_on="RefCode")
    df_merge[["Ref_code", "DOI", "| ASA_m^2/g", "| POAV_cm^3/g", "| %H2_Up"]].to_csv("dm_clean_sa_pv_h2up_add_doi.csv")
#merge_df()


def tm_add_mofname_new():

    #df_sa_pv = pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/all_SA_extract.csv")
    #df_sa_pv = df_sa_pv.loc[df_sa_pv["MOF Name"] != "*IDK*"]
    #df_sa_pv = df_sa_pv.loc[df_sa_pv["MOF Name"] != "*NO_MOF_data*"]
    #df_sa_pv = df_sa_pv.loc[df_sa_pv["Type"] == "BET"]
    #df_sa_pv = df_sa_pv.sort_values(by=["MOF Name", "Value"])
    #print(literal_eval(df_doi_refcode_mofname["RefCode"][0]).values())

    df_sa_pv = pd.read_excel("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/clean_indexed/clean_sa.xlsx")
    df_sa_pv = df_sa_pv[["MOFName", "Type", "Value", "Unit", "DOI"]]

    df_sa_pv = df_sa_pv.loc[df_sa_pv["MOFName"] != "*IDK*"]
    df_sa_pv = df_sa_pv.loc[df_sa_pv["Type"] == "BET"]
    df_sa_pv = df_sa_pv.loc[df_sa_pv["MOFName"] != "*NO_MOF_data*"]
    df_sa_pv = df_sa_pv.sort_values(by=["MOFName", "Value"])

    #df_refcode_mofname1_2 = pd.DataFrame(columns=["RefCode", "MOF_Name1", "MOF_Name2", "DOI1", "DOI2"])
    l = 0
    mofname_now = 0
    mofname2 = 0
    a = 1
    b = 1
    mofnames= []
    for i, mofname in enumerate(df_sa_pv["MOFName"]):
        mofname = re.sub("[^A-Za-z0-9]+", "", str(mofname))
        mofname_pre = mofname

        if  mofname_pre == mofname_now:
            mofname1 = mofname_pre + "_" + str(a)
            a += 1
        else:
            mofname1 = mofname_pre
            a = 1
        mofname_now = mofname_pre
        mofnames.append(mofname1)
    df_sa_pv["MOF_Name_alphnum_indexed"] = mofnames
    df_sa_pv.to_csv("clean_sa_alphanum_indexed_name.csv")
#tm_add_mofname_new()

def match_sa_pv_by_mof_name():
    df_sa = pd.read_csv("/home/omert/Desktop/mof_text_minig/code/result_analysis/tm_sa_add_new_mofname_sorted_value.csv")
    print(len(df_sa))

    df_pv = pd.read_csv("/home/omert/Desktop/mof_text_minig/code/result_analysis/tm_pv_add_new_mofname_sorted_value.csv", low_memory=False)
    print(len(df_pv))

    mof_names_sa = df_sa["MOF_name_new"].to_list()
    mof_names_pv = df_pv["MOF_name_new"].to_list()

    df_sa_pv_merge_by_name_sorted_value = pd.DataFrame(columns=["MOF_name", "Value_sa", "DOI_sa",  "Value_pv", "DOI_pv"])
    l = 0
    for i, mof_name_1 in enumerate(mof_names_sa):
        #temp_mof_name_1 = re.sub("[^A-Za-z0-9]+", "", str(mof_name_1))
        for k, mof_name_2 in enumerate(mof_names_pv):
            #temp_mof_name_2 = re.sub("[^A-Za-z0-9]+", "", str(mof_name_2))
            if mof_name_1 == mof_name_2:
                value_sa = df_sa.iloc[i]["Value"]
                value_pv = df_pv.iloc[k]["Value"]
                df_sa_pv_merge_by_name_sorted_value.loc[l] = [mof_name_1, df_sa.iloc[i]["Value"], df_sa.iloc[i]["DOI"], df_pv.iloc[k]["Value"], df_pv.iloc[k]["DOI"]]
                l += 1
    df_sa_pv_merge_by_name_sorted_value.to_csv("sa_pv_merged_by_name_sorted_value.csv")
#match_sa_pv_by_mof_name()

def merge_dub_names_sa():

    df = pd.read_csv("/home/omert/Desktop/mof_text_minig/code/result_analysis/tm_sa_add_new_mofname_sorted_value.csv")

    #df_pv = pd.read_csv("/home/omert/Desktop/mof_text_minig/code/result_analysis/tm_pv_add_new_mofname_sorted_value.csv", low_memory=False)
    df = df[["MOF Name", "Value"]]#, "DOI"]]
    df_merge = df.astype(str).groupby("MOF Name").agg(";".join)

    df_dic = {}
    for i, row in df_merge.iterrows():
        print ((row["Value"].split(";")))
    #df_merge.to_csv("sa_values_groupby_mofname.csv")

#merge_dub_names_sa()


def merge_dub_doi():

    df = pd.read_csv("/home/omert/Desktop/mof_text_minig/code/result_analysis/all_sa_extract_doi_new_sorted.csv")

    df = df.loc[df["Type"] == "BET"]
    print(len(df))
    df = df[["DOI", "Value"]]#, "DOI"]]
    df_merge = df.astype(str).groupby("DOI").agg(";".join)
    print(len(df_merge))

    #df_dic = {}
    #for i, row in df_merge.iterrows():
    #    print ((row["Value"].split(";")))
    df_merge.to_csv("sa_bet_values_groupby_doi.csv")

#merge_dub_doi()

def match_sa_pv_by_mof_name():
    df_sa = pd.read_csv("/home/omert/Desktop/mof_text_minig/code/result_analysis/all_sa_extract_doi_new_sorted.csv")
    df_sa = df_sa.loc[df_sa["Type"] == "BET"]
    print(len(df_sa))

    df_pv = pd.read_csv("/home/omert/Desktop/mof_text_minig/code/result_analysis/all_pv_extract_doi_new_sorted.csv", low_memory=False)
    print(len(df_pv))

    dois_sa = df_sa["DOI_new"].to_list()
    dois_pv = df_pv["DOI_new"].to_list()

    df_sa_pv_merge_by_name_sorted_value = pd.DataFrame(columns=["DOI", "Value_sa", "Value_pv"])
    l = 0
    for i, doi_sa in enumerate(dois_sa):
        for k, doi_pv in enumerate(dois_pv):
            if doi_sa == doi_pv:
                #value seçen algoritma oluşturuşacak
                #value_sa = df_sa.iloc[i]["Value"]
                #value_pv = df_pv.iloc[k]["Value"]
                #df_sa_pv_merge_by_name_sorted_value.loc[l] = [doi_sa, df_sa.iloc[i]["Value"], df_pv.iloc[k]["Value"]]
                l += 1
                print(l)
    #df_sa_pv_merge_by_name_sorted_value.to_csv("sa_pv_merged_by_name_sorted_value.csv")
#match_sa_pv_by_mof_name()


def add_mofname_alphanum():

    df_sa_pv = pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/clean_pv.csv")
    df_sa_pv = df_sa_pv.loc[df_sa_pv["MOF Name"] != "*IDK*"]
    df_sa_pv = df_sa_pv.loc[df_sa_pv["MOF Name"] != "*NO_MOF_data*"]
    df_sa_pv = df_sa_pv.sort_values(by=["MOF Name", "Value"])
    #df_sa_pv = df_sa_pv.loc[df_sa_pv["Type"] == "BET"]
    #print(literal_eval(df_doi_refcode_mofname["RefCode"][0]).values())

    #df_sa_pv = pd.read_csv("/home/omert/Desktop/data_mining_mof/CSD_540/refcode_mofname.csv",
    #                       low_memory=False)

    alph_num_mof_name = []
    for mofname in df_sa_pv["MOF Name"]:
        alph_num_mof_name.append(re.sub("[^A-Za-z0-9]+", "", str(mofname)))
    
    df_sa_pv["MOF_name_alphanum"] = alph_num_mof_name

    df_sa_pv[["MOF Name", "MOF_name_alphanum", "Type", "Value", "Unit", "DOI"]].to_csv("tm_pv_add_alph_num_mofname_sorted_value.csv")
#add_mofname_alphanum()

def tm_merge_dub_mofnames():

    df = pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/general_results/tm_sa_add_alph_num_mofname_sorted_value.csv",
                           low_memory=False)[["MOF Name", "MOF_name_alphanum", "Value"]]

    df = df[df["MOF_name_alphanum"].apply(lambda x: len(str(x)) > 1)]
    df = df[df["MOF_name_alphanum"].apply(lambda x: not str(x).isdigit())]
    df = df[df["Value"].apply(lambda x: str(x).isdigit())] # for ValueError: could not convert string to float: 'BET'"
    df["Value"] = df["Value"].astype(float)
    df = df[df["Value"].apply(lambda x: 15000 > float(x) > 0)]

    #df = df[["MOF Name", "Value"]]
    df_merge = df.astype(str).groupby("MOF_name_alphanum").agg(";".join)
    df_merge.to_csv("temp.csv")
    df_merge = pd.read_csv("temp.csv")

    #df_merge = pd.read_csv("./pv_values_groupby_mofname.csv")
    df_merge_values = pd.DataFrame(columns=["MOF_name", "MOF_name_alphanum", "Value_%s" %merged_type, "Value_mid", "Value_Av", "Value_mostfreq", "Values_max_without_outliyer"])
    for i, values in enumerate(df_merge["Value"]): # for the iteration data frame as row
        ls_values = [float(value) for value in values.split(";")]

        ls_values_appr = [float(item) for item in ls_values]
        freq_values = Counter(ls_values_appr)
        if len(freq_values.values()) != len(ls_values): # eğer bu şart geçerli ise bir değrden enaz iki tane var
            most_freq_value = [key for key, value in freq_values.items()\
                               if value == max(freq_values.values())]
            most_freq_value = most_freq_value[0]
        else:
            most_freq_value = max(ls_values)

        ls_values_clean = [value for value in ls_values if value <= 15000]
        if ls_values_clean == []:
             continue
        max_without_outliyer = max(ls_values_clean)

        ls_values = np.array(ls_values)
        ls_values = ls_values[np.logical_not(np.isnan(ls_values))]
        if len(ls_values) >= 3:
            quartile_1, quartile_3 = np.percentile(ls_values, [25, 75])
            iqr = quartile_3 - quartile_1
            lower_bound = quartile_1 - (iqr * 1.5)
            upper_bound = quartile_3 + (iqr * 1.5)
            outliers = np.where((ls_values > upper_bound) | (ls_values < lower_bound))
            indexs = np.in1d(ls_values, outliers)
            ls_values = np.delete(ls_values, indexs)

        mofname = str(df_merge.ix[i, "MOF Name"]).split(";")[0]
        mofname = mofname.replace(":","").replace(";", "").replace(",", "")
        df_merge_values.loc[i] = [mofname,
                                  df_merge.ix[i, "MOF_name_alphanum"],
                                  np.amax(ls_values),
                                  np.percentile(sorted(ls_values), 50),
                                  np.average(ls_values),
                                  most_freq_value,
                                  max_without_outliyer]
    df_merge_values.to_csv("tm_sa_selected_values_add_mofname_alphanum.csv")
#tm_merge_dub_mofnames()


def dm_merge_dub_mofnames():

    df_refcode_values = pd.read_csv("./dm_clean_doi_pv_sorted.csv")
    df_refcode_values = df_refcode_values[["Ref_code", "| POAV_cm^3/g"]]

    df = pd.read_csv("/home/omert/Desktop/data_mining_mof/CSD_540/refcode_mofname.csv")[["Ref_code", "MOF_name"]]
    df = df.dropna(subset=["MOF_name"]) #
    df_merge = df.astype(str).groupby("MOF_name").agg(";".join)
    df_merge.to_csv("temp.csv")
    df_merge = pd.read_csv("temp.csv")

    df_merge_values = pd.DataFrame(columns=["MOF_name", "MOF_name_alphanum",
                                            "Value_%s" %merged_type, "Value_mid", "Value_Av",
                                            "Value_mostfreq", "Values_max_without_outliyer"])

    for i, refcodes in enumerate(df_merge["Ref_code"]): # for the iteration data frame as row
        ls_values = []
        refcodes = refcodes.split(";")
        for refcode in refcodes:
            value = df_refcode_values.loc[df_refcode_values["Ref_code"] == refcode]["| POAV_cm^3/g"]
            ls_values += value.to_list()
        if ls_values == []:
            continue
        ls_values_clean = [value for value in ls_values if value <= 15000]
        if ls_values_clean == []:
            continue
        if i%10 == 0:
            print(i)
        max_without_outliyer = max(ls_values_clean)

        freq_values = Counter(ls_values)
        if len(freq_values.values()) != len(ls_values): # eğer bu şart geçerli ise bir değrden enaz iki tane var
            most_freq_value = [key for key, value in freq_values.items()\
                               if value == max(freq_values.values())]
            most_freq_value = most_freq_value[0]
        else:
            most_freq_value = max(ls_values)
        ls_values = np.array(ls_values)
        ls_values = ls_values[np.logical_not(np.isnan(ls_values))]
        if len(ls_values) >= 3:
            quartile_1, quartile_3 = np.percentile(ls_values, [25, 75])
            iqr = quartile_3 - quartile_1
            lower_bound = quartile_1 - (iqr * 1.5)
            upper_bound = quartile_3 + (iqr * 1.5)
            outliers = np.where((ls_values > upper_bound) | (ls_values < lower_bound))
            indexs = np.in1d(ls_values, outliers)
            ls_values = np.delete(ls_values, indexs)

        df_merge_values.loc[i] = [str(df_merge.ix[i, "MOF_name"]),
                                  re.sub("[^A-Za-z0-9]+", "", str(df_merge.ix[i, "MOF_name"])),
                                  np.amax(ls_values),
                                  np.percentile(sorted(ls_values), 50),
                                  np.average(ls_values),
                                  most_freq_value,
                                  max_without_outliyer]
    df_merge_values.to_csv("our_dm_pv_selected_values.csv")
#dm_merge_dub_mofnames()

def obtain_sa_pv(cleaned_sa, cleaned_pv):
    cleaned_pv = cleaned_pv.loc[cleaned_pv.Value != "Pore_volume"]

    df_merge = pd.merge(cleaned_sa, cleaned_pv, how="left", left_on="MOF_Name_alphnum_indexed", right_on="MOF_Name_alphnum_indexed")
    #drop rows of Pandas DataFrame whose value in certain columns is NaN
    df_merge = df_merge[np.isfinite(df_merge["Value_y"].astype(float))]
    return df_merge

#obtain_sa_pv(pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/clean_indexed/clean_sa_alphanum_indexed_name.csv"),
#            pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/clean_indexed/clean_pv_alphanum_indexed_name.csv"))\
#        .to_csv("clea_sa_pv_indexed_merged.csv")

def tm_add_mofname_new():

    value = "ASA_m2_g"
    refcode = "Ref_code"

    df_refcode_values = pd.read_csv("/home/omert/Desktop/mof_text_minig/code/result_analysis/core_refcode_sa_pv_values.csv")
    df_refcode_values = df_refcode_values[[refcode, value]]
    df_refcode_values = df_refcode_values.loc[df_refcode_values[value] != 0]

    df = pd.read_csv("/home/omert/Desktop/data_mining_mof/CSD_540/refcode_mofname.csv")[["Ref_code", "MOF_name"]]
    df = df.dropna(subset=["MOF_name"]) #
    df = df[df["MOF_name"].apply(lambda x: len(x) < 20)]

    #df_merge.to_csv("temp.csv")
    #df_merge = pd.read_csv("temp.csv")

    df_merge = pd.merge(df, df_refcode_values, how="left", left_on="Ref_code", right_on=refcode)
    df_merge = df_merge.dropna(subset=[value]) #

    df_merge = df_merge[["MOF_name", value]]
    df_merge = df_merge.sort_values(by=["MOF_name", value])

    #df_refcode_mofname1_2 = pd.DataFrame(columns=["RefCode", "MOF_Name1", "MOF_Name2", "DOI1", "DOI2"])
    l = 0
    mofname_now = 0
    mofname2 = 0
    a = 1
    b = 1
    mofnames= []
    for i, mofname in enumerate(df_merge["MOF_name"]):
        mofname = re.sub("[^A-Za-z0-9]+", "", str(mofname))
        mofname_pre = mofname

        if  mofname_pre == mofname_now:
            mofname1 = mofname_pre + "_" + str(a)
            a += 1
        else:
            mofname1 = mofname_pre
            a = 1
        mofname_now = mofname_pre
        mofnames.append(mofname1)
    df_merge["MOF_Name_alphnum_indexed"] = mofnames
    df_merge[["MOF_Name_alphnum_indexed", value]].to_csv("core_sa_alphanum_indexed_name.csv")
#tm_add_mofname_new()

def tm__mofname_alphanum_add_index():


    df_sa_pv = pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/tm_clean_indexed/tm_sa_add_alph_num_mofname_sorted_value.csv")
    df_sa_pv = df_sa_pv.sort_values(by=["MOF_name_alphanum", "Value"])

    l = 0
    mofname_now = 0
    mofname2 = 0
    a = 1
    b = 1
    mofnames= []
    for i, mofname in enumerate(df_sa_pv["MOF_name_alphanum"]):
        mofname_pre = mofname

        if  mofname_pre == mofname_now:
            mofname1 = mofname_pre + "_" + str(a)
            a += 1
        else:
            mofname1 = mofname_pre
            a = 1
        mofname_now = mofname_pre
        mofnames.append(mofname1)
    df_sa_pv["MOF_name_alphanum_indexed"] = mofnames
    df_sa_pv.to_csv("tm_sa_mofname_alphanum_indexed.csv")

#tm__mofname_alphanum_add_index()


def count_dois_by_pubs():
    df_sa_pv = pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/all_PV_extract.csv")
    df_sa_pv_no = df_sa_pv.loc[df_sa_pv["MOF Name"] == "*NO_MOF_data*"]
    df_sa_pv_idk = df_sa_pv.loc[df_sa_pv["MOF Name"] == "*IDK*"]
    print(len(df_sa_pv_idk) + len(df_sa_pv_no))
    #uniq_dois = df_sa_pv["DOI"].drop_duplicates()
    #print(len(uniq_dois))
#count_dois_by_pubs()

def dm_merge_dub_mofnames_for_nature_h2_up():

    df_refcode_values = pd.read_excel("../../in_output/mof_mining/Nature_DM.xlsx")
    df_refcode_values = df_refcode_values[["Ref_code", "UG at TPS"]]

    df = pd.read_csv("/home/omert/Desktop/data_mining_mof/CSD_540/refcode_mofname.csv")[["Ref_code", "MOF_name"]]
    df = df.dropna(subset=["MOF_name"]) #
    df_merge = df.astype(str).groupby("MOF_name").agg(";".join)
    df_merge.to_csv("temp.csv")
    df_merge = pd.read_csv("temp.csv")

    df_merge_values = pd.DataFrame(columns=["MOF_name", "MOF_name_alphanum",
                                            "Value_%s" %merged_type, "Value_mid", "Value_Av",
                                            "Value_mostfreq", "Values_max_without_outliyer"])

    for i, refcodes in enumerate(df_merge["Ref_code"]): # for the iteration data frame as row
        ls_values = []
        refcodes = refcodes.split(";")
        for refcode in refcodes:
            value = df_refcode_values.loc[df_refcode_values["Ref_code"] == refcode]["UG at TPS"]
            ls_values += value.to_list()
        if ls_values == []:
            continue
        ls_values_clean = [value for value in ls_values if value <= 15000]
        if ls_values_clean == []:
            continue
        if i%10 == 0:
            print(i)
        max_without_outliyer = max(ls_values_clean)

        freq_values = Counter(ls_values)
        if len(freq_values.values()) != len(ls_values): # eğer bu şart geçerli ise bir değrden enaz iki tane var
            most_freq_value = [key for key, value in freq_values.items()\
                               if value == max(freq_values.values())]
            most_freq_value = most_freq_value[0]
        else:
            most_freq_value = max(ls_values)
        ls_values = np.array(ls_values)
        ls_values = ls_values[np.logical_not(np.isnan(ls_values))]
        if len(ls_values) >= 3:
            quartile_1, quartile_3 = np.percentile(ls_values, [25, 75])
            iqr = quartile_3 - quartile_1
            lower_bound = quartile_1 - (iqr * 1.5)
            upper_bound = quartile_3 + (iqr * 1.5)
            outliers = np.where((ls_values > upper_bound) | (ls_values < lower_bound))
            indexs = np.in1d(ls_values, outliers)
            ls_values = np.delete(ls_values, indexs)

        df_merge_values.loc[i] = [str(df_merge.ix[i, "MOF_name"]),
                                  re.sub("[^A-Za-z0-9]+", "", str(df_merge.ix[i, "MOF_name"])),
                                  np.amax(ls_values),
                                  np.percentile(sorted(ls_values), 50),
                                  np.average(ls_values),
                                  most_freq_value,
                                  max_without_outliyer]
    df_merge_values.to_csv("nature_dm_h2_UGatTPS_mofname_selected_values.csv")

#dm_merge_dub_mofnames_for_nature_h2_up()

def obtain_top100():
    df_top100_Merged_MOF_name = pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/analysis4revision/random_200MOFName.csv")[:100]
    df_all_values_ofMOFS = pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/tm_clean_indexed/tm_pv_add_alph_num_mofname_sorted_value.csv")
    print(df_all_values_ofMOFS.head())
    df_merge = pd.merge(df_top100_Merged_MOF_name, df_all_values_ofMOFS, how="left",
                        left_on="MOF_name", right_on="MOF_name_alphanum")
    df_merge.to_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/analysis4revision/pv_to100_MOFs_values.csv")
    #drop rows of Pandas DataFrame whose value in certain columns is NaN
    #df_merge = df_merge[np.isfinite(df_merge["Value_y"].astype(float))]

#obtain_top100()


def obtain_top100_pv_sa_common_doi():
    df_pv_values_ofMOFS = pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/analysis4revision/analysis_random_100_MOFs_pv_values.csv")
    df_sa_values_ofMOFS = pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/analysis4revision/analysis_random_100_MOFs_sa_values.csv")

    df_merge = pd.merge(df_sa_values_ofMOFS, df_pv_values_ofMOFS, how="left",
                        left_on="MOF_name_alphanum_SA", right_on="MOF_name_alphanum_PV")
    df_merge.to_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/analysis4revision/analysis_random_100_MOFs_sa_pv_values.csv")

#obtain_top100_pv_sa_common_doi()


def add_mofname_alphanum_berend_tdm():

    #df_sa_pv = pd.read_excel("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/analysis4revision/berend_tdm_sa_pv.xlsx", sheet_name="SurfaceArea")
    df_sa_pv = pd.read_excel("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/analysis4revision/berend_tdm_sa_pv.xlsx", sheet_name="PoreVolume")

    alph_num_mof_name = []
    for mofname in df_sa_pv["MOFNAME"]:
        print(mofname)
        alph_num_mof_name.append(re.sub("[^A-Za-z0-9]+", "", str(mofname)))
    
    df_sa_pv["MOF_name_alphanum"] = alph_num_mof_name

    df_sa_pv.to_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/analysis4revision/berend_tdm_pv_add_alph_num_mofname.csv")
#add_mofname_alphanum_berend_tdm()

def berend_tdm_merge_dub_mofnames():

    df = pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/analysis4revision/berend_tdm_pv_add_alph_num_mofname.csv", low_memory=False)
    df = df.loc[df["UNIT"] == " cm3/g"]
    df = df[["MOFNAME_berend", "MOF_name_alphanum", "VALUE_berend"]]

    #df = df[df["MOF_name_alphanum"].apply(lambda x: len(str(x)) > 1)]
    #df = df[df["MOF_name_alphanum"].apply(lambda x: not str(x).isdigit())]
    #df = df[df["VALUE_berend"].apply(lambda x: str(x).isdigit())] # for ValueError: could not convert string to float: 'BET'"
    #df["VALUE_berend"] = df["VALUE_berend"].astype(float)
    #df = df[df["Value"].apply(lambda x: 15000 > float(x) > 0)]

    #df = df[["MOF Name", "Value"]]
    df_merge = df.astype(str).groupby("MOF_name_alphanum").agg(";".join)
    df_merge.to_csv("temp.csv")
    df_merge = pd.read_csv("temp.csv")

    #df_merge = pd.read_csv("./pv_values_groupby_mofname.csv")
    df_merge_values = pd.DataFrame(columns=["MOF_name", "MOF_name_alphanum", "Value_Berend_%s" %merged_type, "Value_Berend_mid", "Value_Berend_Av", "Value_Berend_mostfreq", "Value_Berend_max_without_outliyer"])
    for i, values in enumerate(df_merge["VALUE_berend"]): # for the iteration data frame as row
        ls_values = [float(value) for value in values.split(";")]

        ls_values_appr = [float(item) for item in ls_values]
        freq_values = Counter(ls_values_appr)
        if len(freq_values.values()) != len(ls_values): # eğer bu şart geçerli ise bir değrden enaz iki tane var
            most_freq_value = [key for key, value in freq_values.items()\
                               if value == max(freq_values.values())]
            most_freq_value = most_freq_value[0]
        else:
            most_freq_value = max(ls_values)

        ls_values_clean = [value for value in ls_values if value <= 15000]
        if ls_values_clean == []:
             continue
        max_without_outliyer = max(ls_values_clean)

        ls_values = np.array(ls_values)
        ls_values = ls_values[np.logical_not(np.isnan(ls_values))]
        if len(ls_values) >= 3:
            quartile_1, quartile_3 = np.percentile(ls_values, [25, 75])
            iqr = quartile_3 - quartile_1
            lower_bound = quartile_1 - (iqr * 1.5)
            upper_bound = quartile_3 + (iqr * 1.5)
            outliers = np.where((ls_values > upper_bound) | (ls_values < lower_bound))
            indexs = np.in1d(ls_values, outliers)
            ls_values = np.delete(ls_values, indexs)

        mofname = str(df_merge.ix[i, "MOFNAME_berend"]).split(";")[0]
        mofname = mofname.replace(":","").replace(";", "").replace(",", "")
        df_merge_values.loc[i] = [mofname,
                                  df_merge.ix[i, "MOF_name_alphanum"],
                                  np.amax(ls_values),
                                  np.percentile(sorted(ls_values), 50),
                                  np.average(ls_values),
                                  most_freq_value,
                                  max_without_outliyer]
    df_merge_values.to_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/analysis4revision/berend_tdm_pv_selected_values_add_mofname_alphanum.csv")
#berend_tdm_merge_dub_mofnames()

def merge_our_berend_tdm():
    for merged_type in ["Max", "mid", "Av", "mostfreq", "max_without_outliyer"]:
        our_tdm_sa = pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/tm_mofname_merged/tm_sa_selected_values_mofname_alphanum.csv")\
                [["MOF_name_alphanum", "Value_%s" %merged_type]]
        our_tdm_pv = pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/tm_mofname_merged/tm_pv_selected_values_mofname_alphanum.csv")\
                [["MOF_name_alphanum", "Value_%s" %merged_type]]
        
        berend_tdm_sa= pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/analysis4revision/berend_tdm_sa_selected_values_add_mofname_alphanum.csv")\
                [["MOF_name_alphanum", "Value_Berend_%s" %merged_type]]
        berend_tdm_pv= pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/analysis4revision/berend_tdm_pv_selected_values_add_mofname_alphanum.csv")\
                [["MOF_name_alphanum", "Value_Berend_%s" %merged_type]]
        
        df_merge_sa = pd.merge(our_tdm_sa, berend_tdm_sa, how="left",
                            left_on="MOF_name_alphanum", right_on="MOF_name_alphanum")
        df_merge_sa.dropna(subset=["Value_Berend_%s" %merged_type]).to_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/analysis4revision/merge_our_berend_sa_%s.csv"\
                                                              %merged_type)
        df_merge_pv = pd.merge(our_tdm_pv, berend_tdm_pv, how="left",
                            left_on="MOF_name_alphanum", right_on="MOF_name_alphanum")
        df_merge_pv.dropna(subset=["Value_Berend_%s" %merged_type]).to_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/analysis4revision/merge_our_berend_pv_%s.csv"\
                                                          %merged_type)
#merge_our_berend_tdm()


def merge_our_berend_tdm_v2():
    our_tdm_sa = pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/analysis4revision/new_tdm_cleaned_merged/tm_sa_selected_values_add_mofname_alphanum_new.csv")\
                [["MOF_name_alphanum", "Value_max"]]
    berend_tdm_sa= pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/analysis4revision/new_tdm_cleaned_merged/berend/tm_sa_selected_values_add_mofname_alphanum_just_max_berend.csv")
    df_merge_sa = pd.merge(our_tdm_sa, berend_tdm_sa, how="left",
                            left_on="MOF_name_alphanum", right_on="MOF_name_alphanum")
    print(df_merge_sa.head())
    df_merge_sa.dropna(subset=["Value_max_y"]).to_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/analysis4revision/new_tdm_cleaned_merged/merge_our_max_beren_max.csv")
#merge_our_berend_tdm_v2()

def tm_merge_values_av_add_doi():

    df = pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/general_results/tm_pv_add_alph_num_mofname_sorted_value.csv",
                           low_memory=False)[["MOF Name", "MOF_name_alphanum", "Value", "DOI"]]

    df = df[df["MOF_name_alphanum"].apply(lambda x: len(str(x)) > 1)]
    df = df[df["MOF_name_alphanum"].apply(lambda x: not str(x).isdigit())] #compatible with py3.7
    #df = df[df["Value"].apply(lambda x: str(x).isdigit())] # for ValueError: could not convert string to float: 'BET'" (compatible with py3.7)
    df["Value"] = df["Value"].astype(float)
    #df = df[df["Value"].apply(lambda x: 15000 > float(x) > 0)]
    
    #df = df[["MOF Name", "Value"]]
    df_merge = df.astype(str).groupby("MOF_name_alphanum").agg(";".join)
    df_merge.to_csv("temp.csv")
    df_merge = pd.read_csv("temp.csv")

    #df_merge = pd.read_csv("./pv_values_groupby_mofname.csv")
    df_merge_values = pd.DataFrame(columns=["MOF_name", "MOF_name_alphanum", "Value_Av", "Value_DOI"])
    for i, row in df_merge.iterrows(): # for the iteration data frame as row
        print(i)
        #print(row["DOI"])
        ls_values = [float(value) for value in row["Value"].split(";")]
        ls_dois = [doi for doi in row["DOI"].split(";")]
        ls_values_dois = ["%s:%s" %(value, doi) for value, doi in zip(ls_values, ls_dois)]


        ls_values_appr = [float(item) for item in ls_values]
        freq_values = Counter(ls_values_appr)
        if len(freq_values.values()) != len(ls_values): # eğer bu şart geçerli ise bir değrden enaz iki tane var
            most_freq_value = [key for key, value in freq_values.items()\
                               if value == max(freq_values.values())]
            most_freq_value = most_freq_value[0]
        else:
            most_freq_value = max(ls_values)

        ls_values_clean = [value for value in ls_values if value <= 15000]
        if ls_values_clean == []:
             continue
        max_without_outliyer = max(ls_values_clean)

        ls_values = sorted(np.array(ls_values))
        #ls_values = ls_values[np.logical_not(np.isnan(ls_values))]
        if len(ls_values) >= 3:
            quartile_1, quartile_3 = np.percentile(ls_values, [25, 75])
            iqr = quartile_3 - quartile_1
            lower_bound = quartile_1 - (iqr * 1.5)
            upper_bound = quartile_3 + (iqr * 1.5)
            ind_outliers = np.where((ls_values > upper_bound) | (ls_values < lower_bound))
            #indexs = np.in1d(ls_values, outliers)
            ls_values = np.delete(ls_values, ind_outliers)

        mofname = str(df_merge.ix[i, "MOF Name"]).split(";")[0]
        mofname = mofname.replace(":","").replace(";", "").replace(",", "")
        df_merge_values.loc[i] = [mofname,
                                  df_merge.ix[i, "MOF_name_alphanum"],
                                  "%.2f"%np.average(ls_values),
                                  ls_values_dois]
    df_merge_values.to_csv("tm_pv_avg_values_add_all_values_dois.csv")
#tm_merge_values_av_add_doi()

def tm_merge_dub_mofnames_just_most_freq():
    
    df = pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/general_results/tm_sa_add_alph_num_mofname_sorted_value.csv",
                           low_memory=False)[["MOF_name", "MOF_name_alphanum", "Value", "DOI"]]
    #df = pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/general_results/tm_pv_add_alph_num_mofname_sorted_value.csv",
    #                       low_memory=False)[["MOF_name", "MOF_name_alphanum", "Value", "DOI"]]

    #for Berend data
    #df = pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/analysis4revision/berend_tdm_merged/berend_tdm_sa_add_alph_num_mofname.csv", low_memory=False)
    ##df = df.loc[df["UNIT"] == " cm3/g"]
    #df = df.loc[df["TYPE"] == " BET "]
    #df = df[["MOF_name", "MOF_name_alphanum", "Value"]]

    df = df[df["MOF_name_alphanum"].apply(lambda x: len(str(x)) > 1)]
    df = df[df["MOF_name_alphanum"].apply(lambda x: not str(x).isdigit())]
    df = df[df["Value"].apply(lambda x: str(x).isdigit())] # for ValueError: could not convert string to float: 'BET'. Apply for just SA
    df["Value"] = df["Value"].astype(float)
    df = df[df["Value"].apply(lambda x: 15000.0 > float(x) > 0)] #15000 for SA and 10 for PV

    df_merge = df.astype(str).groupby("MOF_name_alphanum").agg(";".join)
    df_merge.to_csv("temp.csv")
    df_merge = pd.read_csv("temp.csv")

    #df_merge = pd.read_csv("./pv_values_groupby_mofname.csv")
    df_merge_values = pd.DataFrame(columns=["MOF_name", "MOF_name_alphanum",
                                            "Value_mostfreq", "DOI", "Value_DOI"])

    for i, row in df_merge.iterrows(): # for the iteration data frame as row
        #print(row["DOI"])i
        ls_values_0 = [float(value) for value in row["Value"].split(";")]
        ls_values = [float(value) for value in row["Value"].split(";")]
        ls_dois = [doi for doi in row["DOI"].split(";")]
        ls_values_dois = ["%s:%s" %(value, doi) for value, doi in zip(ls_values, ls_dois)]

        if ls_values == []:
             continue

        ls_values = np.array(ls_values)
        ls_values = ls_values[np.logical_not(np.isnan(ls_values))]

        ls_values = sorted(np.array(ls_values))
        #ls_values = ls_values[np.logical_not(np.isnan(ls_values))]
        if len(ls_values) >= 3:
            quartile_1, quartile_3 = np.percentile(ls_values, [25, 75])
            iqr = quartile_3 - quartile_1
            lower_bound = quartile_1 - (iqr * 1.5)
            upper_bound = quartile_3 + (iqr * 1.5)
            ind_outliers = np.where((ls_values > upper_bound) | (ls_values < lower_bound))
            #indexs = np.in1d(ls_values, outliers)
            ls_values = np.delete(ls_values, ind_outliers)

        ls_values_appr = [float(item) for item in ls_values]
        freq_values = Counter(ls_values_appr)
        if len(freq_values.values()) != len(ls_values): # eğer bu şart geçerli ise bir değrden enaz iki tane var
            most_freq_value = [key for key, value in freq_values.items()\
                               if value == max(freq_values.values())]
            most_freq_value = most_freq_value[0]
            #get most_freq_dois
            ls_idx = [ls_values_0.index(value) for value in freq_values.keys()]
            ls_most_freq_dois = [ls_dois[idx] for idx in ls_idx]
            ls_most_freq_dois = list(set(ls_most_freq_dois)) # for remove dublicates
        else:
            most_freq_value = max(ls_values)
            #get most_freq_dois
            idx = ls_values_0.index(most_freq_value)
            ls_most_freq_dois = [ls_dois[idx]]

        mofname = str(df_merge.ix[i, "MOF_name"]).split(";")[0]
        mofname = mofname.replace(":","").replace(";", "").replace(",", "")
        df_merge_values.loc[i] = [mofname,
                                  df_merge.ix[i, "MOF_name_alphanum"],
                                  most_freq_value, ls_most_freq_dois, ls_values_dois]

    df_merge_values.to_csv("tm_sa_selected_values_add_mofname_alphanum_just_most_freq.csv")

def tm_merge_dub_mofnames_just_max():
    
    #df = pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/general_results/tm_sa_add_alph_num_mofname_sorted_value.csv",
    #                       low_memory=False)[["MOF_name", "MOF_name_alphanum", "Value", "DOI"]]
    #df = pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/general_results/tm_pv_add_alph_num_mofname_sorted_value.csv",
    #                       low_memory=False)[["MOF_name", "MOF_name_alphanum", "Value", "DOI"]]

    #for Berend data
    df = pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/analysis4revision/berend_tdm_merged/berend_tdm_sa_add_alph_num_mofname.csv", low_memory=False)
    #df = df.loc[df["UNIT"] == " cm3/g"]
    df = df.loc[df["TYPE"] == " BET "]
    df = df[["MOF_name", "MOF_name_alphanum", "Value"]]

    df = df[df["MOF_name_alphanum"].apply(lambda x: len(str(x)) > 1)]
    df = df[df["MOF_name_alphanum"].apply(lambda x: not str(x).isdigit())]
    #df = df[df["Value"].apply(lambda x: str(x).isdigit())] # for ValueError: could not convert string to float: 'BET'. Apply for just SA
    df["Value"] = df["Value"].astype(float)
    #df = df[df["Value"].apply(lambda x: 10.0 > float(x) > 0)] #15000 for SA and 10 for PV

    df_merge = df.astype(str).groupby("MOF_name_alphanum").agg(";".join)
    df_merge.to_csv("temp.csv")
    df_merge = pd.read_csv("temp.csv")

    #df_merge = pd.read_csv("./pv_values_groupby_mofname.csv")
    df_merge_values = pd.DataFrame(columns=["MOF_name", "MOF_name_alphanum",
                                            "Value_max"])#, "DOI", "Value_DOI"])

    for i, row in df_merge.iterrows(): # for the iteration data frame as row
        #print(row["DOI"])i
        ls_values_0 = [float(value) for value in row["Value"].split(";")]
        ls_values = [float(value) for value in row["Value"].split(";")]
        #ls_dois = [doi for doi in row["DOI"].split(";")]
        #ls_values_dois = ["%s:%s" %(value, doi) for value, doi in zip(ls_values, ls_dois)]

        if ls_values == []:
             continue

        ls_values = np.array(ls_values)
        ls_values = ls_values[np.logical_not(np.isnan(ls_values))]

        ls_values = sorted(np.array(ls_values))
        #ls_values = ls_values[np.logical_not(np.isnan(ls_values))]
        if len(ls_values) >= 3:
            quartile_1, quartile_3 = np.percentile(ls_values, [25, 75])
            iqr = quartile_3 - quartile_1
            lower_bound = quartile_1 - (iqr * 1.5)
            upper_bound = quartile_3 + (iqr * 1.5)
            ind_outliers = np.where((ls_values > upper_bound) | (ls_values < lower_bound))
            #indexs = np.in1d(ls_values, outliers)
            ls_values = np.delete(ls_values, ind_outliers)

        max_value = max(ls_values)
        #get max doi
        #idx = ls_values_0.index(max_value)
        #ls_max_dois = [ls_dois[idx]]

        mofname = str(df_merge.ix[i, "MOF_name"]).split(";")[0]
        mofname = mofname.replace(":","").replace(";", "").replace(",", "")
        df_merge_values.loc[i] = [mofname,
                                  df_merge.ix[i, "MOF_name_alphanum"],
                                  max_value]#, ls_max_dois, ls_values_dois]

    df_merge_values.to_csv("tm_sa_selected_values_add_mofname_alphanum_just_max_berend.csv")
#tm_merge_dub_mofnames_just_max()

def tm_merge_dub_mofnames_v2():
    
    #df = pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/general_results/tm_sa_add_alph_num_mofname_sorted_value.csv",
    #                       low_memory=False)[["MOF Name", "MOF_name_alphanum", "Value", "DOI"]]
    #df = pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/general_results/tm_pv_add_alph_num_mofname_sorted_value.csv",
    #                       low_memory=False)[["MOF Name", "MOF_name_alphanum", "Value", "DOI"]]

    #for Berend data
    df = pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/analysis4revision/berend_tdm_merged/berend_tdm_sa_add_alph_num_mofname.csv", low_memory=False)
    #df = df.loc[df["UNIT"] == " cm3/g"]
    df = df.loc[df["TYPE"] == " BET "]
    df = df[["MOF_name", "MOF_name_alphanum", "Value"]]

    df = df[df["MOF_name_alphanum"].apply(lambda x: len(str(x)) > 1)]
    df = df[df["MOF_name_alphanum"].apply(lambda x: not str(x).isdigit())]
    df = df[df["Value"].apply(lambda x: str(x).isdigit())] # for ValueError: could not convert string to float: 'BET'. Apply for just SA
    df["Value"] = df["Value"].astype(float)
    df = df[df["Value"].apply(lambda x: 15000.0 > float(x) > 0)] #15000 for SA and 10 for PV

    #df = df[["MOF Name", "Value"]]
    df_merge = df.astype(str).groupby("MOF_name_alphanum").agg(";".join)
    df_merge.to_csv("temp.csv")
    df_merge = pd.read_csv("temp.csv")

    #df_merge = pd.read_csv("./pv_values_groupby_mofname.csv")
    df_merge_values = pd.DataFrame(columns=["MOF_name", "MOF_name_alphanum",
                                            "Value_max", "Value_mid", "Value_Av",
                                            "Value_mostfreq", "Values_max_wol",
                                            "Value_mid_wol", "Value_Av_wol","Value_mostfreq_wol",])# "DOI"])

    for i, row in df_merge.iterrows(): # for the iteration data frame as row
        #print(row["DOI"])
        print(i)
        ls_values = [float(value) for value in row["Value"].split(";")]
        #ls_dois = [doi for doi in row["DOI"].split(";")]

        ls_values_appr = [float(item) for item in ls_values]
        freq_values = Counter(ls_values_appr)
        if len(freq_values.values()) != len(ls_values): # eğer bu şart geçerli ise bir değrden enaz iki tane var
            most_freq_value_without_outliyer = [key for key, value in freq_values.items()\
                               if value == max(freq_values.values())]
            most_freq_value_without_outliyer = most_freq_value_without_outliyer[0]
        else:
            most_freq_value_without_outliyer = max(ls_values)

        ls_values_clean = [value for value in ls_values if value <= 15000]
        if ls_values_clean == []:
             continue
        max_without_outliyer = max(ls_values_clean)
        mid_without_outliyer = np.percentile(ls_values, 50)
        av_without_outliyer = np.average(ls_values)

        ls_values = np.array(ls_values)
        ls_values = ls_values[np.logical_not(np.isnan(ls_values))]

        ls_values = sorted(np.array(ls_values))
        #ls_values = ls_values[np.logical_not(np.isnan(ls_values))]
        if len(ls_values) >= 3:
            quartile_1, quartile_3 = np.percentile(ls_values, [25, 75])
            iqr = quartile_3 - quartile_1
            lower_bound = quartile_1 - (iqr * 1.5)
            upper_bound = quartile_3 + (iqr * 1.5)
            ind_outliers = np.where((ls_values > upper_bound) | (ls_values < lower_bound))
            #indexs = np.in1d(ls_values, outliers)
            ls_values = np.delete(ls_values, ind_outliers)

        ls_values_appr = [float(item) for item in ls_values]
        freq_values = Counter(ls_values_appr)
        if len(freq_values.values()) != len(ls_values): # eğer bu şart geçerli ise bir değrden enaz iki tane var
            most_freq_value = [key for key, value in freq_values.items()\
                               if value == max(freq_values.values())]
            most_freq_value = most_freq_value[0]
        else:
            most_freq_value = max(ls_values)

        mofname = str(df_merge.ix[i, "MOF_name"]).split(";")[0]
        mofname = mofname.replace(":","").replace(";", "").replace(",", "")
        df_merge_values.loc[i] = [mofname,
                                  df_merge.ix[i, "MOF_name_alphanum"],
                                  np.amax(ls_values),
                                  np.percentile(ls_values, 50),
                                  np.average(ls_values),
                                  most_freq_value,
                                  max_without_outliyer,
                                  mid_without_outliyer,
                                  av_without_outliyer,
                                  most_freq_value_without_outliyer]#, ls_dois]
    df_merge_values.to_csv("berend_sa_selected_values_add_mofname_alphanum_new.csv")

#tm_merge_dub_mofnames_v2()


def dist_same_mof_name():

    df = pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/general_results/tm_sa_add_alph_num_mofname_sorted_value.csv",
                           low_memory=False)[["MOF Name", "MOF_name_alphanum", "Value"]]
    #df = pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/general_results/tm_pv_add_alph_num_mofname_sorted_value.csv",
    #                       low_memory=False)[["MOF Name", "MOF_name_alphanum", "Value"]]

    df = df[df["MOF_name_alphanum"].apply(lambda x: len(str(x)) > 1)]
    df = df[df["MOF_name_alphanum"].apply(lambda x: not str(x).isdigit())]
    df = df[df["Value"].apply(lambda x: str(x).isdigit())] # for ValueError: could not convert string to float: 'BET'. Apply for just SA
    df["Value"] = df["Value"].astype(float)
    df = df[df["Value"].apply(lambda x: 15000.0 > float(x) > 0)]

    #df = df[["MOF Name", "Value"]]
    df_merge = df.astype(str).groupby("MOF_name_alphanum").agg(";".join)

    dist_list = []
    for i, row in df_merge.iterrows():
        dist_list.append(len(row["Value"].split(";")))
    dist_dic = {i: dist_list.count(i) for i in dist_list}
    df_dist = pd.DataFrame()
    df_dist["Frequency"]= dist_dic.keys()
    df_dist["#MOF_Value"]= dist_dic.values()
    df_dist.to_csv("dist_sa.csv")
    #print(df_dist.head())


#dist_same_mof_name()


def get_just_one_value():

    #df = pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/general_results/tm_sa_add_alph_num_mofname_sorted_value.csv",
    #                       low_memory=False)[["MOF Name", "MOF_name_alphanum", "Value"]]
    df = pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/analysis4revision/berend_tdm_merged/berend_tdm_sa_add_alph_num_mofname.csv",
                           low_memory=False)[["MOF_name", "MOF_name_alphanum", "Value"]]
    #df = pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/general_results/tm_pv_add_alph_num_mofname_sorted_value.csv",
    #                       low_memory=False)[["MOF Name", "MOF_name_alphanum", "Value"]]

    df = df[df["MOF_name_alphanum"].apply(lambda x: len(str(x)) > 1)]
    df = df[df["MOF_name_alphanum"].apply(lambda x: not str(x).isdigit())]
    #df = df[df["Value"].apply(lambda x: str(x).isdigit())] # for ValueError: could not convert string to float: 'BET'. Apply for just SA
    df["Value"] = df["Value"].astype(float)
    df = df[df["Value"].apply(lambda x: 15000.0 > float(x) > 0)]

    #df = df[["MOF Name", "Value"]]
    df_merge = df.astype(str).groupby("MOF_name_alphanum").agg(";".join)

    ls_values = []
    ls_mof_names = []
    for i, row in df_merge.iterrows():
        if len(row["Value"].split(";")) ==1:
            #print(i)
            ls_values.append(row["Value"])
            ls_mof_names.append(i)
    df_dist = pd.DataFrame()
    df_dist["MOF_name_alphanum"]= ls_mof_names
    df_dist["Value"]=  ls_values
    df_dist.to_csv("tdm_just_ones_value_sa_berend.csv")
    #print(df_dist.head())
#get_just_one_value()

def dm_merge_dub_mofnames_v2():
    key_value = "| ASA_m^2/g"
    df_refcode_values = pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/general_results/dm_clean_doi_pv_sorted.csv")
    df_refcode_values = df_refcode_values[["Ref_code", key_value]]
    df_refcode_values = df_refcode_values.loc[df_refcode_values[key_value] != 0.0]
    df_refcode_values = df_refcode_values[np.isfinite(df_refcode_values[key_value])] # for drop nan values
    #print(df_refcode_values.head())
    df = pd.read_csv("/home/omert/Desktop/data_mining_mof/CSD_540/refcode_mofname.csv")[["Ref_code", "MOF_name"]]
    df = df.dropna(subset=["MOF_name"]) #
    df_merge = df.astype(str).groupby("MOF_name").agg(";".join)
    df_merge.to_csv("temp.csv")
    df_merge = pd.read_csv("temp.csv")

    #df_merge = pd.read_csv("./pv_values_groupby_mofname.csv")
    df_merge_values = pd.DataFrame(columns=["MOF_name", "MOF_name_alphanum",
                                            "Value_max", "Value_mid", "Value_Av",
                                            "Value_mostfreq", "Values_max_wol",
                                            "Value_mid_wol", "Value_Av_wol","Value_mostfreq_wol",])# "DOI"])

    for i, refcodes in enumerate(df_merge["Ref_code"]): # for the iteration data frame as row
        ls_values = []
        refcodes = refcodes.split(";")
        for refcode in refcodes:
            value = df_refcode_values.loc[df_refcode_values["Ref_code"] == refcode][key_value]
            ls_values += value.to_list()
        if ls_values == []:
            #print(i)
            continue

        ls_values_appr = [float(item) for item in ls_values]
        freq_values = Counter(ls_values_appr)
        if len(freq_values.values()) != len(ls_values): # eğer bu şart geçerli ise bir değrden enaz iki tane var
            most_freq_value_without_outliyer = [key for key, value in freq_values.items()\
                               if value == max(freq_values.values())]
            most_freq_value_without_outliyer = most_freq_value_without_outliyer[0]
        else:
            most_freq_value_without_outliyer = max(ls_values)

        max_without_outliyer = max(ls_values)
        mid_without_outliyer = np.percentile(ls_values, 50)
        av_without_outliyer = np.average(ls_values)

        ls_values = np.array(ls_values)
        ls_values = ls_values[np.logical_not(np.isnan(ls_values))]

        ls_values = sorted(np.array(ls_values))
        print(ls_values)
        #ls_values = ls_values[np.logical_not(np.isnan(ls_values))]
        if len(ls_values) >= 3:
            quartile_1, quartile_3 = np.percentile(ls_values, [25, 75])
            iqr = quartile_3 - quartile_1
            lower_bound = quartile_1 - (iqr * 1.5)
            upper_bound = quartile_3 + (iqr * 1.5)
            ind_outliers = np.where((ls_values > upper_bound) | (ls_values < lower_bound))
            #indexs = np.in1d(ls_values, outliers)
            ls_values = np.delete(ls_values, ind_outliers)
        print(ls_values)
        ls_values_appr = [float(item) for item in ls_values]
        freq_values = Counter(ls_values_appr)
        if len(freq_values.values()) != len(ls_values): # eğer bu şart geçerli ise bir değrden enaz iki tane var
            most_freq_value = [key for key, value in freq_values.items()\
                               if value == max(freq_values.values())]
            most_freq_value = most_freq_value[0]
        else:
            most_freq_value = max(ls_values)

        df_merge_values.loc[i] = [str(df_merge.ix[i, "MOF_name"]),
                                  re.sub("[^A-Za-z0-9]+", "", str(df_merge.ix[i, "MOF_name"])),
                                  np.amax(ls_values),
                                  np.percentile(ls_values, 50),
                                  np.average(ls_values),
                                  most_freq_value,
                                  max_without_outliyer,
                                  mid_without_outliyer,
                                  av_without_outliyer,
                                  most_freq_value_without_outliyer]#, ls_dois]
    df_merge_values.to_csv("our_dm_sa_selected_values.csv")
#dm_merge_dub_mofnames_v2()

def merge_nature_gcmc_our_tdm_h2_huptake_just_most_freq():
    nature = pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/analysis4revision/new_tdm_cleaned_merged/nature_dm_h2_UGatTPS_mofname_selected_values.csv")\
            [["MOF_name_alphanum", "Value_mostfreq"]]
    our_tdm= pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/analysis4revision/new_tdm_cleaned_merged/tm_sa_pv_merged_h2_uptake.csv_just_mostfreq.csv")\
            [["MOF_name_alphanum", "H2_uptake(%)"]]
    df_merge = pd.merge(nature, our_tdm, how="left",
                            left_on="MOF_name_alphanum", right_on="MOF_name_alphanum")
    print(df_merge.head())
    df_merge.dropna(subset=["H2_uptake(%)"]).to_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/analysis4revision/new_tdm_cleaned_merged/merge_nature_gcmc_our_tdm_h2_huptake_just_most_freq.csv")
#merge_nature_gcmc_our_tdm_h2_huptake_just_most_freq()

def merge_our_dm_our_tdm_just_most_freq():
    our_dm = pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/analysis4revision/new_tdm_cleaned_merged/dm_sa_pv_merged_h2_uptake_mostfreq.csv")\
            [["MOF_name_alphanum", "H2_uptake(%)"]]
    our_tdm= pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/analysis4revision/new_tdm_cleaned_merged/tm_sa_pv_merged_h2_uptake.csv_just_mostfreq.csv")\
            [["MOF_name_alphanum", "H2_uptake(%)"]]
    df_merge = pd.merge(our_dm, our_tdm, how="left",
                            left_on="MOF_name_alphanum", right_on="MOF_name_alphanum")
    print(df_merge.head())
    df_merge.dropna(subset=["H2_uptake(%)_y"]).to_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/analysis4revision/new_tdm_cleaned_merged/merge_h2_uptake_our_dm_our_tdm_mostfreq.csv")
#merge_our_dm_our_tdm_just_most_freq()

def dm_merge_dub_mofnames_for_nature_h2_up_v2():

    df_refcode_values = pd.read_excel("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/Nature_DM.xlsx")
    df_refcode_values = df_refcode_values[["Ref_code", "UG at TPS"]]

    df = pd.read_csv("/home/omert/Desktop/data_mining_mof/CSD_540/refcode_mofname.csv")[["Ref_code", "MOF_name"]]
    df = df.dropna(subset=["MOF_name"]) #
    df_merge = df.astype(str).groupby("MOF_name").agg(";".join)
    df_merge.to_csv("temp.csv")
    df_merge = pd.read_csv("temp.csv")

    df_merge_values = pd.DataFrame(columns=["MOF_name", "MOF_name_alphanum",
                                            "Value_max", "Value_mid", "Value_Av",
                                            "Value_mostfreq", "Values_max_wol",
                                            "Value_mid_wol", "Value_Av_wol","Value_mostfreq_wol",])# "DOI"])

    for i, refcodes in enumerate(df_merge["Ref_code"]): # for the iteration data frame as row
        ls_values = []
        refcodes = refcodes.split(";")
        for refcode in refcodes:
            value = df_refcode_values.loc[df_refcode_values["Ref_code"] == refcode]["UG at TPS"]
            ls_values += value.to_list()
        if ls_values == []:
            continue
        ls_values = [value for value in ls_values if value <= 15000]
        if ls_values == []:
            continue
        print(i)

        ls_values_appr = [float(item) for item in ls_values]
        freq_values = Counter(ls_values_appr)
        if len(freq_values.values()) != len(ls_values): # eğer bu şart geçerli ise bir değrden enaz iki tane var
            most_freq_value_without_outliyer = [key for key, value in freq_values.items()\
                               if value == max(freq_values.values())]
            most_freq_value_without_outliyer = most_freq_value_without_outliyer[0]
        else:
            most_freq_value_without_outliyer = max(ls_values)

        max_without_outliyer = max(ls_values)
        mid_without_outliyer = np.percentile(ls_values, 50)
        av_without_outliyer = np.average(ls_values)

        ls_values = np.array(ls_values)
        ls_values = ls_values[np.logical_not(np.isnan(ls_values))]

        ls_values = sorted(np.array(ls_values))
        #ls_values = ls_values[np.logical_not(np.isnan(ls_values))]
        if len(ls_values) >= 3:
            quartile_1, quartile_3 = np.percentile(ls_values, [25, 75])
            iqr = quartile_3 - quartile_1
            lower_bound = quartile_1 - (iqr * 1.5)
            upper_bound = quartile_3 + (iqr * 1.5)
            ind_outliers = np.where((ls_values > upper_bound) | (ls_values < lower_bound))
            #indexs = np.in1d(ls_values, outliers)
            ls_values = np.delete(ls_values, ind_outliers)

        ls_values_appr = [float(item) for item in ls_values]
        freq_values = Counter(ls_values_appr)
        if len(freq_values.values()) != len(ls_values): # eğer bu şart geçerli ise bir değrden enaz iki tane var
            most_freq_value = [key for key, value in freq_values.items()\
                               if value == max(freq_values.values())]
            most_freq_value = most_freq_value[0]
        else:
            most_freq_value = max(ls_values)

        df_merge_values.loc[i] = [str(df_merge.ix[i, "MOF_name"]),
                                  re.sub("[^A-Za-z0-9]+", "", str(df_merge.ix[i, "MOF_name"])),
                                  np.amax(ls_values),
                                  np.percentile(ls_values, 50),
                                  np.average(ls_values),
                                  most_freq_value,
                                  max_without_outliyer,
                                  mid_without_outliyer,
                                  av_without_outliyer,
                                  most_freq_value_without_outliyer]#, ls_dois]
        df_merge_values.to_csv("nature_dm_h2_UGatTPS_mofname_selected_values.csv")
#dm_merge_dub_mofnames_for_nature_h2_up_v2()

def tm_mofname_alphanum_add_index_v2():

    df_sa_pv = pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/analysis4revision/new_tdm_cleaned_indexed/final_clean_pv.csv")
    #df_sa_pv = df_sa_pv[df_sa_pv["Value"].apply(lambda x: str(x).isdigit())] # for ValueError: could not convert string to float: 'BET'. Apply for just SA
    df_sa_pv["Value"] = df_sa_pv["Value"].astype(float)
    #df_sa_pv = df_sa_pv[df_sa_pv["MOF_name_alphanum"].apply(lambda x: not str(x).isdigit())]
    #df_sa_pv = df_sa_pv[df_sa_pv["Value"].apply(lambda x: 15000.0 > float(x) > 0)] #15000 for SA and 10 for PV
 
    ls_name_alphanum = [re.sub("[^A-Za-z0-9]+", "", str(mofname)) for mofname in df_sa_pv["MOF_name"]]
    df_sa_pv["MOF_name_alphanum"] = ls_name_alphanum
    df_sa_pv = df_sa_pv[df_sa_pv["MOF_name_alphanum"].apply(lambda x: not str(x).isdigit())]

    df_sa_pv = df_sa_pv.sort_values(by=["MOF_name_alphanum", "Value"], ascending=False)
    #df_sa_pv.to_csv("added_mofname_alphanum.csv")

    df_merge = df_sa_pv.astype(str).groupby("MOF_name_alphanum", as_index=False, sort=False).agg(";".join)
    df_merge.to_csv("temp.csv")
    df_merge = pd.read_csv("temp.csv")

    indexed_mofname_alphanum = []
    for i, row in df_merge.iterrows(): # for the iteration data frame as row
        len_mofnames = len(row["Value"].split(";"))
        mofname_alphanum = row["MOF_name_alphanum"]
        if len_mofnames == 1:
            indexed_mofname_alphanum.append(mofname_alphanum)
        else:
            for k in range(len_mofnames):
                indexed_mofname_alphanum.append("%s_%s"%(mofname_alphanum, k + 1))

    df_sa_pv["MOF_name_alphanum_indexed"] = indexed_mofname_alphanum

    df_sa_pv.to_csv("tm_pv_mofname_alphanum_indexed.csv")

#tm_mofname_alphanum_add_index_v2()

def merge_sa_pv_indexed():
    df_sa = pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/analysis4revision/new_tdm_cleaned_indexed/tm_sa_mofname_alphanum_indexed.csv")
    df_pv = pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/analysis4revision/new_tdm_cleaned_indexed/tm_pv_mofname_alphanum_indexed.csv")


    df_merge_sa_pv = pd.merge(df_sa, df_pv, how="left",
                            left_on="MOF_name_alphanum_indexed", right_on="MOF_name_alphanum_indexed")
    df_merge_sa_pv.dropna(subset=["MOF_name_alphanum_y"]).to_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/analysis4revision/new_tdm_cleaned_indexed/merged_sa_pv.csv")
#merge_sa_pv_indexed()

df_1 = pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/analysis4revision/tests/tm_sa_pv_indexed_mofname_alphanum_h2_uptake.csv")["MOF_name_alphanum_indexed"]
df_2 = pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/analysis4revision/new_tdm_cleaned_indexed/tm_sa_mofname_alphanum_indexed.csv")["MOF_name_alphanum_indexed"]

df_merge = pd.merge(df_1, df_1, how="left", left_on="MOF_name_alphanum_indexed", right_on="MOF_name_alphanum_indexed")
print(df_merge)

