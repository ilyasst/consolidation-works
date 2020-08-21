# import numpy as np
import numpy as np

            
class Field:
     def __init__(self, name, shape, problem):
        self.name = name
        self.populate_field(shape, problem)

                    
     def populate_field(self, shape, problem):
         # import pdb; pdb.set_trace()
         self.var = shape.copy()
         var=shape.copy()
         VarConv=shape.copy()
         nx=0
         nyu=0
         nyl=0
         if self.name == "Heat Input":
             for BC in problem.BoundaryConditions:
                 if BC.kind == "Heating":
                     nyaux=0
                     for i, domains in enumerate(problem.domains):
                         nyaux=(domains.Number_of_Elements_in_Y)+nyaux
                         if domains.name == BC.domain:
                             nx = domains.Number_of_Elements_in_X
                             nyl = nyaux-i
                             nyu = nyaux+(domains.Number_of_Elements_in_Y-i)
                         var[nyl:nyu,0:nx] = BC.value
                         
                         
         elif self.name == "Initial Convection Temperature":
             for BC in problem.BoundaryConditions:
                 if BC.kind == "Convection":
                     if BC.edge == "Left Edge":
                         aux=np.zeros((np.shape(VarConv)[0],1))
                         if BC.domain == "Bottom Plate":
                             VarConv=np.concatenate((aux,VarConv),axis=1)
                     if BC.edge == "Bottom Edge":
                         aux=np.zeros((1,np.shape(VarConv)[1]))
                         if BC.domain == "Bottom Plate":
                             VarConv=np.concatenate((aux, VarConv),axis=0)
                     if BC.edge == "Right Edge":
                         aux=np.zeros((np.shape(VarConv)[0],1))
                         if BC.domain == "Bottom Plate":
                             VarConv=np.concatenate((VarConv,aux),axis=1)
                     if BC.edge == "Top Edge":
                         aux=np.zeros((1,np.shape(VarConv)[1]))
                         if BC.domain == "Top Plate":
                             VarConv=np.concatenate(( VarConv,aux),axis=0)
                    
                        
                     for domain_name in problem.domains:
                         if domain_name.name == BC.domain:
                             if BC.domain == "Bottom Plate":
                                 nyl=0
                                 nyu=domain_name.Number_of_Elements_in_Y
                                 if BC.edge == "Bottom Edge":
                                     VarConv[0, 1:domain_name.Number_of_Elements_in_X+1]=BC.value
                                 if BC.edge == "Left Edge":
                                     VarConv[0:domain_name.Number_of_Elements_in_Y, 0]=BC.value
                                 if BC.edge == "Right Edge":
                                    VarConv[1:domain_name.Number_of_Elements_in_Y+1, -1]=BC.value
                                    
                                    
                             if BC.domain == "Top Plate":
                                 nyltp = nyu + problem.domains[1].Number_of_Elements_in_Y
                                 nyutp = nyltp + domain_name.Number_of_Elements_in_Y
                                 if BC.edge == "Top Edge":
                                     VarConv[-1, 1:domain_name.Number_of_Elements_in_X+1]=BC.value
                                 if BC.edge == "Left Edge":
                                     VarConv[1+nyltp:nyutp+1, 0]=BC.value
                                 if BC.edge == "Right Edge":
                                    VarConv[1+nyltp:nyutp+1, -1]=BC.value
                                 # import pdb; pdb.set_trace()
                                    var=VarConv
         else:
             for domain in problem.domains:
                  nx=domain.Number_of_Elements_in_X
                  nyu=nyu+domain.Number_of_Elements_in_Y
                  var[nyl:nyu, 0:nx]=domain.initial_fields[self.name]
                  nyl=nyu
         self.var=var
             
             
