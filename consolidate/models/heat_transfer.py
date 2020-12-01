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

        
        
        uu[1:-1, 1:-1] = uuold[1:-1, 1:-1] + (self.dt/(self.rho[1:-1, 1:-1]*self.cp[1:-1, 1:-1]))*(((self.ky[2:, 1:-1]-self.ky[:-2, 1:-1])/(2*self.dy[:-1, 1:-1])) * ((uuold[2:, 1:-1] - uuold[:-2, 1:-1])/(2*self.dy[:-1, 1:-1])) + self.ky[1:-1, 1:-1] * (uuold[2:,1:-1] -2*uuold[1:-1, 1:-1]+ uuold[:-2, 1:-1])/(2*self.dy2[:-1, 1:-1]) + self.kx[1:-1, 1:-1] * (uuold[1:-1,2:] -2*uuold[1:-1, 1:-1] + uuold[1:-1, :-2])/(2*self.dx2[:-1, 1:-1]) )
        # uu[1:-1, 1:-1] = uuold[1:-1, 1:-1] + (self.dt)*(((self.diffy[2:, 1:-1]-self.diffy[:-2, 1:-1])/(2*self.dy[:-1, 1:-1])) * ((uuold[2:, 1:-1] - uuold[:-2, 1:-1])/(2*self.dy[:-1, 1:-1])) + self.diffy[1:-1, 1:-1] * (uuold[2:,1:-1] -2*uuold[1:-1, 1:-1]+ uuold[:-2, 1:-1])/(2*self.dy2[:-1, 1:-1]) + self.diffx[1:-1, 1:-1] * (uuold[1:-1,2:] -2*uuold[1:-1, 1:-1] + uuold[1:-1, :-2])/(2*self.dx2[:-1, 1:-1]) )

        # import pdb; pdb.set_trace()
        uu[2:-2, 2:-2] = uuold[2:-2, 2:-2] + (self.dt/(self.rho[2:-2, 2:-2]*self.cp[2:-2, 2:-2]))*(((-1/12*self.ky[4:, 2:-2] +2/3*self.ky[3:-1, 2:-2]- 2/3*self.ky[1:-3, 2:-2]+ 1/12*self.ky[:-4, 2:-2])/(self.dy[1:-2, 2:-2])) * ((-1/12*uuold[4:, 2:-2] +2/3*uuold[3:-1, 2:-2]- 2/3*uuold[1:-3, 2:-2]+ 1/12*uuold[:-4, 2:-2])/(self.dy[1:-2, 2:-2])) + self.ky[2:-2, 2:-2] * (-1/12*uuold[4:, 2:-2] +4/3*uuold[3:-1, 2:-2] -5/2*uuold[2:-2, 2:-2] + 4/3*uuold[1:-3, 2:-2] - 1/12*uuold[:-4, 2:-2])/(self.dy2[1:-2, 2:-2]) + self.kx[2:-2, 2:-2] * (-1/12*uuold[2:-2, 4:] +4/3*uuold[ 2:-2, 3:-1] -5/2*uuold[2:-2, 2:-2] + 4/3*uuold[ 2:-2, 1:-3] - 1/12*uuold[ 2:-2,:-4])/(self.dx2[1:-2, 2:-2]) )
        # uu[2:-2, 2:-2] = uuold[2:-2, 2:-2] + (self.dt)*(((-1/12*self.diffy[4:, 2:-2] +2/3*self.diffy[3:-1, 2:-2]- 2/3*self.diffy[1:-3, 2:-2]+ 1/12*self.diffy[:-4, 2:-2])/(self.dy[1:-2, 2:-2])) * ((-1/12*uuold[4:, 2:-2] +2/3*uuold[3:-1, 2:-2]- 2/3*uuold[1:-3, 2:-2]+ 1/12*uuold[:-4, 2:-2])/(self.dy[1:-2, 2:-2])) + self.diffy[2:-2, 2:-2] * (-1/12*uuold[4:, 2:-2] +4/3*uuold[3:-1, 2:-2] -5/2*uuold[2:-2, 2:-2] + 4/3*uuold[1:-3, 2:-2] - 1/12*uuold[:-4, 2:-2])/(self.dy2[1:-2, 2:-2]) + self.diffx[2:-2, 2:-2] * (-1/12*uuold[2:-2, 4:] +4/3*uuold[ 2:-2, 3:-1] -5/2*uuold[2:-2, 2:-2] + 4/3*uuold[ 2:-2, 1:-3] - 1/12*uuold[ 2:-2,:-4])/(self.dx2[1:-2, 2:-2]) )
        
        # import pdb; pdb.set_trace()
        uu[3:-3, 3:-3] = uuold[3:-3, 3:-3] + (self.dt/(self.rho[3:-3, 3:-3]*self.cp[3:-3, 3:-3]))*(((1/60*self.ky[6:, 3:-3] -3/20*self.ky[5:-1, 3:-3] +3/4*self.ky[4:-2, 3:-3] - 3/4*self.ky[2:-4, 3:-3] +3/20*self.ky[1:-5, 3:-3] - 1/60*self.ky[:-6,3:-3])/(self.dy[0:-5, 3:-3])) * ((1/60*uuold[6:, 3:-3] -3/20*uuold[5:-1, 3:-3] +3/4*uuold[4:-2, 3:-3] - 3/4*uuold[2:-4, 3:-3] +3/20*uuold[1:-5, 3:-3] - 1/60*uuold[:-6,3:-3])/(self.dy[0:-5, 3:-3])) + self.ky[3:-3, 3:-3] * (1/90*uuold[6:, 3:-3] -3/20*uuold[5:-1, 3:-3] +3/2*uuold[4:-2, 3:-3] -49/18*uuold[3:-3, 3:-3] +3/2*uuold[2:-4, 3:-3] - 3/20*uuold[1:-5,3:-3] +1/90*uuold[:-6,3:-3])/(self.dy2[0:-5, 3:-3]) + self.kx[3:-3, 3:-3] * (1/90*uuold[3:-3, 6: ] -3/20*uuold[3:-3, 5:-1] +3/2*uuold[3:-3, 4:-2] -49/18*uuold[3:-3, 3:-3] +3/2*uuold[3:-3, 2:-4] - 3/20*uuold[3:-3,1:-5] +1/90*uuold[3:-3,:-6])/(self.dx2[2:-3, 3:-3]) )
        # uu[3:-3, 3:-3] = uuold[3:-3, 3:-3] + (self.dt)*(((1/60*self.diffy[6:, 3:-3] -3/20*self.diffy[5:-1, 3:-3] +3/4*self.diffy[4:-2, 3:-3] - 3/4*self.diffy[2:-4, 3:-3] +3/20*self.diffy[1:-5, 3:-3] - 1/60*self.diffy[:-6,3:-3])/(self.dy[0:-5, 3:-3])) * ((1/60*uuold[6:, 3:-3] -3/20*uuold[5:-1, 3:-3] +3/4*uuold[4:-2, 3:-3] - 3/4*uuold[2:-4, 3:-3] +3/20*uuold[1:-5, 3:-3] - 1/60*uuold[:-6,3:-3])/(self.dy[0:-5, 3:-3])) + self.diffy[3:-3, 3:-3] * (1/90*uuold[6:, 3:-3] -3/20*uuold[5:-1, 3:-3] +3/2*uuold[4:-2, 3:-3] -49/18*uuold[3:-3, 3:-3] +3/2*uuold[2:-4, 3:-3] - 3/20*uuold[1:-5,3:-3] +1/90*uuold[:-6,3:-3])/(self.dy2[0:-5, 3:-3]) + self.diffx[3:-3, 3:-3] * (1/90*uuold[3:-3, 6: ] -3/20*uuold[3:-3, 5:-1] +3/2*uuold[3:-3, 4:-2] -49/18*uuold[3:-3, 3:-3] +3/2*uuold[3:-3, 2:-4] - 3/20*uuold[3:-3,1:-5] +1/90*uuold[3:-3,:-6])/(self.dx2[2:-3, 3:-3]) )


        return uu



    def do_timestep_cond_conv_tg1(self, uu,uuold, uuoldold):
        
    #     # ---------------------------------------------------------------------------------------------------------
    #     # -- ORDER 1 SOLVER --
    #     # import pdb; pdb.set_trace()
        
    #     # dU/dy = (uuold[2:,1:-1] - uuold[0:-2,1:-1]])/deltaY
        
    #     # kdU/dy = kUpred/DeltaY - KUafter/DeltaY
        
    #     # d(kdU/dy)/dy = dk/dy(dU/dy) + K*(d^u/dy^2)
        
        
    #     # d(dU/dy)/dy = d (u)
        
    #     # uu[0,1:-1] = uu[0,1:-1] - 2*self.dy[1,1:-1]*self.h[0,1:-1]*(uu[0,1:-1] - uu[1,1:-1])/self.ky[1,1:-1] 
    #     # uu[-1,1:-1] = uu[-1,1:-1] - 2*self.dy[1,1:-1]*self.h[-1,1:-1]*(uu[-1,1:-1] - uu[-2,1:-1])/self.ky[-2,1:-1]
    #     # uu[1:-1,0] = uu[1:-1,0] - 2*self.dx[:-1,1]*self.h[1:-1,0]*(uu[1:-1,0] - uu[1:-1,1])/self.kx[1:-1,1] 
    #     # uu[1:-1,-1] = uu[1:-1,-1] - 2*self.dx[:-1,-2]*self.h[1:-1,-1]*(uu[1:-1,-1] - uu[1:-1,-2])/self.kx[1:-1,-2]
        

        
    #     # uu[1:-1, 1:-1] = uuold[1:-1, 1:-1] + self.dt*(((self.ky[0:-2, 1:-1]/(self.rho[0:-2, 1:-1]*self.cp[0:-2, 1:-1]))*(0.5*uuold[0:-2, 1:-1]-uuold[1:-1, 1:-1]+0.5*uuold[2:, 1:-1])/self.dy2[:-1,1:-1]) + ((self.ky[2:, 1:-1]/(self.rho[2:, 1:-1]*self.cp[2:, 1:-1]))*(0.5*uuold[0:-2, 1:-1]-uuold[1:-1, 1:-1]+0.5*uuold[2:, 1:-1])/self.dy2[0:-1,1:-1]))
    #     # ORIGINAL WITHOUT INTERFACE
    #     # uu[1:-1, 1:-1] = uuold[1:-1, 1:-1] + (self.dt*self.ky[1:-1,1:-1]/(self.rho[1:-1, 1:-1]*self.cp[1:-1, 1:-1])) * ((uuold[0:-2, 1:-1] - 2*uuold[1:-1, 1:-1] + uuold[2:, 1:-1])/self.dy2[1:-1, 1:-1]) + (self.dt*self.kx[1:-1,1:-1]/(self.rho[1:-1, 1:-1]*self.cp[1:-1, 1:-1]))*((uuold[1:-1, 0:-2] - 2*uuold[1:-1, 1:-1] + uuold[1:-1, 2:])/self.dx2[1:-1, 1:-1]) + self.dt*self.Q[1:-1,1:-1]/(self.rho[1:-1, 1:-1] * self.cp[1:-1, 1:-1])
    #     # uu[1:-1, 1:-1] = uuold[1:-1, 1:-1] + (self.dt*self.ky[1:-1,1:-1]/(self.rho[1:-1, 1:-1]*self.cp[1:-1, 1:-1])) * ((uuold[0:-2, 1:-1] - 2*uuold[1:-1, 1:-1] + uuold[2:, 1:-1])/self.dy2[1:, 1:-1])  + (self.dt*self.kx[1:-1,1:-1]/(self.rho[1:-1, 1:-1]*self.cp[1:-1, 1:-1]))*((uuold[1:-1, 0:-2] - 2*uuold[1:-1, 1:-1] + uuold[1:-1, 2:])/self.dx2[:-1, 1:-1])

        
        
        uu[1:-1, 1:-1] = 4/3*uuold[1:-1, 1:-1] - 1/3*uuoldold[1:-1, 1:-1] + (2/3*self.dt/(self.rho[1:-1, 1:-1]*self.cp[1:-1, 1:-1]))*(((self.ky[2:, 1:-1]-self.ky[:-2, 1:-1])/(2*self.dy[:-1, 1:-1])) * ((uuold[2:, 1:-1] - uuold[:-2, 1:-1])/(2*self.dy[:-1, 1:-1])) + self.ky[1:-1, 1:-1] * (uuold[2:,1:-1] -2*uuold[1:-1, 1:-1]+ uuold[:-2, 1:-1])/(2*self.dy2[:-1, 1:-1]) + self.kx[1:-1, 1:-1] * (uuold[1:-1,2:] -2*uuold[1:-1, 1:-1] + uuold[1:-1, :-2])/(2*self.dx2[:-1, 1:-1]) )
        # uu[1:-1, 1:-1] = 4/3*uuold[1:-1, 1:-1] - 1/3*uuoldold[1:-1, 1:-1]+ (2/3*self.dt)*(((self.diffy[2:, 1:-1]-self.diffy[:-2, 1:-1])/(2*self.dy[:-1, 1:-1])) * ((uuold[2:, 1:-1] - uuold[:-2, 1:-1])/(2*self.dy[:-1, 1:-1])) + self.diffy[1:-1, 1:-1] * (uuold[2:,1:-1] -2*uuold[1:-1, 1:-1]+ uuold[:-2, 1:-1])/(2*self.dy2[:-1, 1:-1]) + self.diffx[1:-1, 1:-1] * (uuold[1:-1,2:] -2*uuold[1:-1, 1:-1] + uuold[1:-1, :-2])/(2*self.dx2[:-1, 1:-1]) )

        # import pdb; pdb.set_trace()
        uu[2:-2, 2:-2] = 4/3*uuold[2:-2, 2:-2] - 1/3*uuoldold[2:-2, 2:-2] + (2/3*self.dt/(self.rho[2:-2, 2:-2]*self.cp[2:-2, 2:-2]))*(((-1/12*self.ky[4:, 2:-2] +2/3*self.ky[3:-1, 2:-2]- 2/3*self.ky[1:-3, 2:-2]+ 1/12*self.ky[:-4, 2:-2])/(self.dy[1:-2, 2:-2])) * ((-1/12*uuold[4:, 2:-2] +2/3*uuold[3:-1, 2:-2]- 2/3*uuold[1:-3, 2:-2]+ 1/12*uuold[:-4, 2:-2])/(self.dy[1:-2, 2:-2])) + self.ky[2:-2, 2:-2] * (-1/12*uuold[4:, 2:-2] +4/3*uuold[3:-1, 2:-2] -5/2*uuold[2:-2, 2:-2] + 4/3*uuold[1:-3, 2:-2] - 1/12*uuold[:-4, 2:-2])/(self.dy2[1:-2, 2:-2]) + self.kx[2:-2, 2:-2] * (-1/12*uuold[2:-2, 4:] +4/3*uuold[ 2:-2, 3:-1] -5/2*uuold[2:-2, 2:-2] + 4/3*uuold[ 2:-2, 1:-3] - 1/12*uuold[ 2:-2,:-4])/(self.dx2[1:-2, 2:-2]) )
        # uu[2:-2, 2:-2] = 4/3*uuold[2:-2, 2:-2] - 1/3*uuoldold[2:-2, 2:-2]  + (2/3*self.dt)*(((-1/12*self.diffy[4:, 2:-2] +2/3*self.diffy[3:-1, 2:-2]- 2/3*self.diffy[1:-3, 2:-2]+ 1/12*self.diffy[:-4, 2:-2])/(self.dy[1:-2, 2:-2])) * ((-1/12*uuold[4:, 2:-2] +2/3*uuold[3:-1, 2:-2]- 2/3*uuold[1:-3, 2:-2]+ 1/12*uuold[:-4, 2:-2])/(self.dy[1:-2, 2:-2])) + self.diffy[2:-2, 2:-2] * (-1/12*uuold[4:, 2:-2] +4/3*uuold[3:-1, 2:-2] -5/2*uuold[2:-2, 2:-2] + 4/3*uuold[1:-3, 2:-2] - 1/12*uuold[:-4, 2:-2])/(self.dy2[1:-2, 2:-2]) + self.diffx[2:-2, 2:-2] * (-1/12*uuold[2:-2, 4:] +4/3*uuold[ 2:-2, 3:-1] -5/2*uuold[2:-2, 2:-2] + 4/3*uuold[ 2:-2, 1:-3] - 1/12*uuold[ 2:-2,:-4])/(self.dx2[1:-2, 2:-2]) )
        
        # import pdb; pdb.set_trace()
        uu[3:-3, 3:-3] = 4/3*uuold[3:-3, 3:-3] - 1/3*uuoldold[3:-3, 3:-3] + (2/3*self.dt/(self.rho[3:-3, 3:-3]*self.cp[3:-3, 3:-3]))*(((1/60*self.ky[6:, 3:-3] -3/20*self.ky[5:-1, 3:-3] +3/4*self.ky[4:-2, 3:-3] - 3/4*self.ky[2:-4, 3:-3] +3/20*self.ky[1:-5, 3:-3] - 1/60*self.ky[:-6,3:-3])/(self.dy[0:-5, 3:-3])) * ((1/60*uuold[6:, 3:-3] -3/20*uuold[5:-1, 3:-3] +3/4*uuold[4:-2, 3:-3] - 3/4*uuold[2:-4, 3:-3] +3/20*uuold[1:-5, 3:-3] - 1/60*uuold[:-6,3:-3])/(self.dy[0:-5, 3:-3])) + self.ky[3:-3, 3:-3] * (1/90*uuold[6:, 3:-3] -3/20*uuold[5:-1, 3:-3] +3/2*uuold[4:-2, 3:-3] -49/18*uuold[3:-3, 3:-3] +3/2*uuold[2:-4, 3:-3] - 3/20*uuold[1:-5,3:-3] +1/90*uuold[:-6,3:-3])/(self.dy2[0:-5, 3:-3]) + self.kx[3:-3, 3:-3] * (1/90*uuold[3:-3, 6: ] -3/20*uuold[3:-3, 5:-1] +3/2*uuold[3:-3, 4:-2] -49/18*uuold[3:-3, 3:-3] +3/2*uuold[3:-3, 2:-4] - 3/20*uuold[3:-3,1:-5] +1/90*uuold[3:-3,:-6])/(self.dx2[2:-3, 3:-3]) )
        # uu[3:-3, 3:-3] = 4/3*uuold[3:-3, 3:-3] - 1/3*uuoldold[3:-3, 3:-3] + (2/3*self.dt)*(((1/60*self.diffy[6:, 3:-3] -3/20*self.diffy[5:-1, 3:-3] +3/4*self.diffy[4:-2, 3:-3] - 3/4*self.diffy[2:-4, 3:-3] +3/20*self.diffy[1:-5, 3:-3] - 1/60*self.diffy[:-6,3:-3])/(self.dy[0:-5, 3:-3])) * ((1/60*uuold[6:, 3:-3] -3/20*uuold[5:-1, 3:-3] +3/4*uuold[4:-2, 3:-3] - 3/4*uuold[2:-4, 3:-3] +3/20*uuold[1:-5, 3:-3] - 1/60*uuold[:-6,3:-3])/(self.dy[0:-5, 3:-3])) + self.diffy[3:-3, 3:-3] * (1/90*uuold[6:, 3:-3] -3/20*uuold[5:-1, 3:-3] +3/2*uuold[4:-2, 3:-3] -49/18*uuold[3:-3, 3:-3] +3/2*uuold[2:-4, 3:-3] - 3/20*uuold[1:-5,3:-3] +1/90*uuold[:-6,3:-3])/(self.dy2[0:-5, 3:-3]) + self.diffx[3:-3, 3:-3] * (1/90*uuold[3:-3, 6: ] -3/20*uuold[3:-3, 5:-1] +3/2*uuold[3:-3, 4:-2] -49/18*uuold[3:-3, 3:-3] +3/2*uuold[3:-3, 2:-4] - 3/20*uuold[3:-3,1:-5] +1/90*uuold[3:-3,:-6])/(self.dx2[2:-3, 3:-3]) )
        

        return uu
    
    

