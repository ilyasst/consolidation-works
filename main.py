from consolidate import *



cwd = os.getcwd()
# All the data from deck.yaml is now in the following deck variable

deck = Deck( cwd + "/TwoPlates.yaml" )

geometry = Geometry(deck)

meshes = MeshTwoPlates( deck,geometry )

BC = BoundaryCondition(deck, geometry, meshes)

model_HT= HeatTransfer(deck,meshes, BC)

model_IC = IntimateContact(meshes,deck)

plots=PlotsTwoPlates(deck,meshes,BC)

solves = SolvesTwoPlates( deck, meshes, BC,model_HT,model_IC,plots)
