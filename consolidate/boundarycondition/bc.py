# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 10:35:47 2020

@author: andre
"""


class BoundaryCondition:
    
    def __init__(self, deck, problem):
        self. set_bcs(deck,problem)
        
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