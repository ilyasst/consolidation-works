import numpy as np

class Mesh:

    def __init__(self,  domain, totalNx=0, totalNy=0):
        self.set_mesh_grid(domain)
        self.name = domain.name
        if totalNx !=0 and totalNy !=0:
            self.set_create_mask(domain, totalNy, totalNx)

    def set_mesh_grid(self, domain):
        self.nx = domain.mesh[0].npx
        self.ny = domain.mesh[0].npy
        self.dx=domain.mesh[0].dx
        self.dy=domain.mesh[0].dy
        # import pdb; pdb.set_trace()
        X, Y = np.meshgrid(np.arange(0, domain.geometry[0].dimensionX, domain.mesh[0].npx), np.arange(0, domain.geometry[0].dimensionY, domain.mesh[0].npy))
        X=X[0,:].copy()
        Y=Y[:,0].copy()
        self.X = X
        self.Y = Y

