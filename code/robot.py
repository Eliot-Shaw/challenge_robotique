import math

class Robot():
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