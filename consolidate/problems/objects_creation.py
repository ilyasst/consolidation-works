# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 00:47:52 2020

@author: andre
"""

    


class Mesh:
    
    def __init__(self, mesh, geometry):
        self.npx = int(mesh["Number of Points in X"])
        self.npy = int(mesh["Number of Points in Y"])
        self.dx = geometry.dimensionX/self.npx
        self.dy = geometry.dimensionY/self.npy


            
class Material:
    
    def __init__(self, material):
        self.kx = float(material["Thermal Conductivity X"])
        self.ky = float(material["Thermal Conductivity Y"])
        self.density = float(material["Density"])
        self.cp = float(material["Specific Heat"])
        viscosity={}
        for prop in material["Viscosity"]:
            viscosity.update({prop: float(material["Viscosity"][prop])})
        self.viscosity=viscosity
        

class Initial_Condition:
    
    def __init__ (self, ic):
        self.temperature = float(ic["Temperature"])
        if "Input Power Density" in ic.keys():
            self.power_density = float(ic["Input Power Density"])
            
        
class BC:
    
    def __init__(self, bc, location):
        self.location = location
        
        if location == "External":
            self.room_temperature={}
            self.h = {}
            if "Left Edge" in bc.keys():
                if "Room Temperature" in bc["Left Edge"].keys():
                    self.room_temperature.update({"Left Edge": float(bc["Left Edge"]["Room Temperature"])})
                if "Convection Coefficient" in bc["Left Edge"].keys():
                    self.h.update({"Left Edge": float(bc["Left Edge"]["Convection Coefficient"])})
                    
                if "Top Edge" in bc.keys():
                    if "Room Temperature" in bc["Top Edge"].keys():
                        self.room_temperature.update({"Top Edge": float(bc["Top Edge"]["Room Temperature"])})
                    if "Convection Coefficient" in bc["Top Edge"].keys():
                        self.h.update({"Top Edge": float(bc["Top Edge"]["Convection Coefficient"])})
                if "Right Edge" in bc.keys():
                    if "Room Temperature" in bc["Right Edge"].keys():
                        self.room_temperature.update({"Right Edge": float(bc["Right Edge"]["Room Temperature"])})
                    if "Convection Coefficient" in bc["Right Edge"].keys():
                        self.h.update({"Right Edge": float(bc["Right Edge"]["Convection Coefficient"])})
                if "Left Edge" in bc.keys():
                    if "Left Temperature" in bc["Left Edge"].keys():
                        self.room_temperature.update({"Left Edge": float(bc["Left Edge"]["Room Temperature"])})
                    if "Convection Coefficient" in bc["Left Edge"].keys():
                        self.h.update({"Left Edge": float(bc["Left Edge"]["Convection Coefficient"])})
                    
        if location == "Internal":
            self.horizontal_ratio = {}
            self.vertical_ratio = {}
            for edge in bc.keys():
                if "Horizontal asperity ratio" in bc[edge].keys():
                    self.horizontal_ratio.update({edge: float(bc[edge]["Horizontal asperity ratio"])}) 
                if "Vertical asperity ratio" in bc[edge].keys():
                    self.vertical_ratio.update({edge: float(bc[edge]["Vertical asperity ratio"])}) 
        


class Geometry:
    
    def __init__(self,deck, key, position):
        if position == 1:
             corner0 = (0, 0)
             corner1 = (float(deck.doc["Domains"][key]["Geometry"]["Width (X)"]), float(deck.doc["Domains"][key]["Geometry"]["Thickness (Y)"]))
             # import pdb; pdb.set_trace()
        if position == 2:
            for domain_aux in deck.doc["Domains"]:
                if deck.doc["Domains"][domain_aux]["Geometry"]["Pos"] == "1":
                    aux=float(deck.doc["Domains"][domain_aux]["Geometry"]["Thickness (Y)"])
                    corner0=(0, aux)
                    corner1 = (float(deck.doc["Domains"][key]["Geometry"]["Width (X)"]), aux + float(deck.doc["Domains"][key]["Geometry"]["Thickness (Y)"]))
            # import pdb; pdb.set_trace()
        if position == 3:
            aux=0
            for domain_aux in deck.doc["Domains"]:
                if domain_aux != key:
                    aux=aux+float(deck.doc["Domains"][domain_aux]["Geometry"]["Thickness (Y)"])
            corner0 = (0, aux)
            corner1 = (float(deck.doc["Domains"][key]["Geometry"]["Width (X)"]), aux + float(deck.doc["Domains"][key]["Geometry"]["Thickness (Y)"]))
            # import pdb; pdb.set_trace()
        self.dimensionX = float(corner1[0]) - float(corner0[0])
        self.dimensionY = float(corner1[1]) - (corner0[1])



class Points:
    def __init__(self, deck, keys, position, pointsY):
        if  position == 1:
            p_x0 = 0
            p_x1 = int(deck.doc["Domains"][keys]["Mesh"]["Number of Points in X"])
            p_y0 = 0
            p_y1 = int(deck.doc["Domains"][keys]["Mesh"]["Number of Points in Y"])-1
                
        if position == 2:
            for domain_aux in deck.doc["Domains"]:
                if deck.doc["Domains"][domain_aux]["Geometry"]["Pos"] == "1":
                    auxeley=int(deck.doc["Domains"][domain_aux]["Mesh"]["Number of Points in Y"])
                    p_x0 = 0
                    p_x1 = int(deck.doc["Domains"][keys]["Mesh"]["Number of Points in X"])
                    p_y0 = auxeley
                    p_y1 = int(deck.doc["Domains"][keys]["Mesh"]["Number of Points in Y"])+auxeley-1
                        
        if position == 3:
            p_x0 = 0
            p_x1 = int(deck.doc["Domains"][keys]["Mesh"]["Number of Points in X"]) -1
            p_y0 = int(pointsY)-int(float(deck.doc["Domains"][keys]["Mesh"]["Number of Points in Y"]))
            p_y1 = int(pointsY)-1
        self.pointsX=[p_x0, p_x1]
        self.pointsY=[p_y0, p_y1]
        
class Mask:
    def __init__(self, name, value):
        self.name = name
        self.value = value
        
class Field:
    def __init__ (self, field_name,value):
        # import pdb; pdb.set_trace()
        self.field=field_name
        self.value=value
        