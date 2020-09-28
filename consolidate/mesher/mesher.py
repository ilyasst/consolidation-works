# -*- coding: utf-8 -*-
import numpy as np
from .mesh import Mesh
from .fields import Field
from .constants import Constants

class Mesher():

    def __init__(self,  problem):
        self.totalNx = problem.totalNx
        self.totalNy = problem.totalNy
        self.create_masks(problem)
        self.fields=[]
        self.set_fields_ic(problem)
        self.set_fields_material(problem)
        self.set_fields_external_bc(problem)
        self.constants=[]
        self.set_constants_material(problem)

    def create_masks(self, problem):
        self.meshes=[]
        for domain in problem.domains:
            self.meshes.append(Mesh( domain, self.totalNx, self.totalNy))
            
    def set_fields_ic(self, problem):
        count=np.size(self.fields)
        for field in set(problem.domains[0].initial_conditions) & set(problem.domains[1].initial_conditions) & set(problem.domains[2].initial_conditions):
            self.fields.append(Field(field))
        for i in range(count, np.size(self.fields)):
            self.fields[i].set_initial_conditions_field(problem)
            
    def set_fields_material(self,problem):
        count=np.size(self.fields)
        for field in set(problem.domains[0].material) & set(problem.domains[1].material) & set(problem.domains[2].material):
            self.fields.append(Field(field))
        for i in range(count, np.size(self.fields)):
            self.fields[i].set_material_field(problem)
            
    def set_fields_external_bc(self,problem):
        count = np.size(self.fields)
        switch=[]
        for domain in problem.domains:
            for edge in domain.boundary_conditions["External"]:
                for var in domain.boundary_conditions["External"][edge]:
                    switch=[]
                    for i in range (np.size(self.fields)):
                        switch.append(var in self.fields[i].name)
                    if any(switch) == False:
                        self.fields.append(Field(var))
        
        for i in range (count, np.size(self.fields)):
                self.fields[i].set_external_bc_field(problem)
                
            
    def set_constants_material(self, problem):
        count = np.size(self.constants)
        for variable in set(problem.domains[0].material) & set(problem.domains[1].material) & set(problem.domains[2].material):
            if isinstance(problem.domains[0].material[variable],dict) == True:
                self.constants.append(Constants(variable))
        for i in range(count, np.size(self.constants)):
            self.constants[i].set_material_constants(problem, self.constants[i].name)

