from .domains import RectangularDomain
import numpy as np


class TwoPlates:

    def __init__(self, deck):
        self.total_plates=int(deck.doc["Problem Type"]["Total Plates"])
        self.set_simulation_parameters(deck)
        self.set_problem_parameters(deck)
        self.set_domains(deck)
        self.set_elements(deck)
        self.set_materials(deck)
        self.set_bcs(deck)
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
        self.length = float(deck.doc["Problem Type"]["Length"])


    def is_top_plate(self,y1,totalthickness):
        return y1 == totalthickness

    def is_bottom_plate(self,y0):
        return y0 == 0

    def set_domains(self, deck):
        self.domains = []
        for domain_name in deck.doc["Domains"]:
            dimen_x0 = float(deck.doc["Domains"][domain_name]["Geometry"]["x0"])
            dimen_x1 = float(deck.doc["Domains"][domain_name]["Geometry"]["x1"])
            dimen_y0 = float(deck.doc["Domains"][domain_name]["Geometry"]["y0"])
            dimen_y1 = float(deck.doc["Domains"][domain_name]["Geometry"]["y1"])
            
            self.domains.append(RectangularDomain(domain_name, dimen_x0, dimen_x1, dimen_y0, dimen_y1))

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
                    aux = aux +  int(deck.doc["Domains"]["Plate " + str(i)]["Mesh"]["Points in Y"])
                p_x0 = 0
                p_x1 = int(deck.doc["Domains"][domain.name]["Mesh"]["Points in X"])-1
                p_y0 = aux
                p_y1 = aux + int(deck.doc["Domains"][domain.name]["Mesh"]["Points in Y"])-1
            
            domain.set_points_domains(p_x0, p_x1, p_y0, p_y1)
            

    def set_materials(self, deck):
        for domain in self.domains:
            material = {}
            domain_dir = deck.doc["Domains"][domain.name]["Material"]
            for param in domain_dir:
                if isinstance(domain_dir[param], str):
                    material[param] = float(domain_dir[param])
                else:
                    material[param] = {}
                    for aux in domain_dir[param]:
                        material[param].update({aux: float(domain_dir[param][aux])})
            domain.set_material(material)

    def set_bcs(self, deck):
        for domain in self.domains:
            bc ={}
            domain_dir = deck.doc["Domains"][domain.name]["Boundary Condition"]
            for bc_type in domain_dir:
                bc[bc_type]={}
                for kind in domain_dir[bc_type]:
                    bc[bc_type][kind]={}
                    for edge in domain_dir[bc_type][kind]:
                        bc[bc_type][kind][edge]={}
                        for param in domain_dir[bc_type][kind][edge]:
                            bc[bc_type][kind][edge].update({param : float(domain_dir[bc_type][kind][edge][param])})
            domain.set_bc(bc)

    def set_create_mask(self, deck):
        for domain in self.domains:
            dimen_y = [float(deck.doc["Domains"][domain.name]["Geometry"]["y0"]), float(deck.doc["Domains"][domain.name]["Geometry"]["y1"])]
            domain.generate_mask(self.totalpy,self.totalpx, dimen_y, self.totalthickness)

    def create_fields(self, deck):
        if deck.doc["Problem Type"]["Type"] == "Welding":
            self.required_fields=["Temperature", "kx", "ky", "Density", "Cp", "Viscosity",  "Power Input Heat", "Intimate Contact", "dx","dy", "Room Temperature","Convection Coefficient"]
        if deck.doc["Problem Type"]["Type"] == "Heat Transfer":
            self.required_fields=["Temperature", "kx", "ky", "Density", "Cp", "Viscosity", "Power Input Heat", "dx","dy", "Room Temperature", "Convection Coefficient"]
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
                    value = inc*domain.mask["Inner"]
                    domain.set_field(field_name, value)
                elif field_name == "dy":
                    delta = float(domain_dir["Geometry"]["y1"]) - float(domain_dir["Geometry"]["y0"])
                    inc = delta/int(domain_dir["Mesh"]["Points in Y"])
                    value = inc*domain.mask["Inner"]
                    domain.set_field(field_name, value)
                elif field_name == "Room Temperature":
                    value=0
                    for kind in domain_dir["Boundary Condition"]["Thermal"]:
                        for edge in domain_dir["Boundary Condition"]["Thermal"][kind]:
                            if kind == "Convection":
                                value = value + float(domain_dir["Boundary Condition"]["Thermal"][kind][edge]["Room Temperature"])*(domain.mask[edge + " External"])
                            elif kind == "Fixed Temperature":
                                value = value + float(domain_dir["Boundary Condition"]["Thermal"][kind][edge]["Temperature"])*(domain.mask[edge + " External"])
                    domain.set_field(field_name, value)
                elif field_name == "Convection Coefficient":
                    value=np.zeros((self.totalpy+2, self.totalpx+2))
                    for kind in domain_dir["Boundary Condition"]["Thermal"]:
                        for edge in domain_dir["Boundary Condition"]["Thermal"][kind]:
                            if kind == "Convection":
                                value = value + float(domain_dir["Boundary Condition"]["Thermal"][kind][edge]["Convection Coefficient"])*(domain.mask[edge + " External"])
                            else:
                                value = value
                    domain.set_field(field_name, value)
                elif field_name == "Intimate Contact":
                    value=0
                    for edge in domain_dir["Boundary Condition"]["Mechanical"]["Intimate Contact"]:
                        har = float(domain_dir["Boundary Condition"]["Mechanical"]["Intimate Contact"][edge]["Horizontal asperity ratio"])
                        value = value + har*domain.mask_contact[edge]
                        domain.set_field(field_name, value)
                elif field_name == "Viscosity":
                    a = float(domain_dir["Material"]["Viscosity"]["A"])
                    b = float(domain_dir["Material"]["Viscosity"]["Ea"])
                    temp = float(domain_dir["Initial Condition"]["Temperature"])
                    value = a*np.exp(b/temp)*domain.mask["Inner"]
                    domain.set_field(field_name, value)
                elif field_name == "Temperature":
                    aux = float(domain_dir["Initial Condition"]["Temperature"])
                    value = aux*domain.mask["Inner"]
                    for kind in domain_dir["Boundary Condition"]["Thermal"]:
                        for location in domain_dir["Boundary Condition"]["Thermal"][kind]:
                            if kind == "Convection":
                                value = value + float(domain_dir["Boundary Condition"]["Thermal"][kind][location]["Room Temperature"])*domain.mask[location + " External"]
                            elif kind == "Fixed Temperature":
                                value = value + float(domain_dir["Boundary Condition"]["Thermal"][kind][location]["Temperature"])*domain.mask[location + " External"]
                            elif kind == "Heat Flux":
                                if location !="Inner":
                                    value = value + float(domain_dir["Boundary Condition"]["Thermal"][kind][location]["Temperature"])*domain.mask[location + " External"]
                    domain.set_field(field_name, value)
                elif field_name == "Power Input Heat":
                    value = 0
                    if "Power Generation" in domain_dir["Initial Condition"]:
                        deltax = float(domain_dir["Geometry"]["x1"]) - float(domain_dir["Geometry"]["x0"])
                        deltay = float(domain_dir["Geometry"]["y1"]) - float(domain_dir["Geometry"]["y0"])
                        incx = deltax/(domain.px[1]-domain.px[0]+1)
                        incy = deltay/(domain.py[1]-domain.py[0]+1)
                        volume = deltax*deltay*self.length
                        # volume = incx*incy*self.length
                        nintervals = (domain.px[1]-domain.px[0]+1)*(domain.py[1]-domain.py[0]+1)
                        value = value+(float(domain_dir["Initial Condition"]["Power Generation"])/(volume))*domain.mask["Inner"]
                    else:
                        value = value + 0*domain.mask ["Inner"]
                    domain.set_field(field_name, value)
                else:
                    aux = float(domain_dir["Material"][field_name])
                    value = aux*domain.mask["Inner"]
                    domain.set_field(field_name, value)