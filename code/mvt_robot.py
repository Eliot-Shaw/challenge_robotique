import mcmc
import math

def go_point(point_x, point_y):
    GO distance(robot, point)
    STOP

def tourner_point(y_point, y_robot, x_point, x_robot):
    angle = math.acos((y_point-y_robot)/math.sqrt((x_point-x_robot)**2+(y_point-y_robot)**2))
    TURN angle # vérifier si tourne dans le bon sens en fonction du +/-, sinon inverser calcul degré



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
