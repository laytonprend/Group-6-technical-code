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
import numpy as np

#import psutil
#import sys
#import traceback

import csv


import matplotlib.pyplot as plt
import seaborn as sns

import os#make folder

#from diff_match_patch import diff_match_patch
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

def join1_sites__policy_snapshots(conn,SQLcategoryFilter,level):
    #sites = pd.read_sql_query("SELECT id, categories from sites WHERE (categories LIKE '%social%' OR categories LIKE '%tech%' OR categories LIKE '%media%') AND  ( (categories LIKE '%sharing%')  OR  categories LIKE '%messageboard%' OR categories LIKE '%blogsandpersonal%') AND NOT categories LIKE '%news%'",conn)
    #SQLcategoryFilter="adult"
    #SQLcategoryFilter=SQLcategoryFilter
    #print('joimn1 start sql',SQLcategoryFilter)
    sites = pd.read_sql_query("SELECT id, categories from sites WHERE categories LIKE '%"+str(SQLcategoryFilter)+"%'",conn)
    
    #temp
    
    
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
    print('join 1 end sql',SQLcategoryFilter)
    join2_result_policy_texts(conn,result,SQLcategoryFilter,level)
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
    
    
    
    
    #result

def join2_result_policy_texts(conn,result,SQLcategoryFilter,level):
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
    print('join 2 sql',SQLcategoryFilter)
    join3_result_alexa_ranks(conn,result,SQLcategoryFilter,level)
def join3_result_alexa_ranks(conn,result,SQLcategoryFilter,level):
    alexa_ranks = pd.read_sql_query("SELECT site_id, rank from alexa_ranks", conn)
    print(alexa_ranks.rank)
    print('alexa_ranks table imported\n', alexa_ranks.head())
    
    result = pd.merge(alexa_ranks, result, on=None, left_on="site_id", right_on="site_id",  how="inner")
    print('join 3 sql',SQLcategoryFilter)
    MainCode(result,SQLcategoryFilter,level)
    #return(result)
    
    

    
    


def DatabaseInterrogation():
    database = r"C:\Users\layto\sqlite\db"#.xz?

    # create a database connection
    conn = create_connection(database)#2nd funct called
    with conn:
     #   print("1. Query task by priority:")
      #  select_task_by_priority(conn, 1)

        print("2. Query all tasks")
        #make so loops in db then runs
        #only if category not in excel?
        left=pd.read_csv('SQL category run summary.csv')#previously ran
        print('left',left)
        right=pd.read_csv('Categories lookup.csv')
        print('right',right)
        SQLRUN = pd.merge(left, right, on=None, left_on="SQLsearchHistorical", right_on="categories",  how="right")
        #SQLRUN=SQLRUN##left join
        print('joined',SQLRUN)
        #SQLRUN = SQLRUN['categories_historic'].str.extract('^(N/A|NA|na|n/a)')
        filter2=SQLRUN['SQLsearchHistorical'].notnull()==False#.null()
        #print(filter2)
        SQLRUN=SQLRUN[filter2]
        #SQLRUN=SQLRUN['categories','categoriescountsemicolon']
        SQLRUN=SQLRUN[['categories','categoriescountsemicolon']]
        print('newsqlrun',SQLRUN)
        
        #filter
        #print(SQLRUN)#print(2,SQLRUN.categories_historic.notnull())
        #loop SQLcategoryFilter
        #'SQlcategoryQueries=SQLRUN['categories']
        #print(SQlcategoryQueries)
        #print(SQLRUN['categories'].unique())
        print(1)
        DatabaseInterrogationLoop(SQLRUN,0,conn)
def DatabaseInterrogationLoop(SQLRUN,StartIndex,conn):
        #SQLRUN['index']=SQLRUN.index()
        for i in SQLRUN.itertuples():
            print(i)
            #print(i[3])#SQLquery
            #print(i[4])#count colon for what level folder to gom into
            #global level
            print('i0',i[0])
            print('i1',i[1])
            print('i2 level',i[2])
            #print('i3',i[3])#close file?, so can write to it further down
            
            level=i[2]
            SQLquery=str(i[1])
            #try:
                
                
            if i[0]>0 and i[0]>StartIndex:#index
                    print('SQLquery',SQLquery)
                    print('SQLquery',SQLquery)
                    global path 
                    mycodelocationpath= os.path.abspath(os.path.dirname(__file__))
    
                    print('mycodelocationpath'+str(mycodelocationpath))#"C:/Users/layto/OneDrive/Documents/GitHub/Group-6-technica-lcode/"+
                    path=mycodelocationpath+'\ '+str(level)

                    try: 
                        os.mkdir(path) 
                    except OSError as error: 
                        print(error)  
                    print('code continued, level folder')
                    path=mycodelocationpath+'\ '+str(level)+'\ '+str(SQLquery)

                    try: 
                        os.mkdir(path) 
                        print('code continued',path,SQLquery)
                        try:
                            join1_sites__policy_snapshots(conn,str(SQLquery),level)
                        except MemoryError as error:
            # Output expected MemoryErrors
                            print('memory error')
                #SQLquery.to_csv('MemoryErrorSearches.csv', mode='a', index=False, header=False)#log_excep(error)
                            fields=[SQLquery]

                            with open(r'MemoryErrorSearches.csv', 'a') as f:
                                writer = csv.writer(f)
                                writer.writerow(fields)
               # df3.to_csv('test SQL category run summary2.csv', mode='a', index=False,Header=False)
                            DatabaseInterrogationLoop(SQLRUN,i[0],conn)#recall when error
                
                            break
                        except Exception as exception:
                            print('memory error2')
            # Output unexpected Exceptions.
                #log_exception(exception, False)
                #SQLquery.to_csv('MemoryErrorSearches.csv', mode='a', index=False, header=False)#log_excep(error)
                            fields=[SQLquery]

                            with open(r'MemoryErrorSearches.csv', 'a') as f:
                                writer = csv.writer(f)
                                writer.writerow(fields)
                            DatabaseInterrogationLoop(SQLRUN,i[0],conn)#recall when error
                            break
                    except OSError as error: #if folder e.g. /1/games made then assumes graphs are made and doesn't create
                        print(error)
                        DatabaseInterrogationLoop(SQLRUN,i[0],conn)#recall when error
                        break

     #result['child'
                        
            


     #result['child'                    
            #join1_sites__policy_snapshots(conn,i[3],level)
     #   for i in range( len(SQLRUN)) :
      #      print(i)
       #     print(SQLRUN.loc[i,'categoriescountsemicolon'])#, df.loc[i, "Age"])
        ###    print('row',i)
           # print('QUERY ',x,'\n\n\n\n\n\n\n\n\n\n',x)
            #join1_sites__policy_snapshots(conn,x)#pass levels through
            
            #print(SQlcategoryQueries.loc[i])#, df.loc[i, "Age"])
        
        #join1_sites__policy_snapshots(conn,SQLcategoryFilter)##3rd function called
        #return result, SQLcategoryFilter 



        








'''def make_folder(SQLcategoryFilter,level):
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
    path=mycodelocationpath+'\ '+str(level)

    try: 
        os.mkdir(path) 
    except OSError as error: 
        print(error)  
    print('code continued')
    path=mycodelocationpath+'\ '+str(level)+'\ '+str(SQLcategoryFilter)

    try: 
        os.mkdir(path) 
    except OSError as error: 
        print(error)  
    print('code continued')'''
   
    

def MainCode(result,SQLcategoryFilter,level):
     """
     Query all rows in the tasks table
     :param conn: the Connection object
     :return:
     """
     #print('MAINCODE SQL\n\n\n\n\n\n',SQLcategoryFilter)
     
     
     
     #make_folder(SQLcategoryFilter,level)
     '''   global path 
     mycodelocationpath= os.path.abspath(os.path.dirname(__file__))
    
     print('mycodelocationpath'+str(mycodelocationpath))#"C:/Users/layto/OneDrive/Documents/GitHub/Group-6-technica-lcode/"+
     path=mycodelocationpath+'\ '+str(level)

     try: 
         os.mkdir(path) 
     except OSError as error: 
         print(error)  
     print('code continued')
     path=mycodelocationpath+'\ '+str(level)+'\ '+str(SQLcategoryFilter)

     try: 
         os.mkdir(path) 
         print('code continued')'''

     #result['child']= re.findall('child[^, ]+',result['policy_text'])
     columns=result.columns
     fieldnames=[]
     for x in columns:
            #print(x)
        fieldnames.append(str(x))
     print('fieldnames',fieldnames)
     
     
     
    
     print('nlp',result['nlp'])
     #fieldnames.remove('year')
     #SQLcategoryFilter="when categories are related to gaming"

    
     #working hashed for efficiency
     
         
     makebarchart(result["year"],result.groupby(result.year)['categories'].transform('count'),'Year','relevant samples that year',SQLcategoryFilter)
     result['nlp']=result['policy_text'].str.count("Parental|parental|guardian|Guardian|child|Child|Child's|child's|Minor|minor|underage|child|kid|young|youth|young people|under-18|under-13|under 13|under 18|under 12|13 years old|under 13 years old|under 18 years old|age of 13|under the age of 18")##here is where to adjust what words ar being checked, not earlier on so other graphs
         
     nlpyear=result.groupby(result.year)['nlp'].transform('mean')
     makebarchart(result["year"],nlpyear,'Year','Mean count of child synonyms',SQLcategoryFilter)
     
         #result['nlpGDPR']=result['policy_text'].str.count("GDPR")##here is where to adjust what words ar being checked, not earlier on so other graphs
         
         #nlpGDPRyear=result.groupby(result.year)['nlpGDPR'].transform('mean')
         #makebarchart(result["year"],nlpGDPRyear,'Year','Mean count of GDPR',SQLcategoryFilter)
     #del result['nlpGDPR']
     lengthyear=result.groupby(result.year)['length'].transform('mean')
     makebarchart(result['year'],lengthyear,'Year','Mean length',SQLcategoryFilter)


     
     flesch_kincaidyear=result.groupby(result.year)['flesch_kincaid'].transform('mean')
     makebarchart(result['year'],flesch_kincaidyear,'Year',
                'Mean flesch_kincaid',SQLcategoryFilter)#lower is harder, so getting slightly easier since 2000
     smogyear=result.groupby(result.year)['smog'].transform('mean')
     makebarchart(result['year'],smogyear,'Year',
                'Mean smog',SQLcategoryFilter)#years of education needed to read
          
     
     #flesch_scores(result, SQLcategoryFilter)
     print('All flesch_scores Graphs constructed')
     
     #save in Excel
     
     print('now make df')
   #  df = pd.DataFrame(my_array, columns = ['SQLsearchHistorical','categories_included_in_search','level','rows','flesch_kincaid_max','flesch_kincaid_min',
    #                                        'smog_max','smog_min','child_synonyms_max','child_synonyms_min',
     #                                       'GDPR max','GDPR min','length max','length min'
      #                                      ])
     #print(df)
     #order=np.array([categories historicalflesch_ease,flesch_kincaid,smog,nlp,nlpGDPR,length])#just write max and min
     #df.to_csv('SQL category run summary.csv', mode='w', index=False, header=False)    
     uniquecategories=''
     uniquecategories=''
     for x in result['categories'].unique():
         #print(x)
         uniquecategories=uniquecategories+'. '+str(x)
     #print(uniquecategories)
     print('SQLcategoryFilter checker',SQLcategoryFilter)
     data={'SQLsearchHistorical':[SQLcategoryFilter],
      'categories_included_in_search':uniquecategories,
      'level':[level],
      'rows':[result.groupby(result.year)['categories'].transform('count').sum()],
      'flesch_kincaid_max':[flesch_kincaidyear.max()],
      'flesch_kincaid_min':[flesch_kincaidyear.min()],
      'smog_max':[smogyear.max()],
      'smog_min':[smogyear.min()],
      'child_synonyms_max':[nlpyear.max()],
      'child_synonyms_min':[nlpyear.min()],
      #'GDPR max':[nlpGDPRyear.max()],
      #'GDPR min':[nlpGDPRyear.min()],
      'length max':[lengthyear.max()],
      'length min':[lengthyear.min()]
      
     
      }
#my_array = np.array(arr)#maybe change to max of by year mean?                   
#print('now make df')
     SQLrunSummary = pd.DataFrame(data)
     print(SQLrunSummary)
     #order=np.array([categories historicalflesch_ease,flesch_kincaid,smog,nlp,nlpGDPR,length])#just write max and min
     SQLrunSummary.to_csv('SQL category run summary2.csv', mode='a', index=False, Header=False)
     SQLrunSummary.to_csv(path+"\."+'SQL category run summary.csv', mode='w', index=False)
         #path+"\."
     #result.to_csv('Categories lookup.csv', mode='a', index=False, header=False)
     #write first time then changeto append
     #pass levels through then set up folder saving structure
     #way to append SQLsummary too?3
 #    except OSError as error: #if folder e.g. /1/games made then assumes graphs are made and doesn't create
  #       print(error)  
     
     
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
    
   #savelabelSQLcategoryfilter=SQLcategoryfilter
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

#if __name__ == '__main__':
 #   MainCode(result,SQLcategoryFilter)
    #create_connection(\"C:\\Users\\layto\\sqlite\")#
    
    
#move joins into one SQL statement
if __name__ == '__main__':
    
   # result, SQLcategoryFilter=
    DatabaseInterrogation()   #start
    print('Database processing complete')