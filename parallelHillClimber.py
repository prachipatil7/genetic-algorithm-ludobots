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

    def Evolve(self):
        self.Evaluate(self.parents, "GUI")
        for currentGeneration in range(c.numberOfGenerations):
            print(f"------GENERATION {currentGeneration+1}-------")
            self.Evolve_For_One_Generation()
        self.Show_Best()

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        for key in self.parents:
            self.Evaluate(self.parents[key].child_solutions, "DIRECT")
        self.Print()
        self.Select()

    def Spawn(self):
        for key, parent in self.parents.items():
            for i in range(c.childrenPerParent):
                child = copy.deepcopy(parent)
                child.myID = self.nextAvailableID
                self.nextAvailableID += 1
                self.parents[key].child_solutions[i] = child

    def Mutate(self):
        for key in self.parents:
            for childkey, child in self.parents[key].child_solutions.items():
                child.Mutate()

    def Evaluate(self, solutions, mode):
        for key, solution in solutions.items():
            solution.Start_Simulation(mode)
        for key, solution in solutions.items():
            solution.Wait_For_Simulation_To_End()

    def Print(self):
        for key in self.parents:
            for childkey, child in self.parents[key].child_solutions.items():
                print(key, self.parents[key].fitness, child.fitness)
        print()

    def Select(self):
        for key in self.parents:
            best_child = self.parents[key]
            for childkey, child in self.parents[key].child_solutions.items():
                if best_child.fitness > child.fitness:
                    best_child = child
        self.parents[key] = best_child
            

    def Show_Best(self):
        min_fitness = 0
        best_parent = self.parents[0]
        for key, parent in self.parents.items():
            if parent.fitness < min_fitness:
                min_fitness = parent.fitness
                best_parent = parent
        best_parent.Start_Simulation("GUI")

