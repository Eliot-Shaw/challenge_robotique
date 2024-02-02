from robot import Robot
import math
import numpy as np
import sys
from time import sleep

class MvtRobot(Robot): 
    def __init__(self):
        super().__init__()
        ##caractiéristiques pour mvt robot
        self.theta_robot = 0.0
        self.x_robot = 0.0
        self.y_robot = 0.0
        self.plan = np.empty((1,2)) # ordre, valeur
        self.plan_robot = 'C:\challenge\script.txt'
    
    def reinitialisation(self):
        self.__init__()

    def ajout_ordre_plan(self, ordre, valeur):
        self.plan = np.concatenate((self.plan, np.array([[ordre, valeur]])), axis=0)

    def go_point(self, x_point, y_point):
        distance = math.sqrt((x_point-self.x_robot)**2+(y_point-self.y_robot)**2)
        if distance == 0.0:
            print("Distance nulle")
            return True
        #consommation
        if self.fuel - distance*self.conso <= 0:
            print(f"Manque de fuel ! fuel restant : {self.fuel}")
            return False
        #temps
        if self.temps_restant - distance/(self.speed) <= 0:
            print(f"Manque de temps_restant ! temps restant : {self.temps_restant}")
            print(f"Temps nécessaire : {distance/(self.speed)}")
            return False
        
        self.fuel -= distance*self.conso
        self.temps_restant -= distance/self.speed
        self.x_robot, self.y_robot = x_point, y_point
        self.ajout_ordre_plan('GO', distance)
        return True

    def tourner_point(self, x_point, y_point):
        angle_point = math.atan2((y_point-self.y_robot),(x_point-self.x_robot))
        angle = angle_point - self.theta_robot
        self.theta_robot = angle_point
        angle = angle*180/math.pi
        self.ajout_ordre_plan('TURN', angle) # vérifier si tourne dans le bon sens en fonction du +/-, sinon inverser calcul degré

    def ecrire_plan_txt(self):
        with open(self.plan_robot, 'w') as f:
        # Write the Python code to the file
            for i in range(len(self.plan)):
                self.plan[i][1] = f"{round(float(self.plan[i][1]))}"
                if self.plan[i][0] == 'GO':
                    f.write(f'GO {self.plan[i][1]}\n')
                elif self.plan[i][0] == 'TURN':
                    f.write(f'TURN {self.plan[i][1]}\n')
            f.write(f'STOP\n')
            f.write(f'FINISH')

    def recup_data_action(self):
        DataMap = open(self.plan_robot, 'r')
        return DataMap.readlines()
    
    # def do_instruction(self, instruction):
    #     if(instruction[:4]) == "TURN":
    #         self.tutel.left(float(instruction[5:]))
    #     if(instruction[:2]) == "GO":
    #         self.tutel.forward(float(instruction[2:])*5)

    def process(self, mcmc_instance):
        ordre = mcmc_instance.process()
        for point in ordre[1:]:
            self.tourner_point(point[0], point[1])
            self.go_point(point[0], point[1])
        self.ecrire_plan_txt()
        
        sleep(0.001)
        instructions_robot = self.recup_data_action()
        return ordre, instructions_robot, self.fuel, self.temps_restant
    

    def faisable(self, ordre):
        i = True
        for point in ordre[1:]:
            self.tourner_point(point[0], point[1])
            i = i and self.go_point(point[0], point[1])
            if not i: break
        return i
    
def ecrire_plan_txt(unplan, unpath):
        with open(unpath, 'w') as f:
        # Write the Python code to the file
            for i in range(len(unplan)):
                unplan[i][1] = f"{round(float(unplan[i][1]))}"
                if unplan[i][0] == 'GO':
                    f.write(f'GO {unplan[i][1]}\n')
                elif unplan[i][0] == 'TURN':
                    f.write(f'TURN {unplan[i][1]}\n')
            f.write(f'STOP\n')
            f.write(f'FINISH')

def main():
    pass
    
if __name__ == '__main__':
    main()