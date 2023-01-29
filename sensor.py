import pyrosim.pyrosim as pyrosim
import numpy as np

import constants as c

class SENSOR:
    def __init__(self, linkName):
        self.linkName = linkName
        self.values = np.zeros(c.sim_steps)

    def Get_Value(self, t):
        self.values[t] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)
