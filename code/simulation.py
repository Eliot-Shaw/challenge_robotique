import math, random
import turtle
from time import sleep
import matplotlib.pyplot as plt
import numpy as np
import chemin_base
from mcmc_class import Mcmc
from mvt_robot import MvtRobot
        
class Cylindre():
    def __init__(self,  base_x = 0.0, base_y = 0.0, base_valeur = 0, base_poids = 0):
        self.valeur = base_valeur
        self.poids = base_poids
        self.x = base_x = 0.0
        self.y = base_y = 0.0
        self.tab_type = [(1.0,1.0),(2.0,2.0),(3.0,2.0)]
        
    def changer_type(self, type_cylindre):
        self.valeur = self.tab_type[type_cylindre-1][0]
        self.poids = self.tab_type[type_cylindre-1][1]
        
    def changer_valeur(self,new_valeur):
        self.valeur = new_valeur
        
    def changer_poids(self, new_poids):
        self.poids = new_poids
    
    def changer_position(self, new_x, new_y):
        self.x = new_x
        self.y = new_y


class Simu():
    def __init__(self, robot_init):
        self.robot = robot_init
        self.cylindres = []   # Liste pour les cylindres
        self.path_actions = "../divers/plan_robot.txt"
        self.path_map = "../divers/rng_donnees-map.txt"
        self.action_list = self.get_action_list()
    
    def creer_cylindres(self, la_map):
        for i in range(len(la_map)):
            x, y, type_cylindre = la_map[i][0], la_map[i][1], la_map[i][2]
            x = float(x)
            y = float(y)
            type_cylindre = int(float(type_cylindre))  # Assumant que le type de cylindre est un entier
            cylindre = Cylindre(x, y)  # Création d'un cylindre avec des valeurs par défaut
            cylindre.changer_type(type_cylindre)
            self.cylindres.append((cylindre))
    
    # Creation d'une map random, return un np.array de la ditre map
    def ecrire_map(self):
        with open(self.path_map, 'w') as f:
        # Write the Python code to the file
            for i in range(20):
                f.write(f'{random.random()*25}\t{random.random()*25}\t{float(random.randint(1,3))}\n')
        #lecture du fichier
        DataMap = np.loadtxt(self.path_map, skiprows=0, dtype=float)
        return DataMap
            
    def recuperer_cylindre_si_proche(self):
        for i in range(len(self.cylindres)):
            distance = math.sqrt((self.cylindres[i].x - self.robot.x)**2 + (self.cylindres[i].y - self.robot.y)**2)
            if distance <= 1:
                self.robot.recuperer_cylindre(self.cylindres[i])
                self.cylindres.remove(self.cylindres[i])
                return

    def get_action_list(self):
        #lecture du fichier
        DataMap = open(self.path_actions, 'r')
        return DataMap.readlines()
            
    def afficher(self, sig0):
        fig = plt.figure(1)

        tColorTab = {1:'yellow', 2:'orange', 3:'red'}
        dbRayon = 0.85

        DataMap = np.loadtxt(self.path_map, dtype=float)
        #affichage des donnees de la carte
        x=DataMap[:,0]
        y=DataMap[:,1]
        t=DataMap[:,2]
        n = len(x)
        fig = plt.figure(1)
        ax = fig.gca()
        for i in range(n):
            plt.plot(x[i],y[i],marker='+',color=tColorTab[int(t[i])])
            c1 = plt.Circle((x[i],y[i]), dbRayon,color=tColorTab[int(t[i])] )
            ax.add_patch(c1)

        plt.plot(sig0.T[0], sig0.T[1])
        plt.plot(np.array([sig0.T[0][-1], sig0.T[0][0]]),np.array([sig0.T[1][-1], sig0.T[1][0]]))
        plt.show()

def main():
    tutel = turtle.Turtle()  # Création d'un robot
    robot = MvtRobot(tutel)  # Création d'un robot
    simulation = Simu(robot) # Création d'une simu

    la_map = simulation.ecrire_map() # Creation d'une map random de cylindres, return un np.array
    simulation.creer_cylindres(la_map) # Ajout des objets cylindres dans la simu
    
    mcmc = Mcmc()
    sig0, instructions_robot = robot.process(mcmc)
    
    simulation.get_action_list()
    for instruction in instructions_robot: #ERREUR path action txt string
        simulation.robot.do_instruction(instruction)
        simulation.recuperer_cylindre_si_proche()
    simulation.afficher(sig0)


if __name__ == '__main__':
    main()

    