import pybullet as p
import pyrosim.pyrosim as pyrosim
import numpy as np

import constants as c

class MOTOR:
    def __init__(self, jointName):
        self.jointName = jointName

        self.amplitude = c.backLegAmplitude
        self.frequency = c.backLegFrequency
        if jointName == 'Torso_BackLeg':
            self.frequency /= 2
        self.phaseOffset = c.backLegPhaseOffset
        self.motorValues = self.amplitude * np.sin(self.frequency * c.x + self.phaseOffset)

    def Set_Value(self, desiredAngle, robotId):
        pyrosim.Set_Motor_For_Joint(bodyIndex = robotId,
                            jointName = self.jointName,
                            controlMode = p.POSITION_CONTROL,
                            targetPosition = desiredAngle,
                            maxForce = c.motor_max_force)
        if desiredAngle+1 == c.sim_steps:
            self.Save_Values()

    def Save_Values(self):
        np.save(f'data/{self.jointName}_MotorValues.npy', self.motorValues)
