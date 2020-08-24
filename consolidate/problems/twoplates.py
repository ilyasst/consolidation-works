from .domains import RectangularDomain
from .boundaryconditions import LinearBC
from .properties import Properties
from .initialconditions import InitialConditions
from .mesh import DefineMesh
from .boundaryconditions2 import BoundaryCondition
from .geometry import DefineGeometry
from .characterizedomain import CharacterizeDomain
from .simulationpar import SimulationParameters


class TwoPlates:

    def __init__(self, deck):
        self.required_fields = ["Initial Temperature", "Thermal Conductivity X", "Thermal Conductivity Y", "Density", "Specific Heat", "Heat Input", "Initial Convection Temperature", "dx","dy"]
        self.set_problem_parameters(deck)
        self.set_domains(deck)
        self.set_simulation_parameters(deck)
        # self.set_boundaryconds(deck)
        # self.set_initialconds(deck)


    def set_simulation_parameters(self,deck):
        self.SimulationParameters=[]
        for par in deck.doc["Simulation"]:
            self.SimulationParameters.append(SimulationParameters(par, deck.doc["Simulation"][par]))
    
    def set_problem_parameters(self, deck):
        ny=0
        t=0
        for domain in deck.doc["Domains"]:
            ny=ny+int(deck.doc["Domains"][domain]["Mesh"]["Number of Elements in Y"])
            t = t+float(deck.doc["Domains"][domain]["Geometry"]["Thickness (Y)"])
        self.TotalNy = ny
        self.TotalThickness = t
        
        
    def set_domains(self, deck):
        self.domains=[]
        MatProp=[]
        InitConditions=[]
        Mesh=[]
        BoundaryConditions=[]
        Geometry=[]
        for deck_domain in deck.doc["Domains"]:
            if deck.doc["Domains"][deck_domain]["Geometry"]["Pos"] == "1":
                name = "Bottom Domain"
                corner0 = (0,0)
                corner1 = (float(deck.doc["Domains"][deck_domain]["Geometry"]["Width (X)"]),float(deck.doc["Domains"][deck_domain]["Geometry"]["Thickness (Y)"]))
                
            if deck.doc["Domains"][deck_domain]["Geometry"]["Pos"] == "2":
                name = "Middle Domain"
                for domain_aux in deck.doc["Domains"]:
                    if deck.doc["Domains"][domain_aux]["Geometry"]["Pos"] == "1":
                        aux=float(deck.doc["Domains"][domain_aux]["Geometry"]["Thickness (Y)"])
                        corner0=(0, aux)
                        corner1 = (float(deck.doc["Domains"][deck_domain]["Geometry"]["Width (X)"]),aux+float(deck.doc["Domains"][deck_domain]["Geometry"]["Thickness (Y)"]))
                       
                        
            if deck.doc["Domains"][deck_domain]["Geometry"]["Pos"] == "3":
                name = "Top Domain"
                corner0 = (0, self.TotalThickness-float(deck.doc["Domains"][deck_domain]["Geometry"]["Thickness (Y)"]))
                corner1 = (float(deck.doc["Domains"][deck_domain]["Geometry"]["Width (X)"]), self.TotalThickness)
                # import pdb; pdb.set_trace()
            # self.domains.append(RectangularDomain(name, corner0, corner1))
                
            for prop in deck.doc["Domains"][deck_domain]["Material"]:
                MatProp.append(Properties(prop, float(deck.doc["Domains"][deck_domain]["Material"][prop])))
                
            for initcond in deck.doc["Domains"][deck_domain]["Initial Condition"]:
                InitConditions.append(InitialConditions(initcond, float(deck.doc["Domains"][deck_domain]["Initial Condition"][initcond])))
            for mesh in deck.doc["Domains"][deck_domain]["Mesh"]:
                Mesh.append(DefineMesh(mesh, float(deck.doc["Domains"][deck_domain]["Mesh"][mesh])))
            # if deck.doc["Domains"][deck_domain]["Geometry"]["Pos"] == "1" or deck.doc["Domains"][deck_domain]["Geometry"]["Pos"] == "3":
            for edge in deck.doc["Domains"][deck_domain]["Boundary Condition"]:
                for BC in deck.doc["Domains"][deck_domain]["Boundary Condition"][edge]:
                    # import pdb; pdb.set_trace()
                    BoundaryConditions.append(BoundaryCondition(edge,BC, float(deck.doc["Domains"][deck_domain]["Boundary Condition"][edge][BC])))
            for geometry in deck.doc["Domains"][deck_domain]["Geometry"]:
                Geometry.append(DefineGeometry(geometry,(deck.doc["Domains"][deck_domain]["Geometry"][geometry])))
            self.domains.append(RectangularDomain(name, corner0, corner1, MatProp,InitConditions, Mesh, BoundaryConditions, Geometry))
            MatProp=[]       
            InitiConditions=[]
            Mesh=[]
            BoundaryConditions=[]
            Geometry=[]
                
                
                
                
                
                
                
                
                
      # def set_boundaryconds(self, deck):
    #     self.BoundaryConditions = []
    #     for BC_domain in self.domains:
    #         if BC_domain.name == "Bottom Plate" or BC_domain.name == "Top Plate":              
    #             for edge in deck.doc["Boundary Conditions"][BC_domain.name].keys(): 
    #                 for model in deck.doc["Boundary Conditions"][BC_domain.name][edge]["Models"].keys():       
    #                     # import pdb; pdb.set_trace()
    #                     if model == "Convection":    
    #                         if edge=="Left Edge":
    #                             # import pdb; pdb.set_trace()
    #                             self.BoundaryConditions.append (LinearBC ( (BC_domain.x0, BC_domain.y0), (BC_domain.x0, BC_domain.y1), model, "Temperature", deck.doc["Boundary Conditions"][BC_domain.name][edge]["Models"][model]["Temperature"], BC_domain.name, edge, BC_domain.Number_of_Elements_in_X, BC_domain.Number_of_Elements_in_Y ) )
    #                         if edge=="Bottom Edge":
    #                             self.BoundaryConditions.append(LinearBC ( (BC_domain.x0, BC_domain.y0), (BC_domain.x1, BC_domain.y0), model, "Temperature", deck.doc["Boundary Conditions"][BC_domain.name][edge]["Models"][model]["Temperature"], BC_domain.name, edge, BC_domain.Number_of_Elements_in_X, BC_domain.Number_of_Elements_in_Y ) )
    #                         if edge=="Right Edge":
    #                             self.BoundaryConditions.append(LinearBC ( (BC_domain.x1, BC_domain.y0), (BC_domain.x1, BC_domain.y1), model, "Temperature", deck.doc["Boundary Conditions"][BC_domain.name][edge]["Models"][model]["Temperature"], BC_domain.name, edge, BC_domain.Number_of_Elements_in_X, BC_domain.Number_of_Elements_in_Y ) )
    #                         if edge=="Top Edge":            
    #                             self.BoundaryConditions.append(LinearBC ( (BC_domain.x0, BC_domain.y1), (BC_domain.x1, BC_domain.y1), model, "Temperature", deck.doc["Boundary Conditions"][BC_domain.name][edge]["Models"][model]["Temperature"], BC_domain.name, edge, BC_domain.Number_of_Elements_in_X, BC_domain.Number_of_Elements_in_Y ) )
                        
    #                     if model == "Intimate Contact":
    #                         for parameter in deck.doc["Boundary Conditions"][BC_domain.name][edge]["Models"][model].keys():
    #                             if edge=="Top Edge":
    #                                 self.BoundaryConditions.append (LinearBC ( (BC_domain.x0, BC_domain.y0), (BC_domain.x0, BC_domain.y1), model, parameter, deck.doc["Boundary Conditions"][BC_domain.name][edge]["Models"][model][parameter], BC_domain.name, edge, BC_domain.Number_of_Elements_in_X, BC_domain.Number_of_Elements_in_Y ) )
    #                             if edge=="Bottom Edge":
    #                                 self.BoundaryConditions.append (LinearBC ( (BC_domain.x0, BC_domain.y0), (BC_domain.x0, BC_domain.y1), model, parameter, deck.doc["Boundary Conditions"][BC_domain.name][edge]["Models"][model][parameter], BC_domain.name, edge, BC_domain.Number_of_Elements_in_X, BC_domain.Number_of_Elements_in_Y ) )
                                          

    #         elif BC_domain.name == "Heat Element":
    #             for model in deck.doc["Boundary Conditions"][BC_domain.name]["Models"].keys():
    #                 if model == "Heating":
    #                     parameter = "Input Power Density"
    #                     self.BoundaryConditions.append (LinearBC ( (BC_domain.x0, BC_domain.y1), (BC_domain.x1, BC_domain.y1), model, parameter, deck.doc["Boundary Conditions"][BC_domain.name]["Models"][model][parameter], BC_domain.name, "all", BC_domain.Number_of_Elements_in_X, BC_domain.Number_of_Elements_in_Y) )             

               
                
                
                    
                
                
            # if deck.doc["Domains"][deck_domain]["Geometry"]["Pos"] == "2":
            #     for deck_aux in deck.doc["Domains"]:
            #         if deck.doc["Domains"][deck_aux]["Geometry"]["Pos"] == "1":
            #             aux=float(deck.doc["Domains"][deck_aux]["Geometry"]["Thickness (Y)"])
            #             corner0 = (0,aux)
            #             corner1 = (float(deck.doc["Domains"][deck_domain]["Geometry"]["Width (X)"]),float(deck.doc["Domains"][deck_domain]["Geometry"]["Thickness (Y)"])+aux)
            #     self.domains.append(RectangularDomain("Middle Domain", corner0, corner1, deck.doc["Domains"][deck_domain]))
            # if deck.doc["Domains"][deck_domain]["Geometry"]["Pos"] == "3":
            #     corner0 = (0,self.TotalThickness - float(deck.doc["Domains"][deck_domain]["Geometry"]["Thickness (Y)"]))
            #     corner1 = (float(deck.doc["Domains"][deck_domain]["Geometry"]["Width (X)"]), self.TotalThickness)
            #     self.domains.append(RectangularDomain("Top Domain", corner0, corner1, deck.doc["Domains"][deck_domain]))
        
        
        
                
            
        
       
        

                
        
                

       

    # def set_domains(self, deck):
    #     self.domains = []
    #     for deck_domain in deck.doc["Materials"]:
    #         if deck_domain == "Bottom Plate":
    #             corner0 = (0,0)
    #             corner1 = self.geometry[deck_domain][0]
    #             plate_material = deck.doc["Materials"][deck_domain]
    #             plate_initial_temperature=float(deck.doc["Initial Conditions"][deck_domain]["Initial Temperature"])
    #             number_of_elements_X = int(deck.doc["Mesh"][deck_domain]["Number of Elements in X"])
    #             number_of_elements_Y = int(deck.doc["Mesh"][deck_domain]["Number of Elements in Y"])
    #             self.domains.append(RectangularDomain(deck_domain, corner0, corner1, plate_initial_temperature, number_of_elements_X, number_of_elements_Y))
    #         elif deck_domain == "Heat Element":
    #             corner0=(0,self.geometry["Bottom Plate"][0][1])
    #             corner1 = (self.geometry[deck_domain][0][0],self.geometry["Bottom Plate"][0][1]+self.geometry[deck_domain][0][1])
    #             plate_material = deck.doc["Materials"][deck_domain]
    #             plate_initial_temperature=float(deck.doc["Initial Conditions"][deck_domain]["Initial Temperature"])
    #             number_of_elements_X = int(deck.doc["Mesh"][deck_domain]["Number of Elements in X"])
    #             number_of_elements_Y = int(deck.doc["Mesh"][deck_domain]["Number of Elements in Y"])
    #             self.domains.append(RectangularDomain(deck_domain, corner0, corner1, plate_material,plate_initial_temperature, number_of_elements_X, number_of_elements_Y))
    #         elif deck_domain == "Top Plate":
    #             corner0 = (0,self.geometry["Bottom Plate"][0][1]+self.geometry["Heat Element"][0][1])
    #             corner1 = (self.geometry[deck_domain][0][0],self.geometry["Bottom Plate"][0][1]+self.geometry["Heat Element"][0][1]++self.geometry[deck_domain][0][1])
    #             plate_material = deck.doc["Materials"][deck_domain]
    #             plate_initial_temperature=float(deck.doc["Initial Conditions"][deck_domain]["Initial Temperature"])
    #             number_of_elements_X = int(deck.doc["Mesh"][deck_domain]["Number of Elements in X"])
    #             number_of_elements_Y = int(deck.doc["Mesh"][deck_domain]["Number of Elements in Y"])
    #             self.domains.append(RectangularDomain(deck_domain, corner0, corner1, plate_material,plate_initial_temperature, number_of_elements_X, number_of_elements_Y ))
                
                
                
                
    # def set_initialconds(self, deck):
    #     for domain in self.domains:
    #         for field in self.required_fields:                
    #             if field in field in domain.MaterialProperties:                    
    #                 domain.set_field_init_value({field: domain.MaterialProperties[field]})
    #             elif field in field in domain.InitialConditions:
    #                 import pdb; pdb.set_trace()
    #                 domain.set_field_init_value({field: domain.InitialConditions[field]})
    #                 import pdb; pdb.set_trace()
    #             elif field =="dx":
    #                 domain.set_field_init_value({field: domain.Lx/domain.Mesh["Number of Elements in X"] })
    #             elif field == "dy":
    #                 domain.set_field_init_value({field: domain.Ly/domain.Mesh["Number of Elements in Y"] })
                    
                    
                # elif field in field in deck.doc["Initial Conditions"][domain.name]:
                #     domain.set_field_init_value({field: domain.InitialConditions[field]})
                # elif field == "dx":
                #     domain.set_field_init_value({field: domain.Lx/domain.Number_of_Elements_in_X })
                # elif field == "dy":
                #     domain.set_field_init_value({field: domain.Ly/domain.Number_of_Elements_in_Y })
                
                    
    
   
            
                    
                
                
        