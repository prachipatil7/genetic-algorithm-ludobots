import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import time
import numpy as np

# Set constants
sim_steps = 1000
motor_max_force = 50

# Initialize arrays to store sensor values
backLegSensorValues = np.zeros(sim_steps)
frontLegSensorValues = np.zeros(sim_steps)

# Create motor sin values
x = np.linspace(0, 2*np.pi, num=sim_steps)

backLegAmplitude = np.pi/3
backLegFrequency = 10
backLegPhaseOffset = 0
backLegTargetAngles = backLegAmplitude * np.sin(backLegFrequency * x + backLegPhaseOffset)
np.save('data/backLegTargetAngles.npy', backLegTargetAngles)

frontLegAmplitude = np.pi/3
frontLegFrequency = 10
frontLegPhaseOffset = np.pi/4
frontLegTargetAngles = frontLegAmplitude * np.sin(frontLegFrequency * x + frontLegPhaseOffset)
np.save('data/frontLegTargetAngles.npy', frontLegTargetAngles)
# exit()

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

# Simulate 1000 steps
for i in range(sim_steps):
    p.stepSimulation()

    # Record sensor values
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")

    # Simulate motor force 
    pyrosim.Set_Motor_For_Joint(bodyIndex = robotId,
                                jointName = "Torso_BackLeg",
                                controlMode = p.POSITION_CONTROL,
                                targetPosition = backLegTargetAngles[i],
                                maxForce = motor_max_force)
    pyrosim.Set_Motor_For_Joint(bodyIndex = robotId,
                                jointName = "Torso_FrontLeg",
                                controlMode = p.POSITION_CONTROL,
                                targetPosition = frontLegTargetAngles[i],
                                maxForce = motor_max_force)

    time.sleep(1/2000)

# Save the sensor values to numpy files
np.save('data/backLegSensorValues.npy', backLegSensorValues)
np.save('data/frontLegSensorValues.npy', frontLegSensorValues)

# Disconnect from the physics server
p.disconnect()
