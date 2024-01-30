import mcmc
import math
import numpy as np

def go_point(x_point, y_point, x_robot, y_robot):
    distance = math.sqrt((x_point-x_robot)**2+(y_point-y_robot)**2)
    ajout_ordre_plan('GO', distance)

def tourner_point(x_point, y_point, x_robot, y_robot):
    angle = math.acos((y_point-y_robot)/math.sqrt((x_point-x_robot)**2+(y_point-y_robot)**2))
    ajout_ordre_plan('TURN', angle) # vérifier si tourne dans le bon sens en fonction du +/-, sinon inverser calcul degré


def ecrire_plan_txt(path_plan, directions):
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

def ajout_ordre_plan(ordre, valeur):
    plan = np.concatenate((plan, np.array([[ordre, valeur]])), axis=0)

def init_plan():
    global plan
    plan = np.array()

def main():
    ordre = mcmc.sig0
    plan_robot = '../divers/plan_robot.txt'
    init_plan()
    for point in ordre:
        tourner_point(point[0], point[1], x_robot, y_robot)
        go_point(point[0], point[1], x_robot, y_robot)
    ecrire_plan_txt(plan_robot, plan)
    