import numpy as np

sim_steps = 1000
motor_max_force = 80
sleep_time = 0
gravity = -9.8
numberOfGenerations = 10
populationSize = 10
numSensorNeurons = 10
numMotorNeurons = 9
motorJointRange = 0.8
numSteps = 10
stairWidth = 30

# Create motor sin values
x = np.linspace(0, 2*np.pi, num=sim_steps)

# Back leg sin constants
backLegAmplitude = np.pi/3
backLegFrequency = 10
backLegPhaseOffset = 0

# Front leg sin constants
frontLegAmplitude = np.pi/3
frontLegFrequency = 10
frontLegPhaseOffset = np.pi/4