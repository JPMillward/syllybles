#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  6 13:31:07 2021

@author: johnm

Query Webster API to get informatioon.
"""

import requests
import pandas as pd

class SyllySearch():
    
    def __init__(self, query, url = None, key = None):
        #API Query Structure
        self.wanted_data = None
        self.query = query
        url = url if url != None else "https://dictionaryapi.com/api/v3/references/learners/json/"
        key = key if key != None else "?key=c3934b84-8966-4d39-9eef-70126f8356aa"
        lookup = url + query + key
        self.data = requests.get(lookup).json()
        if self.assign_ipa() == False: return
        self.search_webster()
    
    def assign_ipa(self):
        #print(self.data[0].keys())
        possible_locations = ['hwi','vrs']
        for loc in possible_locations:
            if loc in self.data[0].keys() and 'prs' in self.data[0][loc]:
                self.ipa = self.data[0][loc]['prs'][0]['ipa']
            else: return False
            return True
                
                                  
    def search_webster(self):
        self.keyvalues = {'word':[self.query], 'ipa':[self.ipa]}
        self.validate_homograph()
        self.update_keyvalues()
        self.wanted_data = pd.DataFrame(self.keyvalues)
        return
 
    
    def update_keyvalues(self):
        for x, homograph in enumerate(self.homograph_list):
            variation = f'alt{x}'
            new_values = {variation:[homograph]}
            self.keyvalues.update(new_values)


    def validate_homograph(self):
        self.homograph_list = []
        check_homograph = 'hom'
        #print(self.data[0].keys())
        if check_homograph not in self.data[0].keys(): return
        for dictionary in self.data:
            word_id = dictionary['meta']['id']
            if self.query == word_id[:-2]:
                try:    homograph = dictionary['hwi']['prs'][0]['ipa']
                except: pass
                try: homograph = dictionary['hwi']['altprs'][0]['ipa']
                except: return('{self.query} is a homograph has one pronunciation.')
                
                if homograph not in self.homograph_list and homograph != self.ipa:
                    self.homograph_list.append(homograph)    
    
    
   