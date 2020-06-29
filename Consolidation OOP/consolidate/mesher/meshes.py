# -*- coding: utf-8 -*-
import numpy as np

class MeshTwoPlates():

    def __init__(self, deck):
        self.deck = deck
        self.set_mesh_grid() 
        self. init_mesh() 
     
    
    def set_mesh_grid(self):
        self.nx = int(float(self.deck.doc["Simulation"]["lenX"])/float(self.deck.doc["Simulation"]["dx"]))
        self.ny = int(float(self.deck.doc["Simulation"]["lenY"])/float(self.deck.doc["Simulation"]["dy"]))
        X, Y = np.meshgrid(np.arange(0, self.ny), np.arange(0, self.nx))
        X=X[1,:].copy()
        Y=Y[:,1].copy()
        self.X = X
        self.Y = Y

    def init_mesh(self):

        self.nx1, self.nx2 = self.nx, self.nx
        self.ny1, self.ny2 = int(self.ny/2), self.ny
        
        T = np.zeros((self.ny, self.nx))        
        T[0:self.ny1, 0:self.nx1] = self.deck.doc["Materials"]["Material1"]["Domain Initial Temperature"] # Set array size and set the interior value with Tini
        T[self.ny1:self.ny2, 0:self.nx2] = self.deck.doc["Materials"]["Material2"]["Domain Initial Temperature"] # Set array size and set the interior value with Tini
        T[int(self.ny/2), int(0.2*self.nx):int(0.8*self.nx+1)] = 100
        T[int(self.ny/2-1), int(0.2*self.nx):int(0.8*self.nx+1)] = 100
        self.T = T.copy()
        self.T0=T.copy()
        
        
        DiffTotalX = np.zeros((self.ny, self.nx)) 
        DiffTotalX[0:self.ny1, 0:self.nx1] = self.deck.doc["Materials"]["Material1"]["Thermal Diffusivity X"]
        DiffTotalX[self.ny1:self.ny2, 0:self.nx2] = self.deck.doc["Materials"]["Material2"]["Thermal Diffusivity X"]

        DiffTotalY = np.zeros((self.ny, self.nx)) 
        DiffTotalY[0:self.ny1, 0:self.nx1] = self.deck.doc["Materials"]["Material1"]["Thermal Diffusivity Y"]
        DiffTotalY[self.ny1:self.ny2, 0:self.nx2] = self.deck.doc["Materials"]["Material2"]["Thermal Diffusivity Y"]
        self.DiffTotalX = DiffTotalX
        self.DiffTotalY = DiffTotalY