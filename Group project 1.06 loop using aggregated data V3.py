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

def MainCode(result,SQLquery,CorrectionRequired,CatergoriesInSearch):
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
     
     #GroupedDF=pd.DataFrame()
     if CorrectionRequired==True:#need to correct aggregations
     #prev 'year':result.groupby(result.year)['year'].transform('mean')
         #print('newyear\n',result.groupby('year').aggregate(lambda tdf: tdf.unique()))
         GroupedDF={'year':result.groupby(result.year)['year'].transform('mean'),'GroupedRows':GroupedRows,
                    'ChildCountMean':result.groupby(result.year)['ChildCountSum'].transform('sum')/GroupedRows
                    ,'lengthMean':result.groupby(result.year)['length_Sum'].transform('sum')/GroupedRows
                    ,'flesch_kincaid_Mean':result.groupby(result.year)['flesch_kincaid_Sum'].transform('sum')/GroupedRows
                    ,'smog_Mean':result.groupby(result.year)['smog_Sum'].transform('sum')/GroupedRows
                    ,'Exact Match?':not CorrectionRequired
                    ,'CategoriesSearched':CatergoriesInSearch
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
                    ,'Exact Match?':not CorrectionRequired
                    ,'CategoriesSearched':CatergoriesInSearch
                    }
     print(GroupedDF)
     GroupedDF=pd.DataFrame(GroupedDF)
     print('df',GroupedDF)
     GroupedDF.sort_values(by=['year'], inplace=True)
     
     GroupedDF=pd.DataFrame(GroupedDF)
     GroupedDF.drop_duplicates(inplace=True)
     GroupedDF.to_csv(savepath+'\Data '+SearchDescription+'.csv', index=False)
     
    #df.loc[df['cyl']==6,'cty']
    #GroupedDF.loc[GroupedDF['GroupedRows']!=0,'year']

     makelinechart(GroupedDF['year'],GroupedDF['GroupedRows'],'Year','relevant samples that year')
     #result['nlp']=result['policy_text'].str.count("Parental|parental|guardian|Guardian|child|Child|Child's|child's|Minor|minor|underage|child|kid|young|youth|young people|under-18|under-13|under 13|under 18|under 12|13 years old|under 13 years old|under 18 years old|age of 13|under the age of 18")##here is where to adjust what words ar being checked, not earlier on so other graphs
         
     #nlpyear=result.groupby(result.year)['ChildCount'].transform('mean')# should be mean anyway
    # temp=GroupedDF['year','ChildCountMean']
     temp = pd.DataFrame().assign(year=GroupedDF['year'], ChildCountMean=GroupedDF['ChildCountMean'])

    # print(temp)
     temp.dropna()
     makelinechart(temp["year"],temp['ChildCountMean'],'Year','Mean count of child synonyms')
     #temp=GroupedDF['year','lengthMean']
     temp = pd.DataFrame().assign(year=GroupedDF['year'], lengthMean=GroupedDF['lengthMean'])

     temp.dropna()

     makelinechart(temp['year'],temp['lengthMean'],'Year','Mean length')

     temp = pd.DataFrame().assign(year=GroupedDF['year'], flesch_kincaid_Mean=GroupedDF['flesch_kincaid_Mean'])

     #temp=GroupedDF['year','flesch_kincaid_Mean']
     temp.dropna()
     #flesch_kincaidyear=result.groupby(result.year)['flesch_kincaid_Mean'].transform('mean')
     makelinechart(temp['year'],temp['flesch_kincaid_Mean'],'Year',
                'Mean flesch_kincaid')#lower is harder, so getting slightly easier since 2000
     #temp=GroupedDF['year','smog_Mean']
     temp = pd.DataFrame().assign(year=GroupedDF['year'], smog_Mean=GroupedDF['smog_Mean'])

     temp.dropna()
     #smogyear=result.groupby(result.year)['smog_Mean'].transform('mean')
     makelinechart(temp['year'],temp['smog_Mean'],'Year',
                'Mean smog')#years of education needed to read
    # GroupedDF.to_csv(mycodelocationpath+'\RanData.csv', index=False)
    
     plt.figure(figsize=(10,8),dpi=80)
     graph=sns.pairplot(GroupedDF,kind='reg')
     graph.fig.subplots_adjust(top=.9)
     graph=graph.fig.suptitle('A Pairplot to show the trends and distributions of each measure for '+SearchDescription)#,lw=7)#linewidth=4)#,hue='species')
     plt.show()#marginal distributions, histograms, so number of samples?
    # return GroupedDF
  #  sns.lmplot(x='e',y='restbp',data=heart_df,fit_reg=True) 
     

                                                     
def makelinechart(x,y,xlabel,ylabel):

   #savelabelSQLquery=SQLquery
  # SQLquery='when categories are related to '+SQLquery 
   plt.rcParams["figure.figsize"] = (10,8)
  # plt.bar(x = x,
   #height = y,
   #color = "blue")
   plt.plot(x,y,linewidth=7)
   plt.plot(x,y,'b*')

   titlelabel=str(ylabel)+' in privacy policies by '+str(xlabel)+'\n'+str(SearchDescription)#area in brackets in main title but not axis
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
File=pd.read_csv('Categories AggV3.csv')
'''print(File.columns)
droplist=File.columns
droplist2=[]
for i in droplist:
    print(i)
    if i.__contains__('max|min|Max|Min')==True:
        droplist2.append(i)
        print(i)

File=File.drop(columns=droplist)'''
File['ChildCountSum']=File['ChildCount']+File['Count_Parental']+File['Count_Guardian']+File['Count_Child']+File['Count_Underage']+File['Count_Kid']+File['Count_Young']+File['Count_Youth']+File['Count_Under1']+File['Count_Under_1']+File['Count_Ageof1']
File=File.drop(columns=['ChildCount','Count_Guardian','Count_Child','Count_Underage','Count_Kid','Count_Young','Count_Youth','Count_Under1','Count_Under_1','Count_Ageof1'])
File=File.drop(columns=['flesch_kincaid_Count','smog_Count','length_Count',])
#File['ChildCount']
#mean create
File['flesch_kincaid_Mean']=File['flesch_kincaid_Sum']/File['total']
File['smog_Mean']=File['smog_Sum']/File['total']
File['length_Mean']=File['length_Sum']/File['total']


File['ChildCount']=File['ChildCountSum']/File['total']#childcount was sum
#sum total,
'''
File['length_Sum']=File['total']*File['length_Mean']#sum length
File['flesch_kincaid_Sum']=File['total']*File['flesch_kincaid_Mean']#sum flesch kincaid
File['smog_Sum']=File['total']*File['smog_Mean']#sum smog
#print(File.head())
#print(File.tail())
'''



#print(File.columns)
Categories=shuffle(File['Categories'].unique())
TimesRan=0
Head=True
CentralDF=pd.DataFrame()
global SearchDescription
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
    CatergoriesInSearch=''
    for x in UniqueCategories:
        CatergoriesInSearch+=str(x)+' - '#InWildcarnt(CatergoriesInSearch)
   # print(CatergoriesInSearch)    
    global savepath
    savepath=os.path.abspath(os.path.dirname(__file__))+'\ '+str(i.count(';'))+'\ '+i+'\ Category Wildcard Match'
    SearchDescription=i+' Wildcard'
    
    try:
        #RanData1=
        MainCode(TempFile,i,True,CatergoriesInSearch)
    except MemoryError as error:
            # Output expected MemoryErrors
            print('error')
    
    Filter=File['Categories']==i
    #Filter=File['Categories'].count(i)>0
    #print(File['run'])
    TempFile=File[Filter]
    savepath=os.path.abspath(os.path.dirname(__file__))+'\ '+str(i.count(';'))+'\ '+i+'\ Exact Match'
    SearchDescription=i+' Exact Match'
    try:
        #RanData2=
        MainCode(TempFile,i,False,i)
    except MemoryError as error:
            # Output expected MemoryErrors
            print('error')
    '''RanData1['Category Search']=i
    RanData1['Categories returned']=CatergoriesInSearch
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
CentralDF.to_csv('RanData.csv', mode='w', header=Head,index=False)'''

#    except MemoryError as error:
 #       print(error)
     