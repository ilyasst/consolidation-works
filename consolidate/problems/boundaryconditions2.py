# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 14:59:38 2020

@author: andre
"""


class BoundaryCondition:
    def __init__(self, edge,name, value,):
        self.edge= edge
        self.name = name
        self.value=value