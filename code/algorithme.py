import sys
import numpy as np
import mcmc_class
import mvt_robot
from chemin_fin import faire_chemin

def importerMap():
    argc = len(sys.argv)
    if argc < 2:
        print("preciser le nom du fichier de donnees en argument...")
        exit()
    #lecture du fichier
    DataMap = np.loadtxt(sys.argv[1], dtype=float)
    return(DataMap)

def Soustraire(lst_cylindres, cylindres_total):

    cylindres = cylindres_total.copy()

    premier_cylindre = lst_cylindres[-1]

    
    
    cylindres = np.delete(cylindres, ((lst_cylindres.T[-1]).astype(int)), axis = 0)

    cylindres = np.concatenate((np.array([premier_cylindre]),cylindres), axis = 0)

    return cylindres


def main():

    map = importerMap()
    map = np.concatenate((np.array([[0, 0, 0]]),map), axis=0)
    nb_cylindre = len(map)
    map = np.concatenate((map, np.array([[i for i in range(nb_cylindre)]]).T), axis=1)


    min = 2
    max = nb_cylindre
    milieu = (min + max)// 2
    macmac = mcmc_class.Mcmc()
    mvt_bot = mvt_robot.MvtRobot()
    meilleur_chemin = macmac.process(milieu)

    chemin_varaiable = meilleur_chemin.copy()
    while min < max-1:
        print(f"dichotomie entre {min} et {max} avec mid : {milieu}")
        mvt_bot.reinitialisation()
        if not mvt_bot.faisable(chemin_varaiable):
            max = milieu
            milieu = (min + max) // 2

            chemin_varaiable = macmac.process(milieu)
        else:
            min = milieu
            milieu = (min + max) // 2
            meilleur_chemin = chemin_varaiable.copy()
            chemin_varaiable = macmac.process(milieu)
    

    mcmc_class.afficher(meilleur_chemin)
    # cheum = Soustraire(meilleur_chemin, map)
    # chemin_final = faire_chemin(cheum,3)
    # mcmc_class.afficher(chemin_final)
    # print(meilleur_chemin[-1])
    # print(cheum[0])


    return meilleur_chemin
    

if __name__ == "__main__":
    main()