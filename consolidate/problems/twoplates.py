from .domains import RectangularDomain
from .boundaryconditions import LinearBC

class TwoPlates:

    def __init__(self, deck):
        self.set_problem_parameters(deck)
        self.set_domains(deck)
        self.set_boundaryconds(deck)

    def set_problem_parameters(self, deck):
        self.dimensions = 2
        self.Keys = []
        for deck_geometry in deck.doc["Geometry"]:
            # if deck_geometry == "Bottom Plate":
            self.Keys.append(deck_geometry)
        self.geometry=dict.fromkeys(self.Keys,None)    
        for deck_geometry in deck.doc["Geometry"]:
            # if deck_geometry == "Bottom Plate":
            self.geometry[deck_geometry]= [((float(deck.doc["Geometry"][deck_geometry]["Width (X)"]), float(deck.doc["Geometry"][deck_geometry]["Thickness (Y)"])))]
           

    def set_domains(self, deck):
        self.domains = []
        for deck_domain in deck.doc["Materials"]:
            if deck_domain == "Bottom Plate":
                corner0 = (0,0)
                corner1 = self.geometry[deck_domain][0]
                plate_material = deck.doc["Materials"][deck_domain]
                plate_initial_temperature=float(deck.doc["Initial Conditions"][deck_domain]["Initial Temperature"])
                self.domains.append(RectangularDomain(deck_domain, corner0, corner1, plate_material,plate_initial_temperature))
            elif deck_domain == "Heat Element":
                corner0=(0,self.geometry["Bottom Plate"][0][1])
                corner1 = (self.geometry[deck_domain][0][0],self.geometry["Bottom Plate"][0][1]+self.geometry[deck_domain][0][1])
                plate_material = deck.doc["Materials"][deck_domain]
                plate_initial_temperature=float(deck.doc["Initial Conditions"][deck_domain]["Initial Temperature"])
                self.domains.append(RectangularDomain(deck_domain, corner0, corner1, plate_material, plate_initial_temperature))
            elif deck_domain == "Top Plate":
                corner0 = (0,self.geometry["Bottom Plate"][0][1]+self.geometry["Heat Element"][0][1])
                corner1 = (self.geometry[deck_domain][0][0],self.geometry["Bottom Plate"][0][1]+self.geometry["Heat Element"][0][1]++self.geometry[deck_domain][0][1])
                plate_material = deck.doc["Materials"][deck_domain]
                plate_initial_temperature=float(deck.doc["Initial Conditions"][deck_domain]["Initial Temperature"])
                self.domains.append(RectangularDomain(deck_domain, corner0, corner1, plate_material,plate_initial_temperature))


    def set_boundaryconds(self, deck):
        self.boundaryconditions = []
        for deck_BC in deck.doc["Boundary Conditions"]:
            if deck_BC == "Top Plate Top":
                self.boundaryconditions.append( LinearBC( (0.,self.domains[2].y1), (self.domains[2].x1,self.domains[2].y1), deck.doc["Boundary Conditions"][deck_BC] ) )
            elif deck_BC == "Top Plate Left":
                self.boundaryconditions.append( LinearBC( (0.,self.domains[2].y0), (0.,self.domains[2].y1), deck.doc["Boundary Conditions"][deck_BC] ) )
            elif deck_BC == "Top Plate Right":
                self.boundaryconditions.append( LinearBC( (self.domains[2].x1,self.domains[2].y0), (self.domains[2].x1,self.domains[2].y1), deck.doc["Boundary Conditions"][deck_BC] ) )
            elif deck_BC == "Bottom Plate Bottom":
                self.boundaryconditions.append( LinearBC( (self.domains[0].x0,self.domains[0].y0), (self.domains[0].x1,0.), deck.doc["Boundary Conditions"][deck_BC] ) )
            elif deck_BC == "Bottom Plate Left":
                self.boundaryconditions.append( LinearBC( (0.,0.), (0.,self.domains[0].y1), deck.doc["Boundary Conditions"][deck_BC] ) )
            elif deck_BC == "Bottom Plate Right":
                self.boundaryconditions.append( LinearBC( (self.domains[0].x1,0.), (self.domains[0].x1,self.domains[0].y1), deck.doc["Boundary Conditions"][deck_BC] ) )

                
    # def set_initialconds(self,deck):
    #     self.initialconds=[]
    #     for deck_IC in deck.doc["Materials"]:
    #         if deck_IC == "Bottom Plate":
    #             self.initialconds.append(LinearBC(()))