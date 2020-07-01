# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 22:07:28 2020

@author: andre
"""

import numpy as np

class IntimateContact():
    
        
        
    def viscosity_timestep(self,v,u):
             
          v[1:-1, 1:-1]=1.14*10**(-12)*np.exp(26300/u[1:-1, 1:-1])
          return v
     

