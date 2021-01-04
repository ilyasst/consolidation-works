# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 11:19:43 2020

@author: andre
"""


from .domains import RectangularDomain
from .local_mesh import LocalFields
from .material import Material
from .bc import BoundaryCondition
from .power import PowerInput
import numpy as np


class TwoPlates:

    def __init__(self, deck):
        self.set_simulation_parameters(deck)
        self.create_fields(deck)
        self.set_problem_parameters(deck)
        self.set_domains(deck)
        self.set_create_mask(deck)
        
        self.material(deck)
        self.bc(deck)
        self.power(deck)
        self.populate_fields_locally()


    def set_simulation_parameters(self,deck):
        self.SimulationParameters = {}
        for par in deck.doc["Simulation"]:
            self.SimulationParameters[par] = deck.doc["Simulation"][par]
    
    def create_fields(self, deck):
        if deck.doc["Problem Type"]["Type"] == "Welding":
            self.required_fields=["Temperature", "kx", "ky", "Density", "Cp", "Viscosity",  "Power Input Heat", "Intimate Contact", "dx","dy","Convection Coefficient", "Outer Temperature"]
        if deck.doc["Problem Type"]["Type"] == "Heat Transfer":
            self.required_fields=["Temperature", "kx", "ky", "Density", "Cp", "Viscosity", "Power Input Heat", "dx","dy", "Convection Coefficient", "Outer Temperature"]

    def set_problem_parameters(self, deck):
        ny = 0
        thickness = 0
        count = 0
        for domain in deck.doc["Domains"]:            
            domain_dir = deck.doc["Domains"][domain]
            if count == 0:
                ny = int((domain_dir["Mesh"]["Points in Y"]))
                count = count+1
            else:
                ny = ny + int(domain_dir["Mesh"]["Points in Y"])-1
            nx = int(domain_dir["Mesh"]["Points in X"])
            current_thickness = float(domain_dir["Geometry"]["y1"])
            if current_thickness > thickness:
                thickness = current_thickness
        self.totalnodes = [nx, ny]
        self.thickness = thickness
        self.length = float(deck.doc["Problem Type"]["Length"])


    def is_top_plate(self,y1,totalthickness):
        return y1 == totalthickness

    def is_bottom_plate(self,y0):
        return y0 == 0

    def set_domains(self, deck):
        self.domains = []
        count=0
        for domain_name in deck.doc["Domains"]:
            bc ={}
            dimen_x0 = float(deck.doc["Domains"][domain_name]["Geometry"]["x0"])
            dimen_x1 = float(deck.doc["Domains"][domain_name]["Geometry"]["x1"])
            dimen_y0 = float(deck.doc["Domains"][domain_name]["Geometry"]["y0"])
            dimen_y1 = float(deck.doc["Domains"][domain_name]["Geometry"]["y1"])
            temperature = float(deck.doc["Domains"][domain_name]["Initial Condition"]["Temperature"])

            dormain_dir = deck.doc["Domains"][domain_name]
            dimen_y0 = float(deck.doc["Domains"][domain_name]["Geometry"]["y0"])
            dimen_y1 = float(deck.doc["Domains"][domain_name]["Geometry"]["y1"])
            count=1
            if self.is_bottom_plate(dimen_y0):
                p_x0 = 0
                p_x1 = int(deck.doc["Domains"][domain_name]["Mesh"]["Points in X"])-1
                p_y0 = 0
                p_y1= int(deck.doc["Domains"][domain_name]["Mesh"]["Points in Y"])-1
            else:
                aux=0
                for i in range (1, int(domain_name[-1])):
                    aux = aux +  int(deck.doc["Domains"]["Plate " + str(i)]["Mesh"]["Points in Y"])-1
                p_x0 = 0
                p_x1 = int(deck.doc["Domains"][domain_name]["Mesh"]["Points in X"])-1*count
                p_y0 = aux
                p_y1 = aux + int(deck.doc["Domains"][domain_name]["Mesh"]["Points in Y"])-1*count
                count=count+1
            nodes=[[p_x0,p_x1],[p_y0, p_y1]]
            
            
            self.domains.append(RectangularDomain(domain_name, dimen_x0, dimen_x1, dimen_y0, dimen_y1, nodes, temperature))
            

    def set_create_mask(self, deck):
        for i,domain in enumerate(self.domains):
            domain.generate_mask(i,self.totalnodes[1],self.totalnodes[0], self.thickness)
            
    def initial_temperature(self, deck):
        for domain in self.domains:
            temperature = float(domain_dir["Initial Condition"]["Temperature"])
            domain.set_temperature(temperature)

    def populate_fields_locally(self):
        LocalFields(self)
        
    def material(self,deck):
        Material(self,deck)
    
    def bc(self,deck):
        BoundaryCondition(self, deck)
        
    def power(self, deck):
        PowerInput(self,deck)
        