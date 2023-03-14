from simulation import SIMULATION
import sys

directOrGUI = sys.argv[1]
solutionID = sys.argv[2]
robotPath = sys.argv[3]
simulation = SIMULATION(directOrGUI, solutionID, robotPath=robotPath)
simulation.Run()
simulation.Get_Fitness()