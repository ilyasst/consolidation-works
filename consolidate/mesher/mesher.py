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

          
            
    def initialize_fields(self, problem):
        
        
        fields = []

        for field_name in problem.required_fields:
            for domain in problem.domains:
                if field_name == "Temperature":
                    value = (domain.initial_temperature*np.ones((domain.Number_of_Elements_in_Y, domain.Number_of_Elements_in_X)))
                    if domain == problem.domains[0]:
                        res=value
                        value=[]
                    else:
                        res=np.concatenate((res, value))
                        value=[]
                   
                if field_name == "Input Power Density":
                    value=(domain.Power_Input_Density*np.ones((domain.Number_of_Elements_in_Y, domain.Number_of_Elements_in_X)))                     
                    if domain == problem.domains[0]:
                        res=value    
                        value=[]
                    else:
                        res=np.concatenate((res, value))
                        value=[]
                elif field_name != "Temperature" or field_name!="Input Power Density":
                    try:
                        value=(float(domain.material[field_name])*np.ones((domain.Number_of_Elements_in_Y, domain.Number_of_Elements_in_X)))
                    except:
                        print ("missing " + field_name + " field")
                        continue
                    if domain == problem.domains[0]:
                        res=value             
                        value=[]
                    else:
                        res=np.concatenate((res, value))
                        value=[]
                
            fields.append(Field(field_name, res))
            self.fields=fields

                        

                    
                
        