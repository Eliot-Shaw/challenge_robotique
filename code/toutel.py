import turtle as t
import numpy as np
import sys
from time import sleep

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
        sleep(1)
        if(instruction[:4]) == "TURN":
            tutel.left(float(instruction[5:]) / np.pi * 180)
            
        
        if(instruction[:2]) == "GO":
            tutel.forward(float(instruction[3:]))

    t.mainloop()


if __name__ == '__main__':
    main()

    