import random
import pyrosim.pyrosim as pyrosim
import constants as c
import numpy as np


class LINK:
    def __init__(self, ID, parent=None, direction="right"):
        self.IDNum = ID
        self.ID = f"Link{ID}"
        self.parent = parent
        self.directionString = direction
        self.linkDirectionVector = np.array(c.directionDict[direction])
        self.jointDirectionVector = np.copy(self.linkDirectionVector)
        self.dimensions = [random.uniform(0.25, c.maxLinkSize)*0.8, 
                            random.uniform(0.25, c.maxLinkSize), 
                            random.uniform(0.25, c.maxLinkSize)*0.5]
        self.children = []
        self.initialize_color()
        
    def create(self, liklihood_of_branching):
        self.isTurning = self.parent.directionString != self.directionString
        self.jointDirectionVector += self.parent.linkDirectionVector
        self.jointPos = self.parent.dimensions * self.jointDirectionVector * 0.5
        self.linkPos = self.dimensions * self.linkDirectionVector * 0.5
        self.jointAxis = np.array2string(np.absolute(1-self.linkDirectionVector))

        self.jointID = f"{self.parent.ID}_{self.ID}"


        pyrosim.Send_Joint(name = self.jointID,
            parent= self.parent.ID , 
            child = self.ID , 
            type = "revolute", 
            position = self.jointPos,
            jointAxis = self.jointAxis)
        pyrosim.Send_Cube(name=f"{self.ID}",
            pos=self.linkPos, 
            size=self.dimensions,
            color=self.linkColorDims,
            colorName = self.linkColorName)

        if random.random() < liklihood_of_branching:
            potential_branch_directions = list(c.directionDict.keys())
            potential_branch_directions.remove(self.directionString)
            potential_branch_directions.remove(c.directionInverseDict[self.directionString])
            branch_direction = random.choice(potential_branch_directions)
            branch_length = random.randint(1,4)
            print(branch_length, branch_direction)
            parent = self
            for i in range(0,branch_length):
                child = LINK(f"{self.IDNum}-{i}", parent, branch_direction)
                child.create(liklihood_of_branching-0.1)
                self.children.append(child)
                parent = child
            

    
    def initialize_color(self):
        self.isSensor = random.choice([True, False])
        if self.isSensor:
            self.linkColorDims = "0 1.0 0 1.0"
            self.linkColorName = "Green"
        else:
            self.linkColorDims = "0 0 1.0 1.0"
            self.linkColorName = "Blue"