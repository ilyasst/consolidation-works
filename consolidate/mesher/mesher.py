# -*- coding: utf-8 -*-
import numpy as np
from .mesh import Mesh

class Mesher():

    def __init__(self, deck, problem):
        self.mesh_domains(deck, problem)

    def mesh_domains(self, deck, problem):
        self.meshes = []
        for domain in problem.domains:
            self.meshes.append( Mesh(deck, domain) )

        
        
