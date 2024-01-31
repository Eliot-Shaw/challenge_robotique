import math
import numpy as np
import random

def ecrire_plan_txt(path_plan):
    with open(path_plan, 'w') as f:
    # Write the Python code to the file
        for i in range(20):
            f.write(f'{random.random()*25}\t{random.random()*25}\t{float(random.randint(1,3))}\n')

def main():
    ecrire_plan_txt('../divers/rng_donnees-map.txt')
    
if __name__ == '__main__':
    main()