import pybullet as p
import pybullet_data


class WORLD:
    def __init__(self, path=None):
        self.planeId = p.loadURDF("plane.urdf")
        if path:
            p.loadSDF(path)
        else:
            p.loadSDF("generation/world.sdf")
