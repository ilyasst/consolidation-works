# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 19:35:49 2020

@author: andre
"""
from PIL import Image
import glob


class Animates:
    
    def __init__(self,deck):
        self.deck=deck
        self.do_animation()
        
        
        
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