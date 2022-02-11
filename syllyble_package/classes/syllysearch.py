#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  6 13:31:07 2021

@author: johnm

Query Webster API to get informatioon.
"""

import requests
import pandas as pd
import re

class SyllySearch():
    
    def __init__(self, query, url = None, key = None):
        #API Query Structure
        self.wanted_data = None
        self.query = query
        self.keyvalues = None
        url = url if url != None else "https://dictionaryapi.com/api/v3/references/learners/json/"
        key = key if key != None else "?key=c3934b84-8966-4d39-9eef-70126f8356aa"
        lookup = url + query + key
        self.data = requests.get(lookup).json()
        self.search_webster()

    
    def assign_ipa(self):
        if isinstance(self.data[0], str):
            print("ERROR: Received String Instance.")
            return False
        possible_locations = ['hwi','vrs']
        for loc in possible_locations:
            if loc in self.data[0].keys() and 'prs' in self.data[0][loc]:
                self.ipa = self.data[0][loc]['prs'][0]['ipa']
            else: return False
            return True
  
    
    def get_result(self):
        return self.wanted_data           
   
                               
    def search_webster(self):
        if self.assign_ipa() == False: return
        self.keyvalues = {'word' : self.query, 'ipa': self.ipa}
        self.validate_homograph()
        self.update_keyvalues()
        self.wanted_data = pd.DataFrame([self.keyvalues])
        return
 
    
    def update_keyvalues(self):
        for x, homograph in enumerate(self.homograph_list):
            variation = f'alt{x}'
            new_values = {variation:[homograph]}
            self.keyvalues.update(new_values)

    def affix_validation(self):
        returned_word_id = self.data[0]['meta']['id']
        print(self.wanted_data)
        pattern = re.compile("\w+'*\w*")
        match = re.search(pattern, returned_word_id)
        print(f"comparing {match[0]} to {self.query}")
        if match[0] == self.query:
            print("100% Match")
        else:
                print(f"{match[0]} DOES NOT MATCH {self.query}, validating.")
    
    def validate_homograph(self):
        self.homograph_list = []
        check_homograph = 'hom'
        #print(self.data[0].keys())
        if check_homograph not in self.data[0].keys(): return #print("No Homograph  for {self.query}")
        for dictionary in self.data:
            word_id = dictionary['meta']['id']
            if self.query == word_id[:-2]:
                try:    homograph = dictionary['hwi']['prs'][0]['ipa']
                except: pass
                try: homograph = dictionary['hwi']['altprs'][0]['ipa']
                except: return('{self.query} is a homograph has one pronunciation.')
                
                if homograph not in self.homograph_list and homograph != self.ipa:
                    self.homograph_list.append(homograph)  


#Test Case        
#test_list = ['completely', 'deeds', "that's", 'rhymes', 'swindled', "it's"] 
#for word in test_list:
#    SyllySearch(word).affix_validation()   