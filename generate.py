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
    cube = [1, 1, 1]
    pyrosim.Send_Cube(name=f"Torso", 
                    pos=[0, 0, 1.5] , 
                    size=cube)

    pyrosim.Send_Joint(name = "Torso_FrontLeg",
                       parent= "Torso" , 
                       child = "FrontLeg" , 
                       type = "revolute", 
                       position = [0.5,0,1])

    pyrosim.Send_Cube(name=f"FrontLeg", 
                pos= [0.5, 0, -0.5], 
                size=cube)

    pyrosim.Send_Joint(name = "Torso_BackLeg",
                   parent= "Torso" , 
                   child = "BackLeg" , 
                   type = "revolute", 
                   position = [-0.5,0,1])

    pyrosim.Send_Cube(name=f"BackLeg", 
            pos= [-0.5, 0, -0.5], 
            size=cube)
    
    pyrosim.End()

create_world()
create_robot()