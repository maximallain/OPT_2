# from pyscipopt import Model
from math import ceil

def read_map(path='input_9.txt'):
    #Read all the data from the input_file
    with open(path,'r') as input:
        input=input.readlines()
        #This extract the radius r1 and r2 from the input file
        r1,r2=input[0].split(',')
        r1=int(r1)
        r2=int(r2)
        # This extract the prices p1 and p2 from the input file
        p1,p2=input[1].split(',')
        p1=int(p1)
        p2=int(p2)

        #This extract the list of art object positions from the input file
        positions_list=[]
        for i in range(2,len(input)):
            positions_list.append(eval(input[i]))

        #This finds the limits of a square that includes all the art objects
        x_list=[position[0] for position in positions_list]
        y_list = [position[1] for position in positions_list]

        x_min=min(x_list)
        y_min=min(y_list)
        x_max=max(x_list)
        y_max=max(y_list)

    return x_min,x_max,y_min,y_max,[r1,r2],[p1,p2],positions_list



def model(input_path='input_9.txt',grid_unit=1):

    #Take all the data from the input_file, with the read_map function
    x_min, x_max, y_min, y_max, [r1, r2], [p1, p2], positions_list =read_map(input_path)

    model=Model('optim')
    c_x_list=[x_min+k*grid_unit for k in range(0,ceil((x_max-x_min)/grid_unit)+1)]
    c_y_list=[y_min+k*grid_unit for k in range(0,ceil((y_max-y_min)/grid_unit)+1)]

    #Variables definition
    # Format : variable_dict={"c-1-14-13" : variable c-1-14-13, "c-2-16-3" : variable c-2-16-3, ... }
    variable_dict={}
    for u in [1,2]:
        for i in c_x_list:
            for j in c_y_list:
                variable_dict["c-"+str(u)+"-"+str(i)+"-"+str(j)]=model.addVar("c-"+str(u)+"-"+str(i)+"-"+str(j), vtype="INTEGER")

    #Objective definition
    total_cost=0
    for var in variable_dict.keys():
        if var[2:3]=="1":
            total_cost+=variable_dict[var]*p1
        if var[2:3]=="2":
            total_cost+=variable_dict[var]*p2

    model.setObjective(total_cost,"minimize")

    #Constraints definition
    for (i,j) in positions_list:
        cons=0
        for (x,y) in grid_disk(i,j,r1,grid_unit):
            cons+=variable_dict["c-1-"+str(x)+"-"+str(y)]
        for (x, y) in grid_disk(i, j, r2, grid_unit):
            cons+=variable_dict["c-2-"+str(x)+"-"+str(y)]
        model.addCons(cons >= 1)

    return model.optimize()

    # x = model.addVar("x")
    # y = model.addVar("y", vtype="INTEGER")
    # model.setObjective(x + y)
    # model.addCons(2 * x - y * y >= 0)
    # model.optimize()


def grid_disk(i,j,l,grid_unit=1):
    #Provides the list of possible cam positions in a l disk around an art object in i,j
    disk_points=[]
    for x in ([i+k*grid_unit for k in range(0,ceil((l/grid_unit)+1))]+[i-k*grid_unit for k in range(1,ceil((l/grid_unit)+1))]):
        for y in ([j + k * grid_unit for k in range(0, ceil((l / grid_unit) + 1))] + [i - k * grid_unit for k in range(1, ceil((l / grid_unit) + 1))]):
            if pow((x-i),2)+pow((y-j),2)<=pow(l,2):
                disk_points.append((x,y))
    return disk_points
