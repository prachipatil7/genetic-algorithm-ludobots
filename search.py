from parallelHillClimber import PARALLEL_HILL_CLIMBER
import constants as c
import os

# os.system("rm -R save/")
# os.system("mkdir save")

phc_lst = [PARALLEL_HILL_CLIMBER(i, "snake") for i in range(int(c.numberOfSeeds/2))]
phc_lst += [PARALLEL_HILL_CLIMBER(int(i+c.numberOfSeeds/2), "random") for i in range(int(c.numberOfSeeds/2))]
for phc in phc_lst:
    print(f"*********************{phc.seedID}**********************")
    phc.Evolve()