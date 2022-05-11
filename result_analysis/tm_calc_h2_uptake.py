# -*- coding:utf-8 *-*

import pandas as pd

def calc_h2Up(PV, SA):
    """
    H2 adsorption in microporous carbons, a linear relationship
    (i.e., the so-called “Chahine rule”- Ref. Panella, B.; Hirscher, M.; Roth, S. Carbon 2005, 43, 2209)
    was observed between surface area and excess hydrogen uptake, nexcess, at 77 K and 35 bar.
    """
    c = 0.021  # H2 mg/m2 --> proportionslity canstant linking SA
    ph2 = 11.5 # kg/m3 (77 K and 35 bar)
    # SA (m2/g)
    # PV (cm3/g)
    #ouput --> % h2 up on MOF
    n_excess = (c/1000) * SA
    n_gas = (ph2*1000) * (PV/1000000)
    h2_up = n_excess + n_gas #ouput --> h2 up (gram H2/gram MOF) 
    return float("%2.2f" % (100*h2_up))

def merge_calc_h2_up_merged():
    df_sa_values = pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/tm_mofname_merged/tm_sa_selected_values_add_mofname_alphanum.csv")
    #df_sa_values = df_sa_values[df_sa_values["MOF_name"].apply(lambda x: len(str(x)) > 1)]
    #df_sa_values = df_sa_values[df_sa_values["Value_Av"].apply(lambda x: 15000 > float(x) > 0)]
    #df_sa_values["Value_Av"] = df_sa_values["Value_Av"].astype(float)

    df_pv_values = pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/tm_mofname_merged/tm_pv_selected_values_mofname_alphanum.csv")
    #df_pv_values = df_pv_values[df_pv_values["MOF_name"].apply(lambda x: len(str(x)) > 1)]
    #df_pv_values = df_pv_values[df_pv_values["Value_Av"].apply(lambda x: 10 > float(x) > 0)]
    df_pv_values["Value_Av"] = df_pv_values["Value_Av"].astype(float)

    sa_pv_merged = pd.merge(df_sa_values, df_pv_values, how="left", left_on="MOF_name_alphanum", right_on="MOF_name_alphanum")
    sa_pv_merged = sa_pv_merged.dropna(subset=["Value_Av_y"])

    for label in ["Value_Max",  "Value_mid",  "Value_Av", "Value_mostfreq",  "Values_max_without_outliyer"]:
        h2_uptake = []
        for i, row in sa_pv_merged.iterrows():
            h2_uptake.append(calc_h2Up(row["%s_y"%label], row["%s_x"%label]))
        sa_pv_merged_final = sa_pv_merged[["MOF_name", "MOF_name_alphanum", "%s_x"%label, "%s_y"%label]]
        sa_pv_merged_final["H2_uptake(%)"] = h2_uptake
        sa_pv_merged_final.to_csv("tm_sa_pv_merged_%s_h2_uptake.csv"%label)

        #sa_pv_merged[["MOF_name_alphanum", "%s_x"%label, "%s_y"%label]].to_csv("tm_sa_pv_merged_%s.csv"%label)
#merge_calc_h2_up_merged()

def merge_calc_h2_up_indexed():
    label = "Value_Av"
    df_sa_values = pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/analysis4revision/tm_merge_av_value_doi/tm_sa_avg_values_add_all_values_dois.csv")
    #df_sa_values = df_sa_values[df_sa_values["MOF_name_alphanum"].apply(lambda x: len(str(x)) > 1)]
    #df_sa_values = df_sa_values[df_sa_values["MOF_name_alphanum"].apply(lambda x: not str(x).isnumeric())]
    #df_sa_values = df_sa_values[df_sa_values["Value"].apply(lambda x: str(x).isnumeric())]
    #df_sa_values = df_sa_values[df_sa_values["Value"].apply(lambda x: 15000 > float(x) > 0)]
    df_sa_values["Value_Av"] = df_sa_values["Value_Av"].astype(float)

    df_pv_values = pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/analysis4revision/tm_merge_av_value_doi/tm_pv_avg_values_add_all_values_dois.csv")
    df_pv_values = df_pv_values[df_pv_values["MOF_name_alphanum"].apply(lambda x: len(str(x)) > 1)]
    df_pv_values = df_pv_values[df_pv_values["Value_Av"].apply(lambda x: 10 > float(x) > 0)]
    #df_pv_values["Value"] = df_pv_values["Value"].astype(float)

    sa_pv_merged = pd.merge(df_sa_values, df_pv_values, how="left", left_on="MOF_name_alphanum", right_on="MOF_name_alphanum")
    sa_pv_merged = sa_pv_merged[["MOF_name_x", "MOF_name_alphanum", "%s_x"%label, "Value_DOI_x", "%s_y"%label, "Value_DOI_y"]]
    sa_pv_merged = sa_pv_merged[sa_pv_merged["MOF_name_x"].apply(lambda x: not str(x).isnumeric())]
    sa_pv_merged = sa_pv_merged.dropna(subset=["Value_Av_y"])
    sa_pv_merged = sa_pv_merged.dropna(subset=["Value_Av_x"])
    sa_pv_merged.to_csv("test00002.csv")
    h2_uptake = []
    for i, row in sa_pv_merged.iterrows():
        h2_uptake.append(calc_h2Up(row["%s_y"%label], row["%s_x"%label]))
    sa_pv_merged["H2_uptake(%)"] = h2_uptake
    sa_pv_merged.to_csv("tm_sa_pv_indexed_mofname_alphanum_h2_uptake.csv")
#merge_calc_h2_up_indexed()

def merge_calc_h2_up_merged_most_freq_add_dois():
    df_sa_values = pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/analysis4revision/new_tdm_cleaned_merged/tm_sa_selected_values_add_mofname_alphanum_just_most_freq.csv")#[["MOF_name", "MOF_name_alphanum", "Value_mostfreq", "DOI"]]
    #df_sa_values = df_sa_values[df_sa_values["MOF_name"].apply(lambda x: len(str(x)) > 1)]
    #df_sa_values = df_sa_values[df_sa_values["Value_Av"].apply(lambda x: 15000 > float(x) > 0)]
    df_sa_values["Value_mostfreq"] = df_sa_values["Value_mostfreq"].astype(float)

    df_pv_values = pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/analysis4revision/new_tdm_cleaned_merged/tm_pv_selected_values_add_mofname_alphanum_just_most_freq.csv")#[["MOF_name", "MOF_name_alphanum", "Value_mostfreq", "DOI"]]
    #df_pv_values = df_pv_values[df_pv_values["MOF_name"].apply(lambda x: len(str(x)) > 1)]
    #df_pv_values = df_pv_values[df_pv_values["Value_Av"].apply(lambda x: 10 > float(x) > 0)]
    df_pv_values["Value_mostfreq"] = df_pv_values["Value_mostfreq"].astype(float)

    sa_pv_merged = pd.merge(df_sa_values, df_pv_values, how="left", left_on="MOF_name_alphanum", right_on="MOF_name_alphanum")
    sa_pv_merged = sa_pv_merged.dropna(subset=["Value_mostfreq_y"])
    #print(sa_pv_merged.head())

    h2_uptake = []
    for i, row in sa_pv_merged.iterrows():
        h2_uptake.append(calc_h2Up(row["Value_mostfreq_y"], row["Value_mostfreq_x"]))
    sa_pv_merged_final = sa_pv_merged[["MOF_name_x", "MOF_name_alphanum", "Value_mostfreq_x", "Value_mostfreq_y", "DOI_x", "DOI_y", "Value_DOI_x", "Value_DOI_y"]]
    sa_pv_merged_final["H2_uptake(%)"] = h2_uptake
    sa_pv_merged_final.to_csv("tm_sa_pv_merged_h2_uptake.csv_just_mostfreq.csv")

#merge_calc_h2_up_merged_most_freq_add_dois()

def merge_calc_h2_up_indexed_v2():
    #df_sa_values = pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/analysis4revision/new_tdm_cleaned_indexed/tm_sa_mofname_alphanum_indexed.csv")\
    #        [["MOF_name_alphanum_indexed", "MOF_name_alphanum", "MOF_name", "Value_SA", "DOI"]]
    ##df_sa_values = df_sa_values[df_sa_values["MOF_name"].apply(lambda x: len(str(x)) > 1)]
    ##df_sa_values = df_sa_values[df_sa_values["Value_Av"].apply(lambda x: 15000 > float(x) > 0)]
    #df_sa_values["Value_mostfreq"] = df_sa_values["Value_mostfreq"].astype(float)

    #df_pv_values = pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/analysis4revision/new_tdm_cleaned_indexed/tm_pv_mofname_alphanum_indexed.csv")\
    #        [["MOF_name_alphanum_indexed", "MOF_name_alphanum", "MOF_name", "Value_SA", "DOI"]]
    ##df_pv_values = df_pv_values[df_pv_values["MOF_name"].apply(lambda x: len(str(x)) > 1)]
    ##df_pv_values = df_pv_values[df_pv_values["Value_Av"].apply(lambda x: 10 > float(x) > 0)]
    #df_pv_values["Value_mostfreq"] = df_pv_values["Value_mostfreq"].astype(float)

    #sa_pv_merged = pd.merge(df_sa_values, df_pv_values, how="left", left_on="MOF_name_alphanum_indexed", right_on="MOF_name_alphanum_indexed")
    #sa_pv_merged = sa_pv_merged.dropna(subset=["Value_PV_y"])
    ##print(sa_pv_merged.head())

    sa_pv_merged = pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/analysis4revision/new_tdm_cleaned_indexed/merged_sa_pv_mofname_indexed.csv")
            #\[["MOF_name_alphanum_indexed", "MOF_name_alphanum", "MOF_name", "Value_SA", "DOI_PV", "Value_PV", "DOI_PV"]]
    h2_uptake = []
    for i, row in sa_pv_merged.iterrows():
        h2_uptake.append(calc_h2Up(float(row["Value_PV"]), float(row["Value_SA"])))
    #sa_pv_merged_final = sa_pv_merged[["MOF_name_x", "MOF_name_alphanum", "Value_mostfreq_x", "Value_mostfreq_y", "DOI_x", "DOI_y", "Value_DOI_x", "Value_DOI_y"]]
    sa_pv_merged["H2_uptake(%)"] = h2_uptake
    sa_pv_merged.to_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/analysis4revision/new_tdm_cleaned_indexed/tm_sa_pv_merged_h2_uptake_indexed.csv")

merge_calc_h2_up_indexed_v2()
