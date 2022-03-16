# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 20:21:57 2022

@author: layto
"""
#rmemeber to open SQLite3

#C:\Users\layto\OneDrive\Documents\GitHub\Group-6-technica-lcode\Group Project Jupyter Notebook-Year 1 Semester 2
import sqlite3
from sqlite3 import Error
import pandas as pd


import matplotlib.pyplot as plt
import seaborn as sns
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
    sites = pd.read_sql_query("SELECT id, categories from sites WHERE categories LIKE '%tech%' or categories LIKE '%media%'", conn)#maybe requery and do .unique and rederfine categories
   #print('sites\n',sites)
    
    #sites[['id','categories']].groupby(['categories']).agg(['count']).sort(['count'])
    #df.set_index(['count'])
    #print(df.index)
    #print('categories\n',df['categories'].unique())#all categories that contaiin tech or media?
    print('sites table imported')
    print( sites.head())
    
    policy_snapshots = pd.read_sql_query("SELECT id, year, phase, policy_text_id,  classifier_probability from policy_snapshots", conn)
    #del result['policy_html_id']
    #del result['policy_reader_view_html_id']
    #del result['site_id']
    print('policy_snapshots table imported\n',policy_snapshots.head())
    
    result = pd.merge(sites, policy_snapshots, how="inner", on=["id", "id"])
    print('merge1 result all columns\n',result.columns)
    del result['id']
    #del result['id_x']
    print('merge1 result\n',result.columns)
    return(join2_result_policy_texts(conn,result))
def join2_result_policy_texts(conn,result):
    #flesch_kincaid, smog,
    policy_texts = pd.read_sql_query("SELECT id, policy_text, flesch_ease, flesch_kincaid , smog,  length from policy_texts", conn)
    print(policy_texts.columns)
    print('policy_texts table imported\n',policy_texts.head())
    
    result = pd.merge(policy_texts, result, on=None, left_on="id", right_on="policy_text_id",  how="inner")# on=["id","policy_text_id"])
    print('merge 2 all columns\n',result.columns)
    #print('unique flesch_ease scores',result['flesch_ease'].unique())
    #print(result.columns)
    del result['policy_text_id']
    del result['id']
    print('merge 2\n',result.columns)
    print(result.head())
    #del result['']
    #del result['']
    return(result)
    
    

    
    


def DatabaseInterrogation():
    database = r"C:\Users\layto\sqlite\db"#.xz?

    # create a database connection
    conn = create_connection(database)
    with conn:
     #   print("1. Query task by priority:")
      #  select_task_by_priority(conn, 1)

        print("2. Query all tasks")
        result=join1_sites__policy_snapshots(conn)
        return(result)


if __name__ == '__main__':
    result=DatabaseInterrogation()   
    print('Database processing complete')
        
    

def MainCode(result):
     """
     Query all rows in the tasks table
     :param conn: the Connection object
     :return:
     """

     #result['child']= re.findall('child[^, ]+',result['policy_text'])
     columns=result.columns
     fieldnames=[]
     for x in columns:
         #print(x)
         fieldnames.append(str(x))
     print('fieldnames',fieldnames)

     result['nlp']=result['policy_text'].str.count("child|Child|Minor|minor|underage|child|kid|young|youth")##here is where to adjust what words ar being checked, not earlier on so other graphs
 #can be made

     #result['year'] = pd.to_datetime(result.year)
     #result.groupby(result.year)['nlp'].transform('mean')
     #nlp=nlp.agg('avg')
     #nlp.groupby(nlp['year'].dt.year)['policy_text'].agg(['mean'])
     print('nlp',result['nlp'])
     #fieldnames.remove('year')
     SQLcategoryFilter='when categories contain tech or media'

    
     #working hashed for efficiency
     #makebarchart(result["year"],result.groupby(result.year)['nlp'].transform('mean'),'Year','Mean count of child synonyms',SQLcategoryFilter)
     del result['nlp']
     #makebarchart(result['year'],result.groupby(result.year)['length'].transform('mean'),'Year','Mean length',SQLcategoryFilter)

     #result['contain_easy'] = result['flesch_ease'].str.count.contains('easy')*100
     #result['contain_easy'] = result['flesch_ease'].str.count.contains('easy')*100
     #result['contain_difficult|confusing']=result.flesch_ease.str.count("difficult|confusing")-result.flesch_ease.str.count("_difficult")#removes fairly difficult
     #unique flesch_ease scores ['difficult' 'very_confusing' None 'fairly_difficult' 'standard' 'easy' 'fairly_easy']
     
     #flesch_scores(result, SQLcategoryFilter)
     #print('All flesch_scores Graphs constructed')

     makebarchart(result['year'],result.groupby(result.year)['flesch_kincaid'].transform('mean'),'Year',
                'Mean flesch_kincaid',SQLcategoryFilter)#lower is harder, so getting slightly easier since 2000
     makebarchart(result['year'],result.groupby(result.year)['smog'].transform('mean'),'Year',
                'Mean smog',SQLcategoryFilter)#years of education needed to read
          
     
     ##now make a loop to make all possible graphs against year
def flesch_scores(result, SQLcategoryFilter):
     result['contain_very_confusing']=result.flesch_ease.str.count("ery_confusing")
     print(result['contain_very_confusing'].head())
     makebarchart(result['year'],result.groupby(result.year)['contain_very_confusing'].transform('mean')*100,'Year',
                  'Mean percentage of privacy policies that are very_confusing to read (The most difficult measurement on scale)',SQLcategoryFilter)
     del result['contain_very_confusing']

     result['contain_just_difficult']=result.flesch_ease.str.count("difficult")-result.flesch_ease.str.count("_difficult")
     print(result['contain_just_difficult'].head())
     makebarchart(result['year'],result.groupby(result.year)['contain_just_difficult'].transform('mean')*100,'Year',
                  'Mean percentage of privacy policies that are difficult to read (The second most difficult measurement on scale)',SQLcategoryFilter)
     del result['contain_just_difficult']

     result['contain_fairly_difficult']=result.flesch_ease.str.count("fairly_difficult")
     print(result['contain_fairly_difficult'].head())
     #print(result['contain_fairly_difficult'].head())
     makebarchart(result['year'],result.groupby(result.year)['contain_fairly_difficult'].transform('mean')*100,'Year',
                 'Mean percentage of privacy policies that are fairly difficult to read (The third most difficult measurement on scale)',SQLcategoryFilter)
  
     result['contain_standard']=result.flesch_ease.str.count('standard')
     print(result['contain_standard'].head())
     makebarchart(result['year'],result.groupby(result.year)['contain_standard'].transform('mean')*100,'Year','Mean percentage of privacy policies that are standard in difficulty to read (The fourth most difficult measurement on scale)',SQLcategoryFilter)
   
   
     result['contain_easy']=result.flesch_ease.str.count("easy")##both types
     print(result['contain_easy'].head())
     makebarchart(result['year'],result.groupby(result.year)['contain_easy'].transform('mean')*100,'Year',
                  'Mean percentage of privacy policies that are easy or fairly_easy in difficulty to read (The fifth and sixth (lowest 2) most difficult measurement on scale)',SQLcategoryFilter)
    
     result['contain_confusing|difficult|fairly_difficult']=result.flesch_ease.str.count("confusing")+result.flesch_ease.str.count("difficult")
     print(result['contain_confusing|difficult|fairly_difficult'].head())
     makebarchart(result['year'],result.groupby(result.year)['contain_confusing|difficult|fairly_difficult'].transform('mean')*100,'Year',
                  'Mean percentage of privacy policies that contain confusing|difficult|fairly_difficult in difficulty to read (The fourth most difficult measurement on scale)',SQLcategoryFilter)

     del result['contain_confusing|difficult|fairly_difficult']
     del result['contain_fairly_difficult']
     del result['contain_standard']
     del result['contain_easy']

     result['contain_none']=result.flesch_ease.str.count("none")##both types
     print(result['contain_none'].head())
     makebarchart(result['year'],result.groupby(result.year)['contain_none'].transform('mean')*100,'Year',
                'Mean percentage of privacy policies that are rated as none (Not Applicable) in difficulty to read',SQLcategoryFilter)
     del result['contain_none']
 
                                                         
def makebarchart(x,y,xlabel,ylabel,SQLcategoryfilter):
   plt.rcParams["figure.figsize"] = (10,8)
   plt.bar(x = x,
   height = y,
   color = "midnightblue")

   titlelabel=str(ylabel)+' in privacy policies by '+str(xlabel)+' '+str(SQLcategoryfilter)#area in brackets in main title but not axis
   ref=0
   for i in range(0,len(ylabel)-1):
        if ylabel[i]=='(' and ref==0:
            ref=i   #print('ref',ref)
   if ref!=0:
       ylabel=ylabel[:ref]#makes y axis smaller
    
   plt.xticks(rotation = 45, fontsize = 13)
   plt.yticks(fontsize = 13)
    
   plt.title(titlelabel, fontsize = 16, fontweight = "bold")
   plt.xlabel(xlabel, fontsize = 13 )
   plt.ylabel(ylabel, fontsize = 13 )
   savelabel=str(ylabel)+' in privacy policies by '+str(xlabel)+' '+str(SQLcategoryfilter)
   savelabel=savelabel[:47]+str('.png')
  # savelabel=str(titlelabel)+str('.png')
   plt.savefig(savelabel)
   plt.show()
   print(titlelabel+' Graph created')

if __name__ == '__main__':
    MainCode(result)
    #create_connection(\"C:\\Users\\layto\\sqlite\")#
    
    
#move joins into one SQL statement