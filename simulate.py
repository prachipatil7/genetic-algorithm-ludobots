import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import time
import numpy as np
import matplotlib.pyplot as plt

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

p.setGravity(0,0,-9.8)
planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")
pyrosim.Prepare_To_Simulate(robotId)

p.loadSDF("world.sdf")
backLegSensorValues = np.zeros(1000)
frontLegSensorValues = np.zeros(1000)
for i in range(1000):
    p.stepSimulation()
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
    time.sleep(1/2000)
np.save('data/backLegSensorValues.npy', backLegSensorValues)
backLegSensorValues = np.load('data/backLegSensorValues.npy')

np.save('data/frontLegSensorValues.npy', frontLegSensorValues)
frontLegSensorValues = np.load('data/frontLegSensorValues.npy')

plt.plot(backLegSensorValues, label='Back Leg', linewidth=1.5)
plt.plot(frontLegSensorValues, label='Front Leg')
plt.legend(loc='upper right')
plt.show()

p.disconnect()

