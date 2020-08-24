class CharacterizeDomain:

    def __init__(self, name, corner0, corner1, MaterialProperties, InitialConditions, Mesh, BC, Geometry):
        self.name = name
        self.MaterialProperties = MaterialProperties
        self.InitialConditions = InitialConditions
        self.Mesh = Mesh
        self.BoundaryConditions=BC
        self.Geometry = Geometry
        