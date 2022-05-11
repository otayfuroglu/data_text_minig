# -*- coding:utf-8 -*-

import pandas as pd
import re
from ast import literal_eval #Extracting list from string
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

refcode_mofname_csd_text_0 = pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/refcode_mofname_csd_text.csv")
refcode_mofname_csd_text_0 = refcode_mofname_csd_text_0.drop_duplicates()
refcode_mofname_csd_text_0 = refcode_mofname_csd_text_0[["MOF_Name", "RefCode"]].astype(str).groupby("MOF_Name").agg(";".join)
refcode_mofname_csd_text_0.to_csv("refcode_mofname_csd_text_01.csv")
