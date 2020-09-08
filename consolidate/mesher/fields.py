# import numpy as np
import numpy as np

            
class Field:
    
    def __init__(self, field, problem):
        self.field=field 
        if field == "External Temperature":
            self.set_convection(field,problem)
        else:
            self.set_field(field, problem)

    def set_field(self, field, problem):
        value=0
        for domain in problem.domains:
            if field in domain.initial_fields:
                value = value + domain.mask * domain.initial_fields[field]
        self.value=value


    def set_convection(self,name,problem):
        M=np.zeros((problem.totalNy+2, problem.totalNx+2))
        for domain in problem.domains:
            # import pdb; pdb.set_trace()
            for edge in domain.boundary_fields[self.field]:
                for variable in domain.boundary_fields[self.field][edge]:
                    value = float(domain.boundary_fields[self.field][edge][variable])
                    if domain.position == 1:
                        if edge == "Bottom Edge":
                            M[0,1:domain.mesh["Number of Elements in X"]+1]=value
                        if edge == "Left Edge":
                            M[ 1:domain.mesh["Number of Elements in Y"]+1, 0]=value
                        if edge == "Right Edge":
                            M[ 1:domain.mesh["Number of Elements in Y"]+1,-1]=value
                    if domain.position == 3:
                            if edge == "Left Edge":
                                M[problem.totalNy-domain.mesh["Number of Elements in Y"]+1:-1, 0]=value
                            if edge == "Right Edge":
                                M[problem.totalNy-domain.mesh["Number of Elements in Y"]+1:-1, -1]=value
                            if edge == "Top Edge":
                                M[-1,problem.totalNx-domain.mesh["Number of Elements in X"]+1:-1 ] = value
                    if domain.position == 2:
                        for domain_aux in problem.domains:
                            if domain_aux.position==1:
                                nylower=domain_aux.mesh["Number of Elements in Y"]
                                nyupper = nylower+domain.mesh["Number of Elements in Y"]
                                if edge =="Left Edge":
                                    M[nylower+1:nyupper+1,0]=value
                                if edge == "Right Edge":
                                    M[nylower+1: nyupper+1,-1]=value
        self.value=M.copy()
