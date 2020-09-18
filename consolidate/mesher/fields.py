# import numpy as np
import numpy as np

            
class Field:
    
    def __init__(self, field, problem):
        self.field=field 
        # self.set_field_initial_temperature(problem)
        # self.set_field_input_power_density(problem)
        self.set_field(field, problem)
        
        
    
    def set_field(self, field, problem):
        
        value=0        
        for domain in problem.domains:
            if field in domain.initial_fields:
                value = value+domain.mask*domain.initial_fields[field]
                
        self.value=value
          

    
    
             
             
