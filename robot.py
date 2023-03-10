import pybullet as p
import pyrosim.pyrosim as pyrosim
from pyrosim.neuralNetwork import NEURAL_NETWORK
import os
from sensor import SENSOR
from motor import MOTOR
import constants as c

class ROBOT:
    def __init__(self, solutionID):
        self.sensors = {}
        self.motors = {}
        self.nn = NEURAL_NETWORK(f"generation/brain{solutionID}.nndf")
        self.robotId = p.loadURDF(f"generation/body{solutionID}.urdf")
        self.solutionId = solutionID
        # os.system(f"rm generation/brain{solutionID}.nndf")
        # os.system(f"rm generation/body{solutionID}.urdf")
        pyrosim.Prepare_To_Simulate(self.robotId)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()

    def Prepare_To_Sense(self):
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)

    def Sense(self, t):
        for linkName, sensor in self.sensors.items():
            sensor.Get_Value(t)

    def Prepare_To_Act(self):
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)

    def Act(self, t):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)    
                desiredAngle = self.nn.Get_Value_Of(neuronName) *  c.motorJointRange
                self.motors[jointName].Set_Value(desiredAngle, self.robotId)

    def Get_Fitness(self):
        xCoors = []
        for i in range(len(self.sensors)-1):
            stateOfLink = p.getLinkState(self.robotId,i)        
            positionOfLink = stateOfLink[0]
            xCoordinateOfLink = positionOfLink[0]
            xCoors.append(xCoordinateOfLink)
        # print(xCoordinateOfLinkZero)
        fitness = sum(xCoors)/len(xCoors)
        fit_file = open(f"data/tmp{self.solutionId}.txt", "w")
        fit_file.write(str(fitness))

        os.system(f"mv data/tmp{self.solutionId}.txt data/fitness{self.solutionId}.txt")
   
    def Think(self):
        self.nn.Update()