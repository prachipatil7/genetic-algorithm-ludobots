import matplotlib.pyplot as plt
import numpy as np

# Load the motor target angles from numpy files
backLegTargetAngles = np.load('data/Torso_BackLeg_MotorValues.npy')
frontLegTargetAngles = np.load('data/Torso_FrontLeg_MotorValues.npy')

# Plot the angle values
plt.plot(backLegTargetAngles, label='Back Leg', linewidth=1.4)
plt.plot(frontLegTargetAngles, label='Front Leg', linewidth=0.7)
plt.legend(loc='upper right')
plt.show()

# Load the sensor values from numpy files
backLegSensorData = np.load('data/backLegSensorValues.npy')
frontLegSensorData = np.load('data/frontLegSensorValues.npy')

# Plot the sensor values
plt.plot(backLegSensorData, label='Back Leg', linewidth=1.4)
plt.plot(frontLegSensorData, label='Front Leg', linewidth=0.7)
plt.legend(loc='upper right')
plt.show()