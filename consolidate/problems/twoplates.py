from .domains import RectangularDomain
# from .boundaryconditions import LinearBC
import numpy as np


class TwoPlates:

    def __init__(self, deck):
        self.set_simulation_parameters(deck)
        self.set_problem_parameters(deck)
        self.set_domains(deck)
        self.set_corner(deck)
        self.set_mesh(deck)
        self.set_material(deck)
        self.set_IC(deck)
        self.set_BC(deck)
        self.set_create_mask(deck)
        self.create_fields(deck)
        self.populate_fields_locally()
        
        
        
    def set_simulation_parameters(self,deck):
        self.SimulationParameters = {}
        for par in deck.doc["Simulation"]:
            self.SimulationParameters[par]= deck.doc["Simulation"][par]
            
            
    def set_problem_parameters(self, deck):
        ny = 0
        t = 0
        for domain in deck.doc["Domains"]:
            ny = ny + int(deck.doc["Domains"][domain]["Mesh"]["Number of Elements in Y"])
            nx = int(deck.doc["Domains"][domain]["Mesh"]["Number of Elements in X"])
            t = t + float(deck.doc["Domains"][domain]["Geometry"]["Thickness (Y)"])
            
        self.totalNy = ny
        self.totalNx = nx
        self.total_thickness = t
        
    def set_domains(self, deck):
        self.domains = []
        
        for deck_domain in deck.doc["Domains"]:
            position = int(deck.doc["Domains"][deck_domain]["Geometry"]["Pos"])
            
            if  position == 1:
                ele_x0 = 0
                ele_x1 = int(deck.doc["Domains"][deck_domain]["Mesh"]["Number of Elements in X"])
                ele_y0 = 0
                ele_y1 = int(deck.doc["Domains"][deck_domain]["Mesh"]["Number of Elements in Y"])-1
                
            if position == 2:
                for domain_aux in deck.doc["Domains"]:
                    if deck.doc["Domains"][domain_aux]["Geometry"]["Pos"] == "1":
                        auxeley=int(deck.doc["Domains"][domain_aux]["Mesh"]["Number of Elements in Y"])
                        ele_x0 = 0
                        ele_x1 = int(deck.doc["Domains"][deck_domain]["Mesh"]["Number of Elements in X"])
                        ele_y0 = auxeley
                        ele_y1 = int(deck.doc["Domains"][deck_domain]["Mesh"]["Number of Elements in Y"])+auxeley-1
                        
            if position == 3:
                ele_x0 = 0
                ele_x1 = int(deck.doc["Domains"][deck_domain]["Mesh"]["Number of Elements in X"])
                ele_y0 = int(self.totalNy)-int(float(deck.doc["Domains"][deck_domain]["Mesh"]["Number of Elements in Y"]))
                ele_y1 = int(self.totalNy)-1

            self.domains.append(RectangularDomain(deck_domain, ele_x0, ele_x1, ele_y0,ele_y1, position))

    def set_corner(self, deck):
        for domain in self.domains:
            domain.set_corners(domain.name, deck)
            
    def set_mesh(self, deck):
        aux={}
        for domain in self.domains:
            domain.set_mesh(domain.name, deck, domain.dimensions)



    def set_BC(self, deck):
        for domain in self.domains:
            domain.set_bc(domain.name, deck)

    def set_material(self, deck):
        for domain in self.domains:
            domain.set_material(domain.name, deck)

    def set_IC(self, deck):
        for domain in self.domains:
            domain.set_IC(domain.name, deck)
            
    
    
    def set_create_mask(self, deck):
        for domain in self.domains:
            domain.generate_mask(self.totalNy,self.totalNx)
    
    def create_fields(self, deck):
            self.required_fields=["Internal Temperature",  "Thermal Conductivity X", "Thermal Conductivity Y", "Density", "Heat Capacity", "Viscosity", "Equivalent External Temperature", "Power Input Heat", "Intimate Contact", "dx","dy"]
    
    def populate_fields_locally(self):
        for field_name in self.required_fields:
            for domain in self.domains:
                if field_name == "Equivalent External Temperature":
                    domain.set_eet(domain.boundary_conditions["External"], field_name, domain.mask_external_boundary,domain.mesh["dy"], domain.mesh["dx"], domain.material["Thermal Conductivity Y"], domain.material["Thermal Conductivity X"], domain.initial_conditions["Temperature"])
                elif field_name == "Intimate Contact":
                    domain.set_ibc(domain.boundary_conditions["Internal"], field_name, domain.mask_contact_interface)
                #     domain.set_fields(domain.boundary_conditions["Internal"], field_name, domain.mask_contact_interface)
                    
                # elif field_name == "Intimate Contact":
                    
                # else:
                #     for mask in domain.masks:
                #         if "Internal" in mask.__dict__.values():
                #             domain.set_fields(domain, field_name, mask)