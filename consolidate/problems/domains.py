import numpy as np
class RectangularDomain:

    def __init__(self, name):
        self.name = name
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

    # @property
    # def is_top_plate(self):
    #     return int(self.name[-1]) == 1
    # @property
    # def is_bottom_plate(self):
    #     return int(self.name[-1]) == self.max_plates

    def generate_mask(self, totalpy, totalpx, dimen_y, total_thickness):
        m=np.zeros((totalpy, totalpx))
        maux=np.zeros((totalpy+2, totalpx+2))
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
                    if dimen_y[0] == 0:
                        mask_bottom[self.py[0]][y_i+1]=1
                        contact_mask[self.py[1]-1][y_i] = 1
                        self.mask_external_boundary.update({"Bottom Edge": mask_bottom})
                        self.mask_contact_interface.update({"Top Edge": contact_mask})
                    if dimen_y[1] == total_thickness:
                        mask_top[-1][y_i+1]=1
                        self.mask_external_boundary.update({"Top Edge": mask_top})
                        contact_mask[self.py[0]][y_i] = 1
                        self.mask_contact_interface.update({"Bottom Edge": contact_mask})
                    if dimen_y[0] != 0 and dimen_y[1] != total_thickness:
                        contact_mask_middle_bottom[self.py[0]][y_i] = 1
                        contact_mask_middle_top[self.py[1]-1][y_i] = 1
                        self.mask_contact_interface.update({"Bottom Edge": contact_mask_middle_bottom})
                        self.mask_contact_interface.update({"Top Edge": contact_mask_middle_top})

    def set_field(self, field_name, value):
        self.local_fields.update({field_name: value})

    def set_points_domains(self, p_x0, p_x1, p_y0, p_y1):
        self.px = [p_x0, p_x1]
        self.py = [p_y0, p_y1]
