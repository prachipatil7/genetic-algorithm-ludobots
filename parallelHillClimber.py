from solution import SOLUTION
import constants as c
import copy
import os

class PARALLEL_HILL_CLIMBER:
    def __init__(self):
        os.system("rm generation/brain*.nndf")
        os.system("rm data/fitness*.nndf")
        self.nextAvailableID = 0
        self.parents = {}
        for i in range(c.populationSize):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1

    def Evolve(self):
        for key, parent in self.parents.items():
            parent.Start_Simulation("DIRECT")
        for key, parent in self.parents.items():
            parent.Wait_For_Simulation_To_End()
        for currentGeneration in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation()
        # self.Show_Best()

    def Evolve_For_One_Generation(self):
        self.Spawn()
        # self.Mutate()
        # self.child.Evaluate("DIRECT")
        # self.Print()
        # self.Select()

    def Spawn(self):
        self.children = {}
        for key, parent in self.parents:
            self.children[key] = copy.deepcopy(parent)
            self.children[key].myID = self.nextAvailableID
            self.nextAvailableID += 1

    def Mutate(self):
        self.child.Mutate()

    def Print(self):
        print(self.parent.fitness, self.child.fitness)

    def Select(self):
        if self.parent.fitness > self.child.fitness:
            self.parent = self.child

    def Show_Best(self):
        # self.parent.Evaluate("GUI")
        pass

