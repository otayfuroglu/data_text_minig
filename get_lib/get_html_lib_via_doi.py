# -*- coding:utf-8 -*-

import pandas as pd
import urllib.request, urllib.parse, urllib.error
from requests_html import HTMLSession
import ssl
import requests
from six.moves import urllib

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

import os
import re
import time

proxies = {'http': 'http://www.someproxy.com:3128'}
urllib.request.ProxyHandler(proxies)


# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def get_doi(source_file):
	with open("%s"%source_file) as lines:
		dois = [line[3:].replace("\n", "") for line in lines if "DI" in line]
	return dois

def get_doi_1(source_file):
    """to use file of Tab delimted format for windows"""
    df = pd.read_csv("%s.txt" % source_file, sep='\t', lineterminator='\r')
    dois = (df["AR"])
    return dois

def get_doi_test(source_file):
    """to use file of csv"""
    df = pd.read_csv("%s.csv" % source_file, low_memory=False)
    dois = (df["DOI"])
    return dois

def get_link(doi):

	try:
	# find to link of pdf file via DOI number from web
		opener = urllib.request.build_opener()
		opener.addheaders = [('Accept', 'application/vnd.crossref.unixsd+xml')]
		# r = opener.open('http://dx.doi.org/10.1016/j.aca.2018.04.033')
		# r = opener.open("http://dx.doi.org/10.1039/C5SC03620H")
		# r = opener.open('http://dx.doi.org/10.1021/cg400096e')
		r = opener.open("http://dx.doi.org/" + str(doi))


		#print (r.info()["Link"])
		link = r.info()["Link"].split(";")[1]

		url = link[link.index("<") + 1:-1]
		#print (url)

		if "pubs.rsc" in url:
			url = url.replace("articlepdf", "articlehtml")

		elif "elsevier" in url:
			#url = "%s&APIKey=e1ea5763a46ff62efee36df6f6a5da04"%url #.replace("xml", "plain")
			url = "https://api.elsevier.com/content/article/doi/%s?APIKey=e1ea5763a46ff62efee36df6f6a5da04" % doi

		elif "pubs.acs" in url:
			url = url.replace("http", "https").replace("pdf", "full")
			# print (url)

		elif "wiley" in url:
			url = "https://onlinelibrary.wiley.com/doi/full/" + doi
			# print (url)

		elif "tandfonline" in url:
			url = "https://www.tandfonline.com/doi/full/%s" % doi

		return url
	except:
		print("DOI is NaN or Your Pc is offline")


def save_html(url, html_dir, file_name):
	#Basic http file downloading from net and saving to disk in python
	save_html = urllib.request.URLopener()
	save_html.retrieve(url, "%s/%s.html"%(html_dir, file_name))

def save_html_1(url, html_dir, file_name):
	r = requests.get(url, stream=True)
	with open("%s/%s.html"%(html_dir, file_name), "wb") as html_f:
		for chunk in r.iter_content(chunk_size=1024):

			# writing one chunk at a time to html file
			if chunk:
				html_f.write(chunk)

def save_html_2(url, html_dir, file_name):
	driver = webdriver.Firefox()
	driver.get(url)

	html_source = driver.page_source
	#print(html_source)

	html_f = open("%s/%s.html"%(html_dir, file_name), "w")
	html_f.write(html_source)
	html_f.close()

	driver.quit()
	#save_me = ActionChains(driver).key_down(Keys.CONTROL) \
		#.key_down('s').key_up(Keys.CONTROL).key_up('s')
	#save_me.perform()
#save_web_page(url)

session = HTMLSession()
def save_html_3(url, html_dir, file_name):
    r = session.get(url)
    open("%s/%s.html"%(html_dir, file_name), "wb").write(r.content)

def save_to_exel(df, file_name):
	writer = pd.ExcelWriter("%s.xlsx"%file_name, engine='xlsxwriter')
	df.to_excel(writer, sheet_name='Sheet1')
	writer.save()



def run_get_html_lib():
	"""xxxxx"""

	doi_source_file = "separated_dois/all_mof_dois_8"
	keyword= "8_5000"
	dois = list(set(get_doi_test(doi_source_file)))

	workdir = os.getcwd()

	try:
		os.mkdir("%s/%s_files" % (workdir, keyword))
	except:
		print ("Bütün klasorler önceden oluşturulmuş!")

	main_dir = "%s/%s_files" % (workdir, keyword)

	acs_dir = "%s/acs_lib"%main_dir
	rsc_dir = "%s/rsc_lib" % main_dir
	elsevier_dir = "%s/elsevier_lib" % main_dir
	wiley_dir = "%s/wiley_lib" % main_dir
	science_pnas_dir =  "%s/science_pnas_lib"%main_dir
	tandfonline_dir = "%s/tandfonline_lib"%main_dir
	springer_dir = "%s/springer_lib"%main_dir
	others_dir = "%s/others_lib"%main_dir


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
		print ("Bütün klasorler önceden oluşturulmuş!")

	#html_dir = "%s/%s_files"%(workdir, keyword)
	#os.chdir("%s/%s_files"%(workdir, keyword))

	not_save = []
	for doi in dois:
		url = get_link(doi)
		if url:
			print(url)

			file_name = doi.replace("/", "_s_").replace(".", "_n_").replace("(", "_p_").replace(")", "_tp_").replace("-", "_ot_")

			try:
				if "pubs.acs" in url:
					html_dir =  acs_dir
					try:
						save_html_1(url, html_dir, file_name)
					except:
						save_html_3(url, html_dir, file_name)

				elif "pubs.rsc" in url:
					html_dir = rsc_dir
					save_html_3(url, html_dir, file_name) #for pubs.rsc

				elif "elsevier" in url:
					html_dir = elsevier_dir
					save_html_1(url, html_dir, file_name)

				elif "wiley" in url:
					html_dir = wiley_dir
					save_html_1(url, html_dir, file_name)

				elif "pnas." in url:
					pass
					#html_dir = science_pnas_dir
					#url = "http://dx.doi.org/" + str(doi)
					#save_html_2(url, html_dir, file_name)

				elif "science" in url:
					pass
					#html_dir = science_pnas_dir
					#url = "http://dx.doi.org/" + str(doi)
					#save_html_2(url, html_dir, file_name)

				elif "tandfonline" in url:
					html_dir = tandfonline_dir
					save_html_1(url, html_dir, file_name)

				elif "springer" in url:
					html_dir = springer_dir
					save_html_1(url, html_dir, file_name)

				else:
					html_dir = others_dir
					save_html_1(url, html_dir, file_name)
			except:
				not_save.append(url)
				print("%s icin html formatında kayıt yapılamadı"%file_name)

			time.sleep(25)
			"""PDF formatındaki dosyalar için kayıt VAR MI ?????"""

	df_not_save = pd.DataFrame()
	df_not_save["Not Save Link"] = not_save

	save_to_exel(df=df_not_save, file_name="%s_Not_Save_Link.xls"%keyword)

run_get_html_lib()

