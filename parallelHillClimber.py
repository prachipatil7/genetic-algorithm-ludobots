from solution import SOLUTION
import constants as c
import copy
import os
from matplotlib import pyplot as plt
import pandas as pd
import random

class PARALLEL_HILL_CLIMBER:
    def __init__(self):
        os.system("rm generation/brain*.nndf")
        os.system("rm generation/body*.urdf")
        os.system("rm data/fitness*.txt")
        os.system("rm -R save/")
        os.system("mkdir save")
        self.nextAvailableID = 0
        self.parents = {}
        self.epochMetrics = {}
        for i in range(c.populationSize):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1
            self.epochMetrics[i] = []

    def Evolve(self):
        self.Evaluate(self.parents, "GUI")
        for key in self.parents:
            self.Save_Body_Brain("First", self.parents[key].myID, key)
        for currentGeneration in range(c.numberOfGenerations):
            os.system("rm generation/brain*.nndf")
            os.system("rm generation/body*.urdf")
            print(f"------GENERATION {currentGeneration+1}-------")
            self.Evolve_For_One_Generation()
        self.Show_Best()
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
            self.epochMetrics[key].append(self.parents[key].fitness)
            # self.Save_Body_Brain("Best", self.parents[key].myID, key)
            
    def Show_Best(self):
        best_parent = self.parents[0]
        for key, curr_parent in self.parents.items():
            if curr_parent.fitness < best_parent.fitness:
                best_parent = curr_parent
            curr_parent.Start_Simulation("GUI")
            curr_parent.Wait_For_Simulation_To_End()
        # best_parent.Start_Simulation("GUI")
        # self.Save_Body_Brain("Best", best_parent.myID, "Final")

    def Plot_Epochs(self):
        x = list(range(c.numberOfGenerations))
        for species in self.epochMetrics:
            y = [y*-1 for y in self.epochMetrics[species]]
            # print(len(x), x)
            # print(len(y), y)
            plt.plot(x,y)
        plt.savefig('save/FitnessCurve.png')

        # df = pd.read_csv("data/epochMetrics.csv")
        # new_col = self.epochMetrics[0]
        # if df.shape: col_index = df.shape[1] + 1
        # else: col_index = 0
        # df[col_index] = new_col
        # df.to_csv("data/epochMetrics.csv", index=False)


        


    def Save_Body_Brain(self, fileName, solutionID, speciesID):
        os.system(f"cp generation/body{solutionID}.urdf save/{fileName}{speciesID}Body.urdf >2")
        os.system(f"cp generation/brain{solutionID}.nndf save/{fileName}{speciesID}Brain.nndf >2")



