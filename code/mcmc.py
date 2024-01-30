import random as rd
import math as mt
import numpy as np
import sys
import matplotlib.pyplot as plt


def importerVilles():
    argc = len(sys.argv)
    if argc < 2:
        print("preciser le nom du fichier de donnees en argument...")
        exit()
    #lecture du fichier
    DataMap = np.loadtxt(sys.argv[1], dtype=float)
    return(DataMap)

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
            Mat[i][j] = distance(lstV[i], lstV[j])

    return Mat

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


    return longueur(sigma0, Villes, matDistance), sigma0


def MCMC2(N, sigma1):
    Villes = np.concatenate([[0, 0, 0]],importerVilles())
    m = len(Villes)
    matDistance = calculMatriceDis(Villes)
    sigma0 = sigma1
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
        temp = np.array(sigmaPrime[iA])
        sigmaPrime[iA] = sigmaPrime[iB]
        sigmaPrime[iB] = temp

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

    return longueur(sigma0, Villes, matDistance), sigma0


def Tn(N, h = 1):
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
    return 10*(0.999**N)

    
#lancement(500)

l, sig0 = MCMC(5000)

# l, sig = MCMC2(50000, sig0)

print(sig0)
print(l)

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
plt.show()

# Villes = importerVilles()
# print(Villes)