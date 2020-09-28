# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 22:49:08 2020

@author: andre
"""


import numpy as np

class Constants:
    
    def __init__ (self, constant):
        self.name=constant
        
        
    def set_material_constants(self, problem,variable):
        print(variable)
        variables={}
        for domain in problem.domains:
            variables[domain.name]={}
            for var in domain.material[variable]:
                variables[domain.name].update({var:domain.material[variable][var]})
        self.value=variables
                
            