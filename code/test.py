import math

def calculer_angle(x1, y1, x2, y2):
    # Calcul de la différence en y et en x
    dy = y2 - y1
    dx = x2 - x1
    
    # Calcul de l'angle en radians en utilisant la fonction arctan2
    angle_rad = math.atan2(dy, dx)
    
    # Conversion de l'angle en degrés
    angle_deg = math.degrees(angle_rad)
    
    # Assurer que l'angle est dans la plage [0, 360)
    angle_deg = angle_deg % 360
    
    return angle_deg

# Exemple d'utilisation :
x1, y1 = 0, 0
x2, y2 = 3, 4
angle = calculer_angle(x1, y1, x2, y2)
print("L'angle par rapport à l'horizontale est:", angle, "degrés")
