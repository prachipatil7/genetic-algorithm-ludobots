from solution import SOLUTION
import constants as c
import copy
import os
from matplotlib import pyplot as plt
import pandas as pd
import random

class PARALLEL_HILL_CLIMBER:
    def __init__(self, seedID, seedType):
        os.system("rm generation/brain*.nndf")
        os.system("rm generation/body*.urdf")
        os.system("rm data/fitness*.txt")
        self.seedID = seedID
        self.seedType = seedType
        self.nextAvailableID = 0
        self.parents = {}
        self.epochMetrics = {}
        self.bodySizeMetrics = {}
        for i in range(c.populationSize):
            self.parents[i] = SOLUTION(self.nextAvailableID, self.seedType)
            self.nextAvailableID += 1
            self.epochMetrics[i] = []
            self.bodySizeMetrics[i] = [0,0,0,0]
            #[initial size, initial fitness, final size, final fitness]

    def Evolve(self):
        input("Start Initial Simulation")
        self.Evaluate(self.parents, "GUI")
        for key in self.parents:
            self.bodySizeMetrics[key][0] = len(self.parents[key].linkDict)
            self.bodySizeMetrics[key][1] = self.parents[key].fitness
            self.Save_Body_Brain("First", self.parents[key].myID, key)
            self.Save_Body_Brain("Best", self.parents[key].myID, key)
        for currentGeneration in range(c.numberOfGenerations):
            # input("Evolve Next")
            os.system("rm generation/brain*.nndf")
            os.system("rm generation/body*.urdf")
            print(f"------GENERATION {currentGeneration+1}-------")
            self.Evolve_For_One_Generation()
        self.Save_Best()
        self.Plot_Epochs()

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        for key in self.parents:
            self.Evaluate(self.children[key], "DIRECT")
        self.Print()
        self.Select()

    def Spawn(self):
        self.children = {}
        for key, parent in self.parents.items():
            self.children[key] = {}
            for i in range(c.childrenPerParent):
                child = copy.deepcopy(parent)
                child.myID = self.nextAvailableID
                self.nextAvailableID += 1
                self.children[key][i] = child

    def Mutate(self):
        for key in self.parents:
            for childkey, child in self.children[key].items():
                mutationType = random.randint(1,3)
                if mutationType==1:
                    child.MutateWeights()
                elif mutationType==2:
                    child.MutateBody()
                elif mutationType==3:
                    child.AddLink()

    def Evaluate(self, solutions, mode):
        for key, solution in solutions.items():
            solution.Start_Simulation(mode)
        for key, solution in solutions.items():
            solution.Wait_For_Simulation_To_End()

    def Print(self):
        for key in self.parents:
            for childkey, child in self.children[key].items():
                print(f"{key}-{childkey}", self.parents[key].fitness, child.fitness, f"({child.mutation})")
            print()

    def Select(self):
        for key in self.parents:
            best_child = self.children[key][0]
            for childkey, curr_child in self.children[key].items():
                if best_child.fitness > curr_child.fitness:
                    best_child = curr_child
            if self.parents[key].fitness > best_child.fitness:
                self.parents[key] = best_child
                self.Save_Body_Brain("Best", self.parents[key].myID, key)
                input("Show Beneficial Mutation Simulation")
                os.system(f"python3 simulate.py GUI {100} save/{self.seedType}{0}_Best{0} 2&>1")
            self.epochMetrics[key].append(self.parents[key].fitness)
             
    def Save_Best(self):
        best_parent = self.parents[0]
        for key, curr_parent in self.parents.items():
            if curr_parent.fitness < best_parent.fitness:
                best_parent = curr_parent
            self.bodySizeMetrics[key][2] = len(curr_parent.linkDict)
            self.bodySizeMetrics[key][3] = curr_parent.fitness
            # curr_parent.Start_Simulation("GUI")
            

    def Plot_Epochs(self):
        return
        x = list(range(c.numberOfGenerations))
        for species in self.epochMetrics:
            y = [y*-1 for y in self.epochMetrics[species]]
            plt.plot(x,y)
        plt.savefig(f'save/{self.seedID}FitnessCurve.png')
        plt.cla()
        df = pd.DataFrame.from_dict(self.epochMetrics, orient="columns")
        df.to_csv(f"save/epochMetrics_{self.seedType}{self.seedID}.csv")

        df = pd.DataFrame.from_dict(self.bodySizeMetrics, orient="index", columns=["initial size", "initial fitness", "final size", "final fitness"])
        df.to_csv(f"save/bodySizeMetrics_{self.seedType}{self.seedID}.csv")


    def Save_Body_Brain(self, fileName, solutionID, speciesID):
        os.system(f"cp generation/body{solutionID}.urdf save/{self.seedType}{self.seedID}_{fileName}{speciesID}Body.urdf >2")
        os.system(f"cp generation/brain{solutionID}.nndf save/{self.seedType}{self.seedID}_{fileName}{speciesID}Brain.nndf >2")



