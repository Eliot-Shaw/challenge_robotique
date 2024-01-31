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


class Simu:
    def __init__(self):
        self.robot = Robot()  # Création d'un robot
        self.cylindres = []   # Liste pour les cylindres
    
    def creer_cylindres(self, nombre):
        for _ in range(nombre):
            valeur = random.randint(1, 100)  # Valeur aléatoire entre 1 et 100
            poids = random.randint(1, 10)     # Poids aléatoire entre 1 et 10
            x = random.uniform(-10, 10)       # Position x aléatoire
            y = random.uniform(-10, 10)       # Position y aléatoire
            cylindre = Cylindre(valeur, poids, x, y)  # Création d'un cylindre
            self.cylindres.append(cylindre)   # Ajout du cylindre à la liste
            
    def recuperer_cylindre_si_proche(self):
        for cylindre in self.cylindres:
            distance = math.sqrt((cylindre.x - self.robot.x)**2 + (cylindre.y - self.robot.y)**2)
            if distance <= 0.1:
                self.robot.recuperer_cylindre(cylindre)
                self.cylindres.remove(cylindre)
                print("Cylindre récupéré !")
                return

# Exemple d'utilisation
simulation = Simu()
simulation.creer_cylindres(5)  # Création de 5 cylindres

# Simulation du déplacement du robot
simulation.robot.x = 0.05
simulation.robot.y = 0.05
simulation.recuperer_cylindre_si_proche()


        
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

    