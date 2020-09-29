import numpy as np
from .objects_creation import Mesh
from .objects_creation import Initial_Condition
from .objects_creation import BC
from .objects_creation import Material
from .objects_creation import Points
from .objects_creation import Geometry
from .objects_creation import Mask
from .objects_creation import Field

class RectangularDomain:

    def __init__(self, name, position):
        self.name = name
        self.position = position
        self.local_fields=[]

    def test_mesh(self, mesh):
        if mesh[0] >= self.points[0].pointsY[0] and mesh[0] <= self.points[0].pointsY[1] and mesh[1] >= self.points[0].pointsX[0] and mesh[1]<= self.points[0].pointsX[1]:
            return True
        else:
            return False


    def generate_mask(self, totalNy, totalNx):
        m=np.zeros((totalNy, totalNx))
        maux=np.zeros((totalNy+2, totalNx+2))
        self.masks=[]
        mask = m.copy()
        mask_external_boundary={}
        mask_contact_interface={}
        mask_left= maux.copy()
        mask_right= maux.copy()
        mask_top= maux.copy()
        mask_bottom= maux.copy()
        contact_mask=m.copy()
        contact_mask_middle_top = m.copy()
        contact_mask_middle_bottom = m.copy()
        for x_i in range (0,np.shape(m)[0]):
            for y_i in range (0,np.shape(m)[1]):
                if self.test_mesh( (x_i, y_i) ):
                    mask[x_i][y_i] = 1
                
                    mask_left[x_i+1][0]=1
                    mask_right[x_i+1][-1]=1
                    mask_external_boundary.update({"Left Edge":mask_left})
                    mask_external_boundary.update({"Right Edge":mask_right})
                    
                    if self.position ==1:
                        mask_bottom[self.points[0].pointsY[0]][y_i+1]=1
                        contact_mask[self.points[0].pointsY[1]][y_i] = 1
                        mask_external_boundary.update({"Bottom Edge": mask_bottom})
                        mask_contact_interface.update({"Top Edge": contact_mask})
                    if self.position ==3:
                        mask_top[-1][y_i+1]=1
                        mask_external_boundary.update({"Top Edge": mask_top})
                        contact_mask[self.points[0].pointsY[0]][y_i] = 1
                        mask_contact_interface.update({"Bottom Edge": contact_mask})
                    if self.position ==2:
                        contact_mask_middle_bottom[self.points[0].pointsY[0]][y_i] = 1
                        contact_mask_middle_top[self.points[0].pointsY[1]][y_i] = 1
                        mask_contact_interface.update({"Bottom Edge": contact_mask_middle_bottom})
                        mask_contact_interface.update({"Top Edge": contact_mask_middle_top})
        self.masks.append(Mask("Internal Mask", mask))
        self.masks.append(Mask("External BC", mask_external_boundary))
        self.masks.append(Mask("Contact", mask_contact_interface))


    def set_points(self, key,deck, totalPointsY):
        self.points=[]
        position = int(deck.doc["Domains"][key]["Geometry"]["Pos"])
        self.points.append(Points(deck, key, position, totalPointsY))
        
        
    def set_dimensions(self, key, deck):
        self.geometry=[]
        position = int(deck.doc["Domains"][key]["Geometry"]["Pos"])
        self.geometry.append(Geometry(deck, key, position))
        

    def set_mesh(self,key,deck,geometry):
        self.mesh=[]
        self.mesh.append(Mesh(deck.doc["Domains"][key]["Mesh"], geometry))


    def set_material(self, key, deck):
        self.material=[]
        self.material.append(Material(deck.doc["Domains"][key]["Material"]))


    def set_IC(self, key, deck):
        self.initial_condition=[]
        self.initial_condition.append(Initial_Condition(deck.doc["Domains"][key]["Initial Condition"]))


    def set_bc(self,key,deck):
        self.boundary_conditions=[]
        for location in deck.doc["Domains"][key]["Boundary Condition"]:
            self.boundary_conditions.append(BC(deck.doc["Domains"][key]["Boundary Condition"][location], location))
        
    # def set_fields(self, domain,field_name):
        
    #     if field_name == "Internal Temperature":
    #         if "temperature" in domain.initial_condition[0].__dict__.keys():
    #             name="temperature"
    #         for mask in self.masks:
    #             if mask.name=="Internal Mask":
    #                 value = mask.value*domain.initial_condition[0].__dict__[name]        
    #                 self.local_fields.append(Field(field_name,value))
    def set_fields(self, domain,field_name):
        value=0
        for mask in self.masks:
            if mask.name == "Internal Mask":
                if field_name == "Internal Temperature":
                    if "temperature" in domain.initial_condition[0].__dict__.keys():
                        name="temperature"
                        value = mask.value*domain.initial_condition[0].__dict__[name]  
                elif field_name == "Power Input Heat":
                    if "power_density" in domain.initial_condition[0].__dict__.keys():
                        name = "power_density"
                        value=mask.value*domain.initial_condition[0].__dict__[name] 
                else:
                    continue
                self.local_fields.append(Field(field_name,value))
