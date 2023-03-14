import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy as np
import time

import constants as c
from world import WORLD
from robot import ROBOT

class SIMULATION:
    def __init__(self, directOrGUI, solutionID, robotPath=None):
        if directOrGUI == "DIRECT":
            c.sleep_time = 0
            self.physicsClient = p.connect(p.DIRECT)
        elif directOrGUI == "GUI":
            c.sleep_time = 1/1000
            self.physicsClient = p.connect(p.GUI)
           
        p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, c.gravity)

        self.world = WORLD()
        if robotPath and robotPath != "-1":
            print(f"ROBOT PATH {robotPath}")
            self.robot = ROBOT(solutionID, nn_path=robotPath+"Brain.nndf", body_path=robotPath+"Body.urdf")
        elif robotPath=="-1":
            print(f"ROBOT NOPATH {robotPath}")
            self.robot = ROBOT(solutionID)

    def Run(self):       
        for t in range(c.sim_steps):
            p.stepSimulation()
            self.robot.Sense(t)
            self.robot.Think()
            self.robot.Act(t)
            time.sleep(c.sleep_time)

    def Get_Fitness(self):
        self.robot.Get_Fitness()

    def Disconnect(self):
        p.disconnect()
        print("disconnected")

    def __del__(self):
        p.disconnect()
        print("disconnected")
