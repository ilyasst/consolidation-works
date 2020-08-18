# -*- coding: utf-8 -*-
import numpy as np
from .mesh import Mesh
from .fields import Field

class Mesher():

    def __init__(self, deck, problem):
        self.mesh_domains(deck, problem)
        self.initialize_fields(problem)

    def mesh_domains(self, deck, problem):
        self.meshes = []
        for domain in problem.domains:
            self.meshes.append( Mesh(deck, domain) )

    def initialize_fields(self, problem):
        self.fields =  []
        for domain in problem.domains:
            self.fields.append(Field( domain))

        
        
