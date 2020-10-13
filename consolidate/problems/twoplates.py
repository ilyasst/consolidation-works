from .domains import RectangularDomain
import numpy as np


class TwoPlates:

    def __init__(self, deck):
        self.deck=deck
        self.set_simulation_parameters(deck)
        self.set_problem_parameters(deck)
        self.set_domains(deck)
        # self.set_corner(deck)
        # self.set_mesh(deck)
        # self.set_material(deck)
        # self.set_IC(deck)
        # self.set_BC(deck)
        self.set_create_mask(deck)
        self.create_fields(deck)
        self.populate_fields_locally2(deck)
        
        
        
        
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
            self.required_fields=["Temperature",  "Thermal Conductivity X", "Thermal Conductivity Y", "Density", "Specific Heat", "Viscosity", "Equivalent External Temperature", "Power Input Heat", "Intimate Contact", "dx","dy"]

    # def populate_fields_locally(self):
    #     for field_name in self.required_fields:
    #         for domain in self.domains:
    #             if field_name == "Equivalent External Temperature":
    #                 domain.set_field_eet(domain.boundary_conditions["External"], field_name, domain.mask_external_boundary,domain)
    #             elif field_name == "Intimate Contact":
    #                 domain.set_field_ic(domain.boundary_conditions["Internal"], field_name, domain.mask_contact_interface)
    #             elif field_name == "dx" or field_name == "dy":
    #                 domain.set_field_mesh(field_name, domain.mesh[field_name], domain.mask)
    #             elif field_name == "Viscosity":
    #                 domain.set_field_viscosity(field_name, domain.material[field_name]["A"], domain.material[field_name]["Ea"],domain.initial_conditions["Temperature"],domain.mask)


    def populate_fields_locally2(self,deck):
        for field_name in self.required_fields:
            for domain in self.domains:
                domain_dir = deck.doc["Domains"][domain.name]
                if field_name == "dx":
                    inc = float(domain_dir["Geometry"]["Width (X)"])/int(domain_dir["Mesh"]["Number of Elements in X"])
                    value = inc*domain.mask
                    domain.set_field(field_name, value)
                elif field_name == "dy":
                    inc = float(domain_dir["Geometry"]["Thickness (Y)"])/int(domain_dir["Mesh"]["Number of Elements in Y"])
                    value = inc*domain.mask
                    domain.set_field(field_name, value)
                elif field_name == "Equivalent External Temperature":
                    temp = float(domain_dir["Initial Condition"]["Temperature"])
                    value=0
                    for edge in domain_dir["Boundary Condition"]["External"]:
                        if edge == "Top Edge" or "Bototm Edge":
                            inc = float(domain_dir["Geometry"]["Thickness (Y)"])/int(domain_dir["Mesh"]["Number of Elements in Y"])
                            k = float(domain_dir["Material"]["Thermal Conductivity Y"])
                            roomtemp = float (domain_dir["Boundary Condition"]["External"][edge]["Room Temperature"])
                            value =value+-2*inc*((float(domain_dir["Boundary Condition"]["External"][edge]["Convection Coefficient"])/k)*(temp-roomtemp) + temp)*(domain.mask_external_boundary[edge])
                        if edge == "Left Edge" or "Right Edge":
                            inc = float(domain_dir["Geometry"]["Width (X)"])/int(domain_dir["Mesh"]["Number of Elements in X"])
                            k = float(domain_dir["Material"]["Thermal Conductivity X"])
                            roomtemp = float (domain_dir["Boundary Condition"]["External"][edge]["Room Temperature"])
                            value =value+-2*inc*((float(domain_dir["Boundary Condition"]["External"][edge]["Convection Coefficient"])/k)*(temp-roomtemp) + temp)*(domain.mask_external_boundary[edge])
                    domain.set_field(field_name, value)
                elif field_name == "Intimate Contact":
                    value=0
                    for edge in domain_dir["Boundary Condition"]["Internal"]:
                        har = float(domain_dir["Boundary Condition"]["Internal"][edge]["Horizontal asperity ratio"])
                        value = value + har*domain.mask_contact_interface[edge]
                        domain.set_field(field_name, value)
                elif field_name == "Viscosity":
                    a = float (domain_dir["Material"]["Viscosity"]["A"])
                    b = float( domain_dir["Material"]["Viscosity"]["Ea"])
                    temp = float(domain_dir["Initial Condition"]["Temperature"])
                    value = a*np.exp(b/temp)*domain.mask
                    domain.set_field(field_name, value)
                elif field_name == "Temperature":
                    aux = float(domain_dir["Initial Condition"]["Temperature"])
                    value = aux*domain.mask
                    domain.set_field(field_name, value)
                elif field_name == "Power Input Heat":
                    value = 0
                    if "Input Power Density" in domain_dir["Initial Condition"]:
                        value = value+float(domain_dir["Initial Condition"]["Input Power Density"])*domain.mask
                    else:
                        value = value + 0*domain.mask
                    domain.set_field(field_name, value)
                else:
                    aux = float(domain_dir["Material"][field_name])
                    value = aux*domain.mask
                    domain.set_field(field_name, value)
                    # print("Hello")
# ((-2*domain.mesh["dy"]*aux[edge]["Convection Coefficient"]/self.material["Thermal Conductivity Y"])*(self.initial_conditions["Temperature"] - aux[edge]["Room Temperature"])+self.initial_conditions["Temperature"])*mask[edge]
                    # domain.set_field_eet2(field_name, roomtemp, convcoeff,mask)
                #     domain.set_field_mesh(field_name, domain.mesh[field_name], domain.mask)
                # elif field_name == "Viscosity":
                #     domain.set_field_viscosity(field_name, domain.material[field_name]["A"], domain.material[field_name]["Ea"],domain.initial_conditions["Temperature"],domain.mask)
