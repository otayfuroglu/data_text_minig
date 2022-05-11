# -*- coding:utf-8 -*-

import pandas as pd
import urllib.request, urllib.parse, urllib.error

import ssl
import requests
from six.moves import urllib

import os
import re

proxies = {'http': 'http://www.someproxy.com:3128'}
urllib.request.ProxyHandler(proxies)


# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def save_to_exel(df, file_name):
	writer = pd.ExcelWriter("%s.xlsx"%file_name, engine='xlsxwriter')
	df.to_excel(writer, sheet_name='Sheet1')
	writer.save()



def get_dois_from_web_of_sci(source_file):
    """to use file of Tab delimted format for windows and file obtained form web of sci"""
    df = pd.read_csv("%s.txt" % source_file, sep='\t', lineterminator='\r')
    dois = (df["AR"])
    return dois


def get_all_dois_from_web_of_sci():
    web_of_sci_all_dois = []
    os.chdir("/home/omert/Desktop/mof_text_minig/get_dois/web_of_sci_all_mof1")

    #for source_file_index in range(1,18): step 1: 83 000 lik data
    for source_file_index in range(1, 27): # step 2: 12400 lik data
        source_file = "web_of_sci_all_mof_%s" % source_file_index

        #all_dois += get_get_doi_1(source_file)


        for doi in get_dois_from_web_of_sci(source_file):
            if ";" in str(doi):
                index = doi.index(";")
                doi = doi[:index]
            if pd.isnull(doi) == False:
                web_of_sci_all_dois.append(doi)

    df_all_dois = pd.DataFrame()
    df_all_dois["DOI"] = web_of_sci_all_dois

    df_all_dois.to_csv("web_of_sci_all_mof_all_year.csv")

    return set(web_of_sci_all_dois)

#get_all_dois_from_web_of_sci()

def compare_dois_web_sci():
    web_of_sci_all_dois = get_all_dois_from_web_of_sci()
    core_all_dois_df = pd.read_csv("structure_doi_CoRE_MOFsV2.0.csv")

    core_all_dois = []
    for core_doi in core_all_dois_df["DOI"]:
        if core_doi != "-":
            core_all_dois.append(core_doi)
            # print(core_doi)

    core_all_dois = set(core_all_dois)  # for unique item

    common_dois1 = []
    non_common_dois1 = []

    for core_doi in core_all_dois:
        if ";" in core_doi:
            index = core_doi.index(";")
            core_doi = core_doi[:index]
        if core_doi in web_of_sci_all_dois:
            common_dois1.append(core_doi)
        else:
            non_common_dois1.append(core_doi)

    df_common_dois1 = pd.DataFrame(common_dois1)
    save_to_exel(df_common_dois1, file_name="common_dois2")

    df_non_common_dois1 = pd.DataFrame(non_common_dois1)
    save_to_exel(df_non_common_dois1, file_name="non_common_dois2")

    percent1 = (len(common_dois1) / len(core_all_dois)) * 100
    print("%2.2f percent" % percent1)

#compare_dois_web_sci()

#web_of_sci()
#source_file = "/home/omert/Desktop/deney_text_mining/web_of_sci_all_mof1/web_of_sci_all_mof_21"
#get_get_doi_1(source_file)



def get_all_dois_from_scopus():
    import os

    all_df = pd.DataFrame()
    os.chdir("/home/omert/Desktop/deney_text_mining/scopus_all_mof")


    for root, dirs, files in os.walk("."):
        for filename in files:
            print(filename)
            df = pd.read_csv("/home/omert/Desktop/deney_text_mining/scopus_all_mof/%s"%filename, low_memory=False)
            #print(df.head())
            all_df = all_df.append(df, sort=False) # add data frame


    #print(all_df.head()["DOI"])
    all_df_doi = all_df["DOI"]
    all_df_doi.to_csv("scopus_all_mof_doi_year_1.csv")


get_all_dois_from_scopus()




def compare_dois_scopus():
    scopus_all_dois = []
    os.chdir("/home/omert/Desktop/deney_text_mining/scopus_all_mof")
    source_file = "scopus_all_mof_all_year.csv"
    #for source_file_index in range(1,18): step 1: 83 000 lik data


    for doi in pd.read_csv(source_file)["DOI"]:
        if ";" in str(doi):
            index = doi.index(";")
            doi = doi[:index]
        if pd.isnull(doi) == False:
            scopus_all_dois.append(doi)

    scopus_all_dois = set(scopus_all_dois)

    core_all_dois_df = pd.read_csv("structure_doi_CoRE_MOFsV2.0.csv")

    core_all_dois = []
    for core_doi in core_all_dois_df["DOI"]:
        if core_doi != "-":
            core_all_dois.append(core_doi)
            #print(core_doi)

    core_all_dois = set(core_all_dois) #for unique item

    common_dois1 = []
    non_common_dois1 = []


    for core_doi in core_all_dois:
        if ";" in core_doi:
            index = core_doi.index(";")
            core_doi = core_doi[:index]
        if core_doi in scopus_all_dois:
            common_dois1.append(core_doi)
        else:
            non_common_dois1.append(core_doi)

    df_common_dois1 = pd.DataFrame(common_dois1)
    save_to_exel(df_common_dois1, file_name="common_dois2")

    df_non_common_dois1 = pd.DataFrame(non_common_dois1)
    save_to_exel(df_non_common_dois1, file_name="non_common_dois2")

    percent1 = (len(common_dois1)/len(core_all_dois))*100
    print("%2.2f percent"%percent1)

#compare_dois_scopus()

def compare_scopus_web_of_sci():
    """Bu fonk.da web of sci ve scopustan elde edilen bütün doiler birleştrilmiştir."""

    scopus_web_of_sci_all_dois = []
    web_of_sci_dir = "/home/omert/Desktop/mof_text_minig/get_dois/web_of_sci_all_mof1"
    web_of_sci_source_file = "%s/web_of_sci_all_mof_all_year.csv"%web_of_sci_dir

    scopus_dir = "/home/omert/Desktop/mof_text_minig/get_dois"
    scopus_source_file = "%s/scopus_all_mof_dois.csv"%scopus_dir

    core_all_dois_df = pd.read_csv("structure_doi_CoRE_MOFsV2.0.csv")

    df_all_dois = pd.read_csv(web_of_sci_source_file).append(pd.read_csv(scopus_source_file)).\
                      append(core_all_dois_df)  #core datadan gelen doileride ekledik

    df_all_dois.to_csv("all_mof_dois.csv")

    for doi in df_all_dois["DOI"]:
        if ";" in str(doi):
            index = doi.index(";")
            doi = doi[:index]
        if pd.isnull(doi) == False:
            scopus_web_of_sci_all_dois.append(doi)


    print(len(scopus_web_of_sci_all_dois))
    scopus_web_of_sci_all_dois = set(scopus_web_of_sci_all_dois)
    print(len(scopus_web_of_sci_all_dois))



    core_all_dois = []
    for core_doi in core_all_dois_df["DOI"]:
        if core_doi != "-":
            core_all_dois.append(core_doi)
            #print(core_doi)

    core_all_dois = set(core_all_dois) #for unique item

    common_dois1 = []
    non_common_dois1 = []


    for core_doi in core_all_dois:
        if ";" in core_doi:
            index = core_doi.index(";")
            core_doi = core_doi[:index]
        if core_doi in scopus_web_of_sci_all_dois:
            common_dois1.append(core_doi)
        else:
            non_common_dois1.append(core_doi)

    df_common_dois1 = pd.DataFrame(common_dois1)
    save_to_exel(df_common_dois1, file_name="common_dois2")

    df_non_common_dois1 = pd.DataFrame(non_common_dois1)
    save_to_exel(df_non_common_dois1, file_name="non_common_dois2")

    percent1 = (len(common_dois1)/len(core_all_dois))*100
    print("%2.2f percent"%percent1)

#compare_scopus_web_of_sci()

def separate_dois():
    all_dois = pd.read_csv("all_mof_dois.csv", low_memory=False)

    os.mkdir("separated_dois")
    os.chdir("separated_dois")

    i = 0
    j = 1

    while i <= len(all_dois["DOI"])+5000:
        all_dois.iloc[i+1:i+5001].to_csv("all_mof_dois_%s.csv" %j)

        i += 5000
        j += 1

#separate_dois()
