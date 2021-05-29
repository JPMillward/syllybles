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
from SyllySql import MillSql
import pandas as pd
import sqlite3


directory = "/Users/johnm/Documents/Projects/Syllables/"
sql_path = directory + 'syllable_database.db'
database_connection = sqlite3.connect(sql_path)
sql = MillSql(database_connection)

file_name = "phoneme_table.xlsx"
directory = "/Users/johnm/Documents/Projects/Syllables/"
full_path = directory + file_name
symbol_table = pd.read_excel(full_path, "Sheet1", index_col = None)
sql.insert_table('symbol_table', symbol_table)
print(symbol_table)