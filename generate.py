import pyrosim.pyrosim as pyrosim
import numpy as np
import constants as c
import random

def create_world():
    pyrosim.Start_SDF(f"generation/world.sdf")
    length, width, height = 1, 1, 1
    xpos, ypos, zpos = -3, 3, 0.5
    pyrosim.Send_Cube(name=f"Box", 
                    pos=[xpos, ypos, zpos] , 
                    size=[length, width, height])
    pyrosim.End()

def random_dimensions():
    length = random.uniform(0.25, c.maxLinkSize)
    width = random.uniform(0.25, c.maxLinkSize)
    height = random.uniform(0.25, c.maxLinkSize)
    return np.array([length, width, height])

def decide_if_sensor_neuron(name, neuron_list):
    is_neuron = random.choice([True, False])
    if is_neuron:
        neuron_list.append(name)
        return "0 1.0 0 1.0", "Green"
    return "0 0 1.0 1.0", "Blue"

def coin_flip():
    return random.choice([True, False])

def generate_body():    
    sensorNeurons = []
    motorNeurons = []
    pyrosim.Start_URDF(f"generation/body0.urdf")
    numLinks = random.randint(2, c.maxLinks)
    print(numLinks)
    length, width, height = random_dimensions()
    cube_color, color_name = decide_if_sensor_neuron(f"Link0", sensorNeurons)
    pyrosim.Send_Cube(name=f"Link0", 
        pos=[0,0,height/2] , 
        size=[length, width, height],
        color=cube_color,
        colorName = color_name)
    pyrosim.Send_Joint(name = f"Link0_Link1",
        parent= f"Link0" , 
        child = f"Link1" , 
        type = "revolute", 
        position = [0, width/-2, height],
        jointAxis = "1 0 0")
    decide_if_sensor_neuron(f"Link0_Link1", motorNeurons)
    for i in range(1, numLinks):
        length, width, height = random_dimensions()
        cube_color, color_name = decide_if_sensor_neuron(f"Link0", sensorNeurons)
        pyrosim.Send_Cube(name=f"Link{i}", 
            pos=[0,width/-2,height/2] , 
            size=[length, width, height],
            color=cube_color,
            colorName = color_name)
        if i < numLinks-1:
            pyrosim.Send_Joint(name = f"Link{i}_Link{i+1}",
                parent= f"Link{i}" , 
                child = f"Link{i+1}" , 
                type = "revolute", 
                position = [0, width/-1, height],
                jointAxis = "1 0 0")
            decide_if_sensor_neuron(f"Link{i}_Link{i+1}", motorNeurons)
    pyrosim.End()
    print(sensorNeurons)
    print(motorNeurons)


def generate_brain():
    numSensorNeurons = random.randint(0,19)
    pyrosim.Start_NeuralNetwork(f"generation/brain0.nndf")
    pyrosim.End()