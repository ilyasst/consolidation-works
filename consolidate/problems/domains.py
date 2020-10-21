import numpy as np
class RectangularDomain:

    def __init__(self, name,x0,x1,y0,y1):
        self.name = name
        self.dimensions =  [[x0,x1],[y0,y1]]
        self.local_fields={}

    def test_mesh(self, mesh):
        if mesh[0] >= self.py[0] and mesh[0] <= self.py[1] and mesh[1] >= self.px[0] and mesh[1]<= self.px[1]:
            return True
        else:
            return False
        
    def test_mesh_bottom(self, mesh):
        if mesh[0] == self.elementsY[0] and mesh[1] >= self.elementsX[0] and mesh[1]<= self.elementsX[1]:
            return True
        else:
            return False
    def test_mesh_top(self, mesh):
        if mesh[0] == self.elementsY[1] and mesh[1] >= self.elementsX[0] and mesh[1]<= self.elementsX[1]:
            return True
        else:
            return False
    def test_mesh_left(self, mesh):
        if mesh[0] >= self.elementsY[0] and mesh[0] <= self.elementsY[1] and mesh[1] == self.elementsX[0]:
            return True
        else:
            return False
    def test_mesh_right(self, mesh):
        if mesh[0] >= self.elementsY[0] and mesh[0] <= self.elementsY[1] and mesh[1] == self.elementsX[1]:
            return True
        else:
            return False

    def generate_mask(self, totalpy, totalpx, dimen_y, total_thickness):
        m=np.zeros((totalpy, totalpx))
        # -----------------------------------------------
        # ENABLE THIS FOR ORDER 2 FINITE DIFFERENCE
        # maux=np.zeros((totalpy+4, totalpx+4))
        # mask = maux.copy()
        # self.mask = {}
        # self.mask_contact={}
        # mask_left= maux.copy()
        # mask_left_external= maux.copy()
        # mask_right= maux.copy()
        # mask_right_external= maux.copy()
        # mask_top= maux.copy()
        # mask_top_external = maux.copy()
        # mask_bottom = maux.copy()
        # mask_bottom_external = maux.copy()
        # contact_mask=maux.copy()
        # contact_mask_top = maux.copy()
        # contact_mask_bottom = maux.copy()
        # for x_i in range (0,np.shape(m)[0]):
        #     for y_i in range (0,np.shape(m)[1]):
        #         if self.test_mesh( (x_i, y_i) ):
                    # mask[x_i+2][y_i+2] = 1
                    # mask_left[x_i+2][2] = 1
                    # mask_left_external[x_i+2][0]=1
                    # mask_right[x_i+2][-3]=1
                    # mask_right_external[x_i+2][-1]=1
                    # mask_bottom[self.py[0]+2][y_i+2]=1
                    # mask_bottom_external[self.py[0]][y_i+2]=1
                    # contact_mask_top[self.py[1]+2][y_i+2] = 1
                    # mask_top[-3][y_i+2]=1
                    # mask_top_external[-1][y_i+2]=1
                    # contact_mask_bottom[self.py[0]+2][y_i] = 1
        # -------------------------------------------
        # -------------------------------------------
        # ENABLE THIS FOR ORDER 1 FINITE DIFFERENCE
        maux=np.zeros((totalpy+2, totalpx+2))
        mask = maux.copy()
        self.mask = {}
        self.mask_contact={}
        mask_left= maux.copy()
        mask_left_external= maux.copy()
        mask_right= maux.copy()
        mask_right_external= maux.copy()
        mask_top= maux.copy()
        mask_top_external = maux.copy()
        mask_bottom = maux.copy()
        mask_bottom_external = maux.copy()
        contact_mask=maux.copy()
        contact_mask_top = maux.copy()
        contact_mask_bottom = maux.copy()
        for x_i in range (0,np.shape(m)[0]):
            for y_i in range (0,np.shape(m)[1]):
                if self.test_mesh( (x_i, y_i) ):
                    mask[x_i+1][y_i+1] = 1
                    mask_left[x_i+1][1] = 1
                    mask_left_external[x_i+1][0]=1
                    mask_right[x_i+1][-2]=1
                    mask_right_external[x_i+1][-1]=1
                    mask_bottom[self.py[0]+1][y_i+1]=1
                    mask_bottom_external[self.py[0]][y_i+1]=1
                    contact_mask_top[self.py[1]+1][y_i+1] = 1
                    mask_top[-2][y_i+1]=1
                    mask_top_external[-1][y_i+1]=1
                    contact_mask_bottom[self.py[0]+1][y_i] = 1
                    self.mask["Inner"] = mask
                    self.mask["Left Edge External"] =  mask_left_external
                    self.mask["Left Edge"] = mask_left
                    self.mask["Right Edge External"] = mask_right_external
                    self.mask["Right Edge"] = mask_right
                    if dimen_y[0] == 0:
                        self.mask["Bottom Edge"] = mask_bottom
                        self.mask["Bottom Edge External"] = mask_bottom_external
                        self.mask["Top Edge"] = mask_top
                        self.mask["Top Edge External"] = mask_top_external
                        self.mask_contact["Top Edge"] = contact_mask_top
                    if dimen_y[1] == total_thickness:
                        self.mask["Bottom Edge"] = mask_bottom
                        self.mask_contact["Bottom Edge"] = contact_mask_bottom
                        self.mask["Top Edge"] = mask_top
                        self.mask["Top Edge External"] = mask_top_external
                    if dimen_y[0] != 0 and dimen_y[1] != total_thickness:
                        self.mask["Bottom Edge"] = mask_bottom
                        self.mask["Bottom Edge External"] = mask_bottom_external
                        self.mask["Top Edge"] = mask_top
                        self.mask["Top Edge External"] = mask_top_external
                        self.mask_contact["Bottom Edge"] = contact_mask_bottom
                        self.mask_contact["Top Edge"] = contact_mask_top
        # --------------------------------------------------------------------

    def set_field(self, field_name, value):
        self.local_fields.update({field_name: value})

    def set_points_domains(self, p_x0, p_x1, p_y0, p_y1):
        self.px = [p_x0, p_x1]
        self.py = [p_y0, p_y1]
    
    def set_material(self,material):
        self.material=material
    
    def set_bc(self, bc):
        self.boundary_condition = bc