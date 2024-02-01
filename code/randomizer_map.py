import random
import math

def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def distance_minimale(x, y, points, seuil):
    for point in points:
        if distance(x, y, point[0], point[1]) < seuil:
            return False
    return True

def ecrire_plan_txt(path_plan):
    with open(path_plan, 'w') as f:
        points = []
        for i in range(20):
            new_x = random.random() * 25
            new_y = random.random() * 25
            
            # Vérifie si la distance minimale est respectée par rapport à tous les points précédents
            while not distance_minimale(new_x, new_y, points, 0.85*2):
                new_x = random.random() * 25
                new_y = random.random() * 25
            f.write(f'{new_x}\t{new_y}\t{float(random.randint(1,3))}\n')
            points.append((new_x, new_y))
            
def main():
    ecrire_plan_txt('../divers/rng_donnees-map.txt')
    
if __name__ == '__main__':
    main()