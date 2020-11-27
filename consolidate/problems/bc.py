# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 11:39:17 2020

@author: andre
"""


class BoundaryCondition:
    
    def __init__(self, problem,deck):
        self.set_BCs(problem, deck)
        
    def set_BCs(self, problem, deck):
        for domain in problem.domains:
            bc ={}
            h={}
            for bc_type in deck.doc["Domains"][domain.name]["Boundary Condition"]:
                    bc[bc_type]={}
                    for kind in deck.doc["Domains"][domain.name]["Boundary Condition"][bc_type]:
                        bc[bc_type][kind]={}
                        for edge in deck.doc["Domains"][domain.name]["Boundary Condition"][bc_type][kind]:
                            bc[bc_type][kind][edge]={}
                            for param in deck.doc["Domains"][domain.name]["Boundary Condition"][bc_type][kind][edge]:
                                bc[bc_type][kind][edge].update({param : float(deck.doc["Domains"][domain.name]["Boundary Condition"][bc_type][kind][edge][param])})
                                if kind == "Constant Temperature":
                                    bc[bc_type][kind][edge].update({"h" : 0})
                    domain.set_bc(bc)