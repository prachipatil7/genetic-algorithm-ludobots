import numpy as np

sim_steps = 1500
motor_max_force = 100
sleep_time = 0
gravity = -9.8
numberOfGenerations = 50
populationSize = 10
numSensorNeurons = 6
numMotorNeurons = 5
motorJointRange = 0.8
numSteps = 10

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