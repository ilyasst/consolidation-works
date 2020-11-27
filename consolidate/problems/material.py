# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 11:16:29 2020

@author: andre
"""


class Material:
    def __init__(self, problem,deck):
        self.set_materials(problem, deck)
    
    def set_materials(self, problem, deck):
        for domain in problem.domains:
            material = {}
            domain_dir = deck.doc["Domains"][domain.name]["Material"]
            for param in domain_dir:
                if isinstance(domain_dir[param], str):
                    material[param] = float(domain_dir[param])
                else:
                    material[param] = {}
                    for aux in domain_dir[param]:
                        material[param].update({aux: float(domain_dir[param][aux])})
            domain.set_material(material)
            

