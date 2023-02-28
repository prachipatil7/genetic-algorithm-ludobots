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
![Screen Shot 2023-02-27 at 22 51 13](https://user-images.githubusercontent.com/62350419/221757281-4e24f6df-aa2f-4f42-821a-ed648a6eb7a6.png)

## Evolving the Bodies

## Results of Evolution
In the plots below, I have two different evolutionary runs of 5 species each over 100 generations. There are 
![FitnessCurve](https://user-images.githubusercontent.com/62350419/221757458-add89842-d41c-45c5-a476-14af8a483695.png)
![FitnessCurve-1](https://user-images.githubusercontent.com/62350419/221757471-bdc18f50-c95b-4098-81d5-23cfecc3a0ac.png)

## Instructions
In order to generate and evolve your own robots, pull down this branch and please the numberOfGenerations, populationSize, childrenPerParent to your liking. Then, run search.py

## Acknowledgements
Thanks to r/ludobots and pyrosim and pybullet for making this project possible.
Ludobots: https://www.reddit.com/r/ludobots/wiki/installation/
Pyrosim: https://github.com/jbongard/pyrosim
