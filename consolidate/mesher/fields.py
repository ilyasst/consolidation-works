# import numpy as np
import numpy as np

            
class Field:
    
    def __init__(self, field):
        self.name=field


    def set_initial_conditions_field(self, problem):
        value=0
        for domain in problem.domains:
            value = value + domain.mask * domain.initial_conditions[self.name]
        self.value = value
        
    def set_material_field(self, problem):
        value=0
        for domain in problem.domains:
            if isinstance(domain.material[self.name],dict) == False:
                value = value + domain.mask*domain.material[self.name]
            if isinstance(domain.material[self.name], dict) == True:
                
                aux=[]
                for param in domain.material[self.name]:
                    aux.append(domain.material[self.name][param])
                value = value+domain.mask*aux[0]*np.exp(aux[1]/(8.31*domain.initial_conditions["Temperature"]))
        self.value=value
        
    def set_external_bc_field(self, problem):
        for domain in problem.domains:
            import pdb; pdb.set_trace()