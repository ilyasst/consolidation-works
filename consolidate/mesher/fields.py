import numpy as np

class Field:
    
    
    
    
    def __init__(self,  problem ):
        # self.name = variable
        # self.populate_field(variable,domain)
        self.field_size(problem)
        self.create_field(problem)
        
    # def populate_field(self, variable, domain):
        
    #     if variable == "Temperature":
    #         # import pdb; pdb.set_trace()
    #         value=domain.initial_temperature*np.ones((domain.Number_of_Elements_in_X,domain.Number_of_Elements_in_Y))
    #         # 
    #         self.var=value
        
    def field_size(self, problem):
        nx=0
        ny=0
        for domain in problem.domains:
            nx=nx+domain.Number_of_Elements_in_X
            ny=ny+domain.Number_of_Elements_in_X
        self.nx = nx
        self.ny = ny
        
    def create_field (self, problem):
        
        fields={}
        res=[]
        for field in problem.required_fields:
            for domain in problem.domains:
                if field == "Temperature":
                    test=(domain.initial_temperature*np.ones((domain.Number_of_Elements_in_Y, domain.Number_of_Elements_in_X)))                     
                    if domain == problem.domains[0]:
                        res=test    
                        fields[field]=res
                        test=[]
                    
                    else:
                        res=np.concatenate((res, test))
                        fields[field]=res
                        test=[]
                    
                        
                        
                elif field != "Temperature":
                    try:
                        test=(float(domain.material[field])*np.ones((domain.Number_of_Elements_in_Y, domain.Number_of_Elements_in_X)))
                    except:
                        continue
                    if domain == problem.domains[0]:
                        res=test             
                        fields[field]=res
                        test=[]
                    else:
                        res=np.concatenate((res, test))
                        fields[field]=res
                        test=[]
                                                
                        
                
                # elif field != "Temperature": 
                #     test=(float(domain.material[field])*np.ones((domain.Number_of_Elements_in_Y, domain.Number_of_Elements_in_Y)))
   
                #     if domain == problem.domains[0]:
                #         res=test
                #         import pdb; pdb.set_trace()
                #         test=[]
                #     else:
                #         res=np.concatenate((res,test))
                #         test=[]
  
                        
                # if field=="Temperature":
                #     test= np.vstack((test , domain.initial_temperature*np.ones((domain.Number_of_Elements_in_Y, domain.Number_of_Elements_in_X))))
                    
        
                    self.fields=res
                    self.fieds2=fields

                        
                        
        
        # self.fields[field]=res
    
            
            
            
  