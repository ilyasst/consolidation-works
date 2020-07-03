# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 22:07:28 2020

@author: andre
"""

import numpy as np

class IntimateContact():
    
    def __init__(self, meshes,deck):
            self.meshes=meshes
            self.deck=deck
            self.P = (float(self.deck.doc["Processing Parameters"]["Pressure"]))
            self.init_parameter()
            
    def viscosity_timestep(self,v,u):
             
          v[0:, 0:]=1.14*10**(-12)*np.exp(26300/u[0:,0:])
          return v
     
    def init_parameter(self):
        self.aux=0
    
    def dic_timestep(self, dic, dic0, v, t):
        
        C1=5*(1+0.45)*(0.85)**2
        dic[(self.meshes.ny1 -1):(self.meshes.ny1 +1),0:]=dic0[(self.meshes.ny1 -1):(self.meshes.ny1 +1),0:]*((1+C1*self.P*10**6/v[(self.meshes.ny1 -1):(self.meshes.ny1 +1),0:]*(self.aux+t)))**(1/5)

        np.clip(dic,0,1)
        return dic
    
    
    
    def update_aux(self,t):
        self.aux=self.aux+t
        return self.aux    