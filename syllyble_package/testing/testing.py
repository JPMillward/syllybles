#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 28 17:48:23 2021

@author: johnm
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 22:07:07 2021

@author: johnm
"""

import pathlib
from syllyble_package.classes.syllysql import sql
from syllyble_package.classes.syllysearch import SyllySearch
from syllyble_package.classes.syllysplit import SyllySplit
from syllyble_package.classes.syllybuild import SyllyBuild
from syllyble_package.classes.syllysummon import SyllySummon

import pandas as pd
import re
#print(sql.data_tables)

directory = "/Users/johnm/Documents/Projects/GeniusLyrics/"
text_file = "Look Over Your Shoulder (feat. Kendrick Lamar) by Busta Rhymes.txt"
path = directory + text_file


def get_ipa(input_word):
    ipa_word = sql.search_db('words', 'word', input_word).iloc[0]['ipa']
    return ipa_word

def begin_build():
    smn = SyllySummon(path)
    #print(smn.structure)
    unique_word_list = smn.get_unique_words()
    #print(smn.get_unique_words())
    
    for index in range(len(unique_word_list)):
        one_word = unique_word_list[index]
        print(one_word)
        
        if sql.does_exist(one_word) == False:
            print(f"{one_word} is not in the database")
            
            if not isinstance(SyllySearch(one_word).keyvalues, dict):
                 log_miss(one_word)
                 
            else:
                 print(SyllySearch(one_word).get_result)
             
        else: 
            print(f"{one_word} is in syllyble datatable")

def log_miss(word):
    print(f"ERROR: UnSuccessfully logged {word}. Implement proper logging procedures")


print(pathlib.Path.cwd())
#begin_build()