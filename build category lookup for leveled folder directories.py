# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 20:21:57 2022

@author: layto
"""
#rmemeber to open SQLite3
#PIP INSTALL SQLITE3
# https://visualstudio.microsoft.com/downloads/
#Pip install fuzzywuzzy
#Pip install python-Levenshtein

#C:\Users\layto\OneDrive\Documents\GitHub\Group-6-technica-lcode\Group Project Jupyter Notebook-Year 1 Semester 2
import sqlite3
from sqlite3 import Error
import pandas as pd


import matplotlib.pyplot as plt
import seaborn as sns

import os#make folder

from diff_match_patch import diff_match_patch
#fuzzymatch


sns.set()

con = sqlite3.connect("DB")

def sql_fetch(con):

    cursorObj = con.cursor()

    cursorObj.execute('SELECT name from sqlite_master where type= "table"')

    print(cursorObj.fetchall())

sql_fetch(con)
##


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def join1_sites__policy_snapshots(conn):
    #sites = pd.read_sql_query("SELECT id, categories from sites WHERE (categories LIKE '%social%' OR categories LIKE '%tech%' OR categories LIKE '%media%') AND  ( (categories LIKE '%sharing%')  OR  categories LIKE '%messageboard%' OR categories LIKE '%blogsandpersonal%') AND NOT categories LIKE '%news%'",conn)
  
    sites = pd.read_sql_query("SELECT id, categories from sites",conn)#" WHERE categories LIKE '%"+SQLcategoryFilter+"%'",conn)
    #SQLcategoryFilter="adult"
    
    #print('rows after\n\n',result.shape)
    
    #sites = pd.read_sql_query("SELECT id, categories from sites WHERE (categories LIKE '%tech%' OR categories LIKE '%media%') AND ( (categories LIKE '%sharing%' AND  categories LIKE '%media%')) OR  (categories LIKE '%education%' AND  categories LIKE '%tech%')-- OR  categories LIKE '%messageboard%' OR categories LIKE '%blogsandpersonal%')", conn)#maybe requery and do .unique and rederfine categories
   #category selector
#   and ( (categories LIKE '%sharing%' and  categories LIKE '%media%')) or  (categories LIKE '%education%' and   categories LIKE '%tech%')
 #  or  categories LIKE '%messageboard%') or  categories LIKE '%blogsandpersonal%')))
  # //those that have sharing and media or education and tech? or messageboardsand forums or 'blogsandpersonal;business;newsandmedia' 


   
    #print('sites\n',sites)
    
    #sites[['id','categories']].groupby(['categories']).agg(['count']).sort(['count'])
    #df.set_index(['count'])
    #print(df.index)
    df = pd.DataFrame(columns = ['categories'])
    df['categories']=sites['categories'].drop_duplicates()
    df['categoriescountsemicolon']=df['categories'].str.count(";")
    #result['nlpGDPR']=result['policy_text'].str.count("GDPR")##here is where to adjust what words ar being checked, not earlier on so other graphs
 
    print(df)
    df.to_csv('Categories lookup.csv')
    

    
    

    
    


def DatabaseInterrogation():
    database = r"C:\Users\layto\sqlite\db"#.xz?

    # create a database connection
    conn = create_connection(database)#2nd funct called
    with conn:
     #   print("1. Query task by priority:")
      #  select_task_by_priority(conn, 1)

        print("2. Query all tasks")
        join1_sites__policy_snapshots(conn)##3rd function called
       # return result, SQLcategoryFilter 


if __name__ == '__main__':
    DatabaseInterrogation()   #start
    print('Database processing complete')
        




