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

from syllyble_package.classes.syllysql import sql
from syllyble_package.classes.syllysearch import SyllySearch
from syllyble_package.classes.syllysplit import SyllySplit
from syllyble_package.classes.syllybuild import SyllyBuild
import pandas as pd
import re
#print(sql.data_tables)
input_word = "lead"
test = input_word
table = 'words'


def sort_ubo(ubo_in):
    #Read and Search
    f = open(ubo_in, 'r')
    pattern = re.compile('\\w+', re.ASCII)
    ref = re.findall(pattern, f.read())
    
    #Pandas to sort / manipulate
    df = pd.Series(ref, dtype='string')
    df = df.str.lower().str.strip().value_counts().rename_axis('words').reset_index()
    
    #Make list
    unique_words = []
    #print(range(len(df)))
    for x in range(len(df)):
        unique_words.append(df['words'].iloc[x])
    #Output
    #df.to_csv(ubo_out, index=None, columns=['words'], sep=" ", header=None)
    return unique_words

def does_exist(input_text, table = 'words', column = 'word'):
   check_exist = sql.search_db(table, column, match = input_text, return_column = 'word', discrete = True)
   if str(check_exist) == input_text:
       #print(f"{input_text} is already in Table: {table}")
       return True 
   else: 
       #print(f"{input_text} is not in Table: {table}")
       return False

def get_ipa(input_word):
    ipa_word = sql.search_db('words', 'word', input_word).iloc[0]['ipa']
    return ipa_word
        
source = "/Users/johnm/Documents/Projects/testcases/"
input_file = "11second.txt"
x = sort_ubo(source + input_file)
#print(x)
for word in x:
    if does_exist(word) == True:
        ipa_word = get_ipa(word)
        print(word)
        print(ipa_word)
        print(SyllySplit(ipa_word).get_list())
'''
    #Input processing logic stuff. Not currently important

    if does_exist(word) == False:
        #print('Process new word')
        search = SyllySearch(word).wanted_data
        if str(search) == 'None': print(f"log this: {word} has no ipa prs")
        else: sql.insert_data('words', search)
    else: None
        #print('Pull data from table!')
'''        
'''

print(sql.search_db('words'))
does_exist('ho')
''
'''