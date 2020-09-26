import numpy as np
class RectangularDomain:

    def __init__(self, name, corner0, corner1, ex0, ex1, ey0, ey1, position,):
        self.corners={"X" : [float(corner0[0]), float(corner1[0])], "Y" : [float(corner0[1]),float(corner1[1])]}
        self.dimensions = {"Lx" : float(corner1[0]) - float(corner0[0]), "Ly" : float(corner1[1])-float(corner0[1])}
        self.elements = {"Elements in X":[ex0, ex1], "Elements in Y": [ey0,ey1]}
        self.name = name
        self.position = position

    def test_mesh(self, mesh):
        if mesh[0] >= self.elements["Elements in Y"][0] and mesh[0] <= self.elements["Elements in Y"][1] and mesh[1] >= self.elements["Elements in X"][0] and mesh[1]<= self.elements["Elements in X"][1]:
            return True
        else:
            return False

    def set_field_init_value(self, field_dict):
        for key, value in field_dict.items():
            self.initial_condition[key] = float(value)

    def generate_mask(self, totalNy, totalNx):
        m=np.zeros((totalNy, totalNx))
        maux=np.zeros((totalNy+2, totalNx+2))
        self.mask = m.copy()
        self.mask_external_boundary={}
        self.mask_contact_interface={}
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
                    self.mask[x_i][y_i] = 1
                    mask_left[x_i+1][0]=1
                    mask_right[x_i+1][-1]=1
                    self.mask_external_boundary.update({"Left Edge":mask_left})
                    self.mask_external_boundary.update({"Right Edge":mask_right})
                    
                    if self.position ==1:
                        mask_bottom[self.elements["Elements in Y"][0]][y_i+1]=1
                        contact_mask[self.elements["Elements in Y"][1]][y_i] = 1
                        self.mask_external_boundary.update({"Bottom Edge": mask_bottom})
                        self.mask_contact_interface.update({"Top Edge": contact_mask})
                    if self.position ==3:
                        mask_top[-1][y_i+1]=1
                        self.mask_external_boundary.update({"Top Edge": mask_top})
                        contact_mask[self.elements["Elements in Y"][0]][y_i] = 1
                        self.mask_contact_interface.update({"Bottom Edge": contact_mask})
                    if self.position ==2:
                        contact_mask_middle_bottom[self.elements["Elements in Y"][0]][y_i] = 1
                        contact_mask_middle_top[self.elements["Elements in Y"][1]][y_i] = 1
                        self.mask_contact_interface.update({"Bottom Edge": contact_mask_middle_bottom})
                        self.mask_contact_interface.update({"Top Edge": contact_mask_middle_top})
                        
    def set_bc(self,key,deck):
        bc={}
        for location in deck.doc["Domains"][key]["Boundary Condition"]:
            bc[location]={}
            for edge in deck.doc["Domains"][key]["Boundary Condition"][location]:
                bc[location][edge]={}
                for var in deck.doc["Domains"][key]["Boundary Condition"][location][edge]:
                    bc[location][edge].update({var: float(deck.doc["Domains"][key]["Boundary Condition"][location][edge][var])})
        self.boundary_conditions=bc
    
    def set_mesh(self,key,deck):
        mesh={}
        for mesh_dir in deck.doc["Domains"][key]["Mesh"]:
            mesh[mesh_dir] = int(deck.doc["Domains"][key]["Mesh"][mesh_dir])
        mesh["dx"] = self.dimensions["Lx"]/mesh["Number of Elements in X"]
        mesh["dy"] = self.dimensions["Ly"]/mesh["Number of Elements in Y"]
        self.mesh=mesh
        
    def set_material(self, key, deck):
        material={}
        for mat_dir in deck.doc["Domains"][key]["Material"]:
            if isinstance(deck.doc["Domains"][key]["Material"][mat_dir],dict) == False:
                material[mat_dir]=float(deck.doc["Domains"][key]["Material"][mat_dir])
            if isinstance(deck.doc["Domains"][key]["Material"][mat_dir],dict) == True:
                material[mat_dir]={}
                for param in deck.doc["Domains"][key]["Material"][mat_dir]:
                    material[mat_dir].update({param:float(deck.doc["Domains"][key]["Material"][mat_dir][param])})
        self.material = material
            
    def set_IC(self, key, deck):
        ic = {}
        for ic_dir in deck.doc["Domains"][key]["Initial Condition"]:
            if isinstance(deck.doc["Domains"][key]["Initial Condition"][ic_dir], dict) == False:
                ic[ic_dir] = float(deck.doc["Domains"][key]["Initial Condition"][ic_dir])
            if isinstance(deck.doc["Domains"][key]["Initial Condition"][ic_dir], dict) == True:
                 ic[ic_dir]={}
                 for param in deck.doc["Domains"][key]["Initial Condition"][ic_dir]:
                     ic[ic_dir].update({param: float(deck.doc["Domains"][key]["Initial Condition"][ic_dir][param])})
        self.initial_conditions=ic