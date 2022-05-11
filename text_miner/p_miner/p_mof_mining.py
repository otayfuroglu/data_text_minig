# -*- coding:utf-8 -*-

import pandas as pd
import os
import re

from multiprocessing import Pool
from itertools import product

from sa_extract_p import sa_core
from pv_extract_p import pv_core

def replace(fin_name, srcStr, desStr, fout_name):
    fin = open(fin_name, "r")
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
    file_name = file_name.replace(".html", "")
    if ")" in file_name or "(" in file_name:
        print ("Dosya ismi ( içerdiği için işleme alınmdı !!")
    else:
        os.system("mv %s/%s.html %s/%s.pdf" % (html_dir, file_name, html_dir, file_name))
        os.system("pdftotext %s/%s.pdf" % (html_dir, file_name))
        os.system("mv %s/%s.txt %s/%s.html" % (html_dir, file_name, html_dir, file_name))
        print ("Çevrildi :)")

def doi_match(all_doi_path, file_name, i):
    """doilerin tekrar elde edilmesi için doiler ve file name leri eşleştiriyor
	ve o file name ait doi yi buluyor"""
    dois = pd.read_csv("%s/all_mof_dois_%s.csv" % (all_doi_path, i))["DOI"]
    base = file_name.replace(".html", "")

    for doi in dois:
        if base == doi.replace("/", "").replace(".", ""):
            return doi


def paral_by_fname(file_name, html_dir, i):
    """xxxxxxxxxxxxxx"""

    print (file_name)

    pid = os.getpid()
    work_dir = os.getcwd()
    temp_dirs = [item for item in os.listdir(work_dir) if "temp_" in item]

    if not "temp_%s" %pid in temp_dirs:
        os.mkdir("temp_%s" %pid)

    temp_dir = "%s/temp_%s" %(work_dir, pid)
    all_doi_path = "/home/omert/Desktop/mof_text_minig/get_dois/separated_dois"

    try:
        nw_doi = doi_match(all_doi_path, file_name, i)  # ilk 20,000 lik data için doilerin tekrar elde edilmesi için düzeltme yaptık
        if nw_doi:
            doi = nw_doi
        else:
            doi = file_name.replace(".html", "")

        url = "http://dx.doi.org/" + str(doi)



        try:
            replace("%s/%s" % (html_dir, file_name), ">\d+\w*[</\w+>]*</a>", "></\w+></a>", "%s/temp.html" % temp_dir); \
                    replace("%s/%s" % (html_dir, file_name), ">\d+\w*[</\w+>]*</a>", "></\w+></a>",
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
            
            Ayrıca yeri gelmişken, elsevier den çekilen dosyalarda .text formatında olduğundan aynı verimsizlik 
            bu dosyalar üzerinde de olabilir"""

            replace("%s/%s" % (html_dir, file_name), ">\d+\w*[</\w+>]*</a>", "></\w+></a>", "%s/temp.html" % temp_dir); \
                    replace("%s/%s" % (html_dir, file_name), ">\d+\w*[</\w+>]*</a>", "></\w+></a>",
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

    except:
        print ("Genel bir hata var! Diğer dosyaya geçtik !!!")
        fl3 = open("err_general.log", "a")
        fl3.write("%s\n" % file_name)
        fl3.close()

        data_sa = None
        data_pv = None

    return data_sa, data_pv


def run_paral1(n_proc):
    """xxxxxxx"""

    all_data_sa = []
    all_data_pv = []

    path = "/home/omert/Downloads/mof_lib"

    directorys = [item for item in os.listdir(path) if "5000_" in item and not "." in item]

    for directory in directorys:
        # data yı 5000 lik dosyalara ayırdığımız için burda 5000 lik döngüler oluşturduk
        data_5000_sa = pd.DataFrame()
        data_5000_pv = pd.DataFrame()

        lib_dirs = [item for item in os.listdir("%s/%s" % (path, directory)) if not "." in item]
        i = directory.replace("_5000_files", "")

        for lib_dir in lib_dirs:

            html_dir = ["%s/%s/%s" % (path, directory, lib_dir)] #starmap 'te tek bir öğe olsı için list yaptık
            file_names = [f for f in os.listdir(html_dir[0]) if ".html" in f]

            if len(file_names) != 0:
                with Pool(processes=n_proc) as pool:
                    results = pool.starmap(paral_by_fname, product(file_names, html_dir, i))
                pool.close()

                for result in results:

                    data_5000_sa = data_5000_sa.append(result[0])
                    data_5000_pv = data_5000_pv.append(result[1])

        keyword = "%s_5000" % i
        save_to_exel(data_5000_sa, file_name="%s_SA_extract_paral" % keyword)
        save_to_exel(data_5000_pv, file_name="%s_PV_extract_paral" % keyword)

    #bütün datayı tek frame topluyoruz
        all_data_sa.append(data_5000_sa)
        all_data_pv.append(data_5000_pv)
    all_data_sa = pd.concat(all_data_sa)
    all_data_pv = pd.concat(all_data_pv)

    save_to_exel(all_data_sa, file_name="all_MOF_SA_extract_paral")
    save_to_exel(all_data_pv, file_name="all_MOF_PV_extract_paral")

    import shutil
    work_dir = os.getcwd()
    for item in os.listdir(work_dir):
        if "temp_" in item:
            shutil.rmtree(item)


run_paral1(n_proc=4)

