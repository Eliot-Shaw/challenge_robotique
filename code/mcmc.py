import csv
import random as rd
import math as mt
import matplotlib.pyplot as plt


def importerVilles():
    Villes = []
    nomColonne = ['MAJ', 'Latitude', 'Longitude']

    with open('selected.csv', newline='') as file:
        data = csv.DictReader(file, delimiter = ',')
        for row in data:
            Villes.append([row[nom] for nom in nomColonne])

    return Villes


def distance(VA, VB, lstV):

    iA = 0
    iB = 0
    for i in range(len(lstV)):
        if lstV[i][0] == VA:
            iA = i
        elif lstV[i][0] == VB:
            iB = i
    

    lat1 = float(lstV[iA][1])
    lat2 = float(lstV[iB][1])
    lon1 = float(lstV[iA][2])
    lon2 = float(lstV[iB][2])


    return mt.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)

def calculMatriceDis(lstV):

    n = len(lstV)

    Mat = [ [ None for y in range( n ) ] for x in range( n ) ]
    for i in range(n):
        for j in range(n):
            Mat[i][j] = distance(lstV[i], lstV[j], lstV)

    return Mat

def distanceAvecMat(VA, VB, lstV, matDis):
    iA = 0
    iB = 0
    for i in range(len(lstV)):
        if lstV[i][0] == VA:
            iA = i
        elif lstV[i][0] == VB:
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
    Villes = importerVilles()
    m = len(Villes)
    sigma0 = [Villes[i][0] for i in range(m)]
    lsigma0 = longueur(sigma0, Villes)
    sigma = sigma0.copy()
    T = 100
    matDistance = calculMatriceDis
    for n in range(2,N):
        #T = abs(mt.sin(n)/(n**1.1))*300
        #T *= 0.999
        T = Tn(n)

        iA = rd.randint(0, m-1)
        iB = rd.randint(0, m-1)
        while iA == iB:
            iB = rd.randint(0, m-1)

        sigmaPrime = sigma.copy()
        temp = sigmaPrime[iA]
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


def MCMC2(N, sigma1):
    Villes = importerVilles()
    m = len(Villes)
    sigma0 = sigma1
    lsigma0 = longueur(sigma0, Villes)
    sigma = sigma0.copy()
    T = 100
    matDistance = calculMatriceDis
    for n in range(2,N):
        #T = abs(mt.sin(n)/(n**1.1))*300
        #T *= 0.999
        T = Tn(n)

        iA = rd.randint(0, m-1)
        iB = rd.randint(0, m-1)
        while iA == iB:
            iB = rd.randint(0, m-1)

        sigmaPrime = sigma.copy()
        temp = sigmaPrime[iA]
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

    print(T)

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
    return 1000*(0.999**N)


#lancement(500)

l, sig0 = MCMC(50000)

l, sig = MCMC2(50000, sig0)

print(sig)
print(l)


