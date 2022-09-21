# -*- coding:utf-8 -*-
from __future__ import print_function # her zaman en başta olmalı
import pandas as pd
import os, sys
import re
import shutil
import tqdm

import nltk
nltk.download('wordnet')
nltk.download('omw-1.4')

from multiprocessing import Pool
from itertools import product

from sa_extract_p import sa_core
from pv_extract_p import pv_core

def replace(file_name, srcStr, desStr, fout_name):
    fin = open(file_name, "r")
    fout = open(fout_name, "w")
    txt = fin.read()
    txtout = re.sub(srcStr, desStr, txt)

    fout.write(txtout)
    fin.close()
    fout.close()

def get_dataFrame(file_name, url, doi, Total_DATA):
    identifies = [file_name, url, doi]
    labels = ["MOF Name", "Type", "Value", "Unit", "File_Name", "Link", "DOI"]
    Total_DATA = [tuple(item + identifies) for item in
                  Total_DATA]  # her biri için tanımları ekledik ve pandas data icin listeyi tuple a cevirdik

    # print labels
    # print (Total_DATA)

    df = pd.DataFrame.from_records(Total_DATA, columns=labels)
    return df

def save_to_exel(df, file_name):
    writer = pd.ExcelWriter("%s.xlsx" % file_name, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()
    writer.close()

def pdf2html(file_name, html_dir):
    """xxxxx"""
    try:
        # içerisinde ( ve ya ) olan  file nameden kaynaklı hataları düzelltmek için ekledik
        if ")" in file_name:
            file_name = file_name.replace(")", "\)")  # bash in okuyabilmesi için meta karaktere dönüştürdük
        if "(" in file_name:

            file_name_0 = file_name.replace("(", "\(").replace(".html", "")
            file_name_1 = file_name_0.replace("\(", "").replace("\)", "").replace(".html", "")

            os.system("mv %s/%s.html %s/%s.pdf" % (html_dir, file_name_0, html_dir, file_name_1))
            os.system("pdftotext %s/%s.pdf" % (html_dir, file_name_1))
            os.system("mv %s/%s.txt %s/%s.html" % (html_dir, file_name_1, html_dir, file_name_1))
            file_name = "%s.html" % file_name_1

        else:
            file_name = file_name.replace(".html", "")
            os.system("mv %s/%s.html %s/%s.pdf" % (html_dir, file_name, html_dir, file_name))
            os.system("pdftotext %s/%s.pdf" % (html_dir, file_name))
            os.system("mv %s/%s.txt %s/%s.html" % (html_dir, file_name, html_dir, file_name))
            file_name = "%s.html" % file_name
    except:
        print ("%s isimli dosya .html formatına çevrilemedi" % file_name)

    return file_name

def pdf2html_1(file_name, html_dir):
    """xxxxxxxxx"""
    if ")" in file_name or "(" in file_name:
        print ("Dosya ismi ( içerdiği için işleme alınmadı !!")
    else:
        if ".pdf" in file_name:
            file_name = file_name.replace(".pdf", "")
            os.system("pdftotext %s/%s.pdf" % (html_dir, file_name))
            os.system("mv %s/%s.txt %s/%s.html" % (html_dir, file_name, html_dir, file_name))
            print ("Çevrildi :)")
        else:
            file_name = file_name.replace(".html", "").replace(".pdf", "").replace(".xml", "")
            os.system("mv %s/%s.html %s/%s.pdf" % (html_dir, file_name, html_dir, file_name))
            os.system("pdftotext %s/%s.pdf" % (html_dir, file_name))
            os.system("mv %s/%s.txt %s/%s.html" % (html_dir, file_name, html_dir, file_name))
            print ("Çevrildi :)")

def paral_by_fname(file_name):
    """xxxxxxxxxxxxxx"""

    #!!!Duzelt!!!
    #  puplisher = html_dir.split("/")[-1]
    #  file_names = os.listdir(html_dir)
    #  i = file_names.index(file_name)
    #  print ("%s taranıyor...  %.2f tamamlandı." %(puplisher, 100*i/len(file_names)), end="\r")
    #  sys.stdout.flush()
    #!!!!!

    pid = os.getpid()
    work_dir = os.getcwd()
    temp_dirs = [item for item in os.listdir(work_dir) if "temp_" in item]

    if not "temp_%s" %pid in temp_dirs:
        os.mkdir("temp_%s" %pid)

    temp_dir = "%s/temp_%s" %(work_dir, pid)

    doi = file_name.replace("_s_", "/").replace("_n_", ".") \
            .replace("_p_", "(").replace("_tp_", ")").replace("_ot_", "-") \
            .replace(".html", "").replace(".pdf", "").replace(".xml", "")

    #  try:
    url = "http://dx.doi.org/" + str(doi)

    try:
        replace("%s/%s" % (html_dir, file_name.replace(".pdf", ".html")),
                r">\d+\\w*[</\\w+>]*</a>", r"></\\w+></a>", "%s/temp.html" % temp_dir); \
                replace("%s/%s" % (html_dir, file_name.replace(".pdf", ".html")),
                        r">\d+\\w*[</\\w+>]*</a>", r"></\\w+></a>",
                        "%s/temp2.html" % temp_dir)
        html_doc_sa = open("%s/temp.html" %temp_dir, encoding="UTF-8")  # kaydedilen dosyadan elde edilen içerik (orjinal kodun kullandigi format)
        html_doc_pv = open("%s/temp2.html" %temp_dir, encoding="UTF-8")

    except:
        print ("%s isimli dosya okunamadı .html fromatına çevriliyor" % file_name)
        fl2 = open("err_non_read.log", "a")
        fl2.write("%s\n" % file_name)
        fl2.close()

        pdf2html_1(file_name, html_dir)  # pdf ten html fromatına çevirdik
        """NOT!!! bu şekilde text formatı üzerinden .html formatına çeverilen dosyalar üzerinde
        sa_core ve pv_core fonk.ları verimli sonuç  alamıyor !!!. orjinal html dosyaların elde edilmesi gerekmekte !!!
        Ayrıca yeri gelmişken, elsevier den çekilen dosyalarda .text formatında olduğundan ayn verimsizlik
        bu dosyalar üzerinde de olabilir"""

        file_name = file_name.replace(".pdf", ".html")
        replace("%s/%s" % (html_dir, file_name.replace(".pdf", ".html")), r">\d+\\w*[</\\w+>]*</a>", r"></\\w+></a>", "%s/temp.html" % temp_dir); \
                replace("%s/%s" % (html_dir, file_name), r">\d+\\w*[</\\w+>]*</a>", r"></\\w+></a>",
                        "%s/temp2.html" % temp_dir)
        html_doc_sa = open("%s/temp.html" %temp_dir, encoding="UTF-8")  # kaydedilen dosyadan elde edilen içerik (orjinal kodun kullandigi format)
        html_doc_pv = open("%s/temp2.html" %temp_dir, encoding="UTF-8")

    try:
        Total_DATA_sa = sa_core(html_doc_sa, temp_dir)
        Total_DATA_pv = pv_core(html_doc_pv, temp_dir)
        # print ("\nMOF list\n", MOF_list)
        # print("\nTotal_DATA\n", Total_DATA)
        # print ("\nType_total\n", Type_total)
        # print ("\nlist total\
        data_sa = get_dataFrame(file_name, url, doi, Total_DATA_sa)
        data_pv = get_dataFrame(file_name, url, doi, Total_DATA_pv)

    except Exception:
        print("%s icin rirseyler ters gidiyor" % file_name)
        fl1 = open("err_non_mining.log", "a")
        fl1.write("%s\n" % file_name)
        fl1.close()

        data_sa = None
        data_pv = None

    #  except:
    #      print ("Genel bir hata var! Diğer dosyaya geçtik !!!")
    #      fl3 = open("err_general.log", "a")
    #      fl3.write("%s\n" % file_name)
    #      fl3.close()

        data_sa = None
        data_pv = None

    return data_sa, data_pv

if __name__ == "__main__":

    num_processes = 4

    all_data_sa = []
    all_data_pv = []

    path = "/home/omert/Desktop/data_text_minig/works/html_lib"

    lib_dirs = [item for item in os.listdir(path) if not "." in item]
    done_publishers = [f.replace("_SA_extract.csv", "") for f in os.listdir(os.getcwd()) if "SA_extract.csv" in f]

    for lib_dir in lib_dirs:
        html_dir = "%s/%s" % (path, lib_dir)
        puplisher = html_dir.split("/")[-1]
        file_names = os.listdir(html_dir)

        lib_dir_data_sa = pd.DataFrame()
        lib_dir_data_pv = pd.DataFrame()

        if len(file_names) == 0:
            continue
        if lib_dir in done_publishers:
            continue

        # implementation of  multiprocessor in tqdm.
        # Ref.https://leimao.github.io/blog/Python-tqdm-Multiprocessing/
        pool = Pool(processes=num_processes)
        for result in tqdm.tqdm(pool.imap_unordered(paral_by_fname, file_names),
                                desc=f"Mining {puplisher} papers..",
                                total=len(file_names)):
            lib_dir_data_sa = lib_dir_data_sa.append(result[0])
            lib_dir_data_pv = lib_dir_data_pv.append(result[1])
        pool.close()

        lib_dir_data_sa.to_csv("%s_SA_extract.csv" %lib_dir)
        lib_dir_data_pv.to_csv("%s_PV_extract.csv" %lib_dir)

        all_data_sa.append(lib_dir_data_sa)
        all_data_pv.append(lib_dir_data_pv)

    all_data_sa = pd.concat(all_data_sa)
    all_data_pv = pd.concat(all_data_pv)

    all_data_sa.to_csv("all_SA_extract.csv")
    all_data_pv.to_csv("all_PV_extract.csv")

    work_dir = os.getcwd()
    for item in os.listdir(os.getcwd()):
        if "temp_" in item:
            shutil.rmtree(item)


