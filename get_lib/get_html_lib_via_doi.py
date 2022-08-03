#! /usr/bin/python3.6
# -*- coding:utf-8 -*-

from __future__ import print_function # her zaman en başta olmalı
import pandas as pd
import numpy as np
import urllib.request, urllib.parse, urllib.error
from requests_html import HTMLSession
import ssl
import requests
from six.moves import urllib

from selenium import webdriver

import os, sys
import time
#  from multiprocessing import Pool

proxies = {'http': 'http://www.someproxy.com:3128'}
urllib.request.ProxyHandler(proxies)

session = HTMLSession()

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def get_doi_from_csv(source_file):
    """to use file of csv, return list of doi"""
    df = pd.read_csv(source_file, low_memory=False)
    dois = df["DOI"].to_list()
    return dois


def get_link(doi):
    # find to link of pdf file via DOI number from web
    opener = urllib.request.build_opener()
    opener.addheaders = [('Accept', 'application/vnd.crossref.unixsd+xml')]
    # r = opener.open('http://dx.doi.org/10.1016/j.aca.2018.04.033')
    # r = opener.open("http://dx.doi.org/10.1039/C5SC03620H")
    # r = opener.open('http://dx.doi.org/10.1021/cg400096e')
    r = opener.open("http://dx.doi.org/" + str(doi))

    #  for link in r.info()["Link"].split(";"):
    #      if "http://" in link and\
    links =  [link[link.index("<") + 1:-1]
              for link in r.info()["Link"].split(";")
              if "http://" in link and ("html" in link or "xml" in link)]
    url = [link for link in links if "html" in link]
    if len(url) == 1:
        return url[0], "html"
    else:
        url = [link for link in links if "xml" in link]
        if len(url) == 1:
            return url[0], "xml"
        else:
            url = [link for link in links if "pdf" in link]
            if len(url) == 1:
                return url[0], "pdf"

            else:
                link = r.info()["Link"].split(";")[1]
                return link[link.index("<") + 1:-1], "html"

    # print (url)
    #  return url

#  print(get_link("10.3390/scipharm86010009"))


def save_html(url, html_dir, file_name):
    # Basic http file downloading from net and saving to disk in python
    save_html = urllib.request.URLopener()
    save_html.retrieve(url, "%s/%s.html" % (html_dir, file_name))


def save_html_1(url, html_dir, file_name, file_format):
    r = requests.get(url, stream=True)
    with open("%s/%s.%s" % (html_dir, file_name, file_format), "wb") as html_f:
        for chunk in r.iter_content(chunk_size=1024):

            # writing one chunk at a time to html file
            if chunk:
                html_f.write(chunk)
    html_f.close()


def save_html_wiley(doi, html_dir, file_name, file_format):
    headers = {
        "Wiley-TDM-Client-Token":"7979990b-23e2-4636-a82e-a6d9b3691cea"
    }
    doi = "%2F".join(doi.split("/"))
    url = "https://api.wiley.com/onlinelibrary/tdm/v1/articles/" + doi
    r = requests.get(url, stream=True, headers=headers)
    with open("%s/%s.%s" % (html_dir, file_name, file_format), "wb") as html_f:
        for chunk in r.iter_content(chunk_size=1024):

            # writing one chunk at a time to html file
            if chunk:
                html_f.write(chunk)
    html_f.close()


def save_html_2(url, html_dir, file_name, file_format):
    driver = webdriver.Firefox()
    driver.get(url)

    html_source = driver.page_source
    # print(html_source)

    html_f = open("%s/%s.%s" % (html_dir, file_name, file_format), "w")
    html_f.write(html_source)
    html_f.close()
    driver.quit()


def save_html_3(url, html_dir, file_name, file_format):
    r = session.get(url, headers={"User-Agent": "TDMCrawler"})
    open("%s/%s.html" % (html_dir, file_name), "wb").write(r.content)


def save_to_exel(df, file_name):
    writer = pd.ExcelWriter("%s.xlsx" % file_name, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()


def check_saved_file(doi, saved_files_dir):
    """xxxxxx"""
    for path, subdirs, files in os.walk(saved_files_dir):  # iç içe klasörledeki bütün dosyaları listeler
        for saved_file_name in files:
            saved_file_doi = saved_file_name.replace("_s_", "/").replace("_n_", ".") \
                .replace("_p_", "(").replace("_tp_", ")").replace(
                "_ot_", "-")
            if doi.lower() in saved_file_doi.lower():
                print("Bu doi'ye ait paper daha önce kaydedilmiş! Atladık :)")
                return True


def dois_match(doi_1, dois):
    for doi_2 in dois:
        if str(doi_1) == str(doi_2):
            return True


def run_get_html_lib():
    """xxxxx"""

    BASE_DIR = "/home/omert/Desktop/data_text_minig/"
    doi_source_file = f"{BASE_DIR}/works/all_non_download_doi_catagories_fromDOIs_1.csv"
    saved_files_dir = f"{BASE_DIR}/works/html_lib"
    all_doi_categories = pd.read_csv(doi_source_file, low_memory=False)

    acs_dois = all_doi_categories["pubs.acs"].dropna().to_list()
    rsc_dois = all_doi_categories["pubs.rsc"].dropna().to_list()
    elsevier_dois = all_doi_categories["elsevier"].dropna().to_list()
    wiley_dois = all_doi_categories["wiley"].dropna().to_list()
    science_dois = all_doi_categories["science"].dropna().to_list()
    pnas_dois = all_doi_categories["pnas."].dropna().to_list()
    tandfonline_dois = all_doi_categories["tandfonline"].dropna().to_list()
    springer_dois = all_doi_categories["springer"].dropna().to_list()
    others_dois = all_doi_categories["others"].dropna().to_list()
    publisher_list = [acs_dois, rsc_dois, elsevier_dois, wiley_dois,
                      others_dois, science_dois, pnas_dois, tandfonline_dois, springer_dois]
    # workdir = os.getcwd()
    output_dir = f"{BASE_DIR}/works/html_lib"

    try:
        os.mkdir(output_dir)
    except:
        print("Bütün klasorler önceden oluşturulmuş!")

    main_dir = output_dir
    acs_dir = "%s/acs_lib" % main_dir
    rsc_dir = "%s/rsc_lib" % main_dir
    elsevier_dir = "%s/elsevier_lib" % main_dir
    wiley_dir = "%s/wiley_lib" % main_dir
    science_pnas_dir = "%s/science_pnas_lib" % main_dir
    tandfonline_dir = "%s/tandfonline_lib" % main_dir
    springer_dir = "%s/springer_lib" % main_dir
    others_dir = "%s/others_lib" % main_dir

    try:
        os.mkdir(acs_dir)
        os.mkdir(rsc_dir)
        os.mkdir(elsevier_dir)
        os.mkdir(wiley_dir)
        os.mkdir(science_pnas_dir)
        os.mkdir(tandfonline_dir)
        os.mkdir(springer_dir)
        os.mkdir(others_dir)
    except:
        print("Bütün klasorler önceden oluşturulmuş!")

    couldnt_get_dois = open("%s/couldnt_get_dois.csv" %output_dir, "w")
    couldnt_get_dois.write("DOI\n")
    couldnt_get_dois.close()
    list_couldnt_get_dois = pd.read_csv("%s/couldnt_get_dois.csv" %output_dir)["DOI"].to_list()


    counter = 1
    previus_ind = 0
    for i in range(len(all_doi_categories)):
        #ind = i%len(publisher_list)

        # indeksi rastgele elde ediyor
        ind = np.random.randint(0, len(publisher_list))
        if ind == previus_ind:
            ind -= 1
        previus_ind = ind

        # ençok doi elsevierden olduğu için, elsevierde doi kalmadığında çekmeyi bitirir
        if len(elsevier_dois) == 0:
            break
        if len(publisher_list[ind]) == 0:
            continue

        doi = publisher_list[ind].pop()

        if check_saved_file(doi, saved_files_dir):
            continue
        if dois_match(doi, list_couldnt_get_dois):
            print("Doi match !!!")
            continue
        try:
            url, file_format = get_link(doi)
        except:
            couldnt_get_dois = open("%s/couldnt_get_dois.csv" %output_dir, "a")
            couldnt_get_dois.write("%s\n" %doi)
            couldnt_get_dois.close()
            print("Couldn't get link, May be your Pc is offline or DOI is wrong !!!")
            continue

        if url:
            #print(url)
            #print("%s yayın evinden, %d. DOI 'ye ait yayın indiriliyor ..." %(all_doi_categories.columns[ind+1],
            #                                                                    counter), end="\r")
            print("%s yayın evinden, %d. DOI 'ye ait yayın indiriliyor ..." %([
                "acs_dois",
                "rsc_dois",
                "elsevier_dois",
                "wiley_dois",
                "others_dois",
                "science_dois",
                "pnas_dois",
                "tandfonline_dois",
                "springer_dois"][ind], counter), end="\r")
            sys.stdout.flush()

            counter += 1
            #os.system("find %s/%s_files -type f | wc -l" % (output_dir, "1111")) + 1

            file_name = doi.replace("/", "_s_").replace(".", "_n_") \
                .replace("(", "_p_").replace(")", "_tp_").replace(
                "-", "_ot_")
            try:
                if "pubs.acs" in url:
                    continue
                    url = url.replace("http", "https").replace("pdf", "full")
                    html_dir = acs_dir
                    try:
                        save_html_1(url, html_dir, file_name, file_format="html")
                    except:
                        save_html_3(url, html_dir, file_name, file_format="html")
                elif "pubs.rsc" in url:
                    url = url.replace("articlepdf", "articlehtml")
                    html_dir = rsc_dir
                    save_html_3(url, html_dir, file_name, file_format="html")  # for pubs.rsc
                elif "elsevier" in url:
                    url = "%s&APIKey=e1ea5763a46ff62efee36df6f6a5da04" % url
                    html_dir = elsevier_dir
                    save_html_1(url, html_dir, file_name, file_format="xml")
                elif "wiley" in url:
                    html_dir = wiley_dir
                    save_html_wiley(doi, html_dir, file_name, file_format="pdf")
                elif "pnas." in url:
                    html_dir = science_pnas_dir
                    url = "http://dx.doi.org/" + str(doi)
                    save_html_2(url, html_dir, file_name, file_format)
                elif "science" in url:
                    html_dir = science_pnas_dir
                    url = "http://dx.doi.org/" + str(doi)
                    save_html_2(url, html_dir, file_name, file_format)
                elif "tandfonline" in url:
                    url = "https://www.tandfonline.com/doi/full/%s" % doi
                    html_dir = tandfonline_dir
                    save_html_1(url, html_dir, file_name, file_format)
                elif "springer" in url:
                    html_dir = springer_dir
                    save_html_1(url, html_dir, file_name, file_format)
                else:
                    html_dir = others_dir
                    save_html_1(url, html_dir, file_name, file_format)

            except:
                print("%s icin html formatında kayıt yapılamadı" % file_name)

            sleep_time = np.random.uniform(9, 19)
            time.sleep(sleep_time)

run_get_html_lib()
