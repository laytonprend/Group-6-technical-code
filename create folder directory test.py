# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 17:32:20 2022

@author: layto
"""

import os
  
# Directory
directory = "GeeksforGeeks"
  
# Parent Directory path
parent_dir = "C:/Users/layto/OneDrive/Documents/GitHub/Group-6-technica-lcode/"
#"D:/Pycharm projects/  

path = 'D:/Pycharm projects / GeeksForGeeks'
    
# Create the directory 
# 'GeeksForGeeks' in 
# '/home / User / Documents' 
try: 
    os.mkdir(path) 
except OSError as error: 
    print(error)  
print('code continued')