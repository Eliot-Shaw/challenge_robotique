import random as rd
import math as mt
import numpy as np
import sys
import matplotlib.pyplot as plt
import chemin_base as chem

def importerVilles():
    argc = len(sys.argv)
    if argc < 2:
        print("preciser le nom du fichier de donnees en argument...")
        exit()
    #lecture du fichier
    DataMap = np.loadtxt(sys.argv[1], dtype=float)
    return(DataMap)

def distancePercue(VA, VB):

    # iA = 0
    # iB = 0
    # for i in range(len(lstV)):
    #     if np.array_equal(lstV[i],VA):
    #         iA = i
    #     elif np.array_equal(lstV[i],VB):
    #         iB = i
    

    # lat1 = float(lstV[iA][0])
    # lat2 = float(lstV[iB][0])
    # lon1 = float(lstV[iA][1])
    # lon2 = float(lstV[iB][1])


    lat1 = float(VA[0])
    lat2 = float(VB[0])
    lon1 = float(VA[1])
    lon2 = float(VB[1])

    distance_raw = mt.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)
    distance_valeur = distance_raw/(chem.type_cylindre[int(VB[2])-1][0] * 1.25)
    distance_valeur_poids = distance_valeur*chem.type_cylindre[int(VB[2])-1][1]
    return distance_valeur_poids

def distance(VA, VB):

    # iA = 0
    # iB = 0
    # for i in range(len(lstV)):
    #     if np.array_equal(lstV[i],VA):
    #         iA = i
    #     elif np.array_equal(lstV[i],VB):
    #         iB = i
    

    # lat1 = float(lstV[iA][0])
    # lat2 = float(lstV[iB][0])
    # lon1 = float(lstV[iA][1])
    # lon2 = float(lstV[iB][1])


    lat1 = float(VA[0])
    lat2 = float(VB[0])
    lon1 = float(VA[1])
    lon2 = float(VB[1])

    return mt.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)
    

def calculMatriceDis(lstV):

    n = len(lstV)

    Mat = [ [ None for y in range( n ) ] for x in range( n ) ]
    for i in range(n):
        for j in range(n):
            Mat[i][j] = distancePercue(lstV[i], lstV[j])

    return Mat

def distanceAvecMat(iA, iB, matDis):
    # iA = 0
    # iB = 0
    # for i in range(len(lstV)):
    #     if np.array_equal(lstV[i],VA):
    #         iA = i
    #     elif np.array_equal(lstV[i],VB):
    #         iB = i
    return matDis[int(iA)][int(iB)]


def longueur(Chemin, matDis):
    res = 0
    for i in range(len(Chemin)-1):
        VA = Chemin[i]
        VB = Chemin[i+1]
        res += distanceAvecMat(VA[3], VB[3], matDis)


    # res += distanceAvecMat(Chemin[-1][3], Chemin[0][3], matDis)

    return res

def longueurReelle(Chemin):
    res = 0
    for i in range(len(Chemin)-1):
        VA = Chemin[i]
        VB = Chemin[i+1]
        res += distance(VA, VB)


    # res += distance(Chemin[-1], Chemin[0])

    return res

def MCMC(N):
    Villes = np.concatenate((np.array([[0, 0, 0]]),importerVilles()), axis=0)
    m = len(Villes)
    matDistance = calculMatriceDis(Villes)
    sigma0 = np.array([Villes[i] for i in range(m)])
    lsigma0 = longueur(sigma0, Villes, matDistance)
    sigma = sigma0.copy()
    T = 100
    
    for n in range(2,N):
        #T = abs(mt.sin(n)/(n**1.1))*300
        #T *= 0.999
        T = Tn(n)

        iA = rd.randint(0, m-1)
        iB = rd.randint(0, m-1)
        while iA == iB:
            iB = rd.randint(0, m-1)

        sigmaPrime = sigma.copy()
        # temp = sigmaPrime[iA]
        # sigmaPrime[iA] = sigmaPrime[iB]
        # sigmaPrime[iB] = temp

       
        sigmaPrime[[iA, iB]] = sigmaPrime[[iB, iA]]

        lsigma = longueur(sigma, Villes, matDistance)
        deltaLong = lsigma - longueur(sigmaPrime, Villes, matDistance)
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
            
    return longueurReelle(sigma0), sigma0


def MCMC2(N, sigma1, a, b):
    Villes = np.concatenate((np.array([[0, 0, 0]]),importerVilles()), axis=0)
    m = len(Villes)
    Villes = np.concatenate((Villes, np.array([[i for i in range(m)]]).T), axis=1)
    matDistance = calculMatriceDis(Villes)
    sigma0 = sigma1
    lsigma0 = longueur(sigma0, matDistance)
    sigma = sigma0.copy()
    T = 100
    for n in range(2,N):
        # T = abs(mt.sin(n)/(n**b))*a
        #T *= 0.999
        # T = Tn(n, a, b)
        T = Tn(n)
        if T == 0.0:
            print(f"b trop bas{b}")
            break
        iA = rd.randint(1, m-1)
        iB = rd.randint(1, m-1)
        while iA == iB:
            iB = rd.randint(1, m-1)

        sigmaPrime = sigma.copy()
        # temp = np.array(sigmaPrime[iA])
        # sigmaPrime[iA] = sigmaPrime[iB]
        # sigmaPrime[iB] = temp

        sigmaPrime[[iA, iB]] = sigmaPrime[[iB, iA]]


        lsigma = longueur(sigma, matDistance)
        deltaLong = lsigma - longueur(sigmaPrime, matDistance)
        if deltaLong >= 0:
            rho = 1
        else:
            try:
                rho =  mt.exp((deltaLong) / T)
            except Exception:
                print(T)
                exit()
            # rho =  mt.exp((deltaLong) / T)
        

        if rho >= 1:
            sigma = sigmaPrime.copy()
        else:
            U = rd.random()
            if U < rho:
                sigma = sigmaPrime.copy()

        if lsigma0 > lsigma:
            sigma0 = sigma.copy()
            lsigma0 = lsigma

    return longueurReelle(sigma0), sigma0


def MCMC3(N, a, b, lim_cylindre = 5):
    Villes = np.concatenate((np.array([[0, 0, 0]]),importerVilles()), axis=0)
    m = len(Villes)
    Villes = np.concatenate((Villes, np.array([[i for i in range(m)]]).T), axis=1)
    matDistance = calculMatriceDis(Villes)
    sigma0 = np.array([Villes[i] for i in range(lim_cylindre)])
    lsigma0 = longueur(sigma0, matDistance)
    sigma = sigma0.copy()
    T = 100
    lst_indice = [i for i in range(lim_cylindre)]
    for n in range(2,N):
        # T = abs(mt.sin(n)/(n**b))*a
        #T *= 0.999
        # T = Tn(n, a, b)
        T = Tn(n)
        if T == 0.0:
            print(f"b trop bas : {b}")
            break
        iA = rd.choice(lst_indice[1:])
        iB = rd.randint(1, m-1)
        while iA == iB:
            iB = rd.randint(1, m-1)

        

        sigmaPrime = sigma.copy()
        for i in range(lim_cylindre):
            if sigma[i][3] == iA:
                sigmaPrime[i] = Villes[iB]
            elif sigma[i][3] == iB:
                sigmaPrime[i] = Villes[iA]


        # sigmaPrime[[iA, iB]] = Villes[[iB, iA]]


        lsigma = longueur(sigma, matDistance)
        deltaLong = lsigma - longueur(sigmaPrime, matDistance)
        if deltaLong >= 0:
            rho = 1
        else:
            try:
                rho =  mt.exp((deltaLong) / T)
            except Exception:
                print(T)
                exit()
            # rho =  mt.exp((deltaLong) / T)
        

        if rho >= 1:
            sigma = sigmaPrime.copy()
            lst_indice.remove(iA)
            lst_indice.append(iB)
        else:
            U = rd.random()
            if U < rho:
                sigma = sigmaPrime.copy()
                lst_indice.remove(iA)
                lst_indice.append(iB)

        if lsigma0 > lsigma:
            sigma0 = sigma.copy()
            lsigma0 = lsigma

    return longueurReelle(sigma0), sigma0


def Tn(N, a = 100, b = 0.99, h = 11):
    
    k = 1
    n = N
    a = mt.exp((k - 1) * h)
    b = mt.exp(k * h)
    while not((a < n) and (n <= b)) and k < 300:
        k += 1
        a = mt.exp((k - 1) * h)
        try:
            b = mt.exp(k * h)
        except Exception:
            print(k)
            exit()

    if k == 300:
        print(n)
        print("Y a problème")

    return 1/k
    
    # return 2.5 - np.log(np.log(2.71828182846 + N))
    # return a*(b**N)

    
#lancement(500)

# sig = chem.faire_chemin()

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


l, sig0 = MCMC3(100000, a=10, b=0.998, lim_cylindre = 12)
# l, sig0 = MCMC(1000000)

# print(sig) # chemin_base
# print(sig0) # mcmc 
print(sig0)
print(f"longueur reelle mcmc : {longueurReelle(sig0)}") # longueur de mcmc
# print(f"longueur reelle chemin de base : {longueurReelle(sig)}") # longueur de chemin_base

def afficher():
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

# Villes = importerVilles()
# print(Villes)
    
afficher()
