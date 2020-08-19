import numpy as np

class Field:
    
    
    
    
    def __init__(self,  name, variable, domain ):
        self.name=name
        self.populate_field(variable,domain)
        
        
    def populate_field(self, variable, domain):
        
        value=np.zeros((domain.Number_of_Elements_in_X,domain.Number_of_Elements_in_Y))
        value[:]=variable
        self.var=value