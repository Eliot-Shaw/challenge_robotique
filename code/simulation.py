import math
import sys
import turtle as t
from time import sleep
import chemin_base

class Robot:
    def __init__(self, base_fuel = 10000, base_masse = 0, base_valeur = 0, base_x = 0.0, base_y = 0.0, base_orientation = 0.0, base_index_instruction = 0, base_speed = 1, base_conso = 100, base_temps_restant = 600):
        # stats
        self.fuel = base_fuel
        self.masse = base_masse
        self.valeur = base_valeur
        self.x = base_x
        self.y = base_y
        self.orientation = base_orientation
        self.index_instruction = base_index_instruction
        self.speed = base_speed # vitesse
        self.conso = base_conso # consommation L au m
        self.temps_restant = base_temps_restant

        # characteristiques
        self.speed_per_kg = 0.00698 # vitesse au km
        self.conso_per_kg = 3 # consommation L au m et au kg
        self.base_speed = base_speed
        self.base_conso = base_conso
    
    def recuperer_cylindre(self, type_cylindre):
        gain = chemin_base.type_cylindre[type_cylindre][0]
        masse = chemin_base.type_cylindre[type_cylindre][1]
        self.valeur += gain
        self.masse += masse
        
        self.speed = self.base_speed * (1-math.exp(-self.speed_per_kg*self.masse))
        self.conso = self.base_conso + self.conso_per_kg*self.masse

    def avancer(self, distance):
        if distance == 0.0:
            print("Distance nulle")
            return
        #consommation
        if self.fuel - distance*self.conso < 0:
            print(f"Manque de fuel ! fuel restant:{self.fuel}")
            return
        #temps
        if self.temps_restant - 1/(self.speed/distance):
            print(f"Manque de temps_restant ! temps restant:{self.temps_restant}")
            return

        self.fuel -= distance*self.conso
        self.temps_restant -= distance/self.speed
        self.x =+ math.cos(self.orientation/(180*math.pi))*distance
        self.y =+ math.sin(self.orientation/(180*math.pi))*distance
        
    def tourner(self, angle):
        self.orientation += angle
        self.orientation %= 360
        
class Cylindre:
    tab_type = [(1.0,1.0),
                (2.0,2.0),
                (3.0,2.0)]
    def __init__(self,  base_x = 0.0, base_y = 0.0, base_valeur = 0, base_poids = 0):
        self.valeur = base_valeur
        self.poids = base_poids
        self.x = base_x = 0.0
        self.y = base_y = 0.0
        
    def changer_type(self, type_cylindre):
        self.valeur = tab_type[type_cylindre-1][0]
        self.poids = tab_type[type_cylindre-1][1]
        
    def changer_valeur(self,new_valeur):
        self.valeur = new_valeur
        
    def changer_poids(self, new_poids):
        self.poids = new_poids
    
    def changer_position(self, new_x, new_y):
        self.x = new_x
        self.y = new_y


class Simu:
    def __init__(self):
        self.robot = Robot()  # Création d'un robot
        self.cylindres = []   # Liste pour les cylindres
    
    def creer_cylindres(self):
        file_path = "../divers/rng_donnees-map.txt"
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()

            for line in lines:
                data = line.strip().split('\t')
                if len(data) == 3:
                    x, y, type_cylindre = data
                    x = float(x)
                    y = float(y)
                    type_cylindre = int(type_cylindre)  # Assumant que le type de cylindre est un entier
                    cylindre = Cylindre(x, y)  # Création d'un cylindre avec des valeurs par défaut
                    cylindre.changer_type(type_cylindre)
                    self.cylindres.append((cylindre))
                else:
                    print("Format de ligne incorrect:", line)
        except FileNotFoundError:
            print("Fichier non trouvé à l'emplacement spécifié.")
            
    def recuperer_cylindre_si_proche(self):
        for cylindre in self.cylindres:
            distance = math.sqrt((cylindre.x - self.robot.x)**2 + (cylindre.y - self.robot.y)**2)
            if distance <= 0.1:
                self.robot.recuperer_cylindre(cylindre)
                self.cylindres.remove(cylindre)
                print("Cylindre récupéré !")
                return


def main():
    pass


if __name__ == '__main__':
    main()

    