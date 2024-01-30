import mcmc
import math

def go_point(point_x, point_y):
    distance = distance(robot, point)
    ajout_ordre_plan('GO', distance)

def tourner_point(point_x, point_y):
    calcul_degré()
    angle = angle(robot, point) # vérifier si tourne dans le bon sens en fonction du +/-, sinon inverser calcul degré
    ajout_ordre_plan('TURN', angle)

def calcul_degré(orientation_robot):
    orientation_to_point = *
    return orientation_to_point - orientation_robot



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
