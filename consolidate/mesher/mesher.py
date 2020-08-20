# -*- coding: utf-8 -*-
import numpy as np
from .mesh import Mesh
from .fields import Field

class Mesher():

    def __init__(self,  problem):
        self.mesh_domains( problem)
        self.initialize_fields(problem)
# 
    def mesh_domains(self, problem):
        self.meshes = []
        for domain in problem.domains:
            self.meshes.append( Mesh(domain) )

           
            
    # def initialize_fields(self, problem):
        
    #     self.fields=[]
    #     for field in problem.required_fields:                
    #         for domain in problem.domains: 
    #             self.fields.append (Field(field, domain))
                    
            
    def initialize_fields(self, problem):
        
        self.fields=[]
        self.fields.append (Field(problem))
        
                    
                
        