#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 11:12:40 2021

@author: johnm

Class that ultimately combines other modules to achieve desired end result
Includes several redundancy checks and attempts to reduce api calls as much as possible
"""

from syllyble_package.classes.syllysql import sql
from syllyble_package.classes.syllysearch import SyllySearch
from syllyble_package.classes.syllysplit import SyllySplit
from syllyble_package.classes.syllybuild import SyllyBuild
from syllyble_package.classes.syllysummon import SyllySummon

import pandas as pd
import re

directory = "/Users/johnm/Documents/Projects/GeniusLyrics/"
text_file = "Look Over Your Shoulder (feat. Kendrick Lamar) by Busta Rhymes.txt"
path = directory + text_file

class SyllyStart():
    
    def __init__(self, file_path):
        print("Starting Syllyble Package")
        self.to_be_inserted = pd.DataFrame(data = None, index = None, columns = ['word', 'ipa', 'alt0'])
        self.path = file_path        
        #self.begin_build()
        self.text_by_line = SyllySummon(path).bars
        self.text_structure = SyllySummon(path).structure

        
  
    
    def begin_build(self):
        smn = SyllySummon(path)
        #print(smn.structure)
        smn.get_unique_words()
        for index in range(len(smn.unique_words)):
            one_word = smn.unique_words[index]
            if sql.does_exist(smn.unique_words[index]) == False:
                result_dataframe = SyllySearch(one_word).get_result()
                if not isinstance(result_dataframe, pd.DataFrame):
                     self.log_miss(one_word)
                else:
                    self.to_be_inserted = pd.concat([self.to_be_inserted, result_dataframe], ignore_index = True)
            else: 
                print(f"{one_word} is in syllyble datatable")
        sql.insert_data('test_table', self.to_be_inserted)
        return
    
    def build_lines(self):
        pattern = re.compile(r"\w+'*\w*", re.ASCII)
        self.ipa_by_line = []
        for line in range(len(self.text_by_line)):
            temp_line = []
            words_in_line = re.findall(pattern, self.text_by_line[line])

            for i, item in enumerate(words_in_line):
                temp_line.append(sql.get_ipa(item))
            print(temp_line)
        
        
    def log_miss(self, word):
        log_file = open(directory + "word_log.txt", 'a+')
        read_file = open(directory + "word_log.txt", 'r')
        for line in read_file:
            if line[:-1] == word: return #print(f"'{word}' already in log")
        log_file.write(word + "\n")
        return #print(f"Successfully logged {word}")
    
SyllyStart(path).build_lines()
for line in SyllyStart(path).text_by_line:
    print(line)
print(SyllySummon(path).get_unique_count())