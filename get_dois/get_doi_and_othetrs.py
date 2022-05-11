# -*- coding:utf-8 -*-

import pandas as pd
import os

def save_to_exel(df, file_name):
	writer = pd.ExcelWriter("%s.xlsx"%file_name, engine='xlsxwriter')
	df.to_excel(writer, sheet_name='Sheet1')
	writer.save()

def get_all_mofs_doi_year_from_web_ofsci_scopus(path_output):
    i = 1
    df_mofs_web_ofsci = []
    while i <= 26:
        fl = "/home/omert/Desktop/mof_text_minig/in_output/get_dois/web_of_sci_all_mof1/web_of_sci_all_mof_%s" %i

        df_mof = pd.read_csv("%s.txt" %fl, sep='\t', lineterminator='\r')
        df_mofs_web_ofsci.append(df_mof)
        i += 1

    df_mofs_web_ofsci = pd.concat(df_mofs_web_ofsci)
    df_mofs_scopus = pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/get_dois/scopus_all_mof_all_year_1.csv", low_memory=False)

    df_mofs_web_ofsci_doi_year = df_mofs_web_ofsci[["AR", "PD"]]
    df_mofs_web_ofsci_doi_year = df_mofs_web_ofsci_doi_year.rename(columns={"AR": "DOI"})
    df_mofs_web_ofsci_doi_year = df_mofs_web_ofsci_doi_year.rename(columns={"PD": "Year"})

    df_mofs_scopus_doi_year = df_mofs_scopus[["DOI", "Year"]]


    df_all_mofs_doi_year = pd.concat([df_mofs_web_ofsci_doi_year, df_mofs_scopus_doi_year])

    df_all_mofs_doi_year = df_all_mofs_doi_year.drop_duplicates()

    #save_to_exel(df_mofs_web_ofsci, "%s/df_mofs_web_ofsci" % path_output)
    return df_all_mofs_doi_year


def get_all_mofs_doi_and_orhers_from_web_ofsci_scopus(path_output):
    i = 1
    df_mofs_web_ofsci = []
    while i <= 26:
        fl = "/home/omert/Desktop/mof_text_minig/in_output/get_dois/web_of_sci_all_mof1/web_of_sci_all_mof_%s" %i

        df_mof = pd.read_csv("%s.txt" %fl, sep='\t', lineterminator='\r')
        df_mofs_web_ofsci.append(df_mof)
        i += 1

    df_mofs_web_ofsci = pd.concat(df_mofs_web_ofsci)
    df_mofs_scopus = pd.read_csv("/home/omert/Desktop/mof_text_minig/in_output/get_dois/scopus_all_mof_all_year_1.csv", low_memory=False)

    # "Authors" "Title" "Publisher" "DOI", "Year"
    df_mofs_web_ofsci_doi_and_orhers = df_mofs_web_ofsci[["PT", "Z2", "Z3", "AR", "PD"]]
    fix_web_ofsci_doi_name = {"PT": "Authors", "Z2": "Title", "Z3": "Publisher", "AR": "DOI", "PD": "Years"}

    for i in range(len(list(fix_web_ofsci_doi_name))):
        df_mofs_web_ofsci_doi_and_orhers = df_mofs_web_ofsci_doi_and_orhers.rename(
            columns={list(fix_web_ofsci_doi_name.keys())[i]: list(fix_web_ofsci_doi_name.values())[i]})


    df_mofs_scopus_doi_and_orhers = df_mofs_scopus[["Authors", "Title", "Source title", "DOI", "Year"]]
    df_mofs_scopus_doi_and_orhers = df_mofs_scopus_doi_and_orhers.rename(columns={"Source title":"Publisher"})


    df_all_mofs_doi_and_orhers = pd.concat([df_mofs_web_ofsci_doi_and_orhers, df_mofs_scopus_doi_and_orhers], sort=True)
    df_all_mofs_doi_and_orhers = df_all_mofs_doi_and_orhers.drop_duplicates().reset_index(drop=True)

    unique_dois = df_all_mofs_doi_and_orhers["DOI"].drop_duplicates().reset_index(drop=True)
    print(len(unique_dois))

    #save_to_exel(unique_dois, "%s/unique_dois" % path_output)
    #return df_all_mofs_doi_and_orhers

path_output = "/home/omert/Desktop/mof_text_minig/in_output/"+str((os.getcwd().split("/")[-1]))
get_all_mofs_doi_and_orhers_from_web_ofsci_scopus(path_output)


def separate_dois():

    input_path = "/home/omert/Desktop/mof_text_minig/in_output/get_dois"
    all_dois = pd.read_excel("%s/unique_dois.xlsx"%input_path) #low_memory=False)

    os.mkdir("%s/unique_separated_dois"%input_path)
    os.chdir("%s/unique_separated_dois"%input_path)

    i = 0
    j = 1

    while i <= len(all_dois["DOI"])+5000:
        all_dois.iloc[i+1:i+5001].to_csv("all_mof_dois_%s.csv" %j)

        i += 5000
        j += 1

#separate_dois()