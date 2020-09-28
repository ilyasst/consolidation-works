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
        aux={}
        for prop in material.keys():
            if isinstance(material[prop],dict)==False:
                aux[prop] = float(material[prop])
            else:
                aux[prop]={}
                for param in material[prop]:
                    aux[prop].update({param:material[prop][param]})
        self.material=aux
        
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
        aux={}
        for variable in ic.keys():
            aux[variable] = float(ic[variable])
        self.variables=aux
            

        
class BC:
    
    def __init__(self, bc, location,mesh,material,init_cond):
        aux={}
        self.location=location
        
        for edge in bc:
            aux[edge]={}
            for var in bc[edge]:
                aux[edge].update({var:float(bc[edge][var])})
        self.edges=aux


