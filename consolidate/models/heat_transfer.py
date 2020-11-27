import numpy as np

class HeatTransfer:

    def __init__(self, mesh, problem):
        fields ={}
        for aux in mesh.fields:
            fields[aux.name]= aux.value
        self.dt = float(problem.SimulationParameters["Step Time"])
        self.dx = fields["dx"]
        self.dy = fields["dy"]
        self.dx2 = fields["dx"] * fields["dx"]
        self.dy2 = fields["dy"] * fields["dy"]
        self.rho = fields["Density"]
        self.cp = fields["Cp"]
        self.kx = fields["kx"]
        self.ky = fields["ky"]
        self.Q = fields["Power Input Heat"]
        self.h = fields ["Convection Coefficient"]
        self.calc_diffusivity()
        

    def calc_diffusivity(self):
        aux = self.rho*self.cp 
        self.diffy=np.zeros(np.shape(aux))
        self.diffx=np.zeros(np.shape(aux))
        self.diffy[1:-1,1:-1] = self.ky[1:-1,1:-1]/ aux[1:-1,1:-1]
        self.diffx[1:-1,1:-1] = self.kx[1:-1,1:-1]/ aux[1:-1,1:-1]

    # def do_timestep(self, u):
    #     u[1:-1, 1:-1] = u[1:-1, 1:-1] + self.diffy[1:-1, 1:-1]* self.dt * ((u[2:, 1:-1] - 2*u[1:-1, 1:-1] + u[:-2, 1:-1])/self.dy2[1:-1, 1:-1] ) + self.diffx[1:-1, 1:-1]* self.dt * ( (u[1:-1, 2:] - 2*u[1:-1, 1:-1] + u[1:-1, :-2])/self.dx2[1:-1, 1:-1] ) + self.dt*self.Q[1:-1,1:-1]/(self.cp[1:-1,1:-1]*self.rho[1:-1,1:-1])
    #     return u

    def do_timestep_cond_conv(self, uu,uuold):
        
        # ---------------------------------------------------------------------------------------------------------
        # -- ORDER 1 SOLVER --
        # import pdb; pdb.set_trace()
        
        # dU/dy = (uuold[2:,1:-1] - uuold[0:-2,1:-1]])/deltaY
        
        # kdU/dy = kUpred/DeltaY - KUafter/DeltaY
        
        # d(kdU/dy)/dy = dk/dy(dU/dy) + K*(d^u/dy^2)
        
        
        # d(dU/dy)/dy = d (u)
        
        uu[0,1:-1] = uu[0,1:-1] - 2*self.dy[1,1:-1]*self.h[0,1:-1]*(uu[0,1:-1] - uu[1,1:-1])/self.ky[1,1:-1] 
        uu[-1,1:-1] = uu[-1,1:-1] - 2*self.dy[1,1:-1]*self.h[-1,1:-1]*(uu[-1,1:-1] - uu[-2,1:-1])/self.ky[-2,1:-1]
        uu[1:-1,0] = uu[1:-1,0] - 2*self.dx[:-1,1]*self.h[1:-1,0]*(uu[1:-1,0] - uu[1:-1,1])/self.kx[1:-1,1] 
        uu[1:-1,-1] = uu[1:-1,-1] - 2*self.dx[:-1,-2]*self.h[1:-1,-1]*(uu[1:-1,-1] - uu[1:-1,-2])/self.kx[1:-1,-2]
        

        
        # uu[1:-1, 1:-1] = uuold[1:-1, 1:-1] + self.dt*(((self.ky[0:-2, 1:-1]/(self.rho[0:-2, 1:-1]*self.cp[0:-2, 1:-1]))*(0.5*uuold[0:-2, 1:-1]-uuold[1:-1, 1:-1]+0.5*uuold[2:, 1:-1])/self.dy2[:-1,1:-1]) + ((self.ky[2:, 1:-1]/(self.rho[2:, 1:-1]*self.cp[2:, 1:-1]))*(0.5*uuold[0:-2, 1:-1]-uuold[1:-1, 1:-1]+0.5*uuold[2:, 1:-1])/self.dy2[0:-1,1:-1]))
        # ORIGINAL WITHOUT INTERFACE
        # uu[1:-1, 1:-1] = uuold[1:-1, 1:-1] + (self.dt*self.ky[1:-1,1:-1]/(self.rho[1:-1, 1:-1]*self.cp[1:-1, 1:-1])) * ((uuold[0:-2, 1:-1] - 2*uuold[1:-1, 1:-1] + uuold[2:, 1:-1])/self.dy2[1:-1, 1:-1]) + (self.dt*self.kx[1:-1,1:-1]/(self.rho[1:-1, 1:-1]*self.cp[1:-1, 1:-1]))*((uuold[1:-1, 0:-2] - 2*uuold[1:-1, 1:-1] + uuold[1:-1, 2:])/self.dx2[1:-1, 1:-1]) + self.dt*self.Q[1:-1,1:-1]/(self.rho[1:-1, 1:-1] * self.cp[1:-1, 1:-1])
        # uu[1:-1, 1:-1] = uuold[1:-1, 1:-1] + (self.dt*self.ky[1:-1,1:-1]/(self.rho[1:-1, 1:-1]*self.cp[1:-1, 1:-1])) * ((uuold[0:-2, 1:-1] - 2*uuold[1:-1, 1:-1] + uuold[2:, 1:-1])/self.dy2[1:, 1:-1])  + (self.dt*self.kx[1:-1,1:-1]/(self.rho[1:-1, 1:-1]*self.cp[1:-1, 1:-1]))*((uuold[1:-1, 0:-2] - 2*uuold[1:-1, 1:-1] + uuold[1:-1, 2:])/self.dx2[:-1, 1:-1])
        # import pdb; pdb.set_trace()
        # uu[1:-1, 1:-1] = uuold[1:-1, 1:-1] + self.dt * (((self.ky[0:-2,1:-1]/(self.rho[0:-2,1:-1]*self.cp[0:-2,1:-1]))*uuold[0:-2,1:-1])-2*((self.ky[1:-1,1:-1]/(self.rho[1:-1,1:-1]*self.cp[1:-1,1:-1]))*uuold[1:-1,1:-1])+((self.ky[2:,1:-1]/(self.rho[2:,1:-1]*self.cp[2:,1:-1]))*uuold[2:,1:-1]))/(self.dy2[0:-1,1:-1])

        uu[1:-1, 1:-1] = uuold[1:-1, 1:-1] + (self.dt/(self.rho[1:-1, 1:-1]*self.cp[1:-1, 1:-1]*self.dy[:-1, 1:-1]))*(((self.ky[2:, 1:-1] - self.ky[:-2, 1:-1])/2)*((uuold[2:,1:-1]-uuold[:-2,1:-1])/2) + self.ky[1:-1, 1:-1]*(uuold[0:-2, 1:-1] - 2*uuold[1:-1, 1:-1] + uuold[2:, 1:-1])) + (self.dt*self.kx[1:-1,1:-1]/(self.rho[1:-1, 1:-1]*self.cp[1:-1, 1:-1]))*((uuold[1:-1, 0:-2] - 2*uuold[1:-1, 1:-1] + uuold[1:-1, 2:])/self.dx2[0:-1, 1:-1])
        
        # + (self.dt*self.kx[1:-1,1:-1]/(self.rho[1:-1, 1:-1]*self.cp[1:-1, 1:-1]))*((uuold[1:-1, 0:-2] - 2*uuold[1:-1, 1:-1] + uuold[1:-1, 2:])/self.dx2[0:-1, 1:-1])
        
        # uu[1:-1, 1:-1] = uuold[1:-1, 1:-1] + (self.dt/(self.dy2[1:,1:-1]))*((self.ky[0:-2,1:-1]*uuold[0:-2,1:-1]/(self.rho[0:-2,1:-1]*self.cp[0:-2,1:-1]))- 2*(self.ky[1:-1,1:-1]*uuold[1:-1,1:-1]/(self.rho[1:-1,1:-1]*self.cp[1:-1,1:-1]))+(self.ky[2:,1:-1]*uuold[2:,1:-1]/(self.rho[2:,1:-1]*self.cp[2:,1:-1])))
        

        # Border correction
        # uu[0,1:-1] = uu[1,1:-1] + (self.dt*self.ky[1,1:-1]/(self.rho[1, 1:-1]*self.cp[1, 1:-1]))*((uuold[0,1:-1] - 2*uuold[1,1:-1] +uuold[2,1:-1])/self.dy2[1, 1:-1]) + (self.dt*self.kx[1, 1:-1]/(self.rho[1, 1:-1]*self.cp[1, 1:-1]))*((uuold[0, 1:-1] - 2*uuold[1, 1:-1] + uuold[2, 1:-1])/self.dx2[1, 1:-1]) 
        # uu[-1,1:-1] = uu[-1,1:-1] + (self.dt*self.ky[-2,1:-1]/(self.rho[-2, 1:-1]*self.cp[-2, 1:-1]))*((uuold[-1,1:-1] - 2*uuold[-2,1:-1] +uuold[-3,1:-1])/self.dy2[-2, 1:-1]) + (self.dt*self.kx[-2,1:-1]/(self.rho[-2,1:-1]*self.cp[-2,1:-1]))*((uuold[-1, 1:-1] - 2*uuold[-2, 1:-1] + uuold[-3, 1:-1])/self.dx2[-2,1:-1]) 
        # uu[1:-1,0] = uu[1:-1,0] + (self.dt*self.ky[1:-1,1]/(self.rho[1:-1,1]*self.cp[1:-1,1]))*((uuold[1:-1,0] - 2*uuold[1:-1,1] +uuold[1:-1,2])/self.dy2[1:-1,1]) + (self.dt*self.kx[1:-1,1]/(self.rho[1:-1,1]*self.cp[1:-1,1]))*((uuold[1:-1,0] - 2*uuold[1:-1,1] + uuold[1:-1, 2])/self.dx2[1:-1,1]) 
        # uu[1:-1,-1] = uu[1:-1,-1] + (self.dt*self.ky[1:-1,-2]/(self.rho[1:-1,-2]*self.cp[1:-1,-2]))*((uuold[1:-1,-1] - 2*uuold[1:-1,-2] +uuold[1:-1,-3])/self.dy2[1:-1,-2]) + (self.dt*self.kx[1:-1,-2]/(self.rho[1:-1,-2]*self.cp[1:-1,-2]))*((uuold[1:-1,-1] - 2*uuold[1:-1,-2] + uuold[1:-1,-3])/self.dx2[1:-1,-2]) 
        # ---------------------------------------------------------------------------------------------------------

        # ---------------------------------------------------------------------------------------------------------
        # -- ORDER 2 SOLVER --
        # uu[2:-2, 2:-2] = uuold[2:-2, 2:-2] + (self.dt*self.ky[2:-2,2:-2]/(self.rho[2:-2,2:-2]*self.cp[2:-2,2:-2])) * ((-(1/12)*uuold[0:-4,2:-2] + (4/3)*uuold[1:-3,2:-2] - (5/2)*uuold[2:-2,2:-2] + (4/3)*uuold[3:-1,2:-2] - (1/12)*uuold[4:,2:-2] )/self.dy2[2:-2,2:-2]) + (self.dt*self.kx[2:-2,2:-2]/(self.rho[2:-2,2:-2]*self.cp[2:-2,2:-2]))*((-(1/12)*uuold[2:-2,0:-4] +(4/3)*uuold[2:-2,1:-3] - (5/2)*uuold[2:-2, 2:-2] + (4/3)*uuold[2:-2,3:-1] - (1/12)*uuold[2:-2,4:])/self.dx2[2:-2,2:-2]) + self.dt*self.Q[2:-2,2:-2]/(self.rho[2:-2,2:-2] * self.cp[2:-2,2:-2])
        # ---------------------------------------------------------------------------------------------------------

        return uu


