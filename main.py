from consolidate import *




cwd = os.getcwd()
# All the data from deck.yaml is now in the following deck variable

deck = Deck( cwd + "/TwoPlates.yaml" )


meshes = MeshTwoPlates( deck )

model_HT= HeatTransfer(deck)

model_IC = IntimateContact(meshes,deck)

plots=PlotsTwoPlates(deck,meshes,meshes.T)

solves = SolvesTwoPlates( deck,model_HT,meshes,plots,model_IC)
