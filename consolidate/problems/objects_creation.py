# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 00:47:52 2020

@author: andre
"""


class Mesh:
    
    def __init__(self, mesh, dimensions):
        aux={}
        for prop in mesh.keys():
            aux[prop]=int(mesh[prop])
        aux.update({"dx": dimensions["lx"]/aux["Number of Elements in X"] })
        aux.update({"dy": dimensions["ly"]/aux["Number of Elements in Y"]})
        self.properties=aux
            
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
        
# class Material:
    
#     def __init__(self, prop,value):
#         self.property = prop
#         if isinstance(value, dict) == True:
#             aux={}
#             for param in value:
#                 aux[param]={}
#                 aux[param] =  float(value[param])
#         else:
#             aux=float(value)
#         self.value=aux
            
class Initial_Condition:
    
    def __init__ (self, ic):
        self.temperature = ic["Temperature"]
        if "Input Power Density" in ic.keys():
            self.power_density = ic["Input Power Density"]
            
# class Initial_Condition:
    
#     def __init__ (self, ic):
#         aux={}
#         for variable in ic.keys():
#             aux[variable] = float(ic[variable])
#         self.variables=aux

        
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
        



# class BC:
    
#     def __init__(self, bc, location,mesh,material,init_cond):
#         aux={}
#         self.location=location
        
#         for edge in bc:
#             aux[edge]={}
#             for var in bc[edge]:
#                 aux[edge].update({var:float(bc[edge][var])})
#         self.edges=aux

