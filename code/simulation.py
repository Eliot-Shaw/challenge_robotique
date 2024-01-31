import math, random
import turtle
from time import sleep
import matplotlib.pyplot as plt
import numpy as np
import chemin_base
from mcmc_class import Mcmc
from mvt_robot import MvtRobot

class Robot_Deprecated():
    def __init__(self, init_tutel, base_fuel = 10000, base_masse = 0, base_valeur = 0, base_x = 0.0, base_y = 0.0, base_orientation = 0.0, base_index_instruction = 0, base_speed = 1, base_conso = 100, base_temps_restant = 600):
        self.tutel = init_tutel 
        # stats
        self.fuel = base_fuel
        self.masse = base_masse
        self.valeur = base_valeur
        self.x = base_x
        self.y = base_y
        self.orientation = base_orientation
        self.speed = base_speed # vitesse
        self.conso = base_conso # consommation L au m
        self.temps_restant = base_temps_restant

        # characteristiques
        self.speed_per_km = 0.00698 # vitesse au km
        self.conso_per_kg = 3 # consommation L au m et au kg
        self.base_speed = base_speed
        self.base_conso = base_conso

    def recuperer_cylindre(self, un_cylindre):
        gain = un_cylindre.valeur
        masse = un_cylindre.poids
        self.valeur += gain
        self.masse += masse
        
        self.speed = self.base_speed * (1-math.exp(-self.speed_per_km*self.masse))
        self.conso = self.base_conso + self.conso_per_kg*self.masse

    def avancer(self, distance):
        if distance == 0.0:
            print("Distance nulle")
            return
        #consommation
        if self.fuel - distance*self.conso <= 0:
            print(f"Manque de fuel ! fuel restant:{self.fuel}")
            return
        #temps
        if self.temps_restant - distance/(self.speed) <= 0:
            print(f"Manque de temps_restant ! temps restant:{self.temps_restant}")
            print(f"Claclou vetu:{distance/(self.speed)}")
            return

        self.fuel -= distance*self.conso
        self.temps_restant -= distance/self.speed
        self.x =+ math.cos(self.orientation/(180*math.pi))*distance
        self.y =+ math.sin(self.orientation/(180*math.pi))*distance
        
    def tourner(self, angle):
        self.orientation += angle
        self.orientation %= 360
    
    def do_instruction(self, instructions, id):
        instruction = instructions[id]
        if(instruction[:4]) == "TURN":
            self.tutel.left(float(instruction[5:]))
        if(instruction[:2]) == "GO":
            self.tutel.forward(float(instruction[2:])*5)
            self.avancer(float(instruction[2:]))
        
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
            print("creer cylindres done")
    
    # Creation d'une map random, return un np.array de la ditre map
    def ecrire_map(self):
        with open(self.path_map, 'w') as f:
        # Write the Python code to the file
            for i in range(20):
                f.write(f'{random.random()*25}\t{random.random()*25}\t{float(random.randint(1,3))}\n')
        #lecture du fichier
        DataMap = np.loadtxt(self.path_map, skiprows=0, dtype=float)
        print("ecrire map random done")
        return DataMap
            
    def recuperer_cylindre_si_proche(self):
        for i in range(len(self.cylindres)):
            distance = math.sqrt((self.cylindres[i].x - self.robot.x)**2 + (self.cylindres[i].y - self.robot.y)**2)
            if distance <= 1:
                self.robot.recuperer_cylindre(self.cylindres[i])
                self.cylindres.remove(self.cylindres[i])
                print("Cylindre récupéré !")
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
    sig0 = robot.process(mcmc)
    
    simulation.get_action_list()
    for i in range(len(sig0)): #ERREUR path action txt string
        print(f"ceci est for n°{i}")
        simulation.robot.do_instruction(i)
        simulation.recuperer_cylindre_si_proche()
    simulation.afficher(sig0)


if __name__ == '__main__':
    main()

    