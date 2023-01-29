import numpy as np

sim_steps = 1500
motor_max_force = 50
sleep_time = 0
gravity = -9.8
numberOfGenerations = 1
populationSize = 1
numSensorNeurons = 3
numMotorNeurons = 2

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