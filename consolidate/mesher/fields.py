# import numpy as np


            
class Field:
     def __init__(self, name, shape, problem):
        self.name = name
        self.populate_field(shape, problem)

                    
     def populate_field(self, shape, problem):
         # import pdb; pdb.set_trace()
         self.var = shape
         var=shape
         nx=0
         nyu=0
         nyl=0
         for domain in problem.domains:
             nx=domain.Number_of_Elements_in_X
             nyu=nyu+domain.Number_of_Elements_in_Y
             var[nyl:nyu, 0:nx]=domain.initial_fields[self.name]
             nyl=nyu
         self.var=var
             
             
