# ludobots
cs366: artificial life -- r/ludobots project

In this version of the project, I am creating branching robots. 

In order to generate 10 awesome and random ludobots, all you have to do is pull this branch and run search.py!

Here is an example of the kinds of robots that are generated in the code:
![Screen Shot 2023-02-21 at 00 29 55](https://user-images.githubusercontent.com/62350419/220265201-6d618bf9-3965-403b-88c9-70d9e0a84b62.png)

The algorithm for generating these robots is as follows:
1. Randomly select the length of the main torso "snake"
2. Start building this snake. 
3. For every link that is sent, a coin is flipped to decide if a new branch will extend from that link. A coin is also flipped for every link to decide if it is contains a sensor neuron or not.
4. If creating a new branch, randomly decide the length of that branch and the direction in which it will extend. The new branch must extend along a different axis than the branch that is currently being built. 
5. Again, every link on this new branch also has the possibility of being the start of yet another branch. However, the liklihood of branching goes down depending on how deeply we have branched already. 

Here is a GIF that illustrates the process of a robot being made:
![Ludobots](https://user-images.githubusercontent.com/62350419/220272068-63b36636-fe18-443f-95c0-9391fbb9c47e.gif)


Thanks to r/ludobots and pyrosim and pybullet for making this project possible.
