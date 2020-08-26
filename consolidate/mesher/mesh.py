import numpy as np

class Mesh:

    def __init__(self,  domain):
        import pdb; pdb.set_trace
        self.set_mesh_grid(domain)
        self.name = domain.name

    def set_mesh_grid(self, domain):
        self.nx = domain.mesh["Number of Elements in X"]
        self.ny = domain.mesh["Number of Elements in Y"]
        self.dx=domain.Lx/self.nx
        self.dy=domain.Ly/self.ny
        X, Y = np.meshgrid(np.arange(domain.x0, domain.x1, self.dx), np.arange(domain.y0, domain.y1, + self.dy))
        X=X[0,:].copy()
        Y=Y[:,0].copy()
        self.X = X
        self.Y = Y