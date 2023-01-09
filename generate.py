import pyrosim.pyrosim as pyrosim

pyrosim.Start_SDF("boxes.sdf")

for row in range(5):
    for col in range(5):
        length, width, height = 1, 1, 1
        xpos, ypos, zpos = row, col, 0.5
        for i in range(10):
            pyrosim.Send_Cube(name=f"Box{i}", 
                            pos=[xpos, ypos, zpos] , 
                            size=[length, width, height])
            length *= 0.9
            width *= 0.9
            zpos += height/2
            height *= 0.9
            zpos += height/2
pyrosim.End()