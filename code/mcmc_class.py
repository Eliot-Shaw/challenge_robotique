import random as rd
import math as mt
import numpy as np
import sys
import matplotlib.pyplot as plt
import chemin_base as chem

class Mcmc():

    def __init__(self):
        self.Villes = np.concatenate((np.array([[0, 0, 0]]),self.importerVilles()), axis=0)
        self.m = len(self.Villes)
        self.Villes = np.concatenate((self.Villes, np.array([[i for i in range(self.m)]]).T), axis=1)
        self.matDistance = self.calculMatriceDis()


    def importerVilles(self):
        argc = len(sys.argv)
        if argc < 2:
            print("preciser le nom du fichier de donnees en argument...")
            exit()
        #lecture du fichier
        DataMap = np.loadtxt(sys.argv[1], dtype=float)
        return(DataMap)

    def distancePercue(self, VA, VB):

        lat1 = float(VA[0])
        lat2 = float(VB[0])
        lon1 = float(VA[1])
        lon2 = float(VB[1])

        distance_raw = mt.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)
        distance_valeur = distance_raw/chem.type_cylindre[int(VB[2])-1][0]
        distance_valeur_poids = distance_valeur*chem.type_cylindre[int(VB[2])-1][1]
        return distance_valeur_poids

    def distance(self, VA, VB):

        lat1 = float(VA[0])
        lat2 = float(VB[0])
        lon1 = float(VA[1])
        lon2 = float(VB[1])

        return mt.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)
    

    def calculMatriceDis(self):

        n = len(self.Villes)
        Mat = [ [ None for y in range( n ) ] for x in range( n ) ]
        for i in range(n):
            for j in range(n):
                Mat[i][j] = self.distancePercue(self.Villes[i], self.Villes[j])

        return Mat

    def distanceAvecMat(self, iA, iB, matDis):
        return matDis[int(iA)][int(iB)]


    def longueur(self, Chemin, matDis):
        res = 0
        for i in range(len(Chemin)-1):
            VA = Chemin[i]
            VB = Chemin[i+1]
            res += self.distanceAvecMat(VA[3], VB[3], matDis)
        res += self.distanceAvecMat(Chemin[-1][3], Chemin[0][3], matDis)

        return res

    def longueurReelle(self, Chemin):
        res = 0
        for i in range(len(Chemin)-1):
            VA = Chemin[i]
            VB = Chemin[i+1]
            res += self.distance(VA, VB)
        res += self.distance(Chemin[-1], Chemin[0])

        return res


    def MCMC2(self, N, sigma1, a, b):
        sigma0 = sigma1
        lsigma0 = self.longueur(sigma0, self.matDistance)
        sigma = sigma0.copy()
        T = 100
        for n in range(2,N):
            T = abs(mt.sin(n)/(n**b))*a
            #T *= 0.999
            # T = Tn(n, a, b)
            if T == 0.0:
                print(f"b trop bas{b}")
                break
            iA = rd.randint(1, self.m-1)
            iB = rd.randint(1, self.m-1)
            while iA == iB:
                iB = rd.randint(1, self.m-1)

            sigmaPrime = sigma.copy()
            # temp = np.array(sigmaPrime[iA])
            # sigmaPrime[iA] = sigmaPrime[iB]
            # sigmaPrime[iB] = temp

            sigmaPrime[[iA, iB]] = sigmaPrime[[iB, iA]]


            lsigma = self.longueur(sigma, self.matDistance)
            deltaLong = lsigma - self.longueur(sigmaPrime, self.matDistance)
            if deltaLong >= 0:
                rho = 1
            else:
                rho = mt.exp((deltaLong) / T)


            if rho >= 1:
                sigma = sigmaPrime.copy()
            else:
                U = rd.random()
                if U < rho:
                    sigma = sigmaPrime.copy()

            if lsigma0 > lsigma:
                sigma0 = sigma.copy()
                lsigma0 = lsigma

        return self.longueurReelle(sigma0), sigma0


    def Tn(self, N, a = 100, b = 0.99, h = 1):
        return 2.5 - np.log(np.log(2.71828182846 + N))
        # return a*(b**N)
    
        '''
        k = 1
        n = N % 100000
        a = mt.exp((k - 1) * h)
        b = mt.exp(k * h)
        while not((a < n) and (n <= b)) and k < 300:
            k += 1
            a = mt.exp((k - 1) * h)
            b = mt.exp(k * h)

        if k == 300:
            print("Y a problème")

        return 1/mt.sqrt(k)
        '''

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


def main(map):
    # Villes = importerVilles()
    # print(Villes)
    #lancement(500)
    mcmc = Mcmc()
    sig = chem.faire_chemin(map)
    l, sig0 = mcmc.MCMC2(500000, sig, a=300, b=1.1)
    # afficher(sig0)
    print(f"longueur reelle mcmc (sig0) : {mcmc.longueurReelle(sig0)}") # longueur de mcmc
    print(f"longueur reelle mcmc (chemin_base) : {mcmc.longueurReelle(sig)}") # longueur de chemin_base

    # VRAI CODE
    # Open a file in write mode
    # with open('../divers/resultats.txt', 'w') as f:
    #     # Write the Python code to the file
    #     for i in range(0,20,1):
    #         for j in range(5):
    #                 a = 10
    #                 bz = 0.985+i*0.0001
    #                 l, sig0 = MCMC2(5000, sig, a, bz) #iterations et chemin
    #                 f.write(f'a={a} --- b={bz} --- l={l}\n')

    #FAUX CODE DE TEST
    # with open('../divers/resultats.txt', 'w') as f:
    #     # Write the Python code to the file
    #     a = 10
    #     bz = 0.996
    #     l, sig0 = 1,sig
    #     f.write(f'a={a} --- b={bz} --- l={l}\n')

    # print(sig) # chemin_base
    # print(sig0) # mcmc 

if __name__ == '__main__':
    main()