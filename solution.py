import numpy as np
import pyrosim.pyrosim as pyrosim
import constants as c
import os
import random
import time
from link import LINK

class SOLUTION:
    def __init__(self, ID):
        self.myID = ID
        self.numTorsoLinks = random.randint(2, c.maxLinks)
        self.sensorNeurons = []
        self.motorNeurons = []
        self.links = []

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

    def create_root_link(self):
        root_link = LINK(0)
        position = root_link.dimensions * np.array([0, 0, 0.5])
        position[2] += 5
        pyrosim.Send_Cube(name=root_link.ID, 
            pos=position, 
            size=root_link.dimensions,
            color=root_link.linkColorDims,
            colorName=root_link.linkColorName)
        self.links.append(root_link)
        return root_link

    def create_root_joint(self, root_link):
        position = root_link.dimensions * np.array([0, 0.5, 0.5])
        position[2] += 5
        pyrosim.Send_Joint(name = f"Link0_Link1",
            parent= f"Link0" , 
            child = f"Link1" , 
            type = "revolute", 
            position = position,
            jointAxis = "1 0 1")
        self.motorNeurons.append(f"Link0_Link1")

    def create_first_relative_joint(self):
        link1 = LINK(1)
        position = link1.dimensions * np.array([0, 0.5, 0])
        pyrosim.Send_Cube(name=link1.ID, 
            pos=position, 
            size=link1.dimensions,
            color=link1.linkColorDims,
            colorName=link1.linkColorName)
        self.links.append(link1)
        return link1

    def record_sensor_neurons(self, lst):
        for link in lst:
            if link.isSensor:
                self.sensorNeurons.append(link.ID)
        for link in lst:
            self.record_sensor_neurons(link.children)
        
    def Create_Body(self):
        pyrosim.Start_URDF(f"generation/body{self.myID}.urdf")
        self.numTorsoLinks = random.randint(3, 7)

        root_link = self.create_root_link()
        self.create_root_joint(root_link)
        parent = self.create_first_relative_joint()
        self.links.append(parent)
        for i in range(2, self.numTorsoLinks):
            child = LINK(str(i), parent, "right")
            child.create(3/self.numTorsoLinks)
            self.motorNeurons.append(child.jointID)
            self.links.append(child)
            parent = child

        pyrosim.End()
        
        self.record_sensor_neurons(self.links)
        print("sensor names:", self.sensorNeurons)

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