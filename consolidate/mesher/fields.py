# import numpy as np
import numpy as np

            
class Field:
    def __init__(self, name, shape, problem):
        self.name = name
        self.create_mask
        # self.populate_field(shape, problem)
        
    
    def create_mask(self, problem, shape):
        M=shape.copy()
        for domain in problem.domains:
            domain.generate_mask(M)
            initialmask = domain.mask
            self.dunno=initialmask
            
    
        
        
    def populate_field(self, shape, problem):
        M=shape.copy()
        field=0
        for domain in problem.domains:            
            domain.generate_mask(M)
        self.field=field
         
        
         # VarConv = np.concatenate((var, np.zeros((np.shape(var)[0],2))), axis=1)
         # nx_var = np.shape(VarConv)[1]
         # VarConv= np.concatenate((VarConv, np.zeros((2, nx_var))), axis=0)
        

         # nx=0
         # nyu=0
         # nyl=0
         # if self.name == "Heat Input":
         #     for BC in problem.BoundaryConditions:
         #         if BC.kind == "Heating":
         #             nyaux=0
         #             for i, domains in enumerate(problem.domains):
         #                 nyaux=(domains.Number_of_Elements_in_Y)+nyaux
         #                 if domains.name == BC.domain:
         #                     nx = domains.Number_of_Elements_in_X
         #                     nyl = nyaux-i
         #                     nyu = nyaux+(domains.Number_of_Elements_in_Y-i)
         #                 var[nyl:nyu,0:nx] = BC.value
                         
                         
         # elif self.name == "Initial Convection Temperature":
         #     for BC in problem.BoundaryConditions:
         #         if BC.kind == "Convection":
         #             if (BC.x0 == BC.x1) and (BC.x0 != 0.0):
         #                 if BC.y0 == 0.0:
         #                     VarConv[1:BC.ny+1,-1] = BC.value
         #                 if BC.y0 != 0.0:
         #                     VarConv[-2:-BC.ny-2:-1,-1] = BC.value                             
         #             if (BC.x0 == BC.x1) and (BC.x0 == 0.0):
         #                 if BC.y0 == 0.0:
         #                     VarConv[1:BC.ny+1, 0]=BC.value
         #                 if BC.y0 != 0.0:
         #                    VarConv[-2:-BC.ny-2:-1,0] = BC.value 
         #             if (BC.y0 == BC.y1) and (BC.y0 == problem.Total_Thickness):
         #                    VarConv[-1, 1:BC.nx+1] = BC.value
         #             if (BC.y0 == BC.y1) and (BC.y0 == 0.0):   
         #                 VarConv[0, 1:BC.nx+1] = BC.value
         #            # if BC.edge == "Bottom Edge":
         #            #     if BC.y0 == 0:
         #             var=VarConv
         #        # import pdb; pdb.set_trace()
                             
                  
                                    
         # else:
         #     for domain in problem.domains:
         #         nx=domain.Number_of_Elements_in_X
         #         nyu=nyu+domain.Number_of_Elements_in_Y
         #         var[nyl:nyu, 0:nx]=domain.initial_fields[self.name]
         #         nyl=nyu
         # self.var=var
             
             
