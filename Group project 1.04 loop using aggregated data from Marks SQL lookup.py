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

def MakeFolder(path):
    try: #make folders going down to savepath
         os.mkdir(path) 
    except OSError as error: 
         print(error)  
         print('code continued')

def MainCode(result,SQLquery,CorrectionRequired):
     level=str(SQLquery.count(';'))
   #  global path
    # path= os.path.abspath(os.path.dirname(__file__))#temp
     print(11)  
      
     mycodelocationpath= os.path.abspath(os.path.dirname(__file__))#+'\ Individual categories'
    
     print('mycodelocationpath'+str(mycodelocationpath))#"C:/Users/layto/OneDrive/Documents/GitHub/Group-6-technica-lcode/"+
     path=mycodelocationpath+'\ '+str(level)
#os.path.abspath(os.path.dirname(__file__)),os.path.abspath(os.path.dirname(__file__)),SQLquery+\ Individual categories'
     MakeFolder(path)
    
 #    try: 
  #       os.mkdir(path) 
   #  except OSError as error: 
    #     print(error)  
     #    print('code continued, level folder')
     folderpath=mycodelocationpath+'\ '+str(level)+'\ '+str(SQLquery)
     MakeFolder(folderpath)
     
     GroupedRows=result.groupby(result.year)['total'].transform('sum')
     MakeFolder(savepath)
     GroupedDF=pd.DataFrame()
     if CorrectionRequired==True:#need to correct aggregations
         #MakeFolder(savepath)#(folderpath+'\ Category Wildcard Match')
         
         #GroupedDF={'year':result.groupby(result.year)['ChildCount'],'GroupedRows':GroupedRows,'nlpCount':result.groupby(result.year)['ChildCountSum'].transform('sum')/GroupedRows}
     #    print('year\n',result.groupby(result.year)['year'].transform('mean'))
      #   print('GroupedRows',GroupedRows)
       #  print('nlpCountMean',result.groupby(result.year)['ChildCountSum'].transform('sum')/GroupedRows)
        # print('lengthMean',result.groupby(result.year)['lengthSum'].transform('sum')/GroupedRows)
         #print('flesch_kincaid_Mean',result.groupby(result.year)['flesch_kincaid_Sum'].transform('sum')/GroupedRows)
         #print('smog_Mean',result.groupby(result.year)['smog_Sum'].transform('sum')/GroupedRows)
         GroupedDF={'year':result.groupby(result.year)['year'].transform('mean'),'GroupedRows':GroupedRows,
                    'ChildCountMean':result.groupby(result.year)['ChildCountSum'].transform('sum')/GroupedRows
                    ,'lengthMean':result.groupby(result.year)['lengthSum'].transform('sum')/GroupedRows
                    ,'flesch_kincaid_Mean':result.groupby(result.year)['flesch_kincaid_Sum'].transform('sum')/GroupedRows
                    ,'smog_Mean':result.groupby(result.year)['smog_Sum'].transform('sum')/GroupedRows
                    }
         
      #   GroupedDF['year']=result.groupby(result.year)['ChildCount']
       #  GroupedDF['GroupedData']=GroupedRows
       #  ={'year':result.groupby(result.year)['ChildCount'],'GroupedRows':GroupedRows,
        #   'nlpCount':result.groupby(result.year)['ChildCountSum'].transform('sum')/GroupedRows}
         
         #print('GroupedDF\n',GroupedDF)#GroupedDF=pd.Dataframe(GroupedDF)
         #{ 'Author': auth_series, 'Article': article_series }
         #result = pd.DataFrame(frame)
         
         
         #nlpyear=result.groupby(result.year)['ChildCountSum'].transform('sum')
    #     lengthyear=result.groupby(result.year)['lengthSum'].transform('sum')
     #    flesch_kincaidyear=result.groupby(result.year)['flesch_kincaid_Sum'].transform('sum')
      #   smogyear=result.groupby(result.year)['smog_Sum'].transform('sum')
        #create sum fields
         #result['ChildCountSum']=result['total']*ChilsCount
         
         #ChildCountSum too
         #GroupedRows=#toal is rows
        
     
         '''
         File['ChildCountSum']=File['ChildCount']
File['ChildCount']=File['ChildCount']/File['total']#childcount is sum
#sum total,
File['LengthSum']=File['total']*File['length_Mean']#sum length
File['flesch_kincaid_Sum']=File['total']*File['flesch_kincaid_Mean']#sum flesch kincaid
File['smog_Sum']=File['total']*File['smog_Mean']#sum smog
print(File.head())
         
         
         #sum total,
result['LengthSum']=result['total']*result['length_Mean']#sum length
result['flesch_kincaid_Sum']=result['total']*result['flesch_kincaid_Mean']#sum flesch kincaid
result['smog_Sum']=result['total']*result['smog_Mean']#sum smog
print(File.head())
         
         
        
         #get sum by aggregation
         print(result.dtypes) 
         result['sumChildCount']=result['ChildCount'].mul(result['total'])
         result['sumChildCount']=result.groupby(['Categories','year'])['sumChildCount'].transform('sum')
         print(result['sumChildCount'])#sum created
         nlpyear=result['sumChildCount']/result.groupby(['Categories','year'])['total'].transform('sum')
         print(nlpyear,'\n 1')
         #result['numrows']=result.groupby(['Categories','year'])['total']
        # print(result['childcountgroup'])
         
        # nlpcatyear=np.multiply(childcountgroup,numrows)#df.groupby(['col5', 'col2']
         #nlpcatyear=numrows.mul(childcountgroup)
         #nlpcatyear=numrows*childcountgroup
     #    groupresult=result.groupby(['year','Categories'])
      #   xx = groupresult.apply(
       #  lambda x: x.assign(childcountgroup = x.childcountgroup*float(x.numrows)))\
      #                .reset_index(['year','Categories'], drop = True)
         #nlpyear=nlpcatyear/result.groupby(result.year)['total'].transform('sum')
         
         
         '''
         
   #      lengthyear=result.groupby(result.year)['length_Mean'].transform('sum')/result.groupby(result.year)['total'].transform('sum')
    #     flesch_kincaidyear=result.groupby(result.year)['flesch_kincaid_Mean'].transform('sum')/result.groupby(result.year)['total'].transform('sum')
     #    smogyear=result.groupby(result.year)['smog_Mean'].transform('sum')
         
     else:#if CorrectionRequired==False:#doesn't matter if transform is mean etc.
         GroupedDF={'year':result.groupby(result.year)['ChildCount'].transform('mean'),'GroupedRows':GroupedRows,
                    'ChildCountMean':result.groupby(result.year)['ChildCount'].transform('mean')
                    ,'lengthMean':result.groupby(result.year)['length_Mean'].transform('mean')
                    ,'flesch_kincaid_Mean':result.groupby(result.year)['flesch_kincaid_Mean'].transform('mean')
                    ,'smog_Mean':result.groupby(result.year)['smog_Mean'].transform('mean')
                    }
     
   #  with open('test4.csv', 'w') as csvfile:
    #        writer = csv.DictWriter(csvfile, fieldnames = employee_info)
     #       writer.writeheader()
      #      writer.writerows(new_dict)

        #pd.DataFrame(GroupedDF) 
     #GroupedDF.to_csv(savepath+'\data.csv', index=False)
         #(folderpath+'\ Exact Match')
         #nlpyear=result.groupby(result.year)['ChildCount'].transform('mean')
         #lengthyear=result.groupby(result.year)['length_Mean'].transform('mean')
         #flesch_kincaidyear=result.groupby(result.year)['flesch_kincaid_Mean'].transform('mean')
       #  smogyear=result.groupby(result.year)['smog_Mean'].transform('mean')

    
     
     
     GroupedDF=pd.DataFrame(GroupedDF)
     GroupedDF.drop_duplicates(inplace=True)
     GroupedDF.to_csv(savepath+'\Data.csv', index=False)
     
    
     #print('nlp',result['nlp'])
     #fieldnames.remove('year')
     #SQLquery="when categories are related to gaming"

    
     #working hashed for efficiency
     
    # print(11)    
   #  print(GroupedDF['year'].shape)
    # print(GroupedDF[''].shape)
     makebarchart(GroupedDF["year"],GroupedDF['GroupedRows'],'Year','relevant samples that year',SQLquery)
     #result['nlp']=result['policy_text'].str.count("Parental|parental|guardian|Guardian|child|Child|Child's|child's|Minor|minor|underage|child|kid|young|youth|young people|under-18|under-13|under 13|under 18|under 12|13 years old|under 13 years old|under 18 years old|age of 13|under the age of 18")##here is where to adjust what words ar being checked, not earlier on so other graphs
         
     #nlpyear=result.groupby(result.year)['ChildCount'].transform('mean')# should be mean anyway
     makebarchart(GroupedDF["year"],GroupedDF['ChildCountMean'],'Year','Mean count of child synonyms',SQLquery)
     
         #result['nlpGDPR']=result['policy_text'].str.count("GDPR")##here is where to adjust what words ar being checked, not earlier on so other graphs
         
         #nlpGDPRyear=result.groupby(result.year)['nlpGDPR'].transform('mean')
         #makebarchart(result["year"],nlpGDPRyear,'Year','Mean count of GDPR',SQLquery)
     #del result['nlpGDPR']
    # lengthyear=result.groupby(result.year)['length_Mean'].transform('mean')
     makebarchart(GroupedDF['year'],GroupedDF['lengthMean'],'Year','Mean length',SQLquery)


     
     #flesch_kincaidyear=result.groupby(result.year)['flesch_kincaid_Mean'].transform('mean')
     makebarchart(GroupedDF['year'],GroupedDF['flesch_kincaid_Mean'],'Year',
                'Mean flesch_kincaid',SQLquery)#lower is harder, so getting slightly easier since 2000
     
     #smogyear=result.groupby(result.year)['smog_Mean'].transform('mean')
     makebarchart(GroupedDF['year'],GroupedDF['smog_Mean'],'Year',
                'Mean smog',SQLquery)#years of education needed to read
          
     
     #flesch_scores(result, SQLquery)
   
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
   plt.savefig(savepath+"\."+savelabel)
   plt.show()
   print(titlelabel+' Graph created')
   
   
   
File=pd.read_csv('Categories Agg.csv')
File['ChildCountSum']=File['ChildCount']
File['ChildCount']=File['ChildCount']/File['total']#childcount is sum
#sum total,
File['lengthSum']=File['total']*File['length_Mean']#sum length
File['flesch_kincaid_Sum']=File['total']*File['flesch_kincaid_Mean']#sum flesch kincaid
File['smog_Sum']=File['total']*File['smog_Mean']#sum smog
print(File.head())
print(File.tail())
print(File.columns)
columns=File['Categories'].unique()
num=0
for i in columns:
    i= str(i)
    num=+1
    print(num,' times ran')
    #TempFile=File
   # if not pd.isnull(i):
    print(i)
    Filter=File['Categories'].str.contains(i)
    Filter= Filter.fillna(False)#nulls are false
    print(Filter)
    TempFile=File[Filter]
    
    global savepath
    savepath=os.path.abspath(os.path.dirname(__file__))+'\ '+str(i.count(';'))+'\ '+i+'\ Category Wildcard Match'
    try:
        MainCode(TempFile,i,True)
    except MemoryError as error:
            # Output expected MemoryErrors
            print('memory error')
    
    Filter=File['Categories']==i
    #Filter=File['Categories'].count(i)>0
    #print(File['run'])
    TempFile=File[Filter]
    savepath=os.path.abspath(os.path.dirname(__file__))+'\ '+str(i.count(';'))+'\ '+i+'\ Exact Match'
    try:
        MainCode(TempFile,i,False)
    except MemoryError as error:
            # Output expected MemoryErrors
            print('memory error')
        
    
    '''
if __name__ == '__main__':
    

    MainCode()   #start
    print('Database processing complete')'''