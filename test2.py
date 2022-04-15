# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 18:12:55 2022

@author: layto
"""

import os
print(__file__)
print(os.path.join(os.path.dirname(__file__), '..'))
print(os.path.dirname(os.path.realpath(__file__)))
print(os.path.abspath(os.path.dirname(__file__)))