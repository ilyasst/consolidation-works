# The problem



Consider two adherents of length X and Y (defined by the user) with initial set of temperatures (defined by the user). In their common interface, in a centralized region, a different temperature is found (defined by the user). In case of heating, this central temperature is higher than the adherents' temperature and, in case pf cooling, lower.

This assigned temperature is part of the initial condition. The temperature field and history is, in a forward fashion, solved by central differences.

At the current version, the user needs to define the number of steps and the desired  step time(this will soon be updated in a way that the user just input the desired simulation time). At the end of the set number of steps, a temperature field is obtained.
Also, the user can generate temperature field plots spaced by N-steps intervals, which is also defined by the user.

All the parameters needed for running this code needs to be input in the .yaml found in the root folder.


```yaml
Problem Type:
    Type: TwoPlates
Materials:
  Material1:
    Thermal Diffusivity X: 10.
    Thermal Diffusivity Y: 10.
    Domain Initial Temperature: 10.
  Material2:
    Thermal Diffusivity X: 10.
    Thermal Diffusivity Y: 10.
    Domain Initial Temperature: 30.

Simulation:
  Time Step: 0.0002
  Number Time Steps: 10001
  lenX: 20
  lenY: 10
  dx: 0.1
  dy: 0.1

Plot:
  folder: "./output/"
  figure name: temperatue
  Color Interpolation: 50
  Color Map: "inferno"
  plot interval: 500
  
Animation:
    name: temperature
	
```


# Getting Started

### Mesh

A class named "Mesh Two Plates" is defined to create the mesh and assign Initial Temperature, Thermal Diffusivity in X and Thermal Diffusivity in Y in each element.
### Model
A class named "Heat Transfer" solves the heat transfer problem by central differences.
### Plot and Animation
A class named "PlotsTwoPlates" is defined to generate figures of the thermal history in spaced intervals. In the end, a .GIF is created from those figures.
### Solver
A class named "SolvesTwoPlates" is defined to create a forward step analysis, solving the heat transfer model and plotting the figures when convenient.