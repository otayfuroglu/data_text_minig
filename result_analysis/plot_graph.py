# -*- coding:utf-8 -*-

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

import matplotlib.ticker as ticker

def save_to_exel(df, file_name):
	writer = pd.ExcelWriter("%s.xlsx"%file_name, engine='xlsxwriter')
	df.to_excel(writer, sheet_name='Sheet1')
	writer.save()

#df_data = pd.read_excel("sort_betSA_PV_H2_up_2.xlsx")

def plot_pv(df_data):

    value_pv = df_data["Value_PV(cm3/g)"]
    h2_up = df_data["H2_UP (w/W %)"]


    fig = plt.figure()

    ax = fig.add_axes([0.1, 0.1, 1.0, 1.0])
    #ax.plot([value_pv, value_pv*value_pv])

    ax.scatter(value_pv, h2_up, alpha=0.5)
    ax.set_ylabel("$H_2$ Uptake (w/W %)")
    ax.set_xlabel("Pore Volume ($cm_3$/g)")
    ax.set_title("Distributions of H2_UP $H_2$ Uptake (w/W %) by Pore Volume ($cm_3$/g)")
    ax.scatter(h2_up, value_pv, alpha=0.2)

    limited_h2_up = df_data.loc[df_data["H2_UP (w/W %)"] > 8]

    limited_h2_up_index = limited_h2_up.index

    #limited_value_pv = df_data.loc[df_data["Value_PV(cm3/g)"] > 5]

    mof_names = limited_h2_up["MOF Name"]
    for i, txt in zip(limited_h2_up_index, mof_names):
        ax.annotate(txt, (value_pv[i], h2_up[i]))

#plot_pv(df_data)

def plot_sa(df_data):

    value_sa = df_data["Value_SA(m2/g)"]
    h2_up = df_data["H2_UP (w/W %)"]

    fig1 = plt.figure()
    ax1 = fig1.add_axes([0.1, 0.1, 1.0, 1.0])

    ax1.scatter(value_sa, h2_up, alpha=0.7)
    ax1.set_ylabel("$H_2$ Uptake (w/W %)")
    ax1.set_xlabel("Surface Area ($cm_2$/g)")
    ax1.set_title("Distributions of H2_UP $H_2$ Uptake (w/W %) bySurface Area ($cm_2$/g)")
    ax1.set_xlim([0, 12000])
    ax1.set_ylim([0, 50])

    plt.xticks(np.arange(10))

    #ax1.set_yscale("log")
    #ax1.set_xscale('log')

    ax2 = fig1.add_axes([0.2, 0.5, 0.4, 0.4])
    ax2.scatter(value_sa, h2_up, alpha=0.7)
    ax2.set_xlim([5000, 10000])
    ax2.set_ylim([10, 20])
    ax2.set_title("Zoom")
    ax2.set_xscale('log')



    limited_h2_up = df_data.loc[df_data["H2_UP (w/W %)"] > 8]
    limited_h2_up_index = limited_h2_up.index
    mof_names = limited_h2_up["MOF Name"]
    for i, txt in zip(limited_h2_up_index, mof_names):
        ax2.annotate(txt, (value_sa[i], h2_up[i]))


    plt.show()

#plot_sa(df_data)

#fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(4, 2))

#axes[0].plot(x, y, color="blue", linestyle="-")
#axes[1].plot(x, z, color="red", linestyle="-.")

def get_all_mofs_from_web_ofsci_scopus():
    i = 1
    df_mofs_web_ofsci = []
    while i <= 26:
        fl = "/home/omert/Desktop/mof_text_minig/get_dois/web_of_sci_all_mof1/web_of_sci_all_mof_%s" %i

        df_mof = pd.read_csv("%s.txt" %fl, sep='\t', lineterminator='\r')
        df_mofs_web_ofsci.append(df_mof)
        i += 1

    df_mofs_web_ofsci = pd.concat(df_mofs_web_ofsci)
    df_mofs_scopus = pd.read_csv("/home/omert/Desktop/mof_text_minig/get_dois/scopus_all_mof_all_year_1.csv", low_memory=False)

    df_mofs_web_ofsci_doi_year = df_mofs_web_ofsci[["AR", "PD"]]
    df_mofs_web_ofsci_doi_year = df_mofs_web_ofsci_doi_year.rename(columns={"AR": "DOI"})
    df_mofs_web_ofsci_doi_year = df_mofs_web_ofsci_doi_year.rename(columns={"PD": "Year"})

    df_mofs_scopus_doi_year = df_mofs_scopus[["DOI", "Year"]]


    df_all_mofs_doi_year = pd.concat([df_mofs_web_ofsci_doi_year, df_mofs_scopus_doi_year])

    df_all_mofs_doi_year = df_all_mofs_doi_year.drop_duplicates()

    #save_to_exel(df_all_mofs_doi_year, "all_mofs_doi_year_from_web_ofsci")
    return df_all_mofs_doi_year

#get_all_mofs_from_web_ofsci_scopus()

def graph_mofs_byyear(df_all_mofs_doi_year):
    sns.set()
    all_mofs_byyears = df_all_mofs_doi_year["Year"]

    start_year = 2017
    finish_year = 1969

    year_Number = {}
    for i in range(start_year-finish_year):
        year = start_year - i

        n_mofs = len(all_mofs_byyears.loc[all_mofs_byyears==year])
        #print (year, "--->", n_mofs)
        year_Number[year] = n_mofs


    years = np.array(list(year_Number.keys()))
    number_ofmofs_byyear = np.array(list(year_Number.values()))


    #get graph

    fig = plt.figure()
    ax = fig.add_axes([0.1, 0.1, 1.0, 1.0])

    ax.bar(years, number_ofmofs_byyear, alpha=0.5, align='center')
    ax.set_ylabel("Years")
    ax.set_xlabel("Number of Publication related MOF and Coordination Polymers")
    ax.set_title("Distribution of Number of Publication related MOF and Coordination Polymers by years")
    ax.set_xlim(1995, 2020)
    ax.set_ylim(0, 30000)

    # polt regression line
    from numpy.polynomial.polynomial import polyfit
    b, m = polyfit(years, number_ofmofs_byyear, 1)
    plt.plot(years, b + m * years)
    #plt.xticks(year_Number.keys(), year_Number.values())

    plt.show()


def graph_mofs_byyear_sns(df_all_mofs_doi_year):

    all_mofs_byyears = df_all_mofs_doi_year["Year"]

    start_year = 2017
    finish_year = 1969

    df_number_ofmofs_byyear = pd.DataFrame(columns=["Year", "Number of MOF"])

    year_Number = {}
    for i in range(start_year-finish_year):
        year = start_year - i

        n_mofs = len(all_mofs_byyears.loc[all_mofs_byyears==year])
        #print (year, "--->", n_mofs)
        year_Number[year] = n_mofs


    df_number_ofmofs_byyear["Year"] = list(year_Number.keys())
    df_number_ofmofs_byyear["Number of MOF"] = list(year_Number.values())


    #get graph
    sns.set(style="ticks", color_codes=True, font_scale=1)
    #sns.lmplot("Year", "Number of MOF", data=df_number_ofmofs_byyear, fit_reg=False)

    #fig = plt.figure()


    ax = sns.barplot(x="Year", y="Number of MOF", data=df_number_ofmofs_byyear)
    ax.set_xlabel("Years")
    ax.set_ylabel("Number of Publication")
    ax.set_title("Distribution of Number of Publication Related MOF and Coordination Polymers by Years")

    ax.set_ylim(0, 30000)
    ax.autoscale_view(scalex=True)

    #ax.set_xticklabels(labels=sorted(list(year_Number.keys())[:28]), rotation=45, ha='right', )

    ax.xaxis.set_major_locator(plt.AutoLocator())
    ax.xaxis.set_minor_locator(plt.MultipleLocator(1))

    #ax.yaxis.set_major_locator(plt.LogLocator(base=10.0, numticks=15))

    #ax1 = sns.regplot(x="Year", y="Number of MOF", data=df_number_ofmofs_byyear, truncate=True)
    #ax1.set_yscale("log")

    plt.show()


    #manager = plt.get_current_fig_manager()

    #plt.savefig("number_of_mofs_per_year.jpeg",)

#df_all_mofs_doi_year = pd.read_excel("all_mofs_doi_year_from_web_ofsci.xlsx")
#graph_mofs_byyear_sns(df_all_mofs_doi_year)


def compare_indexed():
    value = "| POAV_cm^3/g"
    label_value = "Surface Area"
    tm = pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/clean_indexed/clean_pv_alphanum_indexed_name.csv")\
            [["MOF_Name_alphnum_indexed", "Value"]]
    dm = pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/mof_mining/result_analysis/dm_mofname_indexed/ours_dm_pv_alphanum_indexed_name.csv")
    df_merge = pd.merge(tm, dm, how="left", left_on="MOF_Name_alphnum_indexed", right_on="MOF_Name_alphnum_indexed")
    df_merge = df_merge[df_merge["MOF_Name_alphnum_indexed"].apply(lambda x: len(x) > 1)]
    df_merge = df_merge.dropna(subset=[value])
    df_merge = df_merge[df_merge["Value"].apply(lambda x: float(x) > 0)]
    df_merge = df_merge[df_merge[value].apply(lambda x: float(x) > 0)]
    df_merge["Value"] = df_merge["Value"].astype(float)

    #df_merge.to_csv("merge_test.csv")
    
    sns.relplot(x=value, y="Value", data=df_merge)
    plt.ylabel("TM %s ($cm_2$/g)" %label_value)
    plt.xlabel("DM %s ($cm_2$/g)" %label_value)


    #values_tm = df_merge["Value"].astype(float)
    #values_dm = df_merge[value].astype(float)

    #fig1 = plt.figure()
    #ax1 = fig1.add_subplot(111)
    #ax1.scatter(values_tm, values_dm)
    ##ax1.set_title("Distributions of H2_UP $H_2$ Uptake (w/W %) bySurface Area ($cm_2$/g)")
    #ax1.set_xlim([0, 10000])
    #ax1.set_ylim([0, 10000])

    #plt.xticks(np.arange(10))

    #ax1.set_yscale("log")
    #ax1.set_xscale('log')

    #ax2 = fig1.add_axes([0.2, 0.5, 0.4, 0.4])
    #ax2.scatter(value_sa, h2_up, alpha=0.7)
    #ax2.set_xlim([5000, 10000])
    #ax2.set_ylim([10, 20])
    #ax2.set_title("Zoom")
    #ax2.set_xscale('log')



    plt.show()
compare_indexed()
