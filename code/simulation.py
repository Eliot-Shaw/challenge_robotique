import math, random
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
        
    def get_action_list():
        argc = len(sys.argv)
        if argc < 2:
            print("preciser le nom du fichier de donnees en argument...")
            exit()
        #lecture du fichier
        DataMap = open(sys.argv[1], 'r')
        return DataMap.readlines()
    
    def do_next_action(instructions)
        for instruction in instructions:
        sleep(0.01)
        if(instruction[:4]) == "TURN":
            tutel.left(float(instruction[5:]))
            
        if(instruction[:2]) == "GO":
            tutel.forward(float(instruction[2:])*5)
    

    #TODO
    #fction action suivante pour robot
        
class Cylindre:
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


class Simu:
    def __init__(self):
        self.robot = Robot()  # Création d'un robot
        self.cylindres = []   # Liste pour les cylindres
        self.path_map = "../divers/rng_donnees-map.txt"
    
    def creer_cylindres(self):
        with open(self.path_map, 'r') as file:
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
    
    def ecrire_map(self):
        with open(self.path_map, 'w') as f:
        # Write the Python code to the file
            for i in range(20):
                f.write(f'{random.random()*25}\t{random.random()*25}\t{float(random.randint(1,3))}\n')
            
    def recuperer_cylindre_si_proche(self):
        for cylindre in self.cylindres:
            distance = math.sqrt((cylindre.x - self.robot.x)**2 + (cylindre.y - self.robot.y)**2)
            if distance <= 1:
                self.robot.recuperer_cylindre(cylindre)
                self.cylindres.remove(cylindre)
                print("Cylindre récupéré !")
                return
            
    def afficher(sig0):
        fig = plt.figure(1)

        tColorTab = {1:'yellow', 2:'orange', 3:'red'}
        dbRayon = 0.85

        DataMap = np.loadtxt(sys.argv[1], dtype=float)
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
    simulation = Simu()
    simulation.ecrire_map()
    simulation.creer_cylindres()
    simulation.afficher_map()
    simulation.robot.get_action_list()
    simulation.robot.do_next_action()


if __name__ == '__main__':
    main()

    