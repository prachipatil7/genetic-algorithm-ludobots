import numpy as np
import pyrosim.pyrosim as pyrosim
import constants as c
import os
import random
import time
from link import LINK
import copy


class SOLUTION:
    def __init__(self, ID):
        self.myID = ID
        self.numTorsoLinks = random.randint(2, c.maxLinks)
        self.sensorNeurons = []
        self.motorNeurons = []
        self.links = []
        self.linkDict = {}


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

    def MutateWeights(self):
        self.mutation = "change weights"
        row = random.randint(0,self.numSensorNeurons-1)
        col = random.randint(0,self.numMotorNeurons-1)
        self.weights[row][col] = random.random() * 2 - 1

    def AddLink(self):
        self.mutation = "add link"
        parentOfNewLinkName = random.choice([link for link in self.linkNames if len(self.linkDict[link].children)<2])
        parentOfNewLink = self.linkDict[parentOfNewLinkName]
        potential_link_directions = list(c.directionDict.keys())
        potential_link_directions.remove(parentOfNewLink.directionString)
        potential_link_directions.remove(c.directionInverseDict[parentOfNewLink.directionString])
        link_direction = random.choice(potential_link_directions)
        newLink = LINK(f"{parentOfNewLink.IDNum}-0", parentOfNewLink, link_direction)
        newLink.jointDirectionVector += newLink.parent.linkDirectionVector
        parentOfNewLink.children.append(newLink)
        self.linkDict[newLink.ID] = newLink

    def MutateBody(self):
        self.mutation = "change link"
        linkToChange = random.choice(self.linkNames)
        newLink = copy.deepcopy(self.linkDict[linkToChange])
        newLink.dimensions *= np.absolute(newLink.linkDirectionVector)
        newLink.dimensions = [d if d!=0 else random.uniform(0.25, c.maxLinkSize) for d in newLink.dimensions]                                                                         
        newLink.initialize_color()
        self.linkDict[linkToChange] = newLink


    def Create_World(self):
        pyrosim.Start_SDF(f"generation/world.sdf")

        # length, width, height = 1, 1, 1
        # xpos, ypos, zpos = -3, 3, 0.5
        # pyrosim.Send_Cube(name=f"Box", 
                        #   pos=[xpos, ypos, zpos] , 
                        #   size=[length, width, height])

        pyrosim.End()

    def create_root_link(self, root_link=None):
        if not root_link:
            root_link = LINK(0)
        position = root_link.dimensions * np.array([0, 0, 0.5])
        position[2] += 2
        pyrosim.Send_Cube(name=root_link.ID, 
            pos=position, 
            size=root_link.dimensions,
            color=root_link.linkColorDims,
            colorName=root_link.linkColorName)
        self.links.append(root_link)
        return root_link

    def create_root_joint(self, root_link):
        position = root_link.dimensions * np.array([0, 0.5, 0.5])
        position[2] += 2
        pyrosim.Send_Joint(name = f"Link0_Link1",
            parent= f"Link0" , 
            child = f"Link1" , 
            type = "revolute", 
            position = position,
            jointAxis = "1 0 1")
        self.motorNeurons.append(f"Link0_Link1")

    def create_first_relative_joint(self, link1=None):
        if not link1:
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
            self.linkDict[link.ID]= link
            self.record_sensor_neurons(link.children)
            
        
    def Create_Body(self):
        pyrosim.Start_URDF(f"generation/body{self.myID}.urdf")
        if len(self.links)==0:
            self.numTorsoLinks = random.randint(3, 5)

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
            self.record_sensor_neurons(self.links)
            # print("sensor names:", self.sensorNeurons)
            # print("link names:", list(self.linkDict.keys()))
            self.linkNames = list(self.linkDict.keys())
        else:
            self.linkNames = list(self.linkDict.keys())
            self.linkNames.remove("Link0")
            self.create_root_link(self.linkDict["Link0"])
            self.create_root_joint(self.linkDict["Link0"])
            self.linkNames.remove("Link1")
            self.create_first_relative_joint(self.linkDict["Link1"])
            for linkName in self.linkNames:
                self.linkDict[linkName].create(-1, first_pass=False)

        pyrosim.End()
        

    def Create_Brain(self):
        self.numSensorNeurons = len(self.sensorNeurons)
        self.numMotorNeurons = len(self.motorNeurons)
        self.weights = np.random.rand(self.numSensorNeurons,self.numMotorNeurons) * 2 - 1
        # print("synapse_weights: ", self.weights)
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