# -*- coding: utf-8 -*-
import numpy as np


class SolvesTwoPlates:
    
    def __init__(self, deck,model_HT,meshes,plots,model_IC):
        self.deck = deck
        # Compute the TEMPERATURE for each node
        self.model_HT = model_HT
        self.model_IC=model_IC
        self.meshes=meshes  
        self.plots = plots
        self.do_solver()
        
            
        
        
        
    def do_solver(self):
        for m in range(int(self.deck.doc["Simulation"]["Number Time Steps"])):
            self.meshes.T0, self.meshes.T = self.model_HT.do_timestep(self.meshes.T0, self.meshes.T, self.meshes.DiffTotalX, self.meshes.DiffTotalY)
            self.meshes.T[int(self.meshes.ny/2), int(0.2*self.meshes.nx):int(0.8*self.meshes.nx+1)] = self.deck.doc["Processing Parameters"]["Temperature"]
            self.meshes.T[int(self.meshes.ny/2-1), int(0.2*self.meshes.nx):int(0.8*self.meshes.nx+1)] = self.deck.doc["Processing Parameters"]["Temperature"]
            self.meshes.T0=self.meshes.T.copy()
            self.meshes.Visc=self.model_IC.viscosity_timestep(self.meshes.Visc, self.meshes.T)
            if m in self.plots.mfig:
                self.plots.update_T(self.meshes.T)
                self.plots.do_plots(m)    
        self.plots.do_animation()
            
            
     