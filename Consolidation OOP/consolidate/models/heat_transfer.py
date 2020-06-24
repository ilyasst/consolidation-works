

class HeatTransfer:

    def __init__(self, deck):
        self.dt = float(deck.doc["Simulation"]["Time Step"])
        self.dx2 = float(deck.doc["Simulation"]["dx"])*float(deck.doc["Simulation"]["dx"])
        self.dy2 = float(deck.doc["Simulation"]["dy"])*float(deck.doc["Simulation"]["dy"])

    def do_timestep(self, u0, u, Diffx, Diffy):
        # Propagate with forward-difference in time, central-difference in space
        u[1:-1, 1:-1] = u0[1:-1, 1:-1] + Diffy[1:-1, 1:-1]* self.dt * ((u0[2:, 1:-1] - 2*u0[1:-1, 1:-1] + u0[:-2, 1:-1])/self.dx2 )+ Diffx[1:-1, 1:-1]* self.dt * ( (u0[1:-1, 2:] - 2*u0[1:-1, 1:-1] + u0[1:-1, :-2])/self.dy2 )
        u0 = u.copy()
        
        return u0, u