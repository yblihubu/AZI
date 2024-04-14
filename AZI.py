from gurobipy import *


def Objective(Number):
    for i in range(Number):
        f.write("P_" + str(i + 1) + " + ")
    for i in range(Number - 1):
        f.write("W_" + str(i + 1) + " + ")
    f.write("W_" + str(Number) + "\n")


def Constraints(Number, n_value):
    f.write("n = " + str(n_value) + "\n")
    for i in range(Number - 1):
        f.write("A_" + str(i + 1) + " - " + "[ x_" + str(i + 1) + " * " + "x_" + str((i + 2)) + " ] = 0\n")
    f.write("A_" + str(Number) + " - " + "[ x_" + str(Number) + " * " + "x_" + str(1) + " ] = 0\n")

    for i in range(Number - 1):
        f.write("B_" + str(i + 1) + " - " + "x_" + str(i + 1) + " - " + "x_" + str((i + 2)) + " = -2\n")
    f.write("B_" + str(Number) + " - " + "x_" + str(Number) + " - " + "x_" + str(1) + " = -2\n")

    for i in range(Number):
        f.write("A_" + str(i + 1) + " - " + "[ B_" + str(i + 1) + " * " + "C_" + str(i + 1) + " ] = 0\n")

    for i in range(Number):
        f.write("Q_" + str(i + 1) + " - [ C_" + str(i + 1) + " * " + "C_" + str(i + 1) + " ] = 0\n")

    for i in range(Number):
        f.write("W_" + str(i + 1) + " - [ Q_" + str(i + 1) + " * " + "C_" + str(i + 1) + " ] = 0\n")

    for i in range(Number):
        f.write("D_" + str(i + 1) + " - " + "x_" + str(i + 1) + " = -1\n")

    for i in range(Number):
        f.write("x_" + str(i + 1) + " - " + "[ D_" + str(i + 1) + " * " + "E_" + str(i + 1) + " ] = 0\n")

    for i in range(Number):
        f.write("K_" + str(i + 1) + " - [ E_" + str(i + 1) + " * " + "E_" + str(i + 1) + " ] = 0\n")

    for i in range(Number):
        f.write("V_" + str(i + 1) + " - [ K_" + str(i + 1) + " * " + "E_" + str(i + 1) + " ] = 0\n")

    for i in range(Number):
        f.write("H_" + str(i + 1) + " - " + "x_" + str(i + 1) + " = -2\n")

    for i in range(Number):
        f.write("P_" + str(i + 1) + " - [ V_" + str(i + 1) + " * " + "H_" + str(i + 1) + " ] = 0\n")

    for i in range(Number-1):
        f.write("x_" + str(i + 1) + " + ")
    f.write("x_" + str(Number))
    f.write(" - n = " + str(Number) + "\n")

    for i in range(1, Number):
        f.write("x_" + str(i + 1) + " - n <= " + str(2 - Number) + "\n")
        f.write("x_" + str(i + 1) + " >= 2\n")
    for i in range(1):
        f.write("x_" + str(i + 1) + " - n <= " + str(2 - Number) + "\n")
        f.write("x_" + str(i + 1) + " >= 37\n")


def Bounds():
    for i in range(Number):
        f.write("x_" + str(i + 1) + " <= 500\n")


def Varibles(Number):
    for i in range(Number):
        f.write("x_" + str(i + 1) + "\n")


def check_conditions(lst, n):
    def check_n_equal(lst, n):
        for i in range(len(lst)):
            if all(lst[i] == lst[(i + j) % len(lst)] for j in range(n)):
                return i
        return -1

    start_index = check_n_equal(lst, n)

    if start_index == -1:
        return False


    remaining_indices = set(range(len(lst))) - set((start_index + i) % len(lst) for i in range(n))
    if len(remaining_indices) != len(lst) - n:
        return False
    remaining_values = [lst[j] for j in remaining_indices]


    if len(remaining_values) != 2:
        return False


    condition2 = abs(remaining_values[0] - remaining_values[1]) <= 1
    if not condition2:
        return False


    remaining_indices = list(remaining_indices)
    condition3 = remaining_indices[0] == (remaining_indices[1] - 1) % len(lst) or \
                 remaining_indices[0] == (remaining_indices[1] + 1) % len(lst)

    return condition3


def Judgment(result_file):  # Determine whether the symbol does not match the pole diagram
    file2 = open(result_file, "r")
    my_dict = {}
    count = 0
    for line in file2:
        if count == 0:
            count += 1
            continue
        else:
            line = line.strip()
            key, value = line.split()
            if key[0] == "x":
                my_dict[key] = round(float(value))
    file2.close()
    list_result = []
    for value in my_dict.values():
        list_result.append(value)

    flag = check_conditions(list_result, Number-2)
    return list_result, flag


def main(Number, n_value):
    f.write("MAXIMIZE\n")
    Objective(Number)
    f.write("SUBJECT TO\n")
    Constraints(Number, n_value)
    f.write("INTEGER\n")
    Varibles(Number)
    f.write("END\n")
    f.close()
    m = read(file_name)
    m.optimize()
    m.write("output.sol")
    result_file = "output.sol"
    list_x, flag2 = Judgment(result_file)
    if flag2:
        return str(list_x) + ": Yes"
    else:
        return str(list_x) + ": No"


if __name__ == "__main__":
    Number = 50 #the result of g
    file_name = "AZI.lp"
    file_name2 = "result.txt"
    f2 = open(file_name2, "a")
    final_result = []
    for item in range(1000, 1001): #the result of n
        print("---------------------" + str(item) + "---------------------")
        f = open(file_name, "w")
        temp_list = main(Number, item)
        f2.write(str(item) + " : " + str(temp_list) + "\n")
        final_result.append(temp_list)
    f.close()
    f2.close()
    print(final_result)
