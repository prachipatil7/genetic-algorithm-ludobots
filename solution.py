import numpy as np
import pyrosim.pyrosim as pyrosim
import constants as c
import os
import random
import time


class SOLUTION:
    def __init__(self, ID):
        self.weights = np.random.rand(3,2) * 2 - 1
        self.myID = ID
        # print(f"Solution {self.myID} Created")

    def Start_Simulation(self, directOrGui):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        os.system(f"python3 simulate.py {directOrGui} {self.myID} 2&>1 &")

    def Wait_For_Simulation_To_End(self):
        while not os.path.exists(f"data/fitness{self.myID}.txt"):
            time.sleep(0.1)
        fit_file = open(f"data/fitness{self.myID}.txt", "r")
        fitness = fit_file.read()
        if fitness == '':
            # print(f"Waiting on {self.myID}")
            time.sleep(0.1)
            fitness = fit_file.read()
        self.fitness = float(fitness)
        os.system(f"rm data/fitness{self.myID}.txt")
        # print(self.fitness)

    def Mutate(self):
        row = random.randint(0,2)
        col = random.randint(0,1)
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
        cube = [1, 1, 1]
        leg = [0.2, 1, 0.2]
        pyrosim.Send_Cube(name=f"Torso", 
                       pos=[0, 0, 1] , 
                        size=cube)

        pyrosim.Send_Joint(name = "Torso_FrontLeg",
                       parent= "Torso" , 
                       child = "FrontLeg" , 
                       type = "revolute", 
                       position = [0, 0.5, 1],
                       jointAxis = "1 0 0")

        pyrosim.Send_Cube(name=f"FrontLeg", 
                pos= [0, 0.5, 0], 
                size=leg)

        pyrosim.Send_Joint(name = "Torso_BackLeg",
                   parent= "Torso" , 
                   child = "BackLeg" , 
                   type = "revolute", 
                   position = [0, -0.5, 1],
                   jointAxis = "1 0 0")

        pyrosim.Send_Cube(name=f"BackLeg", 
            pos= [0, -0.5, 0], 
            size=leg)
    
        pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork(f"generation/brain{self.myID}.nndf")

        pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
        pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "BackLeg")
        pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "FrontLeg")

        pyrosim.Send_Motor_Neuron( name = 3 , jointName = "Torso_BackLeg")
        pyrosim.Send_Motor_Neuron( name = 4 , jointName = "Torso_FrontLeg")

        for curr_row in range(c.numSensorNeurons):
            for curr_col in range(c.numMotorNeurons):
                pyrosim.Send_Synapse( sourceNeuronName = curr_row , 
                                      targetNeuronName = curr_col+c.numSensorNeurons , 
                                      weight = self.weights[curr_row][curr_col])

        pyrosim.End()