from .domains import RectangularDomain
import numpy as np


class TwoPlates:

    def __init__(self, deck):
        self.total_plates=int(deck.doc["Problem Type"]["Total Plates"])
        self.set_simulation_parameters(deck)
        self.set_problem_parameters(deck)
        self.set_domains(deck)
        self.set_elements(deck)
        self.set_create_mask(deck)
        self.create_fields(deck)
        self.populate_fields_locally(deck)


    def set_simulation_parameters(self,deck):
        self.SimulationParameters = {}
        for par in deck.doc["Simulation"]:
            self.SimulationParameters[par] = deck.doc["Simulation"][par]

    def set_problem_parameters(self, deck):
        ny = 0
        thickness = 0
        for domain in deck.doc["Domains"]:
            domain_dir = deck.doc["Domains"][domain]
            ny = ny + int(domain_dir["Mesh"]["Points in Y"])
            nx = int(domain_dir["Mesh"]["Points in X"])
            current_thickness = float(domain_dir["Geometry"]["y1"])
            if current_thickness > thickness:
                thickness = current_thickness
            
        self.totalpy = ny
        self.totalpx = nx
        self.totalthickness = thickness

    def is_top_plate(self,y1,totalthickness):
        return y1 == totalthickness

    def is_bottom_plate(self,y0):
        return y0 == 0

    def set_domains(self, deck):
        self.domains = []
        for domain_name in deck.doc["Domains"]:
            self.domains.append(RectangularDomain(domain_name))

    def set_elements(self, deck):
        for domain in self.domains:
            dimen_y0 = float(deck.doc["Domains"][domain.name]["Geometry"]["y0"])
            dimen_y1 = float(deck.doc["Domains"][domain.name]["Geometry"]["y1"])
            if self.is_top_plate(dimen_y1,self.totalthickness):
                p_x0 =  0
                p_x1 = int(deck.doc["Domains"][domain.name]["Mesh"]["Points in X"])-1
                p_y1 = self.totalpy
                p_y0 = p_y1 - int(deck.doc["Domains"][domain.name]["Mesh"]["Points in Y"])
            elif self.is_bottom_plate(dimen_y0):
                p_x0 = 0
                p_x1 = int(deck.doc["Domains"][domain.name]["Mesh"]["Points in X"])-1
                p_y0 = 0
                p_y1= int(deck.doc["Domains"][domain.name]["Mesh"]["Points in Y"])-1
            else:
                aux=0
                for i in range (1, int(domain.name[-1])):
                    aux = aux +  int(deck.doc["Domains"]["Plate " + str(i)]["Mesh"]["Points in X"])
                p_x0 = 0
                p_x1 = int(deck.doc["Domains"][domain.name]["Mesh"]["Points in X"])-1
                p_y0 = aux
                p_y1 = aux + int(deck.doc["Domains"][domain.name]["Mesh"]["Points in Y"])-1
            
            domain.set_points_domains(p_x0, p_x1, p_y0, p_y1)

    def set_create_mask(self, deck):
        for domain in self.domains:
            dimen_y = [float(deck.doc["Domains"][domain.name]["Geometry"]["y0"]), float(deck.doc["Domains"][domain.name]["Geometry"]["y1"])]
            domain.generate_mask(self.totalpy,self.totalpx, dimen_y, self.totalthickness)

    def create_fields(self, deck):
        if deck.doc["Problem Type"]["Type"] == "Welding":
            self.required_fields=["Temperature", "kx", "ky", "Density", "Cp", "Viscosity", "Equivalent External Temperature", "Power Input Heat", "Intimate Contact", "dx","dy"]
        if deck.doc["Problem Type"]["Type"] == "Heat Transfer":
            self.required_fields=["Temperature", "kx", "ky", "Density", "Cp", "Viscosity", "Equivalent External Temperature", "Power Input Heat", "dx","dy"]
    def create_external_mask(self, deck):
        for domain in self.domains:
            self.mask_external_boundary = {}
            deck_dir = deck.doc["Domains"][domain.name]
            bc_ext = {}
            for edge in deck_dir["Boundary Condition"]["External"]:
                bc_ext[edge] = np.zeros((self.totalNy+2, self.totalNx+2))

    def populate_fields_locally(self,deck):
        for field_name in self.required_fields:
            for domain in self.domains:
                domain_dir = deck.doc["Domains"][domain.name]
                if field_name == "dx":
                    delta = float(domain_dir["Geometry"]["x1"]) - float(domain_dir["Geometry"]["x0"])
                    inc = delta/int(domain_dir["Mesh"]["Points in X"])
                    value = inc*domain.mask
                    domain.set_field(field_name, value)
                elif field_name == "dy":
                    delta = float(domain_dir["Geometry"]["y1"]) - float(domain_dir["Geometry"]["y0"])
                    inc = delta/int(domain_dir["Mesh"]["Points in Y"])
                    value = inc*domain.mask
                    domain.set_field(field_name, value)
                elif field_name == "Equivalent External Temperature":
                    temp = float(domain_dir["Initial Condition"]["Temperature"])
                    value=0
                    for edge in domain_dir["Boundary Condition"]["External"]:
                        if edge == "Top Edge" or edge == "Bottom Edge":
                            delta = float(domain_dir["Geometry"]["y1"]) - float(domain_dir["Geometry"]["y0"])
                            inc = delta/int(domain_dir["Mesh"]["Points in Y"])
                            k = float(domain_dir["Material"]["ky"])
                            roomtemp = float (domain_dir["Boundary Condition"]["External"][edge]["Room Temperature"])
                            value =value+-2*inc*((float(domain_dir["Boundary Condition"]["External"][edge]["Convection Coefficient"])/k)*(temp-roomtemp) + temp)*(domain.mask_external_boundary[edge])
                        if edge == "Left Edge" or edge =="Right Edge":
                            delta = float(domain_dir["Geometry"]["x1"]) - float(domain_dir["Geometry"]["x0"])
                            inc = delta/int(domain_dir["Mesh"]["Points in X"])
                            k = float(domain_dir["Material"]["kx"])
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
                    a = float(domain_dir["Material"]["Viscosity"]["A"])
                    b = float(domain_dir["Material"]["Viscosity"]["Ea"])
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