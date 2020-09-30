from .domains import RectangularDomain
# from .boundaryconditions import LinearBC
import numpy as np

class TwoPlates:

    def __init__(self, deck):
        self.set_simulation_parameters(deck)
        self.set_problem_parameters(deck)
        self.set_domains(deck)
        self.set_dimensions(deck)
        self.set_mesh(deck)
        self.set_material(deck)
        self.set_IC(deck)
        self.set_BC(deck)
        self.set_points(deck)
        self.set_create_mask(deck)
        self.fields(deck)
        
        
        
    def set_simulation_parameters(self,deck):
        self.SimulationParameters = {}
        par = "Number of Steps"
        self.SimulationParameters[par] = int(deck.doc["Simulation"][par])
        par="Step Time"
        self.SimulationParameters[par] = float(deck.doc["Simulation"][par])
        self.ProblemType = deck.doc["Problem Type"]["Type"]

        
            
    def set_problem_parameters(self, deck):
        ny = 0
        t = 0
        for domain in deck.doc["Domains"]:
            ny = ny + int(deck.doc["Domains"][domain]["Mesh"]["Number of Points in Y"])
            nx = int(deck.doc["Domains"][domain]["Mesh"]["Number of Points in X"])
            t = t + float(deck.doc["Domains"][domain]["Geometry"]["Thickness (Y)"])
            
        self.totalPointsY = ny
        self.totalPointsX = nx
        self.total_thickness = t
        import pdb; pdb.set_trace

    def set_domains(self, deck):
        self.domains = []
        for deck_domain in deck.doc["Domains"]:
            position = int(deck.doc["Domains"][deck_domain]["Geometry"]["Pos"])
            self.domains.append(RectangularDomain(deck_domain, position))

    def set_points(self, deck):
        for domain in self.domains:
            domain.set_points(domain.name, deck, self.totalPointsY)

    def set_dimensions(self, deck):
        for domain in self.domains:
            domain.set_dimensions(domain.name, deck)

    def set_mesh(self, deck):
        for domain in self.domains:
            geometry=domain.geometry[0]
            domain.set_mesh(domain.name, deck, geometry)

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
            domain.generate_mask(self.totalPointsY,self.totalPointsX)  


    def fields(self, deck):
        if self.ProblemType == "Welding":
            self.required_fields=["Internal Temperature",  "Thermal Conductivity X", "Thermal Conductivity Y", "Density", "Heat Capacity", "Viscosity", "Equivalent External Temperature", "Power Input Heat", "Intimate Contact", "dx","dy"]
        if self.ProblemType == "Heat Transfer":
            self.required_fields = ["Internal Temperature", "Thermal Conductivity X", "Thermal Conductivity Y", "Density", "Heat Capacity","Viscosity", "Equivalent External Temperature", "Power Input Density", "dx","dy"]
       
        for field_name in self.required_fields:
            for domain in self.domains:
                domain.set_fields(domain, field_name)