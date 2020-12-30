import numpy as np
class RectangularDomain:

    def __init__(self, name,x0,x1,y0,y1, nodes, power):
        self.name = name
        self.dimensions =  [[x0,x1],[y0,y1]]
        self.nodes = nodes
        self.material = {}
        self.initial_condition = {}
        self.boundary_condition = {}
        self.power = power
        self.local_fields={}
        
        
    def test_grid_all(self, mesh):
        if mesh[0] >= self.nodes[1][0] and mesh[0] <= self.nodes[1][1] and mesh[1] >= self.nodes[0][0] and mesh[1]<= self.nodes[0][1]:
            return True
        else:
             return False
        
    def test_grid_inner(self, mesh):
        if mesh[0] >= self.nodes[1][0] + 1 and mesh[0] <= self.nodes[1][1] - 1 and mesh[1] >= self.nodes[0][0]+1 and mesh[1]<= self.nodes[0][1] - 1:
            return True
        else:
            return False
    
    def test_grid_bottom(self, mesh):
        if mesh[0] == self.nodes[1][0] and mesh[1] >= self.nodes[0][0]+1  and mesh[1]<= self.nodes[0][1]-1:
            return True
        else:
            return False
        
    def test_grid_top(self, mesh):
        if mesh[0] == self.nodes[1][1] and mesh[1] >= self.nodes[0][0] +1 and mesh[1]<= self.nodes[0][1]-1:
            return True
        else:
            return False
        
    def test_grid_left(self, mesh):
        if mesh[0] >= self.nodes[1][0] and mesh[0] <= self.nodes[1][1] and mesh[1] == self.nodes[0][0]:
            return True
        else:
            return False
        
    def test_grid_right(self, mesh):
        if mesh[0] >= self.nodes[1][0] and mesh[0] <= self.nodes[1][1]  and mesh[1] == self.nodes[0][1]:
            return True
        else:
            return False
        
    def test_grid_inter_nodes(self, mesh):
        if mesh[0] >= self.nodes[1][0] and mesh[0] <= self.nodes[1][1]-1 and mesh[1] >= self.nodes[0][0] and mesh[1]<= self.nodes[0][1]-1:
            return True
        else:
             return False


    def generate_mask(self, i, totalpy, totalpx, total_thickness):

        self.mask_out = {}
        self.mask_nodes= {}
        self.mask_inter_nodes ={}
        self.mask_interface = {}

        m=np.zeros((totalpy, totalpx))
        minternodes=np.zeros((totalpy-1, totalpx-1))
        maux = np.zeros((totalpy+2, totalpx+2))

        mask_nodes_all = m.copy()
        mask_nodes_inner=m.copy()
        mask_nodes_bottom = m.copy()
        mask_nodes_top = m.copy()
        mask_nodes_left = m.copy()
        mask_nodes_right = m.copy()


        for x_i in range (0,np.shape(m)[0]):
            for y_i in range (0,np.shape(m)[1]):
                if self.test_grid_all( (x_i, y_i) ):
                    mask_nodes_all[x_i][y_i] = 1
                if self.test_grid_inner( (x_i, y_i) ):
                    mask_nodes_inner[x_i][y_i] = 1
                if self.test_grid_bottom ( (x_i, y_i) ):
                    mask_nodes_bottom[x_i][y_i] = 1
                if self.test_grid_top ( (x_i, y_i) ):
                    mask_nodes_top[x_i][y_i] = 1
                if self.test_grid_left ( (x_i, y_i) ):
                    mask_nodes_left[x_i][y_i] = 1
                if self.test_grid_right ( (x_i, y_i) ):
                    mask_nodes_right[x_i][y_i] = 1





        self.mask_nodes["All"] = mask_nodes_all.copy()
        self.mask_nodes["Inner"] = mask_nodes_inner.copy()
        self.mask_nodes["Bottom Edge"] = mask_nodes_bottom.copy()
        self.mask_nodes["Top Edge"] = mask_nodes_top.copy()


        mask_out_top = maux.copy()
        mask_out_bottom = maux.copy()
        mask_out_left = maux.copy()
        mask_out_right = maux.copy()
        
        for x_i in range (0,np.shape(maux)[0]):
            for y_i in range (0,np.shape(maux)[1]):
                if self.test_grid_left ( (x_i, y_i) ):
                    mask_out_left[x_i+1][y_i] = 1
                if self.test_grid_right ( (x_i, y_i) ):
                    mask_out_right[x_i+1][y_i+2] = 1
                if self.test_grid_bottom((x_i, y_i)):
                    mask_out_bottom[x_i][y_i+1] = 1
                if self.test_grid_top((x_i, y_i)):
                    mask_out_top[x_i+i][y_i+1] = 1
                    
        for x_i in range (0,np.shape(minternodes)[0]):
            for y_i in range (0,np.shape(minternodes)[1]):
                if self.test_grid_inter_nodes( (x_i, y_i)):
                    minternodes[x_i][y_i] = 1
        self.mask_inter_nodes = minternodes
                    
        if self.nodes[1][0] == 0:
            mask_nodes_left[self.nodes[1][1],0] = 0
            self.mask_nodes["Left Edge"]= mask_nodes_left.copy()
            mask_nodes_right[self.nodes[1][1],-1] = 0
            self.mask_nodes["Right Edge"]= mask_nodes_right.copy()
            
            
            
            
            self.mask_out["Bottom Edge"] = mask_out_bottom.copy()
            # mask_out_left[self.nodes[1][1]+1,0] = 0
            # mask_out_right[self.nodes[1][1]+i+1,-1] = 0
            self.mask_out["Right Edge"] = mask_out_right.copy()
            self.mask_out["Left Edge"] = mask_out_left.copy()
            self.mask_interface["Top Edge"] = mask_nodes_top.copy()
            return

        if self.nodes[1][1] == totalpy-1:
            mask_nodes_left[self.nodes[1][0],0] = 0
            self.mask_nodes["Left Edge"] = mask_nodes_left.copy()
            mask_nodes_right[self.nodes[1][0],-1] = 0
            self.mask_nodes["Right Edge"] = mask_nodes_right.copy()
            
            
            self.mask_out["Top Edge"] = mask_out_top.copy()
            mask_out_left[self.nodes[1][0]+i-1,0] = 0
            mask_out_right[self.nodes[1][0]+i-1,-1] = 0
            self.mask_out["Right Edge"] = mask_out_right.copy()
            self.mask_out["Left Edge"] = mask_out_left.copy()
            self.mask_interface["Bottom Edge"] = mask_nodes_bottom.copy()
            return

        if self.nodes[1][0] != 0 and self.nodes[1][1] != totalpy-1:
            
            self.mask_nodes["Left Edge"] = mask_nodes_left.copy()
            self.mask_nodes["Right Edge"] = mask_nodes_right.copy()
        
            self.mask_out["Right Edge"] = mask_out_right.copy()
            self.mask_out["Left Edge"] = mask_out_left.copy()
            self.mask_interface["Top Edge"] = mask_nodes_top.copy()
            self.mask_interface["Bottom Edge"] = mask_nodes_bottom.copy()
            return


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

    def set_initial_cond(self, init_cond):
        self.initial_condition.update(init_cond)
