# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 20:21:57 2022

@author: layto
"""
#rmemeber to open SQLite3
#PIP INSTALL SQLITE3
#.open DB

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




def MainCode(result,SQLquery,level):
   #  global path
    # path= os.path.abspath(os.path.dirname(__file__))#temp
     print(11)  
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
     except MemoryError as error:
            # Output expected MemoryErrors
            print('memory error')
            '''        try:
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
                DatabaseInterrogationLoop(SQLRUN,i[0],conn)
                '''
     #result['child']= re.findall('child[^, ]+',result['policy_text'])
    # columns=result.columns
    # fieldnames=[]
    # for x in columns:
    #        #print(x)
    #    fieldnames.append(str(x))
    # print('fieldnames',fieldnames)
     
     
     
    
     #print('nlp',result['nlp'])
     #fieldnames.remove('year')
     #SQLquery="when categories are related to gaming"

    
     #working hashed for efficiency
     
     print(11)    
     makebarchart(result["year"],result.groupby(result.year)['total'].transform('sum'),'Year','relevant samples that year',SQLquery)
     #result['nlp']=result['policy_text'].str.count("Parental|parental|guardian|Guardian|child|Child|Child's|child's|Minor|minor|underage|child|kid|young|youth|young people|under-18|under-13|under 13|under 18|under 12|13 years old|under 13 years old|under 18 years old|age of 13|under the age of 18")##here is where to adjust what words ar being checked, not earlier on so other graphs
         
     nlpyear=result.groupby(result.year)['ChildCount'].transform('mean')# should be mean anyway
     makebarchart(result["year"],nlpyear,'Year','Mean count of child synonyms',SQLquery)
     
         #result['nlpGDPR']=result['policy_text'].str.count("GDPR")##here is where to adjust what words ar being checked, not earlier on so other graphs
         
         #nlpGDPRyear=result.groupby(result.year)['nlpGDPR'].transform('mean')
         #makebarchart(result["year"],nlpGDPRyear,'Year','Mean count of GDPR',SQLquery)
     #del result['nlpGDPR']
     lengthyear=result.groupby(result.year)['length_Mean'].transform('mean')
     makebarchart(result['year'],lengthyear,'Year','Mean length',SQLquery)


     
     flesch_kincaidyear=result.groupby(result.year)['flesch_kincaid_Mean'].transform('mean')
     makebarchart(result['year'],flesch_kincaidyear,'Year',
                'Mean flesch_kincaid',SQLquery)#lower is harder, so getting slightly easier since 2000
     
     smogyear=result.groupby(result.year)['smog_Mean'].transform('mean')
     makebarchart(result['year'],smogyear,'Year',
                'Mean smog',SQLquery)#years of education needed to read
          
     
     #flesch_scores(result, SQLquery)
     '''print('All flesch_scores Graphs constructed')
     
     #save in Excel
     
     print('now make df')
     uniquecategories=''
     uniquecategories=''
     for x in result['categories'].unique():
         #print(x)
         uniquecategories=uniquecategories+'. '+str(x)
     #print(uniquecategories)
     print('SQLquery checker',SQLquery)
     data={'SQLsearchHistorical':[SQLquery],
      'categories_included_in_search':uniquecategories,
      'level':[level],
      'rows':[result.groupby(result.year)['categories'].transform('count').sum()],#possibly remove grouby year
      'flesch_kincaid_max':[flesch_kincaidyear.max()],#line chart approach
      'flesch_kincaid_min':[flesch_kincaidyear.min()],
      'flesch_kincaid_mean':[flesch_kincaidyear.mean()],
      'smog_max':[smogyear.max()],
      'smog_min':[smogyear.min()],
      'smog_mean':[smogyear.mean()],
      'child_synonyms_max':[nlpyear.max()],
      'child_synonyms_min':[nlpyear.min()],
      'child_synonyms_mean':[nlpyear.mean()],
      #'GDPR max':[nlpGDPRyear.max()],
      #'GDPR min':[nlpGDPRyear.min()],
      'length max':[lengthyear.max()],
      'length min':[lengthyear.min()],
      'length mean':[lengthyear.mean()] 
     
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

     '''
     ##now make a loop to make all possible graphs against year
def flesch_scores(result, SQLquery):
     result['contain_very_confusing']=result.flesch_ease.str.count("ery_confusing")
     print(result['contain_very_confusing'].head())
     makebarchart(result['year'],result.groupby(result.year)['contain_very_confusing'].transform('mean')*100,'Year',
                  'Mean percentage of privacy policies that are very_confusing to read (The most difficult measurement on scale)',SQLquery)
     del result['contain_very_confusing']

     result['contain_just_difficult']=result.flesch_ease.str.count("difficult")-result.flesch_ease.str.count("_difficult")
     print(result['contain_just_difficult'].head())
     makebarchart(result['year'],result.groupby(result.year)['contain_just_difficult'].transform('mean')*100,'Year',
                  'Mean percentage of privacy policies that are difficult to read (The second most difficult measurement on scale)',SQLquery)
     del result['contain_just_difficult']

     result['contain_fairly_difficult']=result.flesch_ease.str.count("fairly_difficult")
     print(result['contain_fairly_difficult'].head())
    
     makebarchart(result['year'],result.groupby(result.year)['contain_fairly_difficult'].transform('mean')*100,'Year',
                 'Mean percentage of privacy policies that are fairly difficult to read (The third most difficult measurement on scale)',SQLquery)
  
     result['contain_standard']=result.flesch_ease.str.count('standard')
     print(result['contain_standard'].head())
     makebarchart(result['year'],result.groupby(result.year)['contain_standard'].transform('mean')*100,'Year','Mean percentage of privacy policies that are standard in difficulty to read (The fourth most difficult measurement on scale)',SQLquery)
   
   
     result['contain_easy']=result.flesch_ease.str.count("easy")##both types
     print(result['contain_easy'].head())
     makebarchart(result['year'],result.groupby(result.year)['contain_easy'].transform('mean')*100,'Year',
                  'Mean percentage of privacy policies that are easy or fairly_easy in difficulty to read (The fifth and sixth (lowest 2) most difficult measurement on scale)',SQLquery)
     del result['contain_fairly_difficult']
     del result['contain_standard']
     del result['contain_easy']

     result['contain_none']=result.flesch_ease.str.count("none")##both types
     print(result['contain_none'].head())
     makebarchart(result['year'],result.groupby(result.year)['contain_none'].transform('mean')*100,'Year',
                'Mean percentage of privacy policies that are rated as none (Not Applicable) in difficulty to read',SQLquery)
     del result['contain_none']
 
                                                     
def makebarchart(x,y,xlabel,ylabel,SQLquery):
    
   #savelabelSQLquery=SQLquery
   SQLquery='when categories are related to '+SQLquery 
   plt.rcParams["figure.figsize"] = (10,8)
   plt.bar(x = x,
   height = y,
   color = "blue")

   titlelabel=str(SQLquery)+' '+str(ylabel)+' in privacy policies by '+str(xlabel)#area in brackets in main title but not axis
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
   #savelabel=str(savelabelSQLquery)+' '+str(ylabel)+' in privacy policies by '+str(xlabel)#+' '+str(SQLquery)
   savelabel=str(ylabel)+' in privacy policies by '+str(xlabel)#+' '+str(SQLquery)
   savelabel=savelabel[:47]+str('.png')
  # savelabel=str(titlelabel)+str('.png')
   plt.savefig(path+"\."+savelabel)
   plt.show()
   print(titlelabel+' Graph created')
   
   
   
File=pd.read_csv('Categories Agg.csv')
print(File.head())
print(File.tail())
print(File.columns)
columns=File['Categories'].unique()
for i in columns:
    #TempFile=File
   # if not pd.isnull(i):
    print(i)
    Filter=File['Categories']==i
    #print(File['run'])
    TempFile=File[Filter]
    print(TempFile)
    i=str(i)
    MainCode(TempFile,i,i.count(';'))
    
    '''
if __name__ == '__main__':
    

    MainCode()   #start
    print('Database processing complete')'''