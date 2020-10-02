# -*- coding: utf-8 -*-
import numpy as np
from .fields import Field
from .constants import Constants

class Mesher():

    def __init__(self,  problem):
        self.fields=[]
        self.merge_fields(problem)


    def merge_fields(self, problem):
        i=0
        while i<np.size(problem.required_fields):
            value=0
            for domain in problem.domains:
                value = value + domain.local_fields[i].value
            self.fields.append(Field(domain.local_fields[i].field, value))
            i+=1
