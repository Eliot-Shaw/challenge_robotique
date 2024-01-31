from mcmc_class import Mcmc
from robot import Robot
import math
import numpy as np

class MvtRobot(Robot): 
    def __init__(self, init_tutel):
        super.__init__(init_tutel)
        ##caractiéristiques pour mvt robot
        self.theta_robot = 0.0
        self.x_robot = 0.0
        self.y_robot = 0.0
        self.plan = np.empty((1,2)) # ordre, valeur
        self.plan_robot = '../divers/plan_robot.txt'

    def ajout_ordre_plan(self, ordre, valeur):
        self.plan = np.concatenate((self.plan, np.array([[ordre, valeur]])), axis=0)

    def go_point(self, x_point, y_point):
        if distance == 0.0:
            print("Distance nulle")
            return
        #consommation
        if self.fuel - distance*self.conso <= 0:
            print(f"Manque de fuel ! fuel restant : {self.fuel}")
            return
        #temps
        if self.temps_restant - distance/(self.speed) <= 0:
            print(f"Manque de temps_restant ! temps restant : {self.temps_restant}")
            print(f"Temps nécessaire : {distance/(self.speed)}")
            return
        
        self.fuel -= distance*self.conso
        self.temps_restant -= distance/self.speed
        distance = math.sqrt((x_point-self.x_robot)**2+(y_point-self.y_robot)**2)
        self.x_robot, self.y_robot = x_point, y_point
        self.ajout_ordre_plan('GO', distance)

    def tourner_point(self, x_point, y_point):
        angle_point = math.atan2((y_point-self.y_robot),(x_point-self.x_robot))
        print(f"angle point : {angle_point}")
        angle = angle_point - self.theta_robot
        print(f"angle: {angle}")
        self.theta_robot = angle_point
        print(f"theta_robot : {self.theta_robot}")
        angle = angle*180/math.pi
        self.ajout_ordre_plan('TURN', angle) # vérifier si tourne dans le bon sens en fonction du +/-, sinon inverser calcul degré

    def ecrire_plan_txt(self):
        with open(self.plan_robot, 'w') as f:
        # Write the Python code to the file
            for i in range(len(self.plan)):
                if self.plan[i][0] == 'GO':
                    f.write(f'GO {self.plan[i][1]}\n')
                elif self.plan[i][0] == 'TURN':
                    f.write(f'TURN {self.plan[i][1]}\n')
                f.write(f'STOP\n')
            f.write(f'FINISH')
    
    def do_instruction(self, instructions, id):
        instruction = instructions[id]
        if(instruction[:4]) == "TURN":
            self.tutel.left(float(instruction[5:]))
        if(instruction[:2]) == "GO":
            self.tutel.forward(float(instruction[2:])*5)
            self.avancer(float(instruction[2:]))

    def process(self, mcmc_instance):
        ordre = mcmc_instance.process()
        for point in ordre[1:]:
            self.tourner_point(point[0], point[1])
            self.go_point(point[0], point[1])
        self.ecrire_plan_txt()
        self.do_instruction()
    

def main():
    pass
    
if __name__ == '__main__':
    main()