# Final Project (The Scientist)
Over the course of 9 weeks, I have simulated and evolved motor behavior in simple organisms as well as added my own modifications to create and evolve random morphologies. In this process, I have noticed a correlation betweeen body size and final fitness, which I set out to investigate further in this study. 

[10 second teaser gif]

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
Bot | <img width="308" alt="Screen Shot 2023-03-14 at 16 53 47" src="https://user-images.githubusercontent.com/62350419/225148908-b65f53dc-1b0f-40ca-9056-2de73d2bdb2a.png"> | |
Body Encoding |<img width="158" alt="Screen Shot 2023-03-14 at 17 08 23" src="https://user-images.githubusercontent.com/62350419/225156195-761086de-a089-4499-9e38-983645089267.png">| |
Brain Encoding |<img width="263" alt="Screen Shot 2023-03-14 at 17 27 45" src="https://user-images.githubusercontent.com/62350419/225156272-595f84b1-7a5a-4285-b594-2d38330c6cc0.png">| |
Brain Weights | [[-0.45354025 -0.83160303]<br>[ 0.05263387 -0.15952745]<br>[ 0.26243147  0.55974003]<br>[-0.44464739  0.137477  ]]| |

### Mutating Bodies and Brains

### Fitness and Selection

## The Experiment
### Hypothesis
Since it seems like the starting body is some indicator of how effective evolution will be, I will be testing the following hypotheses:
1. **It is more efficient to start off with a simple body and let the algorithm evolve its appendages, rather than starting out with a complex body with many parts.**
2. **Simpler bodies have higher fitness overall.**

The experiment is inspired by a phenomenon from the natural world. Simple organisms, such as beetles, worms, and even bacteria, have much more diversity than all mammals combined, and certainly more than humans or horses or tigers alone. This makes me think that there are many more beneficial mutations available to simple organisms than to complex ones, which is where this diversity is able to come from. The graph below shows the breakdown of different organism groups. Notice the preference for simpler organisms. I will see if this phenomenon applies to artificial life as well. <br>
![image](https://user-images.githubusercontent.com/62350419/225126240-c7bafc0e-9861-4847-8135-4766f1eb02f1.png)
<a href="https://www.researchgate.net/figure/Diversity-of-life-Percentages-are-based-on-the-estimated-total-number-of-living-species_fig1_278022190"><img src="https://www.researchgate.net/profile/Leif-Nett/publication/278022190/figure/fig1/AS:652250036838400@1532519935117/Diversity-of-life-Percentages-are-based-on-the-estimated-total-number-of-living-species.png" alt="Diversity of life. Percentages are based on the estimated total number of living species."/></a>

In the field of Artificial Life, this experiment could be important for determining more effective seeds for evolutionary algorithms. Even if the goal is to evolve complex behavior, it could be more beneficial for the algorithm to generate the complexity, rather than giving it an already-complex form to optimize. 

[Diagram]

### Method


### Results
Line Chart
![AB_LineChart](https://user-images.githubusercontent.com/62350419/224893662-0a3eb833-318e-4e85-996e-0caa6b882105.png)

Box Plot
![AB_BoxPlot](https://user-images.githubusercontent.com/62350419/224893693-05396daf-3b3a-4fab-b9e9-7f715e9a6a75.png)

![InitialSize_InitialFitness](https://user-images.githubusercontent.com/62350419/224893731-af051325-bb9a-4256-b317-6b12da02284e.png)
![InitialSize_FinalFitness](https://user-images.githubusercontent.com/62350419/224893739-a3b5a561-1b0f-4ab1-9ceb-1eff6212203d.png)
![FinalSize_FinalFitness](https://user-images.githubusercontent.com/62350419/224893743-e882f210-6a45-46f7-a8fd-d608d519e674.png)


| Morphology | Mean | Median | Std Dev |
| --- | --- | --- | --- |
| Snake Start | 5.40883 | 4.92252 | 1.90786 |
| Random Start | 3.73603 | 3.53816 | 1.95109 |

### Summary Video

### Further Study

### Discussion

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
