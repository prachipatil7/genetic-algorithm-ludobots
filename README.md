# Final Project (The Scientist)
Over the course of 9 weeks, I have simulated and evolved motor behavior in simple organisms as well as added my own modifications to create and evolve random morphologies. In this process, I have noticed a correlation betweeen body size and final fitness, which I set out to investigate further in this study. 

![ezgif com-add-text](https://user-images.githubusercontent.com/62350419/225210271-18a1185f-da20-4695-b8ab-6aa5327111e5.gif)


## The Simulations 
Artificial Life relies on running many simulations of an artificial creature's behavior in order to optimize its performance for a certain task. In this section, I will detail some of the specifics of the simulations run in this experiment.
### Simulation Count
To answer my question, I had to do a LOT of simulations. (50,000 to be precise!) Before I did so, I did a couple of mini-experiments to estimate how long the simulations would take! 
| Population Size | Number of Generations | Total Simulations | Total Time (mm:ss) | Time per Sim (s) |
| --- | --- | --- | --- | --- |
| 1 | 100 | 100 | 01:23 | 0.83 |
| 5 | 20 | 100 | 01:28 | 0.88 |
| 10 | 10 | 100 | 01:44 | 1.04 |
| 10 | 50 | 500 | 10:17 | 1.23 |

According to this table, I would estimate 50,000 simulations to take between **11.5 and 17 hours**. Lucky for me, they ended up taking around 12.5 hours. 

### Physics
These simulations take place in a world with just a single plane and standard Earth Gravity (acceleration of -9.8 m/s^2) <br>
*Here is the world with a single green block in it:* <br>
<img width="736" alt="Screen Shot 2023-03-14 at 13 08 08" src="https://user-images.githubusercontent.com/62350419/225098333-f4893750-cb20-4cce-b0c7-809f19e552dc.png">

Because the morphologies are randomly generated at times, I had to make sure that they do not build themselves through or under the plane. To avoid this, the bots are built in the air, and then fall to the plane due to gravitational force. <br>
*Here is a new robot being built in midair, then moving on the plane:* <br>
![ezgif com-optimize](https://user-images.githubusercontent.com/62350419/225100376-5d9d6a29-3ff2-47ed-a286-910ff500efd4.gif)

## The Algorithms
Between each simulation, we need to keep track of the creatures' morphologies and behaviors, while also making beneficial changes to optimize for a certain goal. In this section, I will detail the ways that the algorithm encodes and modifies the bots. 
### Creating Initial Random Bodies
Each round of evolution starts out with 10 randomly generated bodies. In some cases, the bodies are 1 dimensional snakes with no branching, and in others, they are 3 dimensional complex forms with branching. Here is how both of these types of inital morphologies are generated:
#### Snake Bodies
Snake bodies are generated with the following algorithm:
1. Randomly choose a length (3-4 links)
2. For each link, keep track of the position of the parent link to calculate the position of the current link. Each link has random dimensions

Here is a diagram that details the formation of snake morphologies: <br>
![Ludobots_Snake](https://user-images.githubusercontent.com/62350419/225141500-292f0bdb-655d-422a-ae92-4091a635dbfa.gif) <br>
To view each individiual step, go <a href="https://docs.google.com/presentation/d/1QkJtwHdYPnikls9h9UAA4g4Sdw-xNyHXVw-yOt0FwVg/edit?usp=sharing">here</a>.

#### Branching Bodies
Branching bodies are generated with the following algorithm:
1. Randomly choose a length (3-4 links)
2. For each link, keep track of the position of the parent link to calculate the position of the current link. Each link has random dimensions. 
3. For every link that is sent, a coin is flipped to decide if a new branch will extend from that link. A coin is also flipped for every link to decide if it is contains a sensor neuron or not.
4. If creating a new branch, randomly decide the length of that branch and the direction in which it will extend. The new branch must extend along a different axis than the branch that is currently being built.
5. Again, every link on this new branch also has the possibility of being the start of yet another branch. However, the liklihood of branching goes down depending on how deeply we have branched already.

Here is a diagram that details the formation of branching morphologies: <br>
![Ludobots](https://user-images.githubusercontent.com/62350419/225134174-c9be17a4-c1a0-4709-b28b-c4b4843bbc87.gif) <br>
To view each individiual step, go <a href="https://docs.google.com/presentation/d/1CSIokwxJHgnQZs9IMYF87uhRMNs9nSXAmwOiGw9uZ0Y/edit?usp=sharing">here</a>.

### Encoding Brains and Bodies
In order to peform mutations and simulate inheritance, we need a way of encoding the information about the brain and the body. Here are how some of the main characteristics of a robot are encoded:
| Phenotype | Genotype |
| --- | --- |
| Body | The body is encoded through a directed graph. Each link in the body is represented by a python `LINK` object, which has fields for its parent link and child links. This setup can be seen in `link.py`, and it mimics a linked list. |
| Brain Connections | The brain connections are encoded implicitly. Each robot has a list of sensor neurons and motor neurons. The sensor neurons are chosen at random, and all joints have motor neurons. The brain connections are created by creating a synapse between every combination of 1 sensor and 1 motor neuron. This setup can be seen in `solution.py`. Even if the connected graph is not saved, it is easily regenerated by running the `Create_Brain()` function. |
| Brain Weights | The brain weights are stored in a 2D matrix, with the rows and columns representing the sensor neuron and motor neuron of the synapse accordingly. This setup can be seen in `solution.py`. This encoding method was chosen for easier mutability. |

Below are some examples of how these encodings can vary between different bots:
| Description | Snake Example | Branching Example |
| --- | --- | --- |
Bot | <img width="294" alt="Screen Shot 2023-03-14 at 17 05 50" src="https://user-images.githubusercontent.com/62350419/225156563-f1f5604d-9f24-465d-ba68-e1c83ab9b4af.png">|<img width="261" alt="Screen Shot 2023-03-14 at 17 34 05" src="https://user-images.githubusercontent.com/62350419/225157357-9e2bf882-d286-4bf1-bf85-998c58c17975.png">|
Body Encoding |<img width="158" alt="Screen Shot 2023-03-14 at 17 08 23" src="https://user-images.githubusercontent.com/62350419/225156195-761086de-a089-4499-9e38-983645089267.png">|<img width="995" alt="Screen Shot 2023-03-14 at 17 46 21" src="https://user-images.githubusercontent.com/62350419/225161170-4550246d-5c84-4381-8013-a72426a9ba97.png"> |
Brain Encoding |<img width="263" alt="Screen Shot 2023-03-14 at 17 27 45" src="https://user-images.githubusercontent.com/62350419/225156272-595f84b1-7a5a-4285-b594-2d38330c6cc0.png">|<img width="348" alt="Screen Shot 2023-03-14 at 18 02 54" src="https://user-images.githubusercontent.com/62350419/225161198-fda7621c-b598-4e64-b493-97403441bd0a.png"> |
Brain Weights | [[-0.45354025 -0.83160303]<br>[ 0.05263387 -0.15952745]<br>[ 0.26243147  0.55974003]<br>[-0.44464739  0.137477  ]]|[[ 0.65627626  0.59513052 -0.53186706 0.56924339 -0.68057246]<br>[-0.2664973  -0.45951583  0.62196881 -0.55375614  0.47363302]<br>[ 0.52664633  0.01426278  0.39802324 -0.09011762  0.56240639]<br>[ 0.47675202  0.68858778  0.49884554 -0.17353249 -0.52853125]<br>[-0.59335982 -0.96442452 -0.69991917 -0.04104824  0.27055461]<br>[-0.6209788  -0.31870314  0.8402951 -0.62298069 -0.13438554]<br>[-0.04396371 -0.07212602  0.96930183 -0.02911747  0.07195371]<br>[ 0.32499243  0.37942723  0.57721341 -0.13288538 -0.63241947]<br>[ 0.38019559 -0.54588349  0.54491643 0.72398227 -0.44366646]<br>[-0.84768468 -0.52794184  0.98775288 -0.46475363 -0.80020829]<br>[-0.04221524 -0.29335501 -0.21383727  0.35334978  0.09856925]<br>[ 0.52298143  0.19989618  0.52376507 -0.13227678 -0.95953027]]|

### Mutating Bodies and Brains
Once the different morphologies are created, they must be evolved! There are three types of changes that can be made to a bot during the evolutioinary process:
1. Change synapse weights
2. Add a link
3. Change a link (change dimensions and/or sensor status)

Here is an example of how these three mutation types can work together to evolve a bot:
| Gen | Mut | Bot | Body | Brain | Weights | Fit |
| --- | --- | --- | --- | --- | --- | --- |
|0|Start|![ezgif com-optimize (1)](https://user-images.githubusercontent.com/62350419/225178722-3ca63c93-d45f-446a-a6c3-f84cd0358927.gif)| <img width="180" alt="Screen Shot 2023-03-14 at 20 17 10" src="https://user-images.githubusercontent.com/62350419/225179203-b16df3bc-755b-44d0-b295-043229a0a869.png"> |<img width="199" alt="Screen Shot 2023-03-14 at 20 24 37" src="https://user-images.githubusercontent.com/62350419/225180112-7ce783e5-944e-4ca8-845d-a9047faa3c76.png"> | <img width="256" alt="Screen Shot 2023-03-14 at 20 31 28" src="https://user-images.githubusercontent.com/62350419/225181043-a01d5e1d-3ae4-41e5-879c-42defdff813a.png">| -0.457 |
|1|Change Weights| ![ezgif com-video-to-gif](https://user-images.githubusercontent.com/62350419/225180514-8ff44716-b1aa-47fb-b403-babc278421a2.gif)|<img width="180" alt="Screen Shot 2023-03-14 at 20 17 10" src="https://user-images.githubusercontent.com/62350419/225179203-b16df3bc-755b-44d0-b295-043229a0a869.png"> |<img width="199" alt="Screen Shot 2023-03-14 at 20 24 37" src="https://user-images.githubusercontent.com/62350419/225180112-7ce783e5-944e-4ca8-845d-a9047faa3c76.png"> | <img width="258" alt="Screen Shot 2023-03-14 at 20 33 22" src="https://user-images.githubusercontent.com/62350419/225181189-fffd4abf-5794-41b0-bbe3-37bfefe1fbac.png">| -1.227|
|6|Add Link| ![ezgif com-video-to-gif (1)](https://user-images.githubusercontent.com/62350419/225182424-558c3cc9-423f-4c50-a76f-5e1a863a9e5a.gif)|<img width="256" alt="Screen Shot 2023-03-14 at 20 40 43" src="https://user-images.githubusercontent.com/62350419/225182643-d8208fbd-714d-4472-a0cd-0f3aa9559853.png">| <img width="153" alt="Screen Shot 2023-03-14 at 20 41 35" src="https://user-images.githubusercontent.com/62350419/225182747-d1faa48c-e9ae-4d82-b73b-612e6e7d2698.png">| <img width="332" alt="Screen Shot 2023-03-14 at 20 38 15" src="https://user-images.githubusercontent.com/62350419/225182360-2469daf9-4863-4fc8-a012-a4302b4eebda.png">|-1.874|
|56|Change Link|![ezgif com-video-to-gif (2)](https://user-images.githubusercontent.com/62350419/225183110-6db04bee-85fa-4645-acca-e0d321c2adf8.gif)|<img width="254" alt="Screen Shot 2023-03-14 at 20 49 01" src="https://user-images.githubusercontent.com/62350419/225183664-4c64a2f6-b488-4f91-a5a6-2aed2e88c09b.png"> | <img width="170" alt="Screen Shot 2023-03-14 at 20 51 44" src="https://user-images.githubusercontent.com/62350419/225184081-4552dedf-af73-41bf-9b10-ac6b0704c5bf.png">|<img width="389" alt="Screen Shot 2023-03-14 at 20 50 14" src="https://user-images.githubusercontent.com/62350419/225183885-54981d86-24f1-41ac-ad36-4e2b4d6c964d.png"> | -1.888|
|115|Add Link| ![ezgif com-video-to-gif (3)](https://user-images.githubusercontent.com/62350419/225184800-50a1e5bb-4caf-46f8-a98f-bdd4d572c615.gif)|<img width="263" alt="Screen Shot 2023-03-14 at 21 00 29" src="https://user-images.githubusercontent.com/62350419/225185294-da6f0f4e-2c3b-46cf-9c1b-dbc470b7d518.png">| <img width="148" alt="Screen Shot 2023-03-14 at 21 01 35" src="https://user-images.githubusercontent.com/62350419/225185443-ee989a5c-6bb5-4608-afdc-8a631cceb7bb.png">| <img width="389" alt="Screen Shot 2023-03-14 at 21 03 11" src="https://user-images.githubusercontent.com/62350419/225185689-0f4831e5-f589-47a3-b0b8-c70e6ad06008.png">|-4.554|
|252|Change Link| ![ezgif com-video-to-gif (4)](https://user-images.githubusercontent.com/62350419/225186681-16a4fe7b-d060-40b1-95ee-beab443767d8.gif)|<img width="263" alt="Screen Shot 2023-03-14 at 21 00 29" src="https://user-images.githubusercontent.com/62350419/225185294-da6f0f4e-2c3b-46cf-9c1b-dbc470b7d518.png">| <img width="148" alt="Screen Shot 2023-03-14 at 21 01 35" src="https://user-images.githubusercontent.com/62350419/225185443-ee989a5c-6bb5-4608-afdc-8a631cceb7bb.png">| <img width="389" alt="Screen Shot 2023-03-14 at 21 03 11" src="https://user-images.githubusercontent.com/62350419/225185689-0f4831e5-f589-47a3-b0b8-c70e6ad06008.png">|-5.049|

No further beneficial mutations were found. 2 links were added, 2 links were changed and 1 weight was changed. 

### Fitness and Selection
As we are mutating our organisms, we must find a way to select which versions of our organism are better than others. This is where the **fitness function** comes it. The fitness function measures the performance of a bot and reduces it down to a single number. In our case, the fitness function is the average x position of all of the links in the bot. The more negative the fitness is, the further "into" the screen it has moved. 

The fitness is calculated in `robot.py`:
```
xCoors = []
for i in range(len(self.sensors)-1):
    stateOfLink = p.getLinkState(self.robotId,i)
    positionOfLink = stateOfLink[0]
    xCoordinateOfLink = positionOfLink[0]
    xCoors.append(xCoordinateOfLink)
fitness = sum(xCoors)/len(xCoors)
```
Once we have a fitness score for a bot, we need replicate the process of evolution. This is where the **evolutionary algorithm** is used. The evolutionary algorithm that is used is a **parallel hill climber**. Parallel hill climber works by randomly applying one of the mutations discussed above to a bot to create a child bot. Then, the child's fitness is compared with the parent's fitness. If the child has a better fitness, it will be the parent of the next generation. If not, the current parent will continue being the parent. Here is an illustration of the process for 1 generation for a population size of 4.

<img width="759" alt="Screen Shot 2023-03-14 at 21 41 27" src="https://user-images.githubusercontent.com/62350419/225191291-306a3ad1-5857-4056-87b8-639a720b4a05.png">

The selection is done in `parallelHillClimber.py`:
```
for key in self.parents:
    best_child = self.children[key][0]
    for childkey, curr_child in self.children[key].items():
        if best_child.fitness > curr_child.fitness:
            best_child = curr_child
    if self.parents[key].fitness > best_child.fitness:
        self.parents[key] = best_child
```

## The Experiment
Now that we have talked aboutu the basics of simulating and evolving bots, we are ready to test stuff out. In this section, I will go through the layout of the study that I did. 
### Hypothesis
As I was running evolutions with random morphologies, it seemed like the starting body is some indicator of how effective evolution will be. This observation made me come up with the following hypotheses to test: 
1. **It is more efficient to start off with a simple body and let the algorithm evolve its appendages, rather than starting out with a complex body with many parts.**
2. **Simpler bodies have higher fitness overall.**

The experiment is inspired by a phenomenon from the natural world. Simple organisms, such as beetles, worms, and even bacteria, have much more diversity than all mammals combined, and certainly more than humans or horses or tigers alone. This makes me think that there are many more beneficial mutations available to simple organisms than to complex ones, which is where this diversity is able to come from. The graph below shows the breakdown of different organism groups. Notice the preference for simpler organisms. I will see if this phenomenon applies to artificial life as well. <br>
![image](https://user-images.githubusercontent.com/62350419/225126240-c7bafc0e-9861-4847-8135-4766f1eb02f1.png)
<a href="https://www.researchgate.net/figure/Diversity-of-life-Percentages-are-based-on-the-estimated-total-number-of-living-species_fig1_278022190"><img src="https://www.researchgate.net/profile/Leif-Nett/publication/278022190/figure/fig1/AS:652250036838400@1532519935117/Diversity-of-life-Percentages-are-based-on-the-estimated-total-number-of-living-species.png" alt="Diversity of life. Percentages are based on the estimated total number of living species."/></a>

In the field of Artificial Life, this experiment could be important for determining more effective seeds for evolutionary algorithms. Even if the goal is to evolve complex behavior, it could be more beneficial for the algorithm to generate the complexity, rather than giving it an already-complex form to optimize. 

<img width="739" alt="Screen Shot 2023-03-14 at 21 48 40" src="https://user-images.githubusercontent.com/62350419/225192338-e0ed4e13-92b7-4c2d-9cf5-ff7a3bda9297.png">

### Method
In order to test this hypothesis, I created 2 groups for testing. The A group comprised of bots that had a starting morphology of a 1D snake. The B group consisted of bots that had a complex, branching starting morphology. Each group had 5 seed rounds consisting of 10 parents each, which evolved for 500 generations. Through this method, each group had 50 "species" generated. 

In order to generate the two different groups, the following changes were made. First, the first half of the rounds were named "snake", and the other half were named "random".

**Snake**:<br><img width="321" alt="Screen Shot 2023-03-14 at 21 46 26" src="https://user-images.githubusercontent.com/62350419/225192926-df5ec823-ba66-4948-b3d1-e774fb2deab6.png"><br>
**Random**:<br><img width="318" alt="Screen Shot 2023-03-14 at 21 47 04" src="https://user-images.githubusercontent.com/62350419/225192975-d2a65fb0-ef6b-4b1d-8b03-a93c128e7ec9.png"><br>

From `search.py` L8-9:
```
phc_lst = [PARALLEL_HILL_CLIMBER(i, "snake") for i in range(int(c.numberOfSeeds/2))]
phc_lst += [PARALLEL_HILL_CLIMBER(int(i+c.numberOfSeeds/2), "random") for i in range(int(c.numberOfSeeds/2))]
for phc in phc_lst:
```
Second, the snake rounds eliminated the chance of branching so as to only generate the bot along a single dimension.

From `solution.py` L134:
```
liklihoodOfBranching= 0 if self.seedType == "snake" else 3/self.numTorsoLinks
```

As all 50,000 simulations ran, the body size and fitness of each generation was saved so it could be analyzed. 

### Results
#### Hypothesis 1: It is more efficient to start off with a simple body and let the algorithm evolve its appendages, rather than starting out with a complex body with many parts
In order to draw conclusions about this hypothesis, I analyzed the two groups based on their final fitness scores. Overall, I found that the bots that had a simple snake starting morphology had overall better fitness than those that started with complex morphologies. This can be seen in the following two figures. 
<br>
![AB_LineChart](https://user-images.githubusercontent.com/62350419/224893662-0a3eb833-318e-4e85-996e-0caa6b882105.png)
![AB_BoxPlot](https://user-images.githubusercontent.com/62350419/224893693-05396daf-3b3a-4fab-b9e9-7f715e9a6a75.png)
<br>
Therefore, for hypothesis 1, I will say that starting out with simple morphologies and letting the algorithm develop complexity is a more effective way to evolve locomotive functionality than starting with an already complex bot. The statistics breakdown below shows that both groups have similar standard deviations, meaning they follow similar distributions. However, the Snake Start group has a much higher mean and median, which adds even more evidence in favor of this hypothesis. 

| Morphology | Mean | Median | Std Dev |
| --- | --- | --- | --- |
| Snake Start | 5.40883 | 4.92252 | 1.90786 |
| Random Start | 3.73603 | 3.53816 | 1.95109 |

#### Hypothesis 2: Simpler bodies have higher fitness overall.
To investigate this hypothesis, I plotted the initial and final sizes with the final fitnesses: <br>
![InitialSize_FinalFitness](https://user-images.githubusercontent.com/62350419/224893739-a3b5a561-1b0f-4ab1-9ceb-1eff6212203d.png)
![FinalSize_FinalFitness](https://user-images.githubusercontent.com/62350419/224893743-e882f210-6a45-46f7-a8fd-d608d519e674.png) <br>

In both figures, we can see that the fitted line always has a slight downward trend. This supports the fact that not only do simpler starting bodies lead to higher fitness, but also that simpler final bodies also lead to higher fitness. Therefore, there seems to be evidence to support that simpler bots have higher fitness in general.

### Summary Video
The results of this study can be further seen in the video below: <br>
https://user-images.githubusercontent.com/62350419/225210697-14d2e9b2-8db2-4ba4-8149-527cfccf4995.mp4
https://youtu.be/FpmQrnR3f40 

## Installation and Viewing the Simulations
Excited to poke around in the simulations? You're in luck! <br>
In order to experience the simulations from this study for yourself, please pull this branch (`s-final`). <br>
Then, run the following:
```
pip install -r requirements.txt
```
Next, go to `run.py` and run the file in order to see the best simulations, or to run a simulation of your choice! <br>
Prompts will guide you through how to run different parts of the program. Here are the options:
1. Run a random simulation (2 sims to watch)
2. Run any simulation of your choice (2 sims to watch)
3. Run the best simulation from each of the 10 seed rounds (20 sims to watch)
4. Run a shortened version of the evolutionary algorithm (*2 seeds, 1 parent, 5 generations --* 4 sims  to watch)
5. Exit

Feel free to play around with the simulations as much as you like! <br>

## Acknowledgements
Thanks to r/ludobots and pyrosim and pybullet for making this project possible.

Ludobots: https://www.reddit.com/r/ludobots/wiki/installation/

Pyrosim: https://github.com/jbongard/pyrosim
