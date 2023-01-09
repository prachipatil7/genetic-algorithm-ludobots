import pyrosim.pyrosim as pyrosim

length, width, height = 1, 1, 1
xpos, ypos, zpos = 0, 0, 0.5

pyrosim.Start_SDF("boxes.sdf")
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