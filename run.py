import time
import os
import random
import constants as c
from parallelHillClimber import PARALLEL_HILL_CLIMBER

def run_all():
    for seedID in range(10):
        seedType = "snake" if seedID <= 4 else "random"
        for parentID in range(10):
            for evolutionStage in ["First", "Best"]:
                print(f"{seedType}{seedID}_{evolutionStage}{parentID}")
                os.system(f"python3 simulate.py GUI {parentID} results/{seedType}{seedID}_{evolutionStage}{parentID} 2&>1")
                time.sleep(5)
            time.sleep(10)
        time.sleep(10)

def run_random():
    seedID = random.randint(0,9)
    parentID = random.randint(0,9)
    seedType = "snake" if seedID <= 4 else "random"
    for evolutionStage in ["First", "Best"]:
        print(f"Running Simulation {seedType}{seedID}_{evolutionStage}{parentID}")
        os.system(f"python3 simulate.py GUI {parentID} results/{seedType}{seedID}_{evolutionStage}{parentID} 2&>1")

def run_specific(seedID, parentID):
    seedType = "snake" if seedID <= 4 else "random"
    for evolutionStage in ["First", "Best"]:
        print(f"Running Simulation {seedType}{seedID}_{evolutionStage}{parentID}")
        os.system(f"python3 simulate.py GUI {parentID} results/{seedType}{seedID}_{evolutionStage}{parentID} 2&>1")

def run_best():
    parents = [6, 7, 5, 5, 4, 2, 3, 1, 5, 2]
    for seedID in range(10):
        seedType = "snake" if seedID <= 4 else "random"
        parentID = parents[seedID]
        input("Hit enter to continue to the next simulation pair")
        for evolutionStage in ["First", "Best"]:
            print(f"Running Simulation {seedType}{seedID}_{evolutionStage}{parentID}")
            os.system(f"python3 simulate.py GUI {parentID} results/{seedType}{seedID}_{evolutionStage}{parentID} 2&>1")
        

def run_mini_evolution(seedType):
    c.populationSize = 2
    c.numberOfGenerations = 5
    c.numberOfSeeds = 1
    phc = PARALLEL_HILL_CLIMBER(0, seedType)
    phc.Evolve()
    c.populationSize = 10
    c.numberOfGenerations = 500
    c.numberOfSeeds = 10

def validate(num1, num2):
    return num1 in list(range(10)) and num2 in list(range(10))

print()
print("Welcome to the Simulator! Here are the options you can run:")
while True:
    print('''
    1. Run a random simulation (2 sims to watch)
    2. Run any simulation of your choice (2 sims to watch)
    3. Run the best simulation from each of the 10 seed rounds (20 sims to watch)
    4. Run a shortened version of the evolutionary algorithm (4 sims  to watch)
    5. Exit
    ''')
    choice = input("Please enter a command (1-5) that you would like to run: ")
    if choice == "1":
        print("Running Random Simulation...")
        run_random()
    elif choice == "2":
        valid = False
        while not valid:
            seed = (int(input("Enter the seed round you would like to see (0-9): ")))
            parent = (int(input("Enter the parent you would like to see (0-9): ")))
            valid = validate(seed, parent)
            if not valid:
                print("Please select a valid integer.")
            else:
                break
        print(f"Running Simulation {seed}-{parent}...")
        run_specific(seed, parent)
    elif choice == "3":
        print("Running Best Simulations...")
        run_best()
    elif choice == "4":
        os.system("rm -R save/")
        os.system("mkdir save")
        seedChoice = input("Would you like a snake starting morphology (S) or random starting morphology (R): ")
        seed = "snake" if seedChoice=="S" else "random"
        print("Starting Evolution...")
        run_mini_evolution(seed)
        for parentID in range(2):
            os.system(f"python3 simulate.py GUI {parentID} save/{seed}{0}_Best{parentID} 2&>1")
    elif choice == "5":
        print("Thanks for visiting!")
        exit()
    else:
        print("Please choose a valid option.")


#Cool Simulations
# snake0_First6
# random9_First3
