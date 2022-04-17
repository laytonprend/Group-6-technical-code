# -*- coding: utf-8 -*-
"""
Created on Sat Apr 16 11:23:03 2022

@author: layto
"""
import numpy as np
import pandas as pd
import csv
#test
'''fields=['test SQL category run summary']

with open(r'test SQL category run summary', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(fields)
    '''
arr=[1,2,3,4,5,6,7,8,9,10,11,12,13,14]#[1],[2],[3],[4], [5], [6],[7],[8],[9],[10],[11],[12],[13],[14]]
                      #   [result.groupby(result.year)['nlp'].transform('mean').max()],[result.groupby(result.year)['nlp'].transform('mean').min()],
                       #  [result.groupby(result.year)['nlpGDPR'].transform('mean').max()],[result.groupby(result.year)['nlpGDPR'].transform('mean').min()],
                        # [result.groupby(result.year)['length'].transform('mean').max()],[result.groupby(result.year)['length'].transform('mean').min()]]
data={'SQLsearchHistorical':[1],
      'categories_included_in_search':[2],
      'level':[3],
      'rows':[4],
      'flesch_kincaid_max':[5],
      'flesch_kincaid_min':[6],
      'smog_max':[7],
      'smog_min':[8],
      'child_synonyms_max':[9],
      'child_synonyms_min':[9],
      'GDPR max':[10],
      'GDPR min':[11],
      'length max':[12],
      'length min':[13]
      
     
      }
#my_array = np.array(arr)#maybe change to max of by year mean?                   
#print('now make df')
df = pd.DataFrame(data)
print(df)
df2=pd.read_csv(r'test SQL category run summary')
df3=pd.concat([df, df2])
print(df3)
     #order=np.array([categories historicalflesch_ease,flesch_kincaid,smog,nlp,nlpGDPR,length])#just write max and min
df3.to_csv('test SQL category run summary2.csv', mode='a', index=True)

#relearn append as not working