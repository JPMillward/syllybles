#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 29 16:00:54 2021

@author: johnm
"""
from syllyble_package.classes.syllysql import sql

def phoneme_lookup(character, return_request = 'Type'):
    #print(f'Searching for match to {character}')
    symbol_table = sql.search_db('symbol_table')

    from_ipa = symbol_table['IPA'] == character
    from_arpa1 = symbol_table['ARPA1'] == character
    from_arpa2 =  symbol_table['ARPA2'] == character
    lookup = symbol_table.loc[from_ipa|from_arpa1|from_arpa2]
        
    if len(lookup) > 0:
       return_type = lookup[return_request].iloc[0] 
       #print(f"{character} is a {return_type}")
       return return_type
    else: 
       print(f'Problem! No match to {character} found.')
       return None