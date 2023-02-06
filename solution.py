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
        xpos, ypos, zpos = (c.numSteps+1)/-2 - 1, 0, 0.25
        for i in range(c.numSteps):
            length, width, height = c.numSteps-i, 10, 0.5
            pyrosim.Send_Cube(name=f"Box", 
                            pos=[xpos, ypos, zpos] , 
                            size=[length, width, height],
                            mass = 50.0)
            zpos += 0.5
            xpos -= 0.5
        pyrosim.End()

    def Create_Body(self):
        pyrosim.Start_URDF(f"generation/body{self.myID}.urdf")
        cube = [1, 1, 1]
        leg = [0.2, 1, 0.2]
        leg2 = [1, 0.2, 0.2]
        leg3 = [0.2, 0.2, 1]
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

        pyrosim.Send_Joint(name = "FrontLeg_FrontLeg2",
               parent= "FrontLeg" , 
               child = "FrontLeg2" , 
               type = "revolute", 
               position = [0, 1, 0],
               jointAxis = "1 0 0")

        pyrosim.Send_Cube(name=f"FrontLeg2", 
                        pos= [0, 0, -0.5], 
                        size=leg3)

        pyrosim.Send_Joint(name = "Torso_BackLeg",
                   parent= "Torso" , 
                   child = "BackLeg" , 
                   type = "revolute", 
                   position = [0, -0.5, 1],
                   jointAxis = "1 0 0")

        pyrosim.Send_Cube(name=f"BackLeg", 
            pos= [0, -0.5, 0], 
            size=leg)

        pyrosim.Send_Joint(name = "BackLeg_BackLeg2",
                            parent= "BackLeg" , 
                            child = "BackLeg2" , 
                            type = "revolute", 
                            position = [0, -1, 0],
                            jointAxis = "1 0 0")

        pyrosim.Send_Cube(name=f"BackLeg2", 
                pos= [0, 0, -0.5], 
                size=leg3)

        pyrosim.Send_Joint(name = "Torso_TopLeg",
                parent= "Torso" , 
                child = "TopLeg" , 
                type = "revolute", 
                position = [0, 0, 1.5],
                jointAxis = "0 1 0")
        pyrosim.Send_Cube(name=f"TopLeg", 
                        pos= [0, 0, 0.5], 
                        size=leg3)
        pyrosim.Send_Joint(name = "TopLeg_TopLeg2",
                    parent= "TopLeg" , 
                    child = "TopLeg2" , 
                    type = "revolute", 
                    position = [0, 0, 1],
                    jointAxis = "0 1 0")
        pyrosim.Send_Cube(name=f"TopLeg2", 
                pos= [-0.5, 0, 0], 
                size=leg2)
        
        pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork(f"generation/brain{self.myID}.nndf")

        pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
        pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "BackLeg")
        pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "FrontLeg")
        pyrosim.Send_Sensor_Neuron(name = 3 , linkName = "TopLeg")
        pyrosim.Send_Sensor_Neuron(name = 4 , linkName = "BackLeg2")
        pyrosim.Send_Sensor_Neuron(name = 5 , linkName = "FrontLeg2")
        pyrosim.Send_Sensor_Neuron(name = 6 , linkName = "TopLeg2")

        pyrosim.Send_Motor_Neuron( name = 7 , jointName = "Torso_BackLeg")
        pyrosim.Send_Motor_Neuron( name = 8 , jointName = "Torso_FrontLeg")
        pyrosim.Send_Motor_Neuron( name = 9 , jointName = "Torso_TopLeg")
        pyrosim.Send_Motor_Neuron( name = 10 , jointName = "BackLeg_BackLeg2")
        pyrosim.Send_Motor_Neuron( name = 11 , jointName = "FrontLeg_FrontLeg2")
        pyrosim.Send_Motor_Neuron( name = 12 , jointName = "TopLeg_TopLeg2")


        for curr_row in range(c.numSensorNeurons):
            for curr_col in range(c.numMotorNeurons):
                pyrosim.Send_Synapse( sourceNeuronName = curr_row , 
                                      targetNeuronName = curr_col+c.numSensorNeurons , 
                                      weight = self.weights[curr_row][curr_col])

        pyrosim.End()