import matplotlib.pyplot as plt
import numpy as np

backLegTargetAngles = np.load('data/backLegTargetAngles.npy')
frontLegTargetAngles = np.load('data/frontLegTargetAngles.npy')
plt.plot(backLegTargetAngles, label='Back Leg', linewidth=1.4)
plt.plot(frontLegTargetAngles, label='Front Leg', linewidth=0.7)
plt.legend(loc='upper right')
plt.show()
exit()

# Load the sensor values from numpy files
backLegSensorData = np.load('data/backLegSensorValues.npy')
frontLegSensorData = np.load('data/frontLegSensorValues.npy')

# Plot the sensor values
plt.plot(backLegSensorData, label='Back Leg', linewidth=1.4)
plt.plot(frontLegSensorData, label='Front Leg', linewidth=0.7)
plt.legend(loc='upper right')
plt.show()