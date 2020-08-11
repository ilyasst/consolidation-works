# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 11:20:57 2020

@author: andre
"""

import numpy as np

class MeshTwoPlates():

    def __init__(self, deck,geometry):
        self.deck = deck
        self.geometry=geometry
        self.set_mesh_grid() 
        self.set_dx()
        self.set_dy()
        self.set_Element_Position()
        
        
    def set_mesh_grid(self):
        self.nx = int(self.deck.doc["Simulation"]["Number of Elements X"])        
        self.ny =  {
  "Top Adherent": int(self.deck.doc["Simulation"]["Number of Elements Top Plate Thickness"]) ,
  "HE"       : int(self.deck.doc["Simulation"]["Number of Elements HE"]),
  "Bottom Adherent": int(self.deck.doc["Simulation"]["Number of Elements Bottom Plate Thickness"]) 
                  }


        self.number_of_elements_Y=self.ny.get("Top Adherent")+self.ny.get("HE")+self.ny.get("Bottom Adherent")
    
        self.dx = self.geometry.Lx/self.nx
        self.dy = {
        "Top Adherent":self.geometry.Ly.get("Top Adherent")/self.ny.get("Top Adherent"),
        "HE"       :self.geometry.Ly.get("HE")/self.ny.get("HE"),
        "Bottom Adherent":self.geometry.Ly.get("Bottom Adherent")/self.ny.get("Bottom Adherent")
                  }
        
        
        
        
       
       
    
    def set_dx(self):
        Mdx=    {
        "Top Adherent":np.zeros((self.ny.get("Top Adherent"), self.nx)) ,
        "HE"       :np.zeros((self.ny.get("HE"), self.nx)) ,
        "Bottom Adherent":np.zeros((self.ny.get("Bottom Adherent"), self.nx)) 
                  }
        
        Mdx["Top Adherent"][0:self.ny.get("Top Adherent"),0:self.nx]=self.dx
        Mdx["HE"][0:self.ny.get("HE"),0:self.nx]=self.dx
        Mdx["Bottom Adherent"][0:self.ny.get("Bottom Adherent"),0:self.nx]=self.dx
        
        Mdx=np.concatenate((Mdx["Bottom Adherent"], Mdx["HE"], Mdx["Top Adherent"]), axis=0)
        
        
        self.Mdx=Mdx.copy()
        
        
    def set_dy(self):
        Mdy=    {
        "Top Adherent":np.zeros((self.ny.get("Top Adherent"), self.nx)) ,
        "HE"       :np.zeros((self.ny.get("HE"), self.nx)) ,
        "Bottom Adherent":np.zeros((self.ny.get("Bottom Adherent"), self.nx)) 
                  }
        
        Mdy["Top Adherent"][0:self.ny.get("Top Adherent"),0:self.nx]=self.dy.get("Top Adherent")
        Mdy["HE"][0:self.ny.get("HE"),0:self.nx]=self.dy.get("HE")
        Mdy["Bottom Adherent"][0:self.ny.get("Bottom Adherent"),0:self.nx]=self.dy.get("Bottom Adherent")
        
        Mdy=np.concatenate((Mdy["Bottom Adherent"], Mdy["HE"], Mdy["Top Adherent"]), axis=0)
        
        self.Mdy=Mdy.copy()
        
    def set_Element_Position(self):
        
        ElementXPosition=    {
        "Top Adherent":np.arange(self.nx)*self.dx+self.dx ,
        "HE"       :np.arange(self.nx)*self.dx+self.dx ,
        "Bottom Adherent":np.arange(self.nx)*self.dx+self.dx 
                  }
        self.ElementXPosition=ElementXPosition.copy()
        
        ElementYPosition=    {
        "Top Adherent":np.arange(self.ny.get("Top Adherent"))*self.dy.get("Top Adherent")+self.dy.get("Top Adherent") ,
        "HE"       :np.arange(self.ny.get("HE")+1)*self.dy.get("HE"),
        "Bottom Adherent":np.arange(self.ny.get("Bottom Adherent"))*self.dy.get("Bottom Adherent")+self.dy.get("Bottom Adherent") 
                  }
        
       
        self.ElementYPosition=ElementYPosition.copy()
        
        
        if all(self.ElementXPosition["Top Adherent"] == self.ElementXPosition["Bottom Adherent"]) and all(self.ElementXPosition["Top Adherent"] == self.ElementXPosition["HE"] ):
            self.Xposition=self.ElementXPosition.get("Top Adherent")
        else:
            print("Error")
            
        self.Yposition = np.concatenate((ElementYPosition["Bottom Adherent"], ElementYPosition["HE"]+ElementYPosition.get("Bottom Adherent")[-1],ElementYPosition["Top Adherent"]+ElementYPosition.get("HE")[-1]+ElementYPosition.get("Bottom Adherent")[-1]))
    