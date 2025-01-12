sim_steps = 3000
motor_max_force = 80
sleep_time = 1/2000
gravity = -9.8

numberOfGenerations = 1
populationSize = 10
childrenPerParent = 1
numberOfSeeds = 2

motorJointRange = 0.5
maxLinks = 10
maxLinkSize = 1

directionDict = {
    "up": [0,0,1],
    "down": [0,0,-1],
    "right": [0,1,0],
    "left": [0,-1,0],
    "backward": [1,0,0],
    "forward": [-1,0,0]
}
directionInverseDict = {
    "up": "down",
    "down": "up",
    "left": "right",
    "right": "left",
    "forward": "backward",
    "backward": "forward"
}