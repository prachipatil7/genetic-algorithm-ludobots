# CS_396: Artificial Life - Assignment 8 (Evolving Morphologies)
cs366: artificial life -- r/ludobots project

In this version of the project, I am creating, and then evolving robots with random branching morphologies. 

## Generating Random Bodies
The algorithm for generating these robots is as follows:
1. Randomly select the length of the main torso "snake"
2. Start building this snake. Each link has random dimensions. 
3. For every link that is sent, a coin is flipped to decide if a new branch will extend from that link. A coin is also flipped for every link to decide if it is contains a sensor neuron or not.
4. If creating a new branch, randomly decide the length of that branch and the direction in which it will extend. The new branch must extend along a different axis than the branch that is currently being built. 
5. Again, every link on this new branch also has the possibility of being the start of yet another branch. However, the liklihood of branching goes down depending on how deeply we have branched already. 

Here is a GIF that illustrates the process of a robot being made:
![Ludobots](https://user-images.githubusercontent.com/62350419/221757231-19b170ac-5d9a-410d-8ff6-86eaade3d132.gif)

Here is a more in-depth breakdown of the process with words:
![Screen Shot 2023-02-27 at 23 31 49](https://user-images.githubusercontent.com/62350419/221762976-8d256312-04a5-4f3a-ab65-f4077c593445.png)
![Screen Shot 2023-02-27 at 23 31 55](https://user-images.githubusercontent.com/62350419/221762983-e31cd8a4-6d37-4d68-a911-c8ae4b61dd1d.png)
![Screen Shot 2023-02-27 at 23 32 01](https://user-images.githubusercontent.com/62350419/221762988-87f5f991-9180-4d7b-9931-f2985b03c64d.png)

## Evolving the Bodies
In order to evolve the bodies, the morphology of each potential solution is stored so it can be mutated by the algorithm. 
The details of the evolutionary algorithm are as follows:
1. Random bodies are generated to be the starting parent seeds. The number is determined by `populationSize`
2. Each parent has `childrenPerParent` children. Half of these children will only have their weights mutated and the other half will have links added on to them or change the size of existing links. 

**Mutating Weights**: A random weight is chosen and replaced with another random number between -1 and 1. 

**Mutating Link Size**: A random link is chosen. Since the link might be connecting two other links together, one dimensional axis is maintained so the morphology remains intact. The other two dimensions are replaced with a random number between 0.25 and 1. 

**Adding a Link**: A random link is chosen that does not currently contain a branch (it at most is connected to 2 other links) A free face of the link is found and a new link is added to it. This new link does have the potential to branch off, or be a sensor neuron. 

3. Out of all the uniquely mutated children, the one with the best fitness is chosen. If the most fit child has a better fitness than the parent, then it will continue the lineage. Otherwise, the parent will live on to have more children in the next generation. 

**Fitness Function**: The fitness of a solution is determined by the x position of the root link of the robot. A more negative x position will be treated as a better fitness score. 

4. This process will continue for `numberOfGenerations` generations. 
5. Once all generations are done, a plot will be generated showing the most fit robot in each generation, and the fittest robot from each "species" (starting parent strain) will be displayed. 

Here is a diagram showing the process of evolving a population of 5 for a single generation in the case where each parent has 10 children.
![Screen Shot 2023-02-27 at 23 55 32](https://user-images.githubusercontent.com/62350419/221766631-7273eb0b-61c4-4034-bbe9-c73acc8efe4b.png)

## Results of Evolution
In the plots below, I have two different evolutionary runs of 5 species each over 100 generations. As you can see, each "species" starts out with a different fitness and evolves differently based on random chance. They make a step-like pattern when no children are able to surpass the fitness of the parent for many generations. 
![FitnessCurve](https://user-images.githubusercontent.com/62350419/221757458-add89842-d41c-45c5-a476-14af8a483695.png)
![FitnessCurve-1](https://user-images.githubusercontent.com/62350419/221757471-bdc18f50-c95b-4098-81d5-23cfecc3a0ac.png)

## Instructions
In order to generate and evolve your own robots, pull down this branch and please the numberOfGenerations, populationSize, childrenPerParent to your liking. Then, run search.py

## Acknowledgements
Thanks to r/ludobots and pyrosim and pybullet for making this project possible.
Ludobots: https://www.reddit.com/r/ludobots/wiki/installation/
Pyrosim: https://github.com/jbongard/pyrosim
