# -*- coding: utf-8 -*-
import numpy as np
from .mesh import Mesh

class Mesher():

    def __init__(self,  problem):
        self.mesh_domains( problem)
        self.initialize_fields(problem)
# 
    def mesh_domains(self, problem):
        self.meshes = []
        for domain in problem.domains:
            self.meshes.append( Mesh(domain) )

           
            
    def initialize_fields(self, problem):
        
        Fields = {}        
        for field in problem.required_fields:
                
            for i, domain in enumerate(problem.domains): 
                if i == 0:
                    if field == "Temperature":
                        Fields[field]=domain.initial_temperature*np.ones((self.meshes[i].ny, self.meshes[i].nx))    
                    else:    
                        try:
                            Fields[field] = float(domain.material[field])*np.ones((self.meshes[i].ny, self.meshes[i].nx))
                        except:
                             continue
                    continue
                else:
                    # import pdb; pdb.set_trace()
                    if field == "Temperature":
                
                        Fields[field] = np.vstack((Fields[field] , domain.initial_temperature*np.ones((self.meshes[i].ny, self.meshes[i].nx))))
                    else:
                        try:
                            Fields[field] = np.vstack((Fields[field] , float(domain.material[field])*np.ones((self.meshes[i].ny, self.meshes[i].nx))))
                        except: 
                            continue
        self.fields=Fields
                    
                    
                
        