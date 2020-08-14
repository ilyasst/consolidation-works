# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 11:38:36 2020

@author: andre
"""

import numpy as np

class BoundaryCondition():
    
    def __init__(self, deck,geometry,meshes):
        self.deck = deck
        self.geometry = geometry
        self.meshes=meshes
        self.set_temperatures()
        self.set_conductivity()
        self.set_density()
        self.set_specific_heat()
        self.set_diffusivity()
        self.set_viscosity()
        self.set_dic()
        self.set_heat_input_density()
        
    def set_temperatures(self):    
        
        T=    {
        "Top Adherent":np.zeros((self.meshes.ny.get("Top Adherent"), self.meshes.nx)) ,
        "HE"       :np.zeros((self.meshes.ny.get("HE"), self.meshes.nx)) ,
        "Bottom Adherent":np.zeros((self.meshes.ny.get("Bottom Adherent"), self.meshes.nx)) 
                  }
        
        T["Top Adherent"][0:self.meshes.ny.get("Top Adherent"),0:self.meshes.nx] =self.deck.doc["Boundary Condition"]["Initial Temperature Top Adherent"],
        T["HE"][0:self.meshes.ny.get("HE"),0:self.meshes.nx]               =self.deck.doc["Boundary Condition"]["Initial Temperature HE"],
        T["Bottom Adherent"][0:self.meshes.ny.get("Bottom Adherent"),0:self.meshes.nx] =self.deck.doc["Boundary Condition"]["Initial Temperature Bottom Adherent"]
        
        T=np.concatenate((T["Bottom Adherent"], T["HE"], T["Top Adherent"]), axis=0)
        self.T=T.copy()
        self.T0=T.copy()
        
        self.Troom=self.deck.doc["Boundary Condition"]["Room Temperature"]
        
    def set_conductivity(self):
        
        Kx=    {
        "Top Adherent":np.zeros((self.meshes.ny.get("Top Adherent"), self.meshes.nx)) ,
        "HE"       :np.zeros((self.meshes.ny.get("HE"), self.meshes.nx)) ,
        "Bottom Adherent":np.zeros((self.meshes.ny.get("Bottom Adherent"), self.meshes.nx)) 
                  }
        
        Kx["Top Adherent"][0:self.meshes.ny.get("Top Adherent"),0:self.meshes.nx] =self.deck.doc["Materials"]["Top Adherent"]["Thermal Conductivity X"],
        Kx["HE"][0:self.meshes.ny.get("HE"),0:self.meshes.nx]               =self.deck.doc["Materials"]["HE"]["Thermal Conductivity X"],
        Kx["Bottom Adherent"][0:self.meshes.ny.get("Bottom Adherent"),0:self.meshes.nx] =self.deck.doc["Materials"]["Bottom Adherent"]["Thermal Conductivity X"]
        
        Kx=np.concatenate((Kx["Bottom Adherent"], Kx["HE"], Kx["Top Adherent"]), axis=0)
        self.Kx=Kx.copy()
      
        
        
        
        Ky=    {
        "Top Adherent":np.zeros((self.meshes.ny.get("Top Adherent"), self.meshes.nx)) ,
        "HE"       :np.zeros((self.meshes.ny.get("HE"), self.meshes.nx)) ,
        "Bottom Adherent":np.zeros((self.meshes.ny.get("Bottom Adherent"), self.meshes.nx)) 
                  }
        
        Ky["Top Adherent"][0:self.meshes.ny.get("Top Adherent"),0:self.meshes.nx] =self.deck.doc["Materials"]["Top Adherent"]["Thermal Conductivity Y"],
        Ky["HE"][0:self.meshes.ny.get("HE"),0:self.meshes.nx]               =self.deck.doc["Materials"]["HE"]["Thermal Conductivity Y"],
        Ky["Bottom Adherent"][0:self.meshes.ny.get("Bottom Adherent"),0:self.meshes.nx] =self.deck.doc["Materials"]["Bottom Adherent"]["Thermal Conductivity Y"]
        
        Ky=np.concatenate((Ky["Bottom Adherent"], Ky["HE"], Ky["Top Adherent"]), axis=0)
        self.Ky=Ky.copy()

        
        
    def set_density(self):
        
        Rho=    {
        "Top Adherent":np.zeros((self.meshes.ny.get("Top Adherent"), self.meshes.nx)) ,
        "HE"       :np.zeros((self.meshes.ny.get("HE"), self.meshes.nx)) ,
        "Bottom Adherent":np.zeros((self.meshes.ny.get("Bottom Adherent"), self.meshes.nx)) 
                  }
        
        Rho["Top Adherent"][0:self.meshes.ny.get("Top Adherent"),0:self.meshes.nx] =self.deck.doc["Materials"]["Top Adherent"]["Density"],
        Rho["HE"][0:self.meshes.ny.get("HE"),0:self.meshes.nx]               =self.deck.doc["Materials"]["HE"]["Density"],
        Rho["Bottom Adherent"][0:self.meshes.ny.get("Bottom Adherent"),0:self.meshes.nx] =self.deck.doc["Materials"]["Bottom Adherent"]["Density"]
        
        Rho=np.concatenate((Rho["Bottom Adherent"], Rho["HE"], Rho["Top Adherent"]), axis=0)
        self.Rho=Rho.copy()
        
    def set_specific_heat(self):
        
        Cp=    {
        "Top Adherent":np.zeros((self.meshes.ny.get("Top Adherent"), self.meshes.nx)) ,
        "HE"       :np.zeros((self.meshes.ny.get("HE"), self.meshes.nx)) ,
        "Bottom Adherent":np.zeros((self.meshes.ny.get("Bottom Adherent"), self.meshes.nx)) 
                  }
        
        Cp["Top Adherent"][0:self.meshes.ny.get("Top Adherent"),0:self.meshes.nx] =self.deck.doc["Materials"]["Top Adherent"]["Specific Heat Capacity"],
        Cp["HE"][0:self.meshes.ny.get("HE"),0:self.meshes.nx]               =self.deck.doc["Materials"]["HE"]["Specific Heat Capacity"],
        Cp["Bottom Adherent"][0:self.meshes.ny.get("Bottom Adherent"),0:self.meshes.nx] =self.deck.doc["Materials"]["Bottom Adherent"]["Specific Heat Capacity"]
        
        Cp=np.concatenate((Cp["Bottom Adherent"], Cp["HE"], Cp["Top Adherent"]), axis=0)
        self.Cp=Cp.copy()
        
        




    def set_diffusivity(self):
        Dx=np.zeros((np.shape(self.T)))
        Dx[0:,0:]=self.Kx[0:,0:]/(self.Rho[0:,0:]*self.Cp[0:,0:])
        self.Dx=Dx.copy()
        
        Dy=np.zeros((np.shape(self.T)))
        Dy[0:,0:]=self.Ky[0:,0:]/(self.Rho[0:,0:]*self.Cp[0:,0:])
        self.Dy=Dy.copy()
    
    


    def set_viscosity(self):         
        Visc=np.zeros((np.shape(self.T)))
        Visc[0:, 0:]=1.14*10**(-12)*np.exp(26300/self.T[0:, 0:])
        self.Visc=Visc.copy()

    def set_dic(self):
        
        self.Dic0=1./(1.+0.45)        
        
        Dic=    {
        "Top Adherent":np.ones((self.meshes.ny.get("Top Adherent"), self.meshes.nx)) ,
        "HE"       :np.zeros((self.meshes.ny.get("HE"), self.meshes.nx)) ,
        "Bottom Adherent":np.ones((self.meshes.ny.get("Bottom Adherent"), self.meshes.nx)) 
                  }
        Dic["HE"][0:self.meshes.ny.get("HE"),0:self.meshes.nx]               =self.Dic0,

        
        Dic=np.concatenate((Dic["Bottom Adherent"], Dic["HE"], Dic["Top Adherent"]), axis=0)
        self.Dic=Dic.copy()  


    def set_heat_input_density(self):       
        self.q=float(self.deck.doc["Boundary Condition"]["Input Power Density"])
        Q =    {
        "Top Adherent":np.zeros((self.meshes.ny.get("Top Adherent"), self.meshes.nx)) ,
        "HE"       :np.zeros((self.meshes.ny.get("HE"), self.meshes.nx)) ,
        "Bottom Adherent":np.zeros((self.meshes.ny.get("Bottom Adherent"), self.meshes.nx)) 
                  }
        Q["HE"][0:self.meshes.ny.get("HE"),0:self.meshes.nx]               =self.q,

        
        Q=np.concatenate((Q["Bottom Adherent"], Q["HE"], Q["Top Adherent"]), axis=0)
        self.Q=Q.copy()        
        
        
        