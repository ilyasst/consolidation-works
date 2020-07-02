# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 22:07:28 2020

@author: andre
"""

import numpy as np

class IntimateContact():
    
    def __init__(self, meshes):
            self.meshes=meshes
        
    def viscosity_timestep(self,v,u):
             
          v[0:, 0:]=1.14*10**(-12)*np.exp(26300/u[0:,0:])
          return v
     
        
    def dic_timestep(self, dic, dic0, v, t):
        C1=5*(1+0.45)*(0.85)**2
        dic[(self.meshes.ny1 -1):(self.meshes.ny1 +1),0:]=dic0[(self.meshes.ny1 -1):(self.meshes.ny1 +1),0:]*((1+(C1-0.65)*(5*10**5/v[(self.meshes.ny1 -1):(self.meshes.ny1 +1),0:])*t)**(1/5))
        
        return dic