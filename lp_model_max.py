from pyscipopt import Model
from math import ceil

n = str(9)

def read_map(path='input_'+n+'.txt'):
    """
    This function reads the file and return the map's characteristic
    :param path: file's path
    :return: height, width, radius_1, radius_2, price_1, price_2, object's position
    """
    # Read all the data from the input_file
    with open(path, 'r') as input:
        input = input.readlines()

        # This extract the radius r1 and r2 from the input file
        r1, r2 = input[0].split(',')
        r1 = int(r1)
        r2 = int(r2)

        # This extract the prices p1 and p2 from the input file
        p1, p2 = input[1].split(',')
        p1 = int(p1)
        p2 = int(p2)

        # This extract the list of art object positions from the input file
        positions_list = []
        for i in range(2, len(input)):
            positions_list.append(eval(input[i]))

        # This finds the limits of a square that includes all the art objects
        x_list = [position[0] for position in positions_list]
        y_list = [position[1] for position in positions_list]

        x_max = max(x_list)
        y_max = max(y_list)

        print("Map of dimension {} x {} with {} art objects".format(
            x_max, y_max, len(x_list)))

    return x_max, y_max, r1, r2, p1, p2, positions_list


def model(input_path='input_'+n+'.txt', grid_unit=1):
    """
    Function which create the model (variables, constraints)
    :param input_path: file's path
    :param grid_unit: grain's grid
    """
    # Take all the data from the input_file, with the read_map function
    x_max, y_max, r1, r2, p1, p2, positions_list = read_map(input_path)

    model = Model('optim')

    # Cadrillage
    c_x_list = [k * grid_unit for k in range(0, ceil(x_max/grid_unit)+1)]
    c_y_list = [k * grid_unit for k in range(0, ceil(y_max/grid_unit)+1)]

    # Variables definition
    # Format : variable_dict={"c_1_14_13" : variable c_1_14_13, "c_2_16_3" : variable c_2_16_3, ... }
    variable_dict = {}
    for u in [1, 2]:
        for i in c_x_list:
            for j in c_y_list:
                variable_dict["c_" + str(u) + "_" + str(i) + "_" + str(j)] = model.addVar(
                    "c_" + str(u) + "_" + str(i) + "_" + str(j), vtype="INTEGER")

    # print(variable_dict)

    # Objective definition
    total_cost = 0
    for var in variable_dict.keys():
        if var[2:3] == "1":
            total_cost += variable_dict[var]*p1
        if var[2:3] == "2":
            total_cost += variable_dict[var]*p2

    model.setObjective(total_cost, "minimize")

    # Constraints definition
    for (i, j) in positions_list:
        cons = 0
        for (x, y) in grid_disk(i, j, r1, grid_unit):
            if (x >= 0) and (y >= 0) and (x <= x_max) and (y <= y_max):
                cons += variable_dict["c_1_"+str(x)+"_"+str(y)]
        for (x, y) in grid_disk(i, j, r2, grid_unit):
            if (x >= 0) and (y >= 0) and (x <= x_max) and (y <= y_max):
                cons += variable_dict["c_2_"+str(x)+"_"+str(y)]
        model.addCons(cons >= 1)

    # Optimization
    model.optimize()

    # Output's file creation
    with open("BASTIDE_ALLAIN_res.txt", 'w') as file:
        for var in model.getVars():
            p = int(model.getVal(var))
            if p == 1:
                temp = str(var).split("_")[
                    1] + "," + str(var).split("_")[2] + "," + str(var).split("_")[3]+"\n"
                file.write(temp)

    print("valeur fonction obj : {} ".format(model.getObjVal()))


def grid_disk(i, j, l, grid_unit=1):
    """
    Provides the list of possible cam positions in a l disk around an art object in i,j
    """
    disk_points = []
    for x in ([i+k*grid_unit for k in range(0, ceil((l/grid_unit)+1))]+[i-k*grid_unit for k in range(1, ceil((l/grid_unit)+1))]):
        for y in ([j + k * grid_unit for k in range(0, ceil((l / grid_unit) + 1))] + [i - k * grid_unit for k in range(1, ceil((l / grid_unit) + 1))]):
            if pow((x-i), 2)+pow((y-j), 2) <= pow(l, 2):
                disk_points.append((x, y))
    return disk_points


print("Run...")
model(grid_unit=1)
