# CS_396: Artificial Life
Final Project (The Scientist)

## Introduction
Over the course of 9 weeks, I have simulated and evolved motor behavior in simple organisms as well as added my own modifications to create and evolve random morphologies. In this process, I have noticed a correlation betweeen body size and final fitness, which I set out to investigate further in this study. 

[10 second teaser gif]

## Simulation Count
To answer my question, I had to do a LOT of simulations. (50,000 to be precise!) Before I did so, I did a couple of mini-experiments to estimate how long the simulations would take! 
| Population Size | Number of Generations | Total Simulations | Total Time (mm:ss) | Time per Sim (s) |
| --- | --- | --- | --- | --- |
| 1 | 100 | 100 | 01:23 | 0.83 |
| 5 | 20 | 100 | 01:28 | 0.88 |
| 10 | 10 | 100 | 01:44 | 1.04 |
| 10 | 50 | 500 | 10:17 | 1.23 |

According to this table, I would estimate 50,000 simulations to take between **11.5 and 17 hours**. Lucky for me, they ended up taking around 12.5 hours. 

## Physics
These simulations take place in a world with just a single plane and standard Earth Gravity (acceleration of -9.8 m/s^2) <br>
*Here is the world with a single green block in it:* <br>
<img width="736" alt="Screen Shot 2023-03-14 at 13 08 08" src="https://user-images.githubusercontent.com/62350419/225098333-f4893750-cb20-4cce-b0c7-809f19e552dc.png">

Because the morphologies are randomly generated at times, I had to make sure that they do not build themselves through or under the plane. To avoid this, the bots are built in the air, and then fall to the plane due to gravitational force. <br>
*Here is a new robot being built in midair, then moving on the plane:* <br>
![ezgif com-optimize](https://user-images.githubusercontent.com/62350419/225100376-5d9d6a29-3ff2-47ed-a286-910ff500efd4.gif)

## Installation and Viewing the Simulations
In order to experience the simulations from this study for yourself, please pull this branch (s-final). <br>
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
## Hypothesis
Okay, back to the experiment. Since it seems like the starting body is some indicator of how effective evolution will be, I will be testing the following hypotheses:
1. **It is more efficient to start off with a simple body and let the algorithm evolve its appendages, rather than starting out with a complex body with many parts.**
2. **Simpler bodies have higher fitness overall.**

This experiment could be important for determining more effective seeds for evolutionary algorithms. Even if the goal is to evolve complex behavior, it could be more beneficial for the algorithm to generate the complexity, rather than giving it an already-complex form to optimize. 

The experiment is inspired by a phenomenon from the natural world. Simple organisms, such as beetles, worms, and even bacteria, have much more diversity than all mammals combined, and certainly more than humans or horses or tigers alone. This makes me think that there are many more beneficial mutations available to simple organisms than to complex ones, which is where this diversity is able to come from. The graph below shows the breakdown of different organism groups. Notice the preference for simpler organisms. I will see if this phenomenon applies to artificial life as well. <br>
![image](https://user-images.githubusercontent.com/62350419/225126240-c7bafc0e-9861-4847-8135-4766f1eb02f1.png)
<a href="https://www.researchgate.net/figure/Diversity-of-life-Percentages-are-based-on-the-estimated-total-number-of-living-species_fig1_278022190"><img src="https://www.researchgate.net/profile/Leif-Nett/publication/278022190/figure/fig1/AS:652250036838400@1532519935117/Diversity-of-life-Percentages-are-based-on-the-estimated-total-number-of-living-species.png" alt="Diversity of life. Percentages are based on the estimated total number of living species."/></a>

Secondly, 

[Diagram]

## Experiment


## Brains and Bodies

## Mutation

## Results
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

## Summary Video

## Further Study

## Discussion

## Acknowledgements
Thanks to r/ludobots and pyrosim and pybullet for making this project possible.

Ludobots: https://www.reddit.com/r/ludobots/wiki/installation/

Pyrosim: https://github.com/jbongard/pyrosim
