#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  5 19:49:46 2021

@author: 
Helper class for manipulating and querying SQL
"""

import pandas as pd
import sqlite3

directory = "/Users/johnm/Documents/Projects/Syllables/"
sql_path = directory + 'syllable_database.db'
database_connection = sqlite3.connect(sql_path)


class MillSql():
    
    def __init__(self, database_connection):
        self.dbc = database_connection
        self.cur = database_connection.cursor()
        self.data_tables = []
        self.valid_columns = []
        self.list_tables()
        return

        
    def list_tables(self):
        get_all = """SELECT name FROM sqlite_master WHERE type ='table'"""
        db_tables = pd.read_sql(get_all, self.dbc, index_col=None)
        x = 0
        while len(db_tables) > x:
            #print(db_tables.iloc[x][0])
            self.data_tables.append(db_tables.iloc[x][0])
            x += 1
        #print(self.data_tables)
        return
    
    def validate_columns(self, table):
        get_columns = f"""PRAGMA table_info({table})"""
        column_names = pd.read_sql(get_columns, self.dbc)['name'].values
        #print(column_names)
        for item in column_names:     
            #print(item)
            self.valid_columns.append(item)
        print(self.valid_columns)   
        return
        
    def search_db(self, table, column = None, match = None, return_column = None, discrete = False):
        self.validate_columns(table)
        show_table = """SELECT * FROM """
        #print(table)
        #print(self.data_tables)
        if table in self.data_tables: show_table += table
        else: return("ERROR: Invalid Query") 
    
        param = None
        if  match == None or str(match) == 'None' or len(str(match)) == 0: None
        else:
            param = (match,)
            query1 = " WHERE "
            query2 = "=:match"
            if column in self.valid_columns: show_table += query1 + column + query2
            else: return("Error: Invalid Query")
        
        ps_show_table = pd.read_sql(show_table, database_connection,  params=param, index_col=None).drop(columns='index')
        
        ret_table = ps_show_table.iloc[0] if discrete == True else ps_show_table
        
        #print(ret_table)
        #print('\n\n\n')
        if  return_column == None: return ret_table
        else: return ret_table[return_column].values
    
    def insert_data(self, table, data_frame):
        if table not in self.data_tables: return("Error: Invalid Inquiry")
        self.validate_columns(table)
        data_frame.to_sql(table, self.dbc, if_exists='append')
        return(f"***added row to {table}***")
    
    def insert_table(self, table, data_frame):
        if table in self.data_tables:
            print(f"Error: {table} exists. Please insert_data() instead")
            return
        self.data_tables.append(table)
        data_frame.to_sql(table, self.dbc)
        return print(f"***added {table} to sqlite_master***")
        
    def drop_table(self, table):
        if table not in self.data_tables: 
            print("Error: Cannot drop {table} as it does not exist.")
            return
        print(f"dropping {table}")
        drop_table = f"""DROP TABLE {table};"""
        pd.read_sql(drop_table, self.dbc)
        return
