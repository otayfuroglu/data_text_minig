# -*- coding:utf-8 -*-

import pandas as pd
import os
import re

from h2_up_extract_v1 import h2_up_core
from sa_extract import sa_core

#import nltk
#nltk.download('wordnet')

def replace(fin_name, srcStr, desStr, fout_name):
    fin = open(fin_name, "r")
    fout = open(fout_name, "w")
    txt = fin.read()
    txtout = re.sub(srcStr, desStr, txt)

    fout.write(txtout)
    fin.close()
    fout.close()

def get_dataFrame(file_name, doi, Total_DATA):
    identifies = [file_name, doi]
    labels = ["MOF Name", "Type", "Value", "Unit", "File_Name", "DOI"]
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
	if ")" or "(" in file_name:
		print ("Dosya ismi ( içerdiği için işleme alınmdı !!")
	else:
		os.system("mv %s/%s.html %s/%s.pdf" % (html_dir, file_name, html_dir, file_name))
		os.system("pdftotext %s/%s.pdf" % (html_dir, file_name))
		os.system("mv %s/%s.txt %s/%s.html" % (html_dir, file_name, html_dir, file_name))

def doi_match(all_doi_path, file_name, i):
    """doilerin tekrar elde edilmesi için doiler ve file name leri eşleştiriyor
	ve o file name ait doi yi buluyor"""
    dois = pd.read_csv("%s/all_mof_dois_%s.csv" % (all_doi_path, i))["DOI"]
    base = file_name.replace(".html", "")

    for doi in dois:
        if base == doi.replace("/", "").replace(".", ""):
            return doi

def run():
    """xxxxx"""

    all_data_h2_up = pd.DataFrame()

    path = "/home/modellab/workspace/omer/mof_text_minig/in_output/get_lib/test_h2_up/"

    # list_dir = os.listdir("%s/%s" %(path, directory))
    list_dir = [item for item in os.listdir("%s" %path) if not "." in item]
    print(list_dir)

    for directory in list_dir:
        print(directory)
        html_dir = "%s/%s" %(path, directory)
        file_names = [f for f in os.listdir(html_dir) if ".html" in f]

        if len(file_names) != 0:
            for file_name in file_names[:]:
                print (file_name)
                doi = file_name.replace("_s_", "/").replace("_n_", ".") \
                        .replace("_p_", "(").replace("_tp_", ")").replace("_ot_", "-").replace(".html", "")

            #try:
                try:
                    replace("%s/%s" % (html_dir, file_name), ">\d+\w*[</\w+>]*</a>", "></\w+></a>", "temp.html")
                    html_doc_h2_up = open("temp.html", encoding="UTF-8")  # kaydedilen dosyadan elde edilen içerik (orjinal kodun kullandigi format)

                except:
                    print ("%s isimli dosya okunamadı .html fromatına çevriliyor" % file_name)
                    fl2 = open("err_non_read.log", "a")
                    fl2.write("%s\n" % file_name)
                    fl2.close()

                    pdf2html_1(file_name, html_dir)  # pdf ten html fromatına çevirdik

                    replace("%s/%s" % (html_dir, file_name), ">\d+\w*[</\w+>]*</a>", "></\w+></a>", "temp.html")
                    html_doc_h2_up = open("temp.html", encoding="UTF-8")  # kaydedilen dosyadan elde edilen içerik (orjinal kodun kullandigi format)

                #try:
                Total_DATA_h2_up = h2_up_core(html_doc_h2_up)
                # print ("\nMOF list\n", MOF_list)
                # print("\nTotal_DATA\n", Total_DATA)
                # print ("\nType_total\n", Type_total)
                # print ("\nlist total\n", value_list_total)
                all_data_h2_up = all_data_h2_up.append(get_dataFrame(file_name, doi, Total_DATA_h2_up))

                #except Exception:
                #    print("%s icin rirseyler ters gidiyor" % file_name)
                #    fl1 = open("err_non_mining.log", "a")
                #    fl1.write("%s\n" % file_name)
                #    fl1.close()
            #except:
            #    print ("Genel bir hata var! Diğer dosyaya geçtik !!!")
            #    fl3 = open("err_general.log", "a")
            #    fl3.write("%s\n" % file_name)
            #    fl3.close()

    save_to_exel(all_data_h2_up, file_name="all_data_h2_up_extract")

run()
