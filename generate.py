import pyrosim.pyrosim as pyrosim

def create_world():
    pyrosim.Start_SDF("world.sdf")

    length, width, height = 1, 1, 1
    xpos, ypos, zpos = -3, 3, 0.5
    pyrosim.Send_Cube(name=f"Box", 
                    pos=[xpos, ypos, zpos] , 
                    size=[length, width, height])

    pyrosim.End()

def create_robot():
    pyrosim.Start_URDF("body.urdf")
    length, width, height = 1, 1, 1
    xpos, ypos, zpos = 0, 0, 0.5
    pyrosim.Send_Cube(name=f"Torso", 
                    pos=[xpos, ypos, zpos] , 
                    size=[length, width, height])
    pyrosim.End()

create_world()
create_robot()