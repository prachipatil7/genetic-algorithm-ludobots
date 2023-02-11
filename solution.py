import numpy as np
import pyrosim.pyrosim as pyrosim
import constants as c
import os
import random
import time
from generate import random_dimensions, decide_neuron_state


class SOLUTION:
    def __init__(self, ID):
        self.myID = ID
        self.numLinks = random.randint(2, c.maxLinks)
        self.sensorNeurons = []
        self.motorNeurons = []

    def Start_Simulation(self, directOrGui):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        os.system(f"python3 simulate.py {directOrGui} {self.myID} 2&>1")

    def Wait_For_Simulation_To_End(self):
        while not os.path.exists(f"data/fitness{self.myID}.txt"):
            time.sleep(0.1)
        fit_file = open(f"data/fitness{self.myID}.txt", "r")
        fitness = fit_file.read()
        if fitness == '':
            time.sleep(0.1)
            fitness = fit_file.read()
        self.fitness = float(fitness)
        os.system(f"rm data/fitness{self.myID}.txt")

    def Mutate(self):
        row = random.randint(0,c.numSensorNeurons-1)
        col = random.randint(0,c.numMotorNeurons-1)
        self.weights[row][col] = random.random() * 2 - 1

    def Create_World(self):
        pyrosim.Start_SDF(f"generation/world.sdf")

        length, width, height = 1, 1, 1
        xpos, ypos, zpos = -3, 3, 0.5
        pyrosim.Send_Cube(name=f"Box", 
                          pos=[xpos, ypos, zpos] , 
                          size=[length, width, height])

        pyrosim.End()

    def Create_Body(self):
        pyrosim.Start_URDF(f"generation/body{self.myID}.urdf")
        numLinks = random.randint(2, c.maxLinks)
        print("numLinks: ", numLinks)
        length, width, height = random_dimensions()
        cube_color, color_name = decide_neuron_state(f"Link0", self.sensorNeurons)
        pyrosim.Send_Cube(name=f"Link0", 
            pos=[0,0,height/2] , 
            size=[length, width, height],
            color=cube_color,
            colorName = color_name)
        pyrosim.Send_Joint(name = f"Link0_Link1",
            parent= f"Link0" , 
            child = f"Link1" , 
            type = "revolute", 
            position = [0, width/-2, height],
            jointAxis = "1 0 0")
        self.motorNeurons.append(f"Link0_Link1")
        for i in range(1, numLinks):
            length, width, height = random_dimensions()
            cube_color, color_name = decide_neuron_state(f"Link{i}", self.sensorNeurons)
            pyrosim.Send_Cube(name=f"Link{i}", 
                pos=[0,width/-2,height/2] , 
                size=[length, width, height],
                color=cube_color,
                colorName = color_name)
            if i < numLinks-1:
                pyrosim.Send_Joint(name = f"Link{i}_Link{i+1}",
                    parent= f"Link{i}" , 
                    child = f"Link{i+1}" , 
                    type = "revolute", 
                    position = [0, width/-1, height],
                    jointAxis = "1 0 0")
                self.motorNeurons.append(f"Link{i}_Link{i+1}")
        pyrosim.End()
        print("sensor names:", self.sensorNeurons)
        # print(self.motorNeurons)

    def Create_Brain(self):
        self.numSensorNeurons = len(self.sensorNeurons)
        self.numMotorNeurons = len(self.motorNeurons)
        self.weights = np.random.rand(self.numSensorNeurons,self.numMotorNeurons) * 2 - 1
        print("synapse_weights: ", self.weights)
        pyrosim.Start_NeuralNetwork(f"generation/brain{self.myID}.nndf")

        i=0
        for link in self.sensorNeurons:
            pyrosim.Send_Sensor_Neuron(name = i , linkName = link)
            i+=1
        for joint in self.motorNeurons:
            pyrosim.Send_Motor_Neuron( name = i , jointName = joint)
            i+=1

        for curr_row in range(self.numSensorNeurons):
            for curr_col in range(self.numMotorNeurons):
                pyrosim.Send_Synapse( sourceNeuronName = curr_row , 
                                      targetNeuronName = curr_col+self.numSensorNeurons , 
                                      weight = self.weights[curr_row][curr_col])

        pyrosim.End()