# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 09:17:09 2020

@author: andre
"""


class Material:
    
    def __init__(self, deck, problem):
        self.set_materials(deck,problem)
        
        
    def set_materials(self, deck, problem):
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
            
            
    def set_bcs(self, deck, problem):
        for domain in problem.domains:
            bc ={}
            domain_dir = deck.doc["Domains"][domain.name]["Boundary Condition"]
            for bc_type in domain_dir:
                bc[bc_type]={}
                for kind in domain_dir[bc_type]:
                    bc[bc_type][kind]={}
                    for edge in domain_dir[bc_type][kind]:
                        bc[bc_type][kind][edge]={}
                        for param in domain_dir[bc_type][kind][edge]:
                            bc[bc_type][kind][edge].update({param : float(domain_dir[bc_type][kind][edge][param])})
            domain.set_bc(bc)