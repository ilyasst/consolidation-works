# -*- coding: utf-8 -*-
import numpy as np
from .mesh import Mesh
from .fields import Field

class Mesher():

    def __init__(self,  problem):
        self.mesh_domains( problem)
        # self.initialize_empty_field(problem)
        self.initialize_fields(problem)
# 
    def mesh_domains(self, problem):
        self.meshes = []
        for domain in problem.domains:
            self.meshes.append( Mesh(domain) )

    # def initialize_empty_field(self, problem):
    #     self.fields =  []
    #     for i,domain in enumerate(problem.domains):
    #         A=( Field(domain).M)
    #         if i==0:
    #             self.fields = A
    #         else:
    #             # import pdb; pdb.set_trace()
    #             self.fields=np.concatenate((self.fields,A),axis=0)


    # def initialize_fields(self, problem):
    #     self.fields = []
    
    #     for domain in problem.domains:
    #         initial_temperature= domain.initial_temperature
    #         Kx = domain.material["Thermal Conductivity X"]
    #         Ky = domain.material["Thermal Conductivity Y"]
    #         Rho = domain.material["Density"]
    #         Cp = domain.material["Specific Heat Capacity"]
    #         # import pdb; pdb.set_trace()
    #         self.fields.append(Field (domain, initial_temperature, Kx, Ky, Rho, Cp))
           
            
    def initialize_fields(self, problem):
        for i, domain in enumerate(problem.domains):
            # if domain.name == "Bottom Plate":
            self.meshes[i].fields = []
            for field in problem.required_fields:
                if field == "Temperature":
                    variable = domain.initial_temperature
                    self.meshes[i].fields.append(Field(field, variable, domain))
                elif field == "Thermal Conductivity X":
                    variable = domain.material["Thermal Conductivity X"]
                    self.meshes[i].fields.append(Field(field, variable, domain))
                elif field == "Thermal Conductivity Y":
                    variable = domain.material["Thermal Conductivity Y"]
                    self.meshes[i].fields.append(Field(field, variable, domain))
                elif field == "Density":
                    variable = domain.material["Density"]
                    self.meshes[i].fields.append(Field(field, variable, domain))
                elif field == "Specific Heat":
                    variable = domain.material["Specific Heat"]
                    self.meshes[i].fields.append(Field(field, variable, domain))
                

            
        
        
# if deck_domain == "Bottom Plate":
#                 corner0 = (0,0)
#                 corner1 = self.geometry[deck_domain][0]
#                 plate_material = deck.doc["Materials"][deck_domain]
#                 plate_initial_temperature=float(deck.doc["Initial Conditions"][deck_domain]["Initial Temperature"])
#                 number_of_elements_X = int(deck.doc["Mesh"][deck_domain]["Number of Elements in X"])
#                 number_of_elements_Y = int(deck.doc["Mesh"][deck_domain]["Number of Elements in Y"])
#                 self.domains.append(RectangularDomain(deck_domain, corner0, corner1, plate_material,plate_initial_temperature, number_of_elements_X, number_of_elements_Y ))
            