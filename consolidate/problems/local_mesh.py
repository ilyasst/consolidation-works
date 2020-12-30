# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 08:14:07 2020

@author: andre
"""

import numpy as np
class LocalFields:
    
    def __init__(self, problem):
        self.populate_fields_locally(problem)
    
    def populate_fields_locally(self,problem):
        
        for domain in problem.domains:
            for field_name in problem.required_fields:
                value=0
                extTemp=0
                if field_name == "dx":
                    deltaX = domain.dimensions[0][1] - domain.dimensions[0][0]
                    incX = deltaX/(domain.nodes[0][1] - domain.nodes[0][0])
                    value = incX*domain.mask["Increment"]
                    domain.set_field(field_name, value)
                
                elif field_name == "dy":
                    deltaY = domain.dimensions[1][1] - domain.dimensions[1][0]
                    incY = deltaY/(domain.nodes[1][1] - domain.nodes[1][0])
                    value = incY*domain.mask["Increment"]
                    domain.set_field(field_name, value)
                    
                elif field_name == "Temperature":
                    value = domain.initial_condition["Temperature"]*domain.mask["Inner"]
                    h=np.zeros((problem.totalnodes[1], problem.totalnodes[0]))
                    for kind in domain.boundary_condition["Thermal"]:
                        for edge in domain.boundary_condition["Thermal"][kind]:
                            import pdb; pdb.set_trace()
                            extTemp = extTemp + domain.boundary_condition["Thermal"][kind][edge]["Temperature"]*domain.mask_out[edge]
                            if kind == "Fixed Boundary":
                                
                                value = value + domain.boundary_condition["Thermal"][kind][edge]["Temperature"]*domain.mask[edge]
                                h=h
                            elif kind == "Convection":
                                value = value + domain.boundary_condition["Thermal"][kind][edge]["Temperature"]*domain.mask[edge]
                                h = h + domain.boundary_condition["Thermal"][kind][edge]["Convection Coefficient"]*(domain.mask[edge])
                    for edge in domain.mask_interface:
                        value = value + domain.initial_condition["Temperature"]*domain.mask_interface[edge]
                    domain.set_field(field_name, value)
                    domain.set_field("Convection Coefficient", h)
                    domain.set_field("Outer Temperature", extTemp)
                    
                elif field_name in domain.material:
                    if isinstance(domain.material[field_name], float):
                        # if domain.nodes[1][0] == 0 or domain.nodes[1][1] == problem.totalnodes[1]-1:
                        value = domain.material[field_name] * domain.maskprop
                        # else:
                        #     value = domain.material[field_name] * domain.mask["All"]
                        domain.set_field(field_name, value)
                    else:
                        a = domain.material[field_name]["A"]
                        b = domain.material[field_name]["Ea"]
                        temp = domain.initial_condition["Temperature"]
                        
                        if domain.nodes[1][0] == 0 or domain.nodes[1][1] == problem.totalnodes[1]-1:
                            value = a*np.exp(b/temp)* domain.mask["AllMinusInterface"]
                        else:
                            value = a*np.exp(b/temp) * domain.mask["All"]
                        domain.set_field(field_name, value)
                    
                elif field_name == "Power Input Heat":
                    value = np.zeros((problem.totalnodes[1], problem.totalnodes[0]))
                    if bool(domain.power):
                        for location in domain.power:
                            value = value + domain.power[location]*domain.mask[location]
                    else:
                        value = value
                    domain.set_field(field_name, value)
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                        
                #     value=.zeros((self.totalpy+2, self.totalpx+2))
                #     if "Power Generation" in domain_dir["Initial Condition"]:
                #         deltax = float(domain_dir["Geometry"]["x1"]) - float(domain_dir["Geometry"]["x0"])
                #         deltay = float(domain_dir["Geometry"]["y1"]) - float(domain_dir["Geometry"]["y0"])
                #         incx = deltax/(domain.px[1]-domain.px[0]+1)
                #         incy = deltay/(domain.py[1]-domain.py[0]+1)
                #         volume = deltax*deltay*self.length
                #         # volume = incx*incy*self.length
                #         nintervals = (domain.px[1]-domain.px[0]+1)*(domain.py[1]-domain.py[0]+1)
                #         value = value+(float(domain_dir["Initial Condition"]["Power Generation"])/(volume))*domain.mask["Inner"]
                #     else:
                #         value = value + 0*domain.mask ["Inner"]
                #     domain.set_field(field_name, value)
                    
        
        
        
        
        
        

               
              
                # elif field_name == "Intimate Contact":
                #     value=0
                #     for edge in domain_dir["Boundary Condition"]["Mechanical"]["Intimate Contact"]:
                #         har = float(domain_dir["Boundary Condition"]["Mechanical"]["Intimate Contact"][edge]["Horizontal asperity ratio"])
                #         value = value + har*domain.mask_contact[edge]
                #         domain.set_field(field_name, value)
                # elif field_name == "Viscosity":
                #     a = float(domain_dir["Material"]["Viscosity"]["A"])
                #     b = float(domain_dir["Material"]["Viscosity"]["Ea"])
                #     temp = float(domain_dir["Initial Condition"]["Temperature"])
                #     value = a*np.exp(b/temp)*domain.mask["Inner"]
                #     domain.set_field(field_name, value)
                    
                # 
                # elif field_name == "Power Input Heat":
                #     value=np.zeros((self.totalpy+2, self.totalpx+2))
                #     if "Power Generation" in domain_dir["Initial Condition"]:
                #         deltax = float(domain_dir["Geometry"]["x1"]) - float(domain_dir["Geometry"]["x0"])
                #         deltay = float(domain_dir["Geometry"]["y1"]) - float(domain_dir["Geometry"]["y0"])
                #         incx = deltax/(domain.px[1]-domain.px[0]+1)
                #         incy = deltay/(domain.py[1]-domain.py[0]+1)
                #         volume = deltax*deltay*self.length
                #         # volume = incx*incy*self.length
                #         nintervals = (domain.px[1]-domain.px[0]+1)*(domain.py[1]-domain.py[0]+1)
                #         value = value+(float(domain_dir["Initial Condition"]["Power Generation"])/(volume))*domain.mask["Inner"]
                #     else:
                #         value = value + 0*domain.mask ["Inner"]
                #     domain.set_field(field_name, value)
