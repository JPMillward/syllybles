#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  6 13:31:07 2021

@author: johnm

Designed to Print Lyrics to Corresponding Text File
"""
import sqlite3
from SyllySql import MillSql
import os.path
import requests
import pandas as pd


directory = "/Users/johnm/Documents/Projects/Syllables/"
sql_path = directory + 'syllable_database.db'
database_connection = sqlite3.connect(sql_path)
sql = MillSql(database_connection)

class SyllySearch():
    
    def __init__(self, query, url = None, key = None):
        
        #API Query Structure
        self.query = query
        url = url if url != None else "https://dictionaryapi.com/api/v3/references/learners/json/"
        key = key if key != None else "?key=c3934b84-8966-4d39-9eef-70126f8356aa"
        lookup = url + query + key
        self.data = requests.get(lookup).json()
        self.ipa = self.data[0]['hwi']['prs'][0]['ipa']
    
        self.keyvalues = {'word':[self.query], 'ipa':[self.ipa]}
        
    #Deprecated#    
    def check_for_word(self):
        file_path = directory + self.word + "test.txt"
        
        if os.path.exists(file_path):
            return True
        else: return False
    ##########
   
    def validate_homograph(self):
        self.homograph_list = []
        if not isinstance(self.data[0]['hom'], int): return
        for dictionary in self.data:
            word_id = dictionary['meta']['id']
            if self.query == word_id[:-2]:
                try:    homograph = dictionary['hwi']['prs'][0]['ipa']
                except: homograph = dictionary['hwi']['altprs'][0]['ipa']
                
                if homograph not in self.homograph_list and homograph != self.ipa:
                    self.homograph_list.append(homograph)
        return         
    
    def update_keyvalues(self):
        for x, homograph in enumerate(self.homograph_list):
            variation = f'alt{x}'
            new_values = {variation:[homograph]}
            self.keyvalues.update(new_values)
    
    def search_webster(self):
        self.validate_homograph()
        self.update_keyvalues()
        self.wanted_data = pd.DataFrame(self.keyvalues)
        return self.wanted_data

table = 'root_words'
column = 'Syllable'
query = 'lead'
sy = SyllySearch(query)
test_frame = sy.search_webster()
#print('DB:::')
print(sql.data_tables)
print(sql.search_db('symbol_table'))