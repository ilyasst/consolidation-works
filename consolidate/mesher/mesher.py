# -*- coding: utf-8 -*-
import numpy as np
from .mesh import Mesh
from .fields import Field

class Mesher():

    def __init__(self,  problem):
        # self.mesh_domains( problem)
       
        self.totalNx = problem.totalNx
        self.totalNy = problem.totalNy
        self.initialize_fields(problem)

            
            
    def initialize_fields(self, problem):
        self.meshes=[]
        for domain in problem.domains:
            self.meshes.append(Mesh( domain, self.totalNx, self.totalNy))
            
    
                
        