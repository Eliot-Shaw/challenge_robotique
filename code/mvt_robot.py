import mcmc
import math

def go_point(point_x, point_y):
    GO distance(robot, point)
    STOP

def tourner_point(point_x, point_y):
    calcul_degré()
    TURN angle(robot, point) # vérifier si tourne dans le bon sens en fonction du +/-, sinon inverser calcul degré

def calcul_degré(orientation_robot):
    orientation_to_point = *
    return orientation_to_point - orientation_robot



def ecrire_plan(path_plan, directions):
    with open(path_plan, 'w') as f:
    # Write the Python code to the file
        for i in range(len(directions)):
            if directions[0] == 'GO':
                f.write(f'GO {directions[1]}\n')
            elif directions[0] == 'TURN':
                f.write(f'STOP\n')
                f.write(f'TURN {directions[1]}\n')
            elif directions[0] == 'FINISH':
                f.write(f'STOP\n')
                f.write(f'FINISH')
