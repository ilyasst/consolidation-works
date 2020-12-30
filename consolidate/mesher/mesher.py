# -*- coding: utf-8 -*-
import numpy as np
from .fields import Field

class Mesher():

    def __init__(self,  problem):
        # self.totalNx = problem.totalpx
        # self.totalNy = problem.totalpy
        self.set_fields(problem)
        self.set_interfaces(problem)

    def set_fields(self, problem):
        self.fields=[]
        for field_name in problem.required_fields:
            field_value=0
            for domain in problem.domains:
                field_value = field_value + domain.local_fields[field_name]
            self.fields.append(Field(field_name, field_value))
            if field_name== "Temperature":
                self.fields.append(Field("Toldold", field_value))
                
    def set_interfaces(self, problem):
        mask_interface=np.zeros((problem.totalnodes[1], problem.totalnodes[0]))
        for domain_name in problem.domains:
            # import pdb; pdb.set_trace()
            for edge in domain_name.mask_interface:
                mask_interface= mask_interface+domain_name.mask_interface[edge]
            # import pdb; pdb.set_trace()
        self.mask_interface= mask_interface