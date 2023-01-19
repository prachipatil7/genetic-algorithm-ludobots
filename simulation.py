import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy as np
import time

import constants as c
from world import WORLD
from robot import ROBOT

class SIMULATION:
    def __init__(self):
        self.physicsClient = p.connect(p.GUI) 
        
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, c.gravity)

        self.world = WORLD()
        self.robot = ROBOT()

    def Run(self):       
        # Simulate 1000 steps
        for t in range(c.sim_steps):
            p.stepSimulation()
            self.robot.Sense(t)
            self.robot.Think()
            self.robot.Act(t)
            time.sleep(c.sleep_time)

    def __del__(self):
        p.disconnect()
