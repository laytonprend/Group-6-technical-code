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
#import sqlite3
#from sqlite3 import Error
import pandas as pd
#import numpy as np

#import psutil
#import sys
#import traceback

#import csv
#from csv import writer
from sklearn.utils import shuffle


import matplotlib.pyplot as plt
import seaborn as sns

import os#make folder

#from diff_match_patch import diff_match_patch
#fuzzymatch

def MakeFolder(path):
    try: #make folders going down to savepath
         os.mkdir(path) 
    except OSError as error: 
         #print(error)
         t=error
         #print('code continued')

def MainCode(result,SQLquery,CorrectionRequired):
     level=str(SQLquery.count(';'))
   #  global path
    # path= os.path.abspath(os.path.dirname(__file__))#temp
     #print(11)  
      
     mycodelocationpath= os.path.abspath(os.path.dirname(__file__))#+'\ Individual categories'
    
     #print('mycodelocationpath'+str(mycodelocationpath))#"C:/Users/layto/OneDrive/Documents/GitHub/Group-6-technica-lcode/"+
     path=mycodelocationpath+'\ '+str(level)
#os.path.abspath(os.path.dirname(__file__)),os.path.abspath(os.path.dirname(__file__)),SQLquery+\ Individual categories'
     MakeFolder(path)
    
     folderpath=mycodelocationpath+'\ '+str(level)+'\ '+str(SQLquery)
     MakeFolder(folderpath)
     
     GroupedRows=result.groupby(result.year)['total'].transform('sum')
     MakeFolder(savepath)
     GroupedDF=pd.DataFrame()
     if CorrectionRequired==True:#need to correct aggregations
     #prev 'year':result.groupby(result.year)['year'].transform('mean')
         #print('newyear\n',result.groupby('year').aggregate(lambda tdf: tdf.unique()))
         GroupedDF={'year':result.groupby(result.year)['year'].transform('mean'),'GroupedRows':GroupedRows,
                    'ChildCountMean':result.groupby(result.year)['ChildCountSum'].transform('sum')/GroupedRows
                    ,'lengthMean':result.groupby(result.year)['lengthSum'].transform('sum')/GroupedRows
                    ,'flesch_kincaid_Mean':result.groupby(result.year)['flesch_kincaid_Sum'].transform('sum')/GroupedRows
                    ,'smog_Mean':result.groupby(result.year)['smog_Sum'].transform('sum')/GroupedRows
                    }
         
    
   #      lengthyear=result.groupby(result.year)['length_Mean'].transform('sum')/result.groupby(result.year)['total'].transform('sum')
    #     flesch_kincaidyear=result.groupby(result.year)['flesch_kincaid_Mean'].transform('sum')/result.groupby(result.year)['total'].transform('sum')
     #    smogyear=result.groupby(result.year)['smog_Mean'].transform('sum')
         
     else:#if CorrectionRequired==False:#doesn't matter if transform is mean etc.
         GroupedDF={'year':result.groupby(result.year)['year'].transform('mean'),'GroupedRows':GroupedRows,
                    'ChildCountMean':result.groupby(result.year)['ChildCount'].transform('mean')
                    ,'lengthMean':result.groupby(result.year)['length_Mean'].transform('mean')
                    ,'flesch_kincaid_Mean':result.groupby(result.year)['flesch_kincaid_Mean'].transform('mean')
                    ,'smog_Mean':result.groupby(result.year)['smog_Mean'].transform('mean')
                    }
     GroupedDF=pd.DataFrame(GroupedDF)
     GroupedDF.sort_values(by=['year'], inplace=True)
     
     GroupedDF=pd.DataFrame(GroupedDF)
     GroupedDF.drop_duplicates(inplace=True)
     GroupedDF.to_csv(savepath+'\Data.csv', index=False)
     
    

     makebarchart(GroupedDF["year"],GroupedDF['GroupedRows'],'Year','relevant samples that year',SQLquery)
     #result['nlp']=result['policy_text'].str.count("Parental|parental|guardian|Guardian|child|Child|Child's|child's|Minor|minor|underage|child|kid|young|youth|young people|under-18|under-13|under 13|under 18|under 12|13 years old|under 13 years old|under 18 years old|age of 13|under the age of 18")##here is where to adjust what words ar being checked, not earlier on so other graphs
         
     #nlpyear=result.groupby(result.year)['ChildCount'].transform('mean')# should be mean anyway
     makebarchart(GroupedDF["year"],GroupedDF['ChildCountMean'],'Year','Mean count of child synonyms',SQLquery)
     

     makebarchart(GroupedDF['year'],GroupedDF['lengthMean'],'Year','Mean length',SQLquery)


     
     #flesch_kincaidyear=result.groupby(result.year)['flesch_kincaid_Mean'].transform('mean')
     makebarchart(GroupedDF['year'],GroupedDF['flesch_kincaid_Mean'],'Year',
                'Mean flesch_kincaid',SQLquery)#lower is harder, so getting slightly easier since 2000
     
     #smogyear=result.groupby(result.year)['smog_Mean'].transform('mean')
     makebarchart(GroupedDF['year'],GroupedDF['smog_Mean'],'Year',
                'Mean smog',SQLquery)#years of education needed to read
    # GroupedDF.to_csv(mycodelocationpath+'\RanData.csv', index=False)
    
     plt.figure(figsize=(10,8),dpi=80)
     sns.pairplot(GroupedDF,kind='reg')#,lw=7)#linewidth=4)#,hue='species')
     plt.show()#marginal distributions, histograms, so number of samples?
     return GroupedDF
     
'''
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
 '''
                                                     
def makebarchart(x,y,xlabel,ylabel,SQLquery):
    
   #savelabelSQLquery=SQLquery
   SQLquery='when categories are related to '+SQLquery 
   plt.rcParams["figure.figsize"] = (10,8)
  # plt.bar(x = x,
   #height = y,
   #color = "blue")
   plt.plot(x,y,linewidth=7)

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
   plt.savefig(savepath+"\."+savelabel)
   plt.show()
  # print(titlelabel+' Graph created')
   
   
plt.style.use('dark_background') 
File=pd.read_csv('Categories Agg.csv')
File['ChildCountSum']=File['ChildCount']
File['ChildCount']=File['ChildCount']/File['total']#childcount is sum
#sum total,
File['lengthSum']=File['total']*File['length_Mean']#sum length
File['flesch_kincaid_Sum']=File['total']*File['flesch_kincaid_Mean']#sum flesch kincaid
File['smog_Sum']=File['total']*File['smog_Mean']#sum smog
#print(File.head())
#print(File.tail())
#print(File.columns)
Categories=shuffle(File['Categories'].unique())
TimesRan=0
Head=True
CentralDF=pd.DataFrame()
for i in Categories:
    i= str(i)
    TimesRan+=1
    print(TimesRan,' times ran\n',i)
    #TempFile=File
   # if not pd.isnull(i):
    
    Filter=File['Categories'].str.contains(i)
    Filter= Filter.fillna(False)#nulls are false
    #print(Filter)
    TempFile=File[Filter]
    UniqueCategories=TempFile['Categories'].unique()
    CategoriesInWildcard=''
    for x in UniqueCategories:
        CategoriesInWildcard+=str(x)+' - '#InWildcarnt(CategoriesInWildcard)
   # print(CategoriesInWildcard)    
    global savepath
    savepath=os.path.abspath(os.path.dirname(__file__))+'\ '+str(i.count(';'))+'\ '+i+'\ Category Wildcard Match'
    
    
    try:
        RanData1=MainCode(TempFile,i,True)
    except MemoryError as error:
            # Output expected MemoryErrors
            print('error')
    
    Filter=File['Categories']==i
    #Filter=File['Categories'].count(i)>0
    #print(File['run'])
    TempFile=File[Filter]
    savepath=os.path.abspath(os.path.dirname(__file__))+'\ '+str(i.count(';'))+'\ '+i+'\ Exact Match'
    try:
        RanData2=MainCode(TempFile,i,False)
    except MemoryError as error:
            # Output expected MemoryErrors
            print('error')
    RanData1['Category Search']=i
    RanData1['Categories returned']=CategoriesInWildcard
    RanData1['Wildcard Search?']=True
    RanData1['Categories returned']=i
    RanData2['Category search']=i
    RanData2['Wildcard Search?']=False
    #CentralDF.append(RanData1)
    #CentralDF.append(RanData2)
    frames=[CentralDF,RanData1,RanData2]
    CentralDF=pd.concat(frames)
  #  print(CentralDF)
   # print(CentralDF.head())
    #print(CentralDF.tail())
    #print(RanData2)
CentralDF.to_csv('RanData.csv', mode='w', header=Head,index=False)

#    except MemoryError as error:
 #       print(error)
     