from consolidate import *




cwd = os.getcwd()
# All the data from deck.yaml is now in the following deck variable

deck = Deck( cwd + "/TwoPlates.yaml" )


meshes = MeshTwoPlates( deck )

model = HeatTransfer(deck)

plots=PlotsTwoPlates(deck,meshes,meshes.T)

solves = SolvesTwoPlates( deck,model,meshes,plots)
