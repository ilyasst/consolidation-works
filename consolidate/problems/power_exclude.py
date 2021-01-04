# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 18:45:04 2020

@author: andre
"""


class PowerInput:
    
    def __init__(self, problem,deck):
        self.set_power(problem, deck)
        
    def set_power(self, problem, deck):
        for domain in problem.domains:
            power = {}
            for cond_name in deck.doc["Domains"][domain.name]["Initial Condition"]:
                if cond_name == "Power Input":
                    for location in deck.doc["Domains"][domain.name]["Initial Condition"]["Power Input"]:
                        power.update({location : float(deck.doc["Domains"][domain.name]["Initial Condition"]["Power Input"][location])})
                    domain.set_power(power)