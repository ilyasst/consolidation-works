class RectangularDomain:

    def __init__(self, name, corner0, corner1, material, initialcondition, mesh ):
        self.x0 = float(corner0[0])
        self.y0 = float(corner0[1])
        self.x1 = float(corner1[0])
        self.y1 = float(corner1[1])
        self.Lx = self.x1 - self.x0
        self.Ly = self.y1 - self.y0
        self.name = name
        self.material = material.copy()
        self.initial_condition = initialcondition.copy()
        self.mesh = mesh.copy()
        self.initial_fields = self.initial_condition.copy()

    def test(self, point):
        if point[0] > self.x0 and point[0] < self.x1 and point[1] > self.y0 and point[1] < self.y1:
            return True
        else:
            return False
        
    def set_field_init_value(self, field_dict):
        for key, value in field_dict.items():
            self.initial_fields[key] = float(value)
        
    def generate_mask(self, problem_M):
        self.mask = problem_M.copy()
        for x_i, x_ in enumerate(problem_M):
            for y_i, y_ in enumerate(problem_M):
                # import pdb; pdb.set_trace()
                if self.test( (x_i, y_i) ):
                    self.mask[x_i][y_i] = 1