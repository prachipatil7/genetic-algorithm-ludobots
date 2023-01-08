import pyrosim.pyrosim as pyrosim

length, width, height = 1, 2, 3

pyrosim.Start_SDF("box.sdf")
pyrosim.Send_Cube(name="Box", pos=[0,0,0.5] , size=[length, width, height])

pyrosim.End()