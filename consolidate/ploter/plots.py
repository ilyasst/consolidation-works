# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 15:00:34 2020

@author: andre
"""

import matplotlib.pyplot as plt
from PIL import Image
import glob

class PlotsTwoPlates():
    
    def __init__(self, deck,meshes,T):
        self.deck = deck
        self.nsteps =  int(self.deck.doc["Simulation"]["Number Time Steps"])
        self.nsetepinterval =int(self.deck.doc["Plot"]["plot interval"])
        self.meshes=meshes
        self.T = T
        self.set_plots()


    def set_plots(self): 
    
        self.mfig=[]
        for i in range (0,self.nsteps,self.nsetepinterval):
            self.mfig.append(i)
        self.fignum = 0
        self.fig = plt.figure()
        
    def update_T(self,T):
        self.T = T
        
        
    def do_plots(self,m):
                plt.clf()
                self.fignum += 1
                print(m, self.fignum)
                plt.pcolormesh(self.meshes.Y, self.meshes.X, self.T,vmin=290, vmax=800,cmap=self.deck.doc["Plot"]["Color Map"])
                plt.colorbar()
                self.fig.suptitle('time: {:.2f}'.format( m*float(self.deck.doc["Simulation"]["Time Step"])), fontsize=16)
                plt.savefig(self.deck.plot_dir+self.deck.doc["Plot"]["figure name"]+ str("%03d" %self.fignum) + '.jpg')
        
        
    def do_animation(self):   
        frames = []
        # imgs = glob.glob("./output/*.jpg")
        imgs = glob.glob(self.deck.plot_dir + '*.jpg')
        for i in imgs:
            new_frame = Image.open(i)
            frames.append(new_frame)
            print(i)
            
        
         
        # Save into a GIF file that loops forever
        direction=(self.deck.plot_dir+self.deck.doc["Animation"]["name"]+'.gif')
        frames[0].save(direction, format='GIF',
                        append_images=frames[1:],
                        save_all=True,
                        duration=200, loop=0)       
    