from consolidate import *




cwd = os.getcwd()
# All the data from deck.yaml is now in the following deck variable
deck = Deck( cwd + "/deck.yaml" )

meshes = Meshes( deck )

model = HeatTransfer(deck)

plots=Plots(deck,meshes,meshes.T)

solves = Solves( deck,model,meshes,plots)

animates=Animates(deck)