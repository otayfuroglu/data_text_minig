# -*- coding:utf-8
from __future__ import print_function # her zaman en başta olmalı
import pandas as pd
import os, sys

#import urllib.request, urllib.parse, urllib.error
#from requests_html import HTMLSession
#import ssl
#import requests
#from six.moves import urllib



from multiprocessing import Pool

def get_doi_from_webofSci_text(source_path, source_file):
    """to use file of Tab delimted format for windows"""
    df = pd.read_csv("%s/%s" % (source_path, source_file), sep="\t", lineterminator="\r")
    dois = (df["AR"])
    return dois

def run_get_doi_from_webofSci_text():
    source_path = "../../in_output/get_lib/webofsciencecorecollection_mof_files"
    source_files = [item for item in os.listdir(source_path,) if "txt" in item]

    ls_all_dois_50000 = []
    for source_file in source_files:
        for doi in get_doi_from_webofSci_text(source_path, source_file):
            ls_all_dois_50000.append(str(doi).replace("\nJ", "").replace(" ", ""))

    df_all_dois_50000 = pd.DataFrame(ls_all_dois_50000, columns=["DOI"]) 
    df_all_dois_50000.to_csv("df_all_dois_50000.csv")

def get_csd_pups_mof_doi():
    pup_mofs = pd.read_csv("df_all_dois_50000.csv")
    pup_mof_dois = pup_mofs.DOI.drop_duplicates()
    csd_mofs = pd.read_csv("/home/modellab/workspace/omer/data_mining_mof/df_mof_refcode_doi_from_search.csv")
    csd_mof_dois = csd_mofs.DOI.drop_duplicates()
    print (len(csd_mof_dois))

    #df_csd_pup_mof_doi = pup_mof_dois.append(csd_mof_dois).drop_duplicates()
    #df_csd_pup_mof_doi = pd.DataFrame(df_csd_pup_mof_doi, columns=["DOI"])
    #df_csd_pup_mof_doi = df_csd_pup_mof_doi.reset_index()
    #df_csd_pup_mof_doi.to_csv("all_csd_pup_mof_doi.csv")

    df_csd_pup_mof_doi = pd.DataFrame(pup_mof_dois.append(csd_mof_dois), columns=["DOI"])
    df_common_csd_pup_mof_doi = pd.DataFrame(df_csd_pup_mof_doi[df_csd_pup_mof_doi.duplicated()], columns=["DOI"])
    #df_common_csd_pup_mof_doi.t_csv("common_csd_pup_mof_doi.csv")

    just_csd_mof_dois = csd_mof_dois[csd_mof_dois.isin(df_common_csd_pup_mof_doi.DOI) == False]
    #just_pup_mof_dois = pup_mof_dois.append(df_common_csd_pup_mof_doi).drop_duplicates()

#get_csd_pups_mof_doi()

def check_saved_file(doi):
    saved_files_path = "/home/modellab/workspace/omer/mof_text_minig/in_output/get_lib/works"

    i = 1
    for path, subdirs, files in os.walk(saved_files_path):  # iç içe klasörledeki bütün dosyaları listeler
        saved_file_names = [item for item in files if "html" in item]
        for saved_file_name in saved_file_names:
            #if i%100 == 0:
            #    print ("%d \r" % i)
            #i += 1
            saved_file_doi = saved_file_name.replace("_s_", "/").replace("_n_", ".") \
                .replace("_p_", "(").replace("_tp_", ")").replace("_ot_", "-").replace(".html", "")
            if doi == saved_file_doi:
                print("Saved File")
                return True

def get_non_downlaod_doi():

    df_csd_pup_mof_dois = pd.read_csv("all_csd_pup_mof_doi.csv")

    saved_files_path = "/home/modellab/workspace/omer/mof_text_minig/in_output/get_lib/all_files"

    pool = Pool(processes=130)
    ls_non_downlaod_dois = pool.map(check_saved_file, list(df_csd_pup_mof_dois["DOI"]))
    pool.close()

    df_non_downlaod_dois = pd.DataFrame(ls_non_downlaod_dois, columns=["DOI"]).dropna()
    df_non_downlaod_dois.to_csv("all_non_downlaod_dois.csv")
#get_non_downlaod_doi()

#all_csd_pup_mof_doi = pd.read_csv("all_csd_pup_mof_doi.csv", index_col=None)
#download_doi = pd.read_csv("all_downlaod_dois.csv", index_col=None) 
#
#non_download_doi =  pd.DataFrame(all_csd_pup_mof_doi[all_csd_pup_mof_doi.DOI.isin(download_doi.DOI) == False], columns=["DOI"]).reset_index()
#non_download_doi.to_csv("all_non_download_doi.csv")

def get_link_acs(doi):
    print (doi)
    try:
        # find to link of pdf file via DOI number from web
        opener = urllib.request.build_opener()
        opener.addheaders = [('Accept', 'application/vnd.crossref.unixsd+xml')]
        r = opener.open("http://dx.doi.org/" + str(doi))
        link = r.info()["Link"].split(";")[1]
        url = link[link.index("<") + 1:-1]

        if "pubs.acs" in url:
            return True
        else:
            return False
    except:
        return False

def check_acs_doi(doi):
    if "acs" in str(doi):
        return True
    else:
        return False

def check_doi(labels, doi):
    doi_categories = pd.DataFrame(columns=labels)

    try:
        # find to link of pdf file via DOI number from web
        opener = urllib.request.build_opener()
        opener.addheaders = [('Accept', 'application/vnd.crossref.unixsd+xml')]
        r = opener.open("http://dx.doi.org/" + str(doi))
        link = r.info()["Link"].split(";")[1]
        url = link[link.index("<") + 1:-1]

        for label in labels[:-2]:
            if label in url:
                doi_categories[label] = [doi]
                return doi_categories
        if doi_categories.empty:
                doi_categories["others"] = [doi]
                return doi_categories
    except:
        #print("Bu dois için link elde edilemiyor !!!")
        doi_categories["couldnt_link"] = [doi]
        return doi_categories

def run_check_acs():
    all_non_download_doi = pd.read_csv("all_non_download_doi.csv")
    df_csd_pup_mof_dois = pd.read_csv("all_csd_pup_mof_doi.csv")
    pool = Pool(50)
    results = pool.map(check_acs_doi, df_csd_pup_mof_dois.DOI)
    acs_dois = pd.DataFrame(df_csd_pup_mof_dois.loc[results].DOI.reset_index(), columns=["DOI"])
    acs_dois.to_csv("all_acs_dois_in65000.csv")

def run_check_all_dois_fromWeb():
    dois = pd.read_csv("./all_non_download_doi.csv")["DOI"].dropna()
    print(len(dois))

    labels =["pubs.acs",
            "pubs.rsc",
            "elsevier",
            "wiley",
            "pnas.",
            "science",
            "tandfonline",
            "springer",
            "others",
            "couldnt_link"]

    #print(check_doi(labels, "10.1039/c8dt01288a"))
    all_doi_categories = pd.DataFrame(columns=labels)
    i = 1
    for doi in dois[:1000]:
        print(i, end="\r")
        sys.stdout.flush()
        i += 1

        doi_categories = check_doi(labels, doi)
        all_doi_categories = all_doi_categories.append(doi_categories)
    all_doi_categories.reset_index(drop=True).to_csv("all_non_download_doi_catagories.csv")

labels =["pubs.acs",
        "pubs.rsc",
        "elsevier",
        "wiley",
        "springer",
        "pnas.",
        "science",
        "tandfonline",
        "others"
        ]

def run_check_all_dois_fromDOIs(labels, df_dois):

    keys = ["10.1021",
            "10.1039",
            "10.1016",
            "10.1002",
            "10.1080",
            "pnas",
            "10.1126",
            "10.1007"]

    dfs = []
    dois_list = []
    for i, key in enumerate(keys):
        #  df = pd.DataFrame(df_dois[df_dois["DOI"].str.contains(key)]["DOI"].to_list(), columns = [labels[i]])
        doi_list = df_dois[df_dois["DOI"].str.contains(key)]["DOI"].to_list()
        dois_list += doi_list
        dfs.append(pd.DataFrame(doi_list, columns=[labels[i]]))

    df_others = df_dois[~df_dois["DOI"].isin(dois_list)]
    dfs.append(pd.DataFrame(df_others["DOI"].to_list(), columns=[labels[-1]]))
    df_all = pd.concat(dfs, axis=1)
    #  all_doi_categories.reset_index(drop=True).to_csv("all_non_download_doi_catagories_fromDOIs_1.csv")
    df_all.to_csv("all_non_download_doi_catagories_fromDOIs_1.csv")


df_dois = pd.read_csv("../../tdm_ml/workspace/non_disordered_doi_justone_refcode_since2019.csv")
print(len(df_dois))
run_check_all_dois_fromDOIs(labels, df_dois)


#all_doi_categories = pd.read_csv("all_non_download_doi_catagories_fromDOIs_1.csv")
#print(len(all_doi_categories))
#for label in labels:
#    print(label, ": ", len(all_doi_categories[label].dropna()))

def count_all_dois_by_pubs(labels):

    all_dois =  pd.read_csv("./all_csd_pup_mof_doi_65000.csv")["DOI"].to_list()
    print(len(all_dois))

    keys = [".1021",
            ".1039",
            ".1016",
            ".1002",
            #".1080",
            #"pnas",
            #".1126",
            #".1007"
           ]
    total = 0
    for i, key in enumerate(keys):
        n_dois = len([doi for doi in all_dois if key in str(doi)])
        total += n_dois
        print(labels[i],":\t", n_dois)
    print("others:\t", len(all_dois) - total)

#count_all_dois_by_pubs(labels)

def get_new_others_dois_from_html_lib():
    """xxxxxx"""
    all_dois =  pd.read_csv("./all_csd_pup_mof_doi_65000.csv")["DOI"].dropna().to_list()
    saved_files = os.listdir("/home/modellab/workspace/omer/mof_text_minig/in_output/get_lib/all_files/tandfonline_lib")
    saved_files = [item for item in saved_files if ".html" in str(item)]

    new_other_dois = []
    for doi in all_dois:
        for saved_file_name in saved_files:
            saved_file_doi = saved_file_name.replace("_s_", "/").replace("_n_", ".") \
                .replace("_p_", "(").replace("_tp_", ")").replace(
                "_ot_", "-").replace(".pdf", "").replace(".html", "")
            if str(doi).lower() in str(saved_file_doi).lower():
                new_other_dois.append(doi)
    df = pd.DataFrame(columns=["DOI"])
    df["DOI"] = new_other_dois
    df.to_csv("new_tandfonline_dois_just_html.csv")

#get_new_others_dois_from_html_lib()

#  tandfonline_dois = pd.concat([pd.read_csv("../../in_output/sa_pv/mof_mining/tandfonline_lib_SA_extract.csv")["DOI"],
#          pd.read_csv("../../in_output/sa_pv/mof_mining/tandfonline_lib_SA_extract.csv")["DOI"]], ignore_index=True).drop_duplicates()
#  core_dois = pd.read_csv("./core_database_dois.csv")
#  for tandfonline_doi in tandfonline_dois:
#      #print(tandfonline_doi)
#      for core_doi in core_dois:
#          if tandfonline_doi in core_doi:
#              print(tandfonline_doi)
