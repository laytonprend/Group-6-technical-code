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
    SQLcategoryFilter="adult"
    sites = pd.read_sql_query("SELECT id, categories from sites WHERE categories LIKE '%"+SQLcategoryFilter+"%'",conn)
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
    print('categories\n',sites['categories'].unique())#all categories that contaiin tech or media?
    print('sites table imported')
    print( sites.head())
    
    policy_snapshots = pd.read_sql_query("SELECT id, year, policy_url, phase, policy_text_id, site_id,  classifier_probability from policy_snapshots", conn)
    #del result['policy_html_id']
    print('homepage url',policy_snapshots)
    #del result['policy_reader_view_html_id']
    #del result['site_id']
    print('policy_snapshots table imported\n',policy_snapshots.head())
    
    result = pd.merge(sites, policy_snapshots, how="inner", on=["id", "id"])
    
    print('merge1 result all columns\n',result.columns)
    del result['id']
    #del result['id_x']
    print('merge1 result\n',result.columns)
    return join2_result_policy_texts(conn,result), SQLcategoryFilter
def UpdatedPrivacyPolicyClassifierColumnInJoin2(result):
    print('rows first\n\n',(result.shape))
    #result.groupby(result.year)['flesch_kincaid'].transform('mean')
    print('start test')
#    del result['flesch_ease']
 #   del result['flesch_kincaid']
  #  del result['smog']
   # del result['length']
   # del result['phase']
   # del result['policy_text_id']
    
    print('start test')
    #break into 2 df
    #join with year-1
    #similarity to year before using other code
    result2=result
    result['join_condition']=str(result['year'])+str(result['phase'])+str(result['categories'])+str(result['id'])
    
    
    result2['join_condition year-1']=str(result2['year']-1)+str(result2['phase'])+str(result2['categories'])+str(result2['id'])#possibly do if else that makes 1 phase before
    result2['LastYearPrivacyPolicy']=result2['policy_text']#RENAME INSTEAD?
    
    
    del result2['policy_text']
    del result2['categories']
    del result2['id']
    del result2['flesch_ease']
    del result2['flesch_kincaid']
    del result2['smog']
    del result2['length']
    del result2['phase']
    #del result2['policy_text_id']
    del result2['site_id']
    del result2['classifier_probability']
    del result2['year']
    print('result2 columns', result2.columns)
    

    #    TempComparison=pd.dataframe()
 #   TempComparison['year-1']=result['year']-1
    
  #  TempComparison['policy_text year-1']=result['policy_text']
   # TempComparison['join_condition_year_before']=str(TempComparison['year'])+str(TempComparison['categories'])+str(TempComparison['id'])
    #print(TempComparison)
    result = pd.merge(result, result2, how="inner", on=["join_condition", "join_condition year-1"])
    result2=0
    del result['join_condition']
    print('rows after\n\n',result.shape)
    print('column after\n\n',result.column)
    #test count of rows in each join type?
    print('results analysis done',result)
    #del result['year-1']
    
    
    
    
    return(result)

def join2_result_policy_texts(conn,result):
    #flesch_kincaid, smog,
    policy_texts = pd.read_sql_query("SELECT id, policy_text,    length from policy_texts", conn)
    
    #homepage_snapshot_redirected_url

    print(policy_texts.columns)
    print('policy_texts table imported\n',policy_texts.head())
    
    result = pd.merge(policy_texts, result, on=None, left_on="id", right_on="policy_text_id",  how="inner")# on=["id","policy_text_id"])
    del result['id']
    #memory error workaround
    policy_texts = pd.read_sql_query("SELECT id, flesch_ease, flesch_kincaid , smog from policy_texts", conn)
    print(policy_texts.columns)
    print('policy_texts table imported\n',policy_texts.head())
    
    result = pd.merge(policy_texts, result, on=None, left_on="id", right_on="policy_text_id",  how="inner")# on=["id","policy_text_id"])
   
    print('merge 2 all columns\n',result.columns)
    #print('unique flesch_ease scores',result['flesch_ease'].unique())
    #print(result.columns)
    del result['policy_text_id']
    
    
    
    #result=UpdatedPrivacyPolicyClassifierColumnInJoin2(result)
    
    
    
    
    # del result['id']
    print('merge 2\n',result.columns)
    print(result.head())
    #del result['']
    #del result['']
    #return(result)
    
    return(join3_result_alexa_ranks(conn,result))
def join3_result_alexa_ranks(conn,result):
    alexa_ranks = pd.read_sql_query("SELECT site_id, rank from alexa_ranks", conn)
    print(alexa_ranks.rank)
    print('alexa_ranks table imported\n', alexa_ranks.head())
    
    result = pd.merge(alexa_ranks, result, on=None, left_on="site_id", right_on="site_id",  how="inner")
    
    return(result)
    
    

    
    


def DatabaseInterrogation():
    database = r"C:\Users\layto\sqlite\db"#.xz?

    # create a database connection
    conn = create_connection(database)#2nd funct called
    with conn:
     #   print("1. Query task by priority:")
      #  select_task_by_priority(conn, 1)

        print("2. Query all tasks")
        result, SQLcategoryFilter=join1_sites__policy_snapshots(conn)##3rd function called
        return result, SQLcategoryFilter 


if __name__ == '__main__':
    result, SQLcategoryFilter=DatabaseInterrogation()   #start
    print('Database processing complete')
        








def make_folder(SQLcategoryFilter):
    # Directory
    #directory = SQLcategoryFilter
  
# Parent Directory path
    #path = "C:/Users/layto/OneDrive/Documents/GitHub/Group-6-technica-lcode/"+SQLcategoryFilter
#"D:/Pycharm projects/  

    #path = 
    
# Create the directory 
# 'GeeksForGeeks' in 
# '/home / User / Documents' 
    global path 
    mycodelocationpath= os.path.abspath(os.path.dirname(__file__))
    
    print('mycodelocationpath'+str(mycodelocationpath))#"C:/Users/layto/OneDrive/Documents/GitHub/Group-6-technica-lcode/"+
    path=mycodelocationpath+'\ '+str(SQLcategoryFilter)

    try: 
        os.mkdir(path) 
    except OSError as error: 
        print(error)  
    print('code continued')
   
    

def MainCode(result,SQLcategoryFilter):
     """
     Query all rows in the tasks table
     :param conn: the Connection object
     :return:
     """
     
     
     
     make_folder(SQLcategoryFilter)

     #result['child']= re.findall('child[^, ]+',result['policy_text'])
     columns=result.columns
     fieldnames=[]
     for x in columns:
         #print(x)
         fieldnames.append(str(x))
     print('fieldnames',fieldnames)
     
     
     
     
     #result['updated privacy policy?']=UpdatedPrivacyPolicyClassifier(result)





     result['nlp']=result['policy_text'].str.count("Parental|parental|guardian|Guardian|child|Child|Child's|child's|Minor|minor|underage|child|kid|young|youth|young people|under-18|under-13|under 13|under 18|under 12|13 years old|under 13 years old|under 18 years old|age of 13|under the age of 18")##here is where to adjust what words ar being checked, not earlier on so other graphs
     result['nlpGDPR']=result['policy_text'].str.count("GDPR")##here is where to adjust what words ar being checked, not earlier on so other graphs
 
    #can be made

     #result['year'] = pd.to_datetime(result.year)
     #result.groupby(result.year)['nlp'].transform('mean')
     #nlp=nlp.agg('avg')
     #nlp.groupby(nlp['year'].dt.year)['policy_text'].agg(['mean'])
     print('nlp',result['nlp'])
     #fieldnames.remove('year')
     #SQLcategoryFilter="when categories are related to gaming"

    
     #working hashed for efficiency
     makebarchart(result["year"],result.groupby(result.year)['categories'].transform('count'),'Year','relevant samples that year',SQLcategoryFilter)
     makebarchart(result["year"],result.groupby(result.year)['nlp'].transform('mean'),'Year','Mean count of child synonyms',SQLcategoryFilter)
     del result['nlp']
     makebarchart(result["year"],result.groupby(result.year)['nlpGDPR'].transform('mean'),'Year','Mean count of GDPR',SQLcategoryFilter)
     del result['nlpGDPR']
     makebarchart(result['year'],result.groupby(result.year)['length'].transform('mean'),'Year','Mean length',SQLcategoryFilter)

     #result['contain_easy'] = result['flesch_ease'].str.count.contains('easy')*100
     #result['contain_easy'] = result['flesch_ease'].str.count.contains('easy')*100
     #result['contain_difficult|confusing']=result.flesch_ease.str.count("difficult|confusing")-result.flesch_ease.str.count("_difficult")#removes fairly difficult
     #unique flesch_ease scores ['difficult' 'very_confusing' None 'fairly_difficult' 'standard' 'easy' 'fairly_easy']
     
     

     makebarchart(result['year'],result.groupby(result.year)['flesch_kincaid'].transform('mean'),'Year',
                'Mean flesch_kincaid',SQLcategoryFilter)#lower is harder, so getting slightly easier since 2000
     makebarchart(result['year'],result.groupby(result.year)['smog'].transform('mean'),'Year',
                'Mean smog',SQLcategoryFilter)#years of education needed to read
          
     
     #flesch_scores(result, SQLcategoryFilter)
     print('All flesch_scores Graphs constructed')
     
     
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
#     ''' 
#     result['contain_confusing|difficult|fairly_difficult']=result.flesch_ease.str.count("confusing")+result.flesch_ease.str.count("difficult")
#     print(result['contain_confusing|difficult|fairly_difficult'].head())
#     makebarchart(result['year'],result.groupby(result.year)['contain_confusing|difficult|fairly_difficult'].transform('mean')*100,'Year',
##                  'Mean percentage of privacy policies that contain confusing|difficult|fairly_difficult in difficulty to read (The fourth most difficult measurement on scale)',SQLcategoryFilter)
#'''
     #del result['contain_confusing|difficult|fairly_difficult']
     del result['contain_fairly_difficult']
     del result['contain_standard']
     del result['contain_easy']

     result['contain_none']=result.flesch_ease.str.count("none")##both types
     print(result['contain_none'].head())
     makebarchart(result['year'],result.groupby(result.year)['contain_none'].transform('mean')*100,'Year',
                'Mean percentage of privacy policies that are rated as none (Not Applicable) in difficulty to read',SQLcategoryFilter)
     del result['contain_none']
 
                                                         
def makebarchart(x,y,xlabel,ylabel,SQLcategoryfilter):
    
   savelabelSQLcategoryfilter=SQLcategoryfilter
   SQLcategoryfilter='when categories are related to '+SQLcategoryfilter 
   plt.rcParams["figure.figsize"] = (10,8)
   plt.bar(x = x,
   height = y,
   color = "blue")

   titlelabel=str(SQLcategoryfilter)+' '+str(ylabel)+' in privacy policies by '+str(xlabel)#area in brackets in main title but not axis
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
   #savelabel=str(savelabelSQLcategoryfilter)+' '+str(ylabel)+' in privacy policies by '+str(xlabel)#+' '+str(SQLcategoryfilter)
   savelabel=str(ylabel)+' in privacy policies by '+str(xlabel)#+' '+str(SQLcategoryfilter)
   savelabel=savelabel[:47]+str('.png')
  # savelabel=str(titlelabel)+str('.png')
   plt.savefig(path+"\."+savelabel)
   plt.show()
   print(titlelabel+' Graph created')

if __name__ == '__main__':
    MainCode(result,SQLcategoryFilter)
    #create_connection(\"C:\\Users\\layto\\sqlite\")#
    
    
#move joins into one SQL statement