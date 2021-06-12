#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  5 19:49:46 2021

@author: 
Helper class for manipulating and querying SQL
"""

import pandas as pd
import sqlite3
from syllyble_package.constants import database_string
database_connection = sqlite3.connect(database_string)


class MillSql():
    
    def __init__(self, database_connection):
        self.dbc = database_connection
        self.generate_query_whitelist()
        return
    
    def generate_query_whitelist(self):
        self.valid_queries = {}
        valid_tables = self.list_tables()
        for table in valid_tables:
            dictionary = {table:self.list_columns(table)}
            self.valid_queries.update(dictionary)
        print(self.valid_queries)
            

    def list_tables(self):
        data_tables = []
        get_all = """SELECT name FROM sqlite_master WHERE type ='table'"""
        db_tables = pd.read_sql(get_all, self.dbc, index_col=None)
        for x in range(len(db_tables)):
            data_tables.append(db_tables.iloc[x][0])
        #print(self.data_tables)
        return data_tables
    
    def list_columns(self, table):
        table_columns = []
        get_columns = f"""PRAGMA table_info({table})"""
        column_names = pd.read_sql(get_columns, self.dbc)['name'].values
        #print(column_names)
        for item in column_names:     
            table_columns.append(item)
        return table_columns
    
    def get_table(self, table):
        table = self.search_db(table)
        return table
            
    def search_db(self, table, column = None, match = None, return_column = None, discrete = False):
        show_table = """SELECT * FROM """
        if table in self.valid_queries.keys(): show_table += table
        else: return(f"ERROR: Table '{table}' does not exist") 

        if  match == None or str(match) == 'None' or len(str(match)) == 0: param = None
        else:
            param = (match,)
            query1 = " WHERE "
            query2 = "=:match"
            if column in self.valid_queries[table]: show_table += query1 + column + query2
            else: return("Error: Invalid Query")
        
        ps_show_table = pd.read_sql(show_table, self.dbc,  params=param, index_col=None).drop(columns='index')
        if len(ps_show_table) > 0: ret_table = ps_show_table.iloc[0] if discrete == True else ps_show_table
        else: ret_table = ps_show_table
        #print(ret_table)
        #print('\n\n\n')
        if  return_column == None: return ret_table
        else: return ret_table[return_column]
    
    def insert_data(self, table, data_frame):
        if table not in self.valid_queries.keys(): return("Error: Invalid Inquiry")
        data_frame.to_sql(table, self.dbc, if_exists='append')
        return(f"***added row to {table}***")
    
    
    ###Will not work
    def insert_table(self, table, data_frame):
        if table in self.valid_queries: return(f"Error: {table} exists. Please insert_data() instead")
        self.valid_queries.append(table)
        data_frame.to_sql(table, self.dbc)
        return print(f"***added {table} to sqlite_master***")
        
    def drop_table(self, table):
        if table not in self.valid_queries.keys(): return("Error: Cannot drop {table} as it does not exist.")
        print(f"dropping {table} from database")
        drop_table = f"""DROP TABLE {table};"""
        pd.read_sql(drop_table, self.dbc)
        return

sql = MillSql(database_connection)