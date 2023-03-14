import pybullet as p
import pybullet_data
import time
from world import WORLD
from robot import ROBOT
import constants as c
import time

def run(ID, seedType, seedID, evolutionStage, parentID):
    physicsClient = p.connect(p.GUI)
    p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0,0,c.gravity)
    p.loadSDF("generation/world.sdf")
    p.loadURDF("plane.urdf")
    robot = ROBOT(ID, 
                  nn_path=f"save/{seedType}{seedID}_{evolutionStage}{parentID}Brain.nndf",
                  body_path=f"save/{seedType}{seedID}_{evolutionStage}{parentID}Body.urdf")

    for t in range(c.sim_steps):
        p.stepSimulation()
        # robot.Sense(t)
        # robot.Think()
        # robot.Act(t)
        time.sleep(c.sleep_time)
    p.disconnect()

run(0, "random", 9, "First", 9)

run(1, "random", 9, "Best", 9)
