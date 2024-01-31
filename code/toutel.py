import turtle as t
import numpy as np
import sys
from time import sleep
import chemin_base
import math

class Tutel:
    def __init__(self, base_fuel = 10000, base_masse = 0, base_valeur = 0, base_x = 0.0, base_y = 0.0, base_orientation = 0.0, base_index_instruction = 0, base_speed = 1, base_conso = 100):
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
        orientation_rad = self.orientation/(180*math.pi)
        self.x =+ math.cos(orientation_rad)*distance
        self.y =+ math.sin(orientation_rad)*distance
        
    def tourner(self, angle):
        self.orientation += angle
        self.orientation %= 360
        
    def calculer_angle(self, x2, y2):
        dy = y2 - self.y
        dx = x2 - self.x
        
        angle_rad = math.atan2(dy, dx)
        return (math.degrees(angle_rad)% 360)
        
        


class Cylindre:
    def __init__(self, base_valeur, base_poids, base_x = 0.0, base_y = 0.0):
        self.valeur = base_valeur
        self.poids = base_poids
        self.x = base_x = 0.0
        self.y = base_y = 0.0
        
    def changer_valeur(self,new_valeur):
        self.valeur = new_valeur
        
    def changer_poids(self, new_poids):
        self.poids = new_poids
    
    def changer_position(self, new_x, new_y):
        self.x = new_x
        self.y = new_y
    

def recup_data_map():
    argc = len(sys.argv)
    if argc < 2:
        print("preciser le nom du fichier de donnees en argument...")
        exit()
    #lecture du fichier
    DataMap = open(sys.argv[1], 'r')
    return DataMap.readlines()


def main():
    tutel = t.Turtle()
    tutel.pd()
    tutel.home()
    instructions = recup_data_map()

    for instruction in instructions:
        sleep(0.01)
        if(instruction[:4]) == "TURN":
            tutel.left(float(instruction[5:]))
            
        
        if(instruction[:2]) == "GO":
            tutel.forward(float(instruction[2:])*5)

    t.mainloop()


if __name__ == '__main__':
    main()

    