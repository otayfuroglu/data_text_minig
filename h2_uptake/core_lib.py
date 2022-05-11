# -*- coding:utf-8 -*-

import pandas as pd
from nltk.corpus import wordnet as wn
from bs4 import BeautifulSoup


import os
import re


def replace(fin_name,srcStr,desStr,fout_name):
	fin = open(fin_name, "r")
	fout = open(fout_name, "w")
	txt = fin.read()
	txtout = re.sub(srcStr,desStr, txt)

	fout.write(txtout)
	fin.close()
	fout.close()


def mof_in_Paper(html_doc):
    """xxxxxx"""

    Total_DATA = []
    MOF_list = []

    # eliminating HTML tags
    f = BeautifulSoup(html_doc, 'html.parser')
    for i in f(["script", "style", 'ol', 'ul', 'li', 'table', 'a', 'noscript', 'option']):
        i.extract()
    for i in f(["div"]):
        if i.get('class') == ['citationInfo'] or i.get('class') == ['casRecord'] \
                or i.get('class') == ['casContent'] or i.get('class') == ['casTitle'] \
                or i.get('class') == ['casAuthors'] or i.get('class') == ['casAbstract']:
            # print (i.get_text())
            i.extract()

    for i in f(['sup', 'sub']):
        i.unwrap()

    g = f.get_text()
    # pretreatment2
    g = re.sub("\n", "", g)
    g = re.sub("&thinsp;", "", g)
    g = re.sub("&nbsp;", " ", g)
    g = re.sub("\u2009", " ", g)
    g = re.sub("\u2005", " ", g)

    # split in sentences and store in array
    sentences = []
    sentences = g.split(".")
    for i in range(len(sentences)):
        sentences[i] += "."

    front = re.compile('[^A-Z]\d+.$|\s?Fig.\s?$|\s+\w{1,3}[,.]\s?$|i.e.\s?$')
    back = re.compile('^\s?\w?\d+|^g.\s?|^\s?\w+[,.]\s?$|^,')

    appended = 0
    for i in range(len(sentences)):
        value_find = front.search(sentences[i])
        temp_sentence = sentences[i]
        while value_find != None:
            if back.search(sentences[i + 1]) != None:
                temp_sentence += sentences[i + 1]
                del sentences[i + 1]
                sentences.append('\n')
                appended += 1
                value_find = front.search(temp_sentence)
            else:
                value_find = None
        sentences[i] = temp_sentence

    sentences.reverse()
    for i in range(appended):
        del sentences[0]
    sentences.reverse()

    # MOF name candidate - MOF criteria : Need to be modified later
    Upper = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
             'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    Number = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    MOF_in_Paper = []
    words = []

    for i in range(len(sentences)):
        words = sentences[i].split(' ')
        for j in range(len(words)):
            # words pretreatment

            words[j].replace("-", "-")
            if len(words[j]) > 2:
                if words[j][-1] == ')':
                    words[j] = words[j][:-1]
                if words[j][0] == '(':
                    words[j] = words[j][1:]

            if len(words[j]) > 2:
                if words[j][-1] == ',' or words[j][-1] == '.' or words[j][-1] == ';' \
                        or words[j][-1] == ':' or words[j][-1] == "\n":
                    words[j] = words[j][:-1]
                if words[j][-1] == ')':
                    words[j] = words[j][:-1]
                if words[j][0] == '(':
                    words[j] = words[j][1:]
            MOF_Crit = 0

            MOF_Crit_Number = 0
            MOF_Crit_Upper = 0

            if words[j].find('-') != -1:
                MOF_Crit += 2
                if words[j][0] == '-':
                    MOF_Crit += 1

            for k in range(len(Upper)):
                if words[j].find(Upper[k]) != -1:
                    MOF_Crit_Upper += 1

            if MOF_Crit_Upper != 0:
                MOF_Crit += 1

            No_number = 1
            for k in range(len(Number)):
                if words[j].find(Number[k]) != -1:
                    MOF_Crit_Number += 1
                    No_number = 0

            if MOF_Crit_Number != 0:
                MOF_Crit += 1

            if words[j].find('(') * words[j].find(')') >= 0 and words[j].find('(') >= 0:
                MOF_Crit += 1

            if words[j].find('[') * words[j].find(']') >= 0 and words[j].find('[') >= 0:
                MOF_Crit += 1

            if words[j].find('MOF') != -1 or words[j].find('PCN') != -1:
                MOF_Crit += 1

            Linker_words = ["DOBDC", "BTC", "bdc", "CuBT", "13X", "TO", "DBTO", "DTO", "BTO", "Car", "bpe", "tftpa"]
            for k in range(len(Linker_words)):
                if words[j].find(Linker_words[k]) != -1:
                    MOF_Crit += 2

            if words[j] == 'AT':
                MOF_Crit += 2

            if len(words[j]) > 0:
                if words[j].find("13X") == -1:
                    if words[j][0].isdigit() == True or words[j][0] == '+':
                        MOF_Crit = 0

                        # Empirically added no MOF words
            if words[j].find('MJXp') != -1 or words[j].find('PLATON') != -1:
                MOF_Crit = 0

            if words[j].find('=') != -1 or words[j].find('=') != -1:
                MOF_Crit = 0

            if words[j] != '' and words[j][-1] == '-':
                MOF_Crit = 0
            # if MOF_Crit > 2:
            # print (words[j],MOF_Crit)
            Prop_noun = 0
            if words[j].find('-') != -1:
                Prop_noun = 1
                tempword = words[j].split('-')
                for k in range(len(tempword)):
                    passlist = ["MIL", "POST", "NU", "rho", "sod"]
                    contin_crit = 0
                    for l in range(len(passlist)):
                        if tempword[k] == passlist[l]:
                            contin_crit = 1
                    if contin_crit == 1:
                        continue
                    # print (tempword[k],len(tempword[k]))
                    if len(tempword[k]) <= 1:
                        Prop_noun = 0
                    if k != 0 and tempword[k].isdigit():
                        continue
                    # print (wn.lemmas(tempword[k]))
                    Atom_word = 0
                    if len(tempword[k]) == 2 and \
                                    tempword[k].isalpha() == True and tempword[k][0].isupper() == True and \
                                    tempword[k][1].islower() == True and wn.lemmas(tempword[k]) != []:
                        Atom_word = 1
                        Prop_noun = 0
                        continue
                    if len(tempword[k]) > 1 and tempword[k].isdigit() == False and wn.lemmas(tempword[k]) != []:
                        MOF_Crit = 0
                    if len(tempword[k]) > 2 and tempword[k].isalpha() == True and \
                                    tempword[k][0].isupper() == True and \
                                    tempword[k][1:].islower() == True:
                        MOF_Crit = 0
                        break
                        # if MOF_Crit > 2:
                        # print (words[j])
            if len(words[j]) > 3 and words[j][0].isupper() == True and words[j][1:].islower() == True:
                Prop_noun = 1

            if Prop_noun == 1:
                if No_number == 1 and words[j].find('(') == -1 and words[j].find(')') == -1:
                    MOF_Crit = 0

            if wn.lemmas(words[j]) != [] or words[j] == 'D-R':
                MOF_Crit = 0

            if len(words[j]) < 3:
                MOF_Crit = 0

            if MOF_Crit > 2:

                if words[j][0].find('(') != -1:
                    if words[j][-1].find(')') != -1:
                        words[j] = words[j][1:-1]

                if not words[j][0].islower() or words[j][0:3] == 'sod' or \
                                words[j][0:3] == 'rho' or words[j][0:3] == 'bio' or \
                                words[j].find('agglomerate') != -1:  # first letter big
                    if not words[j][0].isdigit():  # first letter not digit
                        if len(MOF_in_Paper) != 0:
                            for l in range(len(MOF_in_Paper)):
                                if MOF_in_Paper.count(words[j]) == 0:  # double check
                                    MOF_in_Paper.append(words[j])
                        else:
                            MOF_in_Paper.append(words[j])
                    elif words[j].find('13X') != -1 or Atom_word == 1:
                        if len(MOF_in_Paper) != 0:
                            for l in range(len(MOF_in_Paper)):
                                if MOF_in_Paper.count(words[j]) == 0:  # double check
                                    MOF_in_Paper.append(words[j])
                        else:
                            MOF_in_Paper.append(words[j])

    print (MOF_in_Paper)

    # Close file and reopen it to solve BOLD problem
    html_doc.close()

    html_doc = open("temp.html", encoding="UTF-8")
    # html_doc = open("ref131.html", encoding = "UTF-8")

    # eliminating HTML tags - Reference delete
    f = BeautifulSoup(html_doc, 'html.parser')
    # extracting non usable tags

    for i in f(["script", "style", 'ol', 'ul', 'li', 'table', 'a', 'noscript', 'option']):
        i.extract()
    for i in f(["div"]):
        if i.get('class') == ['citationInfo'] or i.get('class') == ['casRecord'] \
                or i.get('class') == ['casContent'] \
                or i.get('class') == ['casTitle'] or i.get('class') == ['casAuthors'] \
                or i.get('class') == ['casAbstract']:
            # print (i.get_text())
            i.extract()

    # Treating Bold tag MOFs
    bold_tag = ['1', '1′', '2', '3', '4', '5', '6', '7', '7′', '8', '(1)', '(2)', '(3)', '1a', '1b', '1c', \
                '2a', '2b', '2c', '3a', '3b', '3c', 'a', 'b', 'c', 'd', '1 a', '2 a', '2 b', 'A', 'B', 'C', 'D', '1 d',
                'I', 'II']
    bold_tag_candidate = []
    bold_MOF = []
    for i in f.find_all(['strong', 'b']):
        # set bold MOF tag criteria
        bold_tag_Crit = 1
        No_number = 1
        No_letter = 1
        if i.string == None:
            continue
        i.string = i.string.strip()
        for j in range(len(i.string)):
            if i.string[j].isdigit() == True:
                No_number = 0
            if i.string[j].isalpha() == True:
                No_letter = 0
        if No_number == 1:
            if len(i.string) > 2:
                bold_tag_Crit = 0
            elif No_letter == 1:
                bold_tag_Crit = 0
        elif No_number == 0 and i.string.isdigit() == True:
            if int(i.string) > 1000:
                bold_tag_Crit = 0

        if i.string[:3] == 'Fig' or i.string[:6] == 'Scheme':
            bold_tag_Crit = 0

        for j in range(len(MOF_in_Paper)):
            if i.string.find(MOF_in_Paper[j]) != -1:
                bold_tag_Crit = 0
                break

        if bold_tag_Crit == 1:
            if bold_tag_candidate != []:
                for j in range(len(bold_tag_candidate)):
                    if len(i.string) < 8:
                        if bold_tag_candidate.count(i.string) == 0:
                            bold_tag_candidate.append(i.string)
            else:
                bold_tag_candidate.append(i.string)

    # print (bold_tag_candidate)

    for i in f.find_all(['strong', 'b']):
        if bold_tag_candidate.count(i.string) == 1:
            store = 0
            MOF = ''
            bold_sentence = i.parent.get_text()

            out = 0
            start_pos = 0
            while out == 0:
                bold_index = bold_sentence.find(i.string, start_pos)
                pass_crit = 0
                if bold_index != -1 and bold_index != 0 and bold_index != len(bold_sentence):
                    if bold_sentence[bold_index - 1].isdigit() or bold_sentence[bold_index - 1].isalpha():
                        pass_crit += 1
                    if bold_index + len(i.string) <= len(bold_sentence) \
                            and bold_sentence[bold_index + len(i.string)].isdigit() \
                            or bold_sentence[bold_index + len(i.string)].isalpha():
                        pass_crit += 1
                if pass_crit == 2:
                    start_pos = bold_index + 1
                else:
                    out = 1

            bold_sentence = bold_sentence.split()
            # print (bold_sentence)
            for k in range(len(bold_sentence)):
                bold_index = bold_index - len(bold_sentence[k]) - 1
                if bold_index >= 0:
                    continue
                # print (bold_sentence[k])
                if store == 0 and bold_sentence[k].find(i.string) != -1:
                    # print (k)
                    if k != 0 and k != len(bold_sentence) - 1:
                        for l in range(len(MOF_in_Paper)):
                            if bold_sentence[k - 1] == 'MOF' or bold_sentence[k - 1] == '(MOF':
                                if bold_sentence[k - 2].find(MOF_in_Paper[l]) != -1:
                                    store = 1
                                    MOF = bold_sentence[k - 2]
                                    break
                            if bold_sentence[k - 1].find(MOF_in_Paper[l]) != -1:
                                store = 1
                                MOF = bold_sentence[k - 1]
                                break
                            elif bold_sentence[k + 1].find(MOF_in_Paper[l]) != -1:
                                store = 1
                                MOF = bold_sentence[k + 1]
                                break
                    elif k == 0:
                        for l in range(len(MOF_in_Paper)):
                            if k + 1 < len(bold_sentence):
                                if bold_sentence[k + 1].find(MOF_in_Paper[l]) != -1:
                                    store = 1
                                    MOF = bold_sentence[k + 1]
                                    break
                    elif k == len(bold_sentence) - 1:
                        for l in range(len(MOF_in_Paper)):
                            if bold_sentence[k - 1] == 'MOF' or bold_sentence[k - 1] == '(MOF' \
                                    or bold_sentence[k - 1] == 'Compound' \
                                    or bold_sentence[k - 1] == '(Compound':
                                if bold_sentence[k - 2].find(MOF_in_Paper[l]) != -1:
                                    store = 1
                                    MOF = bold_sentence[k - 2]
                                    break
                            if bold_sentence[k - 1].find(MOF_in_Paper[l]) != -1:
                                store = 1
                                MOF = bold_sentence[k - 1]
                                break
            if store == 1:
                # print (bold_sentence)
                bold_MOF.append(i.string)
                bold_MOF.append(MOF)
                bold_tag_candidate[bold_tag_candidate.index(i.string)] = ''

                # print (bold_MOF)
    return MOF_in_Paper, bold_MOF

html_doc = "101021jacs7b00705.html"
mof_in_Paper(html_doc)