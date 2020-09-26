from .domains import RectangularDomain
# from .boundaryconditions import LinearBC
import numpy as np

class TwoPlates:

    def __init__(self, deck):
        self.set_simulation_parameters(deck)
        self.set_problem_parameters(deck)
        self.set_domains(deck)
        self.set_mesh(deck)
        self.set_BC(deck)
        self.set_IC(deck)
        self.set_material(deck)
        # self.set_initialconds(deck)
        
        
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
                corner0 = (0, 0)
                corner1 = (float(deck.doc["Domains"][deck_domain]["Geometry"]["Width (X)"]), float(deck.doc["Domains"][deck_domain]["Geometry"]["Thickness (Y)"]))
                ele_x0 = 0
                ele_x1 = int(deck.doc["Domains"][deck_domain]["Mesh"]["Number of Elements in X"])
                ele_y0 = 0
                ele_y1 = int(deck.doc["Domains"][deck_domain]["Mesh"]["Number of Elements in Y"])-1
                
            if position == 2:
                for domain_aux in deck.doc["Domains"]:
                    if deck.doc["Domains"][domain_aux]["Geometry"]["Pos"] == "1":
                        aux=float(deck.doc["Domains"][domain_aux]["Geometry"]["Thickness (Y)"])
                        auxeley=int(deck.doc["Domains"][domain_aux]["Mesh"]["Number of Elements in Y"])
                        corner0=(0, aux)
                        corner1 = (float(deck.doc["Domains"][deck_domain]["Geometry"]["Width (X)"]), aux + float(deck.doc["Domains"][deck_domain]["Geometry"]["Thickness (Y)"]))
                        ele_x0 = 0
                        ele_x1 = int(deck.doc["Domains"][deck_domain]["Mesh"]["Number of Elements in X"])
                        ele_y0 = auxeley
                        ele_y1 = int(deck.doc["Domains"][deck_domain]["Mesh"]["Number of Elements in Y"])+auxeley-1
                        
            if position == 3:
                corner0 = (0, self.total_thickness-float(deck.doc["Domains"][deck_domain]["Geometry"]["Thickness (Y)"]))
                corner1 = (float(deck.doc["Domains"][deck_domain]["Geometry"]["Width (X)"]), self.total_thickness)
                ele_x0 = 0
                ele_x1 = int(deck.doc["Domains"][deck_domain]["Mesh"]["Number of Elements in X"])
                ele_y0 = int(self.totalNy)-int(float(deck.doc["Domains"][deck_domain]["Mesh"]["Number of Elements in Y"]))
                ele_y1 = int(self.totalNy)-1

            self.domains.append(RectangularDomain(deck_domain, corner0, corner1, ele_x0, ele_x1, ele_y0,ele_y1, position))


    def set_BC(self, deck):
        for domain in self.domains:
            domain.set_bc(domain.name, deck)

    def set_mesh(self, deck):
        for domain in self.domains:
            domain.set_mesh(domain.name, deck)

    def set_material(self, deck):
        for domain in self.domains:
            domain.set_material(domain.name, deck)

    def set_IC(self, deck):
        for domain in self.domains:
            domain.set_IC(domain.name, deck)
                
            
    def set_initialconds(self, deck):
        for domain in self.domains:
            for variable in deck.doc["Domains"][domain.name]["Material"]:
                domain.set_field_init_value({variable : deck.doc["Domains"][domain.name]["Material"][variable]})
            domain.set_field_init_value({"dx": domain.dimensions["Lx"]/domain.mesh["Number of Elements in X"] })
            domain.set_field_init_value({"dy": domain.dimensions["Ly"]/domain.mesh["Number of Elements in Y"] })
        
            