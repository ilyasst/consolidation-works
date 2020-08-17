from .domains import RectangularDomain
from .boundaryconditions import LinearBC

class TwoPlates:

    def __init__(self, deck):
        self.set_problem_parameters(deck)
        self.set_domains(deck)
        self.set_boundaryconds(deck)

    def set_problem_parameters(self, deck):
        self.dimensions = 2
        self.Lx = float(deck.doc["Geometry"]["Width (X)"])
        self.Ly = float(deck.doc["Geometry"]["Length (Y)"])

    def set_domains(self, deck):
        self.domains = []
        for deck_domain in deck.doc["Materials"]:
            if deck_domain == "Bottom Plate":
                corner0 = (0,0)
                corner1 = (self.Lx ,self.Ly/2.)
                plate_material = deck.doc["Materials"][deck_domain]
                self.domains.append(RectangularDomain(deck_domain, corner0, corner1, plate_material))
            elif deck_domain == "Top Plate":
                corner0 = (0,self.Ly/2.)
                corner1 = (self.Lx ,self.Ly)
                plate_material = deck.doc["Materials"][deck_domain]
                self.domains.append(RectangularDomain(deck_domain, corner0, corner1, plate_material))


    def set_boundaryconds(self, deck):
        self.boundaryconditions = []
        for deck_BC in deck.doc["Boundary Conditions"]:
            if deck_BC == "Top Plate Top":
                self.boundaryconditions.append( LinearBC( (0.,self.Ly), (self.Lx,self.Ly), deck.doc["Boundary Conditions"][deck_BC] ) )
            elif deck_BC == "Top Plate Left":
                self.boundaryconditions.append( LinearBC( (0.,self.Ly/2.), (0.,self.Ly), deck.doc["Boundary Conditions"][deck_BC] ) )
            elif deck_BC == "Top Plate Right":
                self.boundaryconditions.append( LinearBC( (self.Lx,self.Ly/2.), (self.Lx,self.Ly), deck.doc["Boundary Conditions"][deck_BC] ) )
            elif deck_BC == "Bottom Plate Bottom":
                self.boundaryconditions.append( LinearBC( (0.,0.), (self.Lx,0.), deck.doc["Boundary Conditions"][deck_BC] ) )
            elif deck_BC == "Bottom Plate Left":
                self.boundaryconditions.append( LinearBC( (0.,0.), (0.,self.Ly/2.), deck.doc["Boundary Conditions"][deck_BC] ) )
            elif deck_BC == "Bottom Plate Right":
                self.boundaryconditions.append( LinearBC( (self.Lx,0.), (self.Lx,self.Ly/2.), deck.doc["Boundary Conditions"][deck_BC] ) )
            elif deck_BC == "Weld Line":
                self.boundaryconditions.append( LinearBC( (0.,self.Ly/2), (self.Lx,self.Ly/2.), deck.doc["Boundary Conditions"][deck_BC] ) )
