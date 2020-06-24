# -*- coding: utf-8 -*-
import numpy as np


class Solves:
    
    def __init__(self, deck,model,meshes,plots):
        self.deck = deck
        # Compute the TEMPERATURE for each node
        self.model = model
        self.meshes=meshes  
        self.plots = plots
        self.do_solver(plots)
            
        
        
        
    def do_solver(self,plots):
        for m in range(int(self.deck.doc["Simulation"]["Number Time Steps"])):
            self.meshes.T0, self.meshes.T = self.model.do_timestep(self.meshes.T0, self.meshes.T, self.meshes.DiffTotalX, self.meshes.DiffTotalY)
            self.meshes.T[int(self.meshes.ny/2), int(0.2*self.meshes.nx):int(0.8*self.meshes.nx+1)] = 100
            self.meshes.T[int(self.meshes.ny/2-1), int(0.2*self.meshes.nx):int(0.8*self.meshes.nx+1)] = 100
            self.meshes.T0=self.meshes.T.copy()
            if m in self.plots.mfig:
                self.plots.update_T(self.meshes.T)
                self.plots.do_plots(m)    
            
            
            
     