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
    df_sa_values = pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/analysis4revision/new_tdm_cleaned_merged/our_dm_sa_selected_values.csv")
    #df_sa_values = df_sa_values[df_sa_values["MOF_name"].apply(lambda x: len(str(x)) > 1)]
    #df_sa_values = df_sa_values[df_sa_values["Value_Av"].apply(lambda x: 15000 > float(x) > 0)]
    #df_sa_values["Value_Av"] = df_sa_values["Value_Av"].astype(float)

    df_pv_values = pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/analysis4revision/new_tdm_cleaned_merged/our_dm_pv_selected_values.csv")
    #df_pv_values = df_pv_values[df_pv_values["MOF_name"].apply(lambda x: len(str(x)) > 1)]
    #df_pv_values = df_pv_values[df_pv_values["Value_Av"].apply(lambda x: 10 > float(x) > 0)]
    #df_pv_values["Value_Av"] = df_pv_values["Value_Av"].astype(float)

    sa_pv_merged = pd.merge(df_sa_values, df_pv_values, how="left", left_on="MOF_name_alphanum", right_on="MOF_name_alphanum")
    sa_pv_merged = sa_pv_merged.dropna(subset=["Value_Av_y"])

    for label in ["Value_Max",  "Value_mid",  "Value_Av", "Value_mostfreq",  "Values_max_without_outliyer"]:
        h2_uptake = []
        for i, row in sa_pv_merged.iterrows():
            h2_uptake.append(calc_h2Up(row["%s_y"%label], row["%s_x"%label]))
        sa_pv_merged_final = sa_pv_merged[["MOF_name_x", "MOF_name_alphanum", "%s_x"%label, "%s_y"%label]]
        sa_pv_merged_final["H2_uptake(%)"] = h2_uptake
        sa_pv_merged_final.to_csv("dm_sa_pv_merged_%s_h2_uptake.csv"%label)

        #sa_pv_merged[["MOF_name_alphanum", "%s_x"%label, "%s_y"%label]].to_csv("tm_sa_pv_merged_%s.csv"%label)
#merge_calc_h2_up_merged()

def merge_calc_h2_up_indexed():
    label = "Value"
    df_sa_values = pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/dm_mofname_indexed/ours_dm_sa_alphanum_indexed_name.csv")
    df_sa_values = df_sa_values[df_sa_values["MOF_name_alphanum_indexed"].apply(lambda x: len(str(x)) > 1)]
    #df_sa_values = df_sa_values[df_sa_values["MOF_name_alphanum_indexed"].apply(lambda x: not str(x).isnumeric())]
    #df_sa_values = df_sa_values[df_sa_values["Value"].apply(lambda x: str(x).isnumeric())]
    #df_sa_values = df_sa_values[df_sa_values["Value"].apply(lambda x: 15000 > float(x) > 0)]
    #df_sa_values["Value"] = df_sa_values["Value"].astype(float)

    df_pv_values = pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/dm_mofname_indexed/ours_dm_pv_alphanum_indexed_name.csv")
    df_pv_values = df_pv_values[df_pv_values["MOF_name_alphanum_indexed"].apply(lambda x: len(str(x)) > 1)]
    #df_sa_values = df_sa_values[df_sa_values["MOF_name_alphanum_indexed"].apply(lambda x: not str(x).isnumeric())]
    #df_pv_values = df_pv_values[df_pv_values["Value"].apply(lambda x: 10 > float(x) > 0)]
    #df_pv_values["Value"] = df_pv_values["Value"].astype(float)

    sa_pv_merged = pd.merge(df_sa_values, df_pv_values, how="left", left_on="MOF_name_alphanum_indexed", right_on="MOF_name_alphanum_indexed")
    sa_pv_merged = sa_pv_merged[["MOF_name_alphanum_indexed", "| ASA_m^2/g", "| POAV_cm^3/g"]]
    sa_pv_merged = sa_pv_merged.dropna(subset=["| ASA_m^2/g"])
    sa_pv_merged = sa_pv_merged.dropna(subset=["| POAV_cm^3/g"])
    sa_pv_merged.to_csv("test00002.csv")
    h2_uptake = []
    for i, row in sa_pv_merged.iterrows():
        h2_uptake.append(calc_h2Up(row["| ASA_m^2/g"], row["| POAV_cm^3/g"]))
    sa_pv_merged["H2_uptake(%)"] = h2_uptake
    sa_pv_merged.to_csv("dm_sa_pv_indexed_mofname_alphanum_h2_uptake.csv")
#merge_calc_h2_up_indexed()

def merge_calc_h2_up_merged_just_mostfreq():
    df_sa_values = pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/analysis4revision/new_tdm_cleaned_merged/our_dm_sa_selected_values.csv")
    df_pv_values = pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/analysis4revision/new_tdm_cleaned_merged/our_dm_pv_selected_values.csv")

    sa_pv_merged = pd.merge(df_sa_values, df_pv_values, how="left", left_on="MOF_name_alphanum", right_on="MOF_name_alphanum")
    sa_pv_merged = sa_pv_merged.dropna(subset=["Value_mostfreq_y"])

    h2_uptake = []
    for i, row in sa_pv_merged.iterrows():
        h2_uptake.append(calc_h2Up(row["Value_mostfreq_y"], row["Value_mostfreq_x"]))
    sa_pv_merged_final = sa_pv_merged[["MOF_name_x", "MOF_name_alphanum", "Value_mostfreq_x", "Value_mostfreq_y"]]
    sa_pv_merged_final["H2_uptake(%)"] = h2_uptake
    sa_pv_merged_final.to_csv("dm_sa_pv_merged_h2_uptake_mostfreq.csv")
merge_calc_h2_up_merged_just_mostfreq()
