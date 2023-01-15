import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import time
import numpy as np
import matplotlib.pyplot as plt

# Connect to the physics server and set the additional search path to the data path
physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# Set gravity and load the plane and robot URDFs
p.setGravity(0,0,-9.8)
planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")

# Prepare the robot for simulation
pyrosim.Prepare_To_Simulate(robotId)

# Load the world SDF file
p.loadSDF("world.sdf")

# Initialize arrays to store sensor values
backLegSensorValues = np.zeros(1000)
frontLegSensorValues = np.zeros(1000)

# Simulate 1000 steps
for i in range(1000):
    p.stepSimulation()

    # Record sensor values
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")

    # Simulate motor force 
    pyrosim.Set_Motor_For_Joint(bodyIndex = robotId,
                                jointName = "Torso_BackLeg",
                                controlMode = p.POSITION_CONTROL,
                                targetPosition = 0.0,
                                maxForce = 500)

    time.sleep(1/2000)

# Save the sensor values to numpy files
np.save('data/backLegSensorValues.npy', backLegSensorValues)
np.save('data/frontLegSensorValues.npy', frontLegSensorValues)

# Load the sensor values from numpy files
backLegSensorData = np.load('data/backLegSensorValues.npy')
frontLegSensorData = np.load('data/frontLegSensorValues.npy')

# Plot the sensor values
plt.plot(backLegSensorData, label='Back Leg', linewidth=1.3)
plt.plot(frontLegSensorData, label='Front Leg', linewidth=0.8)
plt.legend(loc='upper right')
plt.show()

# Disconnect from the physics server
p.disconnect()
