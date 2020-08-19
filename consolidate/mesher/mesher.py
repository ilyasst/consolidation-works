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
                