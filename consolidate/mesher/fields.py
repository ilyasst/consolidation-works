import numpy as np

class Field:
    
    def __init__(self,  domain):
        
        self.initialize_field(domain)

    def initialize_field(self,domain):
        nx = domain.Number_of_Elements_in_X
        ny = domain.Number_of_Elements_in_Y
        T = np.zeros((nx,ny))
        Rho = np.zeros((nx,ny))
        Cp = np.zeros((nx,ny))
        Kx = np.zeros((nx,ny))
        Ky = np.zeros((nx,ny))
        T[:] = domain.initial_temperature
        Rho [:] = float(domain.material["Density"])
        Cp[:] = float(domain.material["Specific Heat Capacity"])
        Kx[:] = float(domain.material["Thermal Conductivity X"])
        Ky[:] = float(domain.material["Thermal Conductivity Y"])
        
        DiffusivityX = float(domain.material["Thermal Conductivity X"])/(float(domain.material["Specific Heat Capacity"])+float(domain.material["Density"]))
        DiffusivityY = float(domain.material["Thermal Conductivity Y"])/(float(domain.material["Specific Heat Capacity"])+float(domain.material["Density"]))
        self.T=T.copy()
        self.Rho = Rho
        self.Cp = Cp
        self.Kx = Kx
        self.Ky = Ky
        self.DiffusivityX = self.Kx/(self.Rho*self.Cp)
        self.DiffusivityY = self.Kx/(self.Rho*self.Cp)
        
        