import numpy as np

class Mesh:

    def __init__(self, deck, domain):
        self.set_mesh_grid(deck, domain)
        self.name = domain.name

    def set_mesh_grid(self, deck, domain):
        self.nx = int(deck.doc["Mesh"][domain.name]["Number of Elements in X"])
        self.ny = int(deck.doc["Mesh"][domain.name]["Number of Elements in Y"])
        self.dx=domain.Lx/self.nx
        self.dy=domain.Ly/self.ny
        X, Y = np.meshgrid(np.arange(domain.x0, domain.x0 + self.nx), np.arange(domain.y0, domain.y0 + self.ny))
        X=X[1,:].copy()
        Y=Y[:,1].copy()
        self.X = X
        self.Y = Y
        self.ny1= int(self.ny/2)