import numpy as np
class RectangularDomain:

    def __init__(self, name,x0,x1,y0,y1, nodes, temperature):
        self.name = name
        self.dimensions =  [[x0,x1],[y0,y1]]        
        self.nodes = nodes
        self.initial_temperature = temperature
        self.material = {}
        self.boundary_condition = {}
        self.power = {}
        self.local_fields={}

    def test_mesh_all(self, mesh):
        if mesh[0] >= self.nodes[1][0] and mesh[0] <= self.nodes[1][1] and mesh[1] >= self.nodes[0][0] and mesh[1]<= self.nodes[0][1]:
            return True
        else:
            return False
        
    def test_mesh_inner(self, mesh):
        if mesh[0] >= self.nodes[1][0] + 1 and mesh[0] <= self.nodes[1][1] - 1 and mesh[1] >= self.nodes[0][0] + 1 and mesh[1]<= self.nodes[0][1] - 1:
            return True
        else:
            return False
        
    def test_mesh_inc(self, mesh):
        if mesh[0]>=self.nodes[1][0] and mesh[0]<= self.nodes[1][1]-1 and mesh[1] >= self.nodes[0][0] and mesh[1]<= self.nodes[0][1]:
            return True
        else:
            return False
        
    def test_mesh_bottom(self, mesh):
        if mesh[0] == self.nodes[1][0] and mesh[1] >= self.nodes[0][0] + 1 and mesh[1]<= self.nodes[0][1] - 1:
            return True
        else:
            return False
        
    def test_mesh_bottom_out(self, mesh):
        if mesh[0] == self.nodes[1][0] and mesh[1] >= self.nodes[0][0] and mesh[1]<= self.nodes[0][1]:
            return True
        else:
            return False
        
    def test_mesh_top(self, mesh):
        if mesh[0] == self.nodes[1][1] and mesh[1] >= self.nodes[0][0] + 1 and mesh[1]<= self.nodes[0][1] - 1:
            return True
        else:
            return False
        
    def test_mesh_top_out(self, mesh):
        if mesh[0] == self.nodes[1][1] and mesh[1] >= self.nodes[0][0]  and mesh[1]<= self.nodes[0][1] :
            return True
        else:
            return False
        
    def test_mesh_left(self, mesh):
        if mesh[0] >= self.nodes[1][0] and mesh[0] <= self.nodes[1][1] and mesh[1] == self.nodes[0][0]:
            return True
        else:
            return False
        
    def test_mesh_left_out(self, mesh):
        if mesh[0] >= self.nodes[1][0] and mesh[0] <= self.nodes[1][1] and mesh[1] == self.nodes[0][0]:
            return True
        else:
            return False
        
    def test_mesh_right(self, mesh):
        if mesh[0] >= self.nodes[1][0] and mesh[0] <= self.nodes[1][1] and mesh[1] == self.nodes[0][1]:
            return True
        else:
            return False
    
    def test_mesh_right_out(self, mesh):
        if mesh[0] >= self.nodes[1][0] and mesh[0] <= self.nodes[1][1] and mesh[1] == self.nodes[0][1]:
            return True
        else:
            return False
    

    def generate_mask(self, i, totalpy, totalpx, total_thickness):
        # import pdb; pdb.set_trace()
        m=np.zeros((totalpy, totalpx))
        maux=np.zeros((totalpy-1, totalpx))
        maux2 = np.zeros((totalpy+2, totalpx+2))
        mask_inner = m.copy()
        mask_all = m.copy()
        mask_left= m.copy()
        mask_right= m.copy()
        mask_top= m.copy()
        mask_bottom = m.copy()
        contact_mask_top = m.copy()
        contact_mask_bottom = m.copy()
        mask_inc = maux.copy()
        mask_out_top = maux2.copy()
        mask_out_bottom = maux2.copy()
        mask_out_right = maux2.copy()
        mask_out_left = maux2.copy()
        self.mask = {}
        self.mask_interface={}
        self.mask_out={}
        for x_i in range (0,np.shape(m)[0]):
            for y_i in range (0,np.shape(m)[1]):
                if self.test_mesh_all( (x_i, y_i) ):
                    mask_all[x_i][y_i] = 1
                if self.test_mesh_inner( (x_i, y_i) ):
                    mask_inner[x_i][y_i] = 1
                if self.test_mesh_inc( (x_i, y_i) ):
                    mask_inc[x_i][y_i] = 1
                if self.test_mesh_bottom((x_i, y_i)):
                    mask_bottom[x_i][y_i] = 1
                    contact_mask_bottom[self.nodes[1][0]][y_i] = 1
                if self.test_mesh_top((x_i, y_i)):
                    mask_top[x_i][y_i] = 1
                    contact_mask_top[x_i][y_i] = 1
                if self.test_mesh_left((x_i, y_i)):
                    mask_left[x_i][y_i] = 1
                    mask_out_left[x_i+1][y_i] = 1
                if self.test_mesh_right((x_i, y_i)):
                    mask_right[x_i][y_i] = 1
                    mask_out_right[x_i+1][y_i+2]=1
                if self.test_mesh_bottom_out((x_i, y_i)):
                    mask_out_bottom[x_i][y_i+1] = 1
                if self.test_mesh_top_out((x_i, y_i)):
                    mask_out_top[x_i+i][y_i+1] = 1
                    
                    
                
        self.mask["All"] = mask_all.copy()
        self.mask["Bottom Edge"] = mask_bottom.copy()
        self.mask["Top Edge"] = mask_top.copy()
        self.mask["Increment"] = mask_inc.copy()
        self.mask["Inner"] = mask_inner.copy()
        
        
        if self.nodes[1][0] == 0:
            mask_left[self.nodes[1][1],0] = 0
            mask_right[self.nodes[1][1],-1] = 0
            self.mask["Left Edge"] = mask_left.copy()
            self.mask["Right Edge"] = mask_right.copy()
            self.mask_out["Bottom Edge"] = mask_out_bottom.copy()
            mask_out_left[self.nodes[1][1]+1,0] = 0
            mask_out_right[self.nodes[1][1]+i+1,-1] = 0
            self.mask_out["Right Edge"] = mask_out_right.copy()
            self.mask_out["Left Edge"] = mask_out_left.copy()
            contact_mask_top[self.nodes[1][1],0] = 1
            contact_mask_top[self.nodes[1][1],-1] = 1
            self.mask["AllMinusInterface"] = mask_all.copy()-contact_mask_top.copy()
            return
        
        if self.nodes[1][1] == totalpy-1:
            mask_left[self.nodes[1][0],0] = 0
            mask_right[self.nodes[1][0],-1] = 0
            self.mask["Left Edge"] = mask_left.copy()
            self.mask["Right Edge"] = mask_right.copy()
            self.mask_out["Top Edge"] = mask_out_top.copy()
            mask_out_left[self.nodes[1][0]+i-1,0] = 0
            mask_out_right[self.nodes[1][0]+i-1,-1] = 0
            self.mask_out["Right Edge"] = mask_out_right.copy()
            self.mask_out["Left Edge"] = mask_out_left.copy()
            contact_mask_bottom[self.nodes[1][0],0] = 1
            contact_mask_bottom[self.nodes[1][0],-1] = 1
            self.mask["AllMinusInterface"] = mask_all.copy()-contact_mask_bottom.copy()
            return
            
        if self.nodes[1][0] != 0 and self.nodes[1][1] != totalpy-1:
            self.mask_interface["Bottom Edge"] = mask_bottom
            self.mask_interface["Top Edge"] = mask_top
            self.mask["Left Edge"] = mask_left.copy()
            self.mask["Right Edge"] = mask_right.copy()
            self.mask_out["Right Edge"] = mask_out_right.copy()
            self.mask_out["Left Edge"] = mask_out_left.copy()
            contact_mask_top[self.nodes[1][1],-1] = 1
            contact_mask_top[self.nodes[1][1],0] = 1
            contact_mask_bottom[self.nodes[1][0],0] = 1
            contact_mask_bottom[self.nodes[1][0],-1] = 1
            self.mask["AllMinusInterface"] = mask_all.copy()-contact_mask_top.copy()-contact_mask_bottom.copy()
            


    def set_field(self, field_name, value):
        self.local_fields.update({field_name: value})

    def set_points_domains(self, p_x0, p_x1, p_y0, p_y1):
        self.px = [p_x0, p_x1]
        self.py = [p_y0, p_y1]
    
    def set_material(self,material):
        self.material.update(material)
    
    def set_bc(self, bc):
        self.boundary_condition.update(bc)
    
    def set_power(self, power):
        self.power.update(power)
