import numpy as np
import pyrosim.pyrosim as pyrosim
import generate
import constants as c
import os
import random
import time


class SOLUTION:
    def __init__(self, ID):
        self.weights = np.random.rand(c.numSensorNeurons,c.numMotorNeurons) * 2 - 1
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
        while fitness == '':
            # print(f"Waiting on {self.myID}")
            time.sleep(0.1)
            fitness = fit_file.read()
        self.fitness = float(fitness)
        os.system(f"rm data/fitness{self.myID}.txt")
        # print(self.fitness)

    def Mutate(self):
        row = random.randint(0,c.numSensorNeurons-1)
        col = random.randint(0,c.numMotorNeurons-1)
        self.weights[row][col] = random.random() * 2 - 1

    def Create_World(self):
        pyrosim.Start_SDF("generation/world.sdf")
        xpos, ypos, zpos = (c.numSteps+1)/-2 - 5.5, 0, 0.25
        for i in range(c.numSteps):
            length, width, height = 2*(c.numSteps-i), c.stairWidth, 0.5
            pyrosim.Send_Cube(name=f"Box{i}", 
                            pos=[xpos, ypos, zpos] , 
                            size=[length, width, height],
                            mass = 50.0)
            zpos += 0.5
            xpos -= 1
        pyrosim.End()

    def Create_Body(self):
        pyrosim.Start_URDF(f"generation/body{self.myID}.urdf")
        leg = [0.2, 1, 0.2]
        leg2 = [1, 0.2, 0.2]
        leg3 = [0.2, 0.2, 1]
        pyrosim.Send_Cube(name=f"Torso", 
                       pos=[0, 0, 1] , 
                        size=[2, 1, 1])

        pyrosim.Send_Joint(name = "Torso_FrontRightLeg",
                       parent= "Torso" , 
                       child = "FrontRightLeg" , 
                       type = "revolute", 
                       position = [-0.5, 0.5, 1],
                       jointAxis = "0 1 0")

        pyrosim.Send_Cube(name=f"FrontRightLeg", 
                pos= [0, 0.5, 0], 
                size=leg)

        pyrosim.Send_Joint(name = "FrontRightLeg_FrontRightLeg2",
               parent= "FrontRightLeg" , 
               child = "FrontRightLeg2" , 
               type = "revolute", 
               position = [0, 1, 0],
               jointAxis = "0 1 0")

        pyrosim.Send_Cube(name=f"FrontRightLeg2", 
                        pos= [0, 0, -0.5], 
                        size=leg3)

        pyrosim.Send_Joint(name = "Torso_BackRightLeg",
               parent= "Torso" , 
               child = "BackRightLeg" , 
               type = "revolute", 
               position = [0.5, 0.5, 1],
               jointAxis = "0 1 0")
        pyrosim.Send_Cube(name=f"BackRightLeg", 
                pos= [0, 0.5, 0], 
                size=leg)
        pyrosim.Send_Joint(name = "BackRightLeg_BackRightLeg2",
            parent= "BackRightLeg" , 
            child = "BackRightLeg2" , 
            type = "revolute", 
            position = [0, 1, 0],
            jointAxis = "0 1 0")
        pyrosim.Send_Cube(name=f"BackRightLeg2", 
                        pos= [0, 0, -0.5], 
                        size=leg3)



        pyrosim.Send_Joint(name = "Torso_FrontLeftLeg",
               parent= "Torso" , 
               child = "FrontLeftLeg" , 
               type = "revolute", 
               position = [-0.5, -0.5, 1],
               jointAxis = "0 1 0")
        pyrosim.Send_Cube(name=f"FrontLeftLeg", 
                pos= [0, -0.5, 0], 
                size=leg)
        pyrosim.Send_Joint(name = "FrontLeftLeg_FrontLeftLeg2",
            parent= "FrontLeftLeg" , 
            child = "FrontLeftLeg2" , 
            type = "revolute", 
            position = [0, -1, 0],
            jointAxis = "0 1 0")
        pyrosim.Send_Cube(name=f"FrontLeftLeg2", 
                        pos= [0, 0, -0.5], 
                        size=leg3)
        pyrosim.Send_Joint(name = "Torso_BackLeftLeg",
            parent= "Torso" , 
            child = "BackLeftLeg" , 
            type = "revolute", 
            position = [0.5, -0.5, 1],
            jointAxis = "0 1 0")
        pyrosim.Send_Cube(name=f"BackLeftLeg", 
                pos= [0, -0.5, 0], 
                size=leg)
        pyrosim.Send_Joint(name = "BackLeftLeg_BackLeftLeg2",
            parent= "BackLeftLeg" , 
            child = "BackLeftLeg2" , 
            type = "revolute", 
            position = [0, -1, 0],
            jointAxis = "0 1 0")
        pyrosim.Send_Cube(name=f"BackLeftLeg2", 
                        pos= [0, 0, -0.5], 
                        size=leg3)
        pyrosim.Send_Joint(name = "Torso_Head",
                parent= "Torso" , 
                child = "Head" , 
                type = "revolute", 
                position = [-1, 0, 1.5],
                jointAxis = "0 1 0")
        pyrosim.Send_Cube(name=f"Head", 
                pos= [0, 0, 0], 
                size=[0.5,0.5,0.5])
    
        pyrosim.End()       

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork(f"generation/brain{self.myID}.nndf")

        pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
        pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "FrontRightLeg")
        pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "FrontRightLeg2")
        pyrosim.Send_Sensor_Neuron(name = 3 , linkName = "BackRightLeg")
        pyrosim.Send_Sensor_Neuron(name = 4 , linkName = "BackRightLeg2")
        pyrosim.Send_Sensor_Neuron(name = 5 , linkName = "FrontLeftLeg")
        pyrosim.Send_Sensor_Neuron(name = 6 , linkName = "FrontLeftLeg2")
        pyrosim.Send_Sensor_Neuron(name = 7 , linkName = "BackLeftLeg")
        pyrosim.Send_Sensor_Neuron(name = 8 , linkName = "BackLeftLeg2")
        pyrosim.Send_Sensor_Neuron(name = 9 , linkName = "Head")
        
        pyrosim.Send_Motor_Neuron( name = 10 , jointName = "Torso_Head")
        pyrosim.Send_Motor_Neuron( name = 11 , jointName = "Torso_FrontRightLeg")
        pyrosim.Send_Motor_Neuron( name = 12 , jointName = "FrontRightLeg_FrontRightLeg2")   
        pyrosim.Send_Motor_Neuron( name = 13 , jointName = "Torso_BackRightLeg")
        pyrosim.Send_Motor_Neuron( name = 14 , jointName = "BackRightLeg_BackRightLeg2")
        pyrosim.Send_Motor_Neuron( name = 15 , jointName = "Torso_FrontLeftLeg")
        pyrosim.Send_Motor_Neuron( name = 16 , jointName = "FrontLeftLeg_FrontLeftLeg2")
        pyrosim.Send_Motor_Neuron( name = 17 , jointName = "Torso_BackLeftLeg")
        pyrosim.Send_Motor_Neuron( name = 18 , jointName = "BackLeftLeg_BackLeftLeg2")

        for curr_row in range(c.numSensorNeurons):
            for curr_col in range(c.numMotorNeurons):
                pyrosim.Send_Synapse( sourceNeuronName = curr_row , 
                                      targetNeuronName = curr_col+c.numSensorNeurons , 
                                      weight = self.weights[curr_row][curr_col])

        pyrosim.End()