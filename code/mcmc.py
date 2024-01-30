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
    distance_valeur = distance_raw/chem.type_cylindre[int(VB[2])-1][0]
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

def distanceAvecMat(VA, VB, lstV, matDis):
    iA = 0
    iB = 0
    for i in range(len(lstV)):
        if np.array_equal(lstV[i],VA):
            iA = i
        elif np.array_equal(lstV[i],VB):
            iB = i

    return matDis[iA][iB]


def longueur(Chemin, Villes, matDis):
    res = 0
    for i in range(len(Chemin)-1):
        VA = Chemin[i]
        VB = Chemin[i+1]
        res += distanceAvecMat(VA, VB, Villes, matDis)


    res += distanceAvecMat(Chemin[-1], Chemin[0], Villes, matDis)

    return res

def longueurReelle(Chemin, Villes):
    res = 0
    for i in range(len(Chemin)-1):
        VA = Chemin[i]
        VB = Chemin[i+1]
        res += distance(VA, VB)


    res += distance(Chemin[-1], Chemin[0])

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


    return longueurReelle(sigma0, Villes), sigma0


def MCMC2(N, sigma1, a, b):
    Villes = np.concatenate((np.array([[0, 0, 0]]),importerVilles()), axis=0)
    m = len(Villes)
    matDistance = Mat
    sigma0 = sigma1
    lsigma0 = longueur(sigma0, Villes, matDistance)
    sigma = sigma0.copy()
    T = 100
    for n in range(2,N):
        #T = abs(mt.sin(n)/(n**1.1))*300
        #T *= 0.999
        T = Tn(n, a, b)
        if T == 0.0:
            print(f"b trop bas{b}")
            break
        iA = rd.randint(0, m-1)
        iB = rd.randint(0, m-1)
        while iA == iB:
            iB = rd.randint(0, m-1)

        sigmaPrime = sigma.copy()
        # temp = np.array(sigmaPrime[iA])
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

    return longueurReelle(sigma0, Villes), sigma0


def Tn(N, a, b, h = 1):
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
    return a*(b**N)

    
#lancement(500)

sig = chem.faire_chemin()

global() Mat
Mat = calculMatriceDis(Villes)

# l, sig0 = MCMC2(5000, sig, a=0, b=0) #iterations et chemin
# Open a file in write mode
with open('../divers/resultats.txt', 'w') as f:
    # Write the Python code to the file
    for i in range(0,150,10):
        a = 10
        bz = 0.985+i*0.0001
        l, sig0 = MCMC2(5000, sig, a, bz) #iterations et chemin
        f.write(f'a={a} --- b={bz} --- l={l}\n')


# l, sig = MCMC2(50000, sig0)

# print(sig) # chemin_base
# print(sig0) # mcmc 
# print(l) # longueur de mcmc

fig = plt.figure(1)


tColorTab = {1:'red', 2:'green', 3:'blue'}
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