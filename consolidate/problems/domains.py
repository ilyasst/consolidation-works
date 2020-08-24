import numpy as np

class RectangularDomain:

    def __init__(self, name, corner0, corner1, MaterialProperties, InitialConditions, Mesh, BC, Geometry):
        self.x0 = float(corner0[0])
        self.y0 = float(corner0[1])
        self.x1 = float(corner1[0])
        self.y1 = float(corner1[1]) 
        self.name = name
        self.MaterialProperties = MaterialProperties
        self.InitialConditions = InitialConditions
        self.Mesh = Mesh
        self.BoundaryConditions=BC
        self.Geometry = Geometry
        
       

    def test(self, point):
        if point[0] >= self.x0 and point[0] <= self.x1 and point[1] >= self.y0 and point[1] <= self.y1:
            return True
        else:
            return False

 

    def set_field_init_value(self, field_dict):
        
        for key, value in field_dict.items():
            self.initial_fields[key] = float(value)
            
    
    def set_material_properties(self, mat):
        import pdb; pdb.set_trace()
        for key, value in mat:
            self.MaterialProperties[key] = float (value)