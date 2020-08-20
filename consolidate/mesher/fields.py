# import numpy as np


            
class Field:
     def __init__(self, name, shape, problem):
        self.name = name
        self.populate_field(shape, problem)
        
     def populate_field(self, shape, problem):
         # import pdb; pdb.set_trace()
         self.var = shape
         for x_i, x_ in enumerate(self.var):
             for y_i, y_ in enumerate(x_):
                 for domain in problem.domains:
                     self.var[x_i][y_i] = domain.initial_fields[self.name]
                 
                    
                    
      