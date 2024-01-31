import mcmc
import math
import numpy as np


theta_robot = 0.0

def go_point(x_point, y_point, x_robot, y_robot):
    distance = math.sqrt((x_point-x_robot)**2+(y_point-y_robot)**2)
    x_robot, y_robot = x_point, y_point
    ajout_ordre_plan('GO', distance)

def tourner_point(x_point, y_point, x_robot, y_robot):
    global theta_robot
    angle_point = math.atan2((y_point-y_robot),(x_point-x_robot))
    print(f"angle point : {angle_point}")
    angle = angle_point - theta_robot
    print(f"angle: {angle}")
    theta_robot = angle_point
    print(f"theta_robot : {theta_robot}")
    angle = angle*180/math.pi
    ajout_ordre_plan('TURN', angle) # vérifier si tourne dans le bon sens en fonction du +/-, sinon inverser calcul degré

def ecrire_plan_txt(path_plan, directions):
    with open(path_plan, 'w') as f:
    # Write the Python code to the file
        for i in range(len(directions)):
            if directions[i][0] == 'GO':
                f.write(f'GO {directions[i][1]}\n')
            elif directions[i][0] == 'TURN':
                f.write(f'TURN {directions[i][1]}\n')
            f.write(f'STOP\n')
        f.write(f'FINISH')
            
def ajout_ordre_plan(ordre, valeur):
    global plan
    plan = np.concatenate((plan, np.array([[ordre, valeur]])), axis=0)

def init_plan():
    global plan
    plan = np.empty((1,2)) # ordre, valeur

def main():
    x_robot = 0.0
    y_robot = 0.0
    ordre = mcmc.sig0
    plan_robot = '../divers/plan_robot.txt'
    init_plan()
    print(plan)
    for point in ordre[1:]:
        tourner_point(point[0], point[1], x_robot, y_robot)
        go_point(point[0], point[1], x_robot, y_robot)
    ecrire_plan_txt(plan_robot, plan)
    mcmc.afficher()
    
if __name__ == '__main__':
    main()