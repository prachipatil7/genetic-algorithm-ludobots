from solution import SOLUTION
import constants as c
import copy
import os

class PARALLEL_HILL_CLIMBER:
    def __init__(self):
        os.system("rm generation/brain*.nndf")
        os.system("rm data/fitness*.txt")
        self.nextAvailableID = 0
        self.parents = {}
        for i in range(c.populationSize):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1
        self.best_parent = self.parents[0]

    def Evolve(self):
        self.Evaluate(self.parents, "DIRECT")
        for currentGeneration in range(c.numberOfGenerations):
            print("GENERATION ", currentGeneration+1)
            self.Evolve_For_One_Generation()
        self.Show_Best()

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children, "DIRECT")
        self.Print()
        self.Select()

    def Spawn(self):
        self.children = {}
        for key, parent in self.parents.items():
            self.children[key] = copy.deepcopy(parent)
            self.children[key].myID = self.nextAvailableID
            self.nextAvailableID += 1

    def Mutate(self):
        for key, child in self.children.items():
            child.Mutate()

    def Evaluate(self, solutions, mode):
        for key, solution in solutions.items():
            solution.Start_Simulation(mode)
        for key, solution in solutions.items():
            solution.Wait_For_Simulation_To_End()

    def Print(self):
        for key in self.parents:
            print(key, self.parents[key].fitness, self.children[key].fitness)
        print()
        print("Best Fitness: ", self.best_parent.fitness)
        print("Best Weights: ", self.best_parent.weights)
        print()

    def Select(self):
        for key in self.parents:
            if self.parents[key].fitness < self.children[key].fitness:
                self.parents[key] = self.children[key]
            if self.parents[key].fitness > self.best_parent.fitness:
                self.best_parent = self.parents[key]

    def Show_Best(self):
        self.best_parent.Start_Simulation("GUI")
        print("Best Fitness: ", self.best_parent.fitness)
        print("Best Weights: ", self.best_parent.weights)

