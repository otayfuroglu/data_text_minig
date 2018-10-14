# -*- coding:utf-8 -*-

import pandas as pd
import numpy as np

def save_to_exel(df, file_name):
	writer = pd.ExcelWriter("%s.xlsx"%file_name, engine='xlsxwriter')
	df.to_excel(writer, sheet_name='Sheet1')
	writer.save()


def general_result():
	df_data = pd.read_excel("all_MOF_SA_extract.xlsx")

	articles = set(df_data["DOI"])

	mofs = df_data["MOF Name"]

	df_bet_data = df_data.loc[df_data['Type'] == "BET"]
	df_langmuir_data = df_data.loc[df_data["Type"] == "Langmuir"]
	df_no_type_data = df_data.loc[df_data["Type"] == "*No_surface_type*"]



	idk = df_data.loc[df_data['MOF Name'] == "*IDK*"] # IDK içeren satırları getirdik
	non_idk = df_data.loc[df_data['MOF Name'] != "*IDK*"]

	df_bet_data_idk = df_bet_data.loc[df_bet_data['MOF Name'] == "*IDK*"]
	df_langmuir_data_idk = df_langmuir_data.loc[df_langmuir_data['MOF Name'] == "*IDK*"]


	df_bet_data_non_idk = df_bet_data.loc[df_bet_data['MOF Name'] != "*IDK*"]
	df_langmuir_data_non_idk = df_langmuir_data.loc[df_langmuir_data['MOF Name'] != "*IDK*"]

	#according to mof name
	#df_data_mof_name = df_bet_data_non_idk[df_bet_data_non_idk.columns[[0, 2]]] #istediğimiz kolonu indeksler ile seçtik
	df_data_mof_name = df_bet_data_non_idk[["MOF Name", "Valeu"]] #istediğimiz kolonu isimleri ile seçtik
	df1_data_mof_name = df_data_mof_name.astype(str).groupby('MOF Name').agg('; '.join).reset_index()


	#according to DOI number
	df_data_doi_non_idk_bet = df_bet_data_non_idk[["MOF Name", "Valeu", "DOI"]]
	df1_data_doi_non_idk_bet = df_data_doi_non_idk_bet.astype(str).groupby('DOI').agg('; '.join).reset_index()

	df_data_doi_non_idk_lang = df_langmuir_data_non_idk[["MOF Name", "Valeu", "DOI"]]
	df1_data_doi_non_idk_lang = df_data_doi_non_idk_lang.astype(str).groupby('DOI').agg('; '.join).reset_index()

	df_data_doi_non_idk_lang = df_langmuir_data_non_idk[["MOF Name", "Valeu", "DOI"]]
	df1_data_doi_non_idk_lang = df_data_doi_non_idk_lang.astype(str).groupby('DOI').agg('; '.join).reset_index()

	df_data_doi_idk_bet = df_bet_data_idk[["MOF Name", "Valeu", "DOI"]]
	df1_data_doi_idk_bet = df_data_doi_idk_bet.astype(str).groupby('DOI').agg('; '.join).reset_index()

	#save_to_exel(df1_data_doi_idk_bet, file_name="df_data_doi_idk_bet")



	#print (len(set(non_idk["MOF Name"])))


	df_table = pd.DataFrame()
	df_table["Numbers Of DOI"] = len(df_data)
	#print (len(df_data))

	#save_to_exel(df_table, "table")

def merge_pv_sa_values(df_data_sa, df_data_pv):


	#sa_bet_data = df_data_sa.loc[df_data_sa['Type'] == "BET"]
	#sa_bet_data_clean = sa_bet_data.loc[sa_bet_data['MOF Name'] != "*IDK*"]

	sa_data_doi_val_name = df_data_sa[["MOF Name", "Valeu", "DOI"]]
	sa_data_doi_bydoi = sa_data_doi_val_name.astype(str).groupby('DOI').agg('; '.join).reset_index()


	pv_data_doi_val_name = df_data_pv[["MOF Name", "Valeu", "DOI"]]
	pv_data_doi_bydoi = pv_data_doi_val_name.astype(str).groupby('DOI').agg('; '.join).reset_index()



	comm_pv_data_doi_bydoi = []
	comm_sa_data_doi_bydoi = []

	i = 0
	for doi in sa_data_doi_bydoi["DOI"]:
		if doi in list(pv_data_doi_bydoi["DOI"]):

			comm_sa_data_doi_bydoi.append(sa_data_doi_bydoi.iloc[[i]])

			comm_pv_data_doi_bydoi.append(pv_data_doi_bydoi.loc[pv_data_doi_bydoi["DOI"] == doi])
		i += 1

	df_comm_pv_data_doi_bydoi = pd.concat(comm_pv_data_doi_bydoi)
	df_comm_sa_data_doi_bydoi = pd.concat(comm_sa_data_doi_bydoi)

	print (df_comm_sa_data_doi_bydoi[["DOI",]].head())
	#print (len(df_comm_pv_data_doi_bydoi["DOI"]))

	df_comm_sa_data_doi_bydoi["PV MOF Name"] = pd.Series(list(df_comm_pv_data_doi_bydoi["MOF Name"]),
													  index=df_comm_sa_data_doi_bydoi.index)

	df_comm_sa_data_doi_bydoi["PV Value"] = pd.Series(list(df_comm_pv_data_doi_bydoi["Valeu"]),# df1["a"] = df2 formatını kullandığımda saçma
													index=df_comm_sa_data_doi_bydoi.index) # sonuç alıyorım ama bu şekililde yapınca sorun çözüldü


	#df_comm_pv_data_doi_bydoi["SA MOF Name"] = (df_comm_sa_data_doi_bydoi["MOF Name"])
	#df_comm_pv_data_doi_bydoi["SA Value"] = (df_comm_sa_data_doi_bydoi["Valeu"])

	save_to_exel(df_comm_sa_data_doi_bydoi, "df_comm_values")

