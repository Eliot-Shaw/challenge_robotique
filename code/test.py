import numpy as np

def Soustraire(lst_cylindres, cylindres_total):

    cylindres = cylindres_total.copy()

    premier_cylindre = lst_cylindres[-1]

    for cylindre in lst_cylindres:
        cylindres = np.delete(cylindres, int(cylindre[3]), axis=0)

    np.concatenate((np.array([premier_cylindre]),cylindres), axis = 0)

    return cylindres

coucou = np.array([
    [ 0.0, 0.0, 0.0, 0.0],
    [ 1.7554, 1.8713, 3.0,1.0],
    [ 7.8513, 1.7958, 2.0,2.0],
    [13.4731, 3.948,  1.0,3.0],
    [18.1907, 2.0316, 1.0,4.0],
    [ 2.7522, 6.3233, 1.0,5.0],
    [ 8.7189, 8.639,  1.0,6.0],
    [13.4533, 6.7822, 2.0,7.0],
    [17.7831, 6.0675, 2.0,8.0],
    [ 2.2758, 11.9382, 2.0,9.0],
    [ 6.4845, 11.5363, 3.0,10.0],
    [12.2687, 11.2827, 2.0,11.0],
    [17.7956, 12.4128, 3.0,12.0],
    [ 3.0878, 18.0997, 2.0,13.0],
    [ 7.9156, 16.1008, 3.0,14.0],
    [11.2064, 16.9588, 1.0,15.0],
    [17.5926, 17.9633, 3.0,16.0],
    [ 2.2229, 23.4599, 1.0,17.0],
    [ 8.1551, 23.9059, 3.0,18.0],
    [12.594, 21.9754, 3.0,19.0],
    [16.3169, 22.8329, 1.0,20.0]])

coucou2 = np.array([
    [ 0.0, 0.0, 0.0, 0.0],
    [ 1.7554, 1.8713, 3.0,1.0],
    [ 7.8513, 1.7958, 2.0,2.0],
    [13.4731, 3.948,  1.0,3.0],
    [18.1907, 2.0316, 1.0,4.0],
    [ 2.7522, 6.3233, 1.0,5.0],
    [ 8.7189, 8.639,  1.0,6.0],
    [13.4533, 6.7822, 2.0,7.0],
    [17.7831, 6.0675, 2.0,8.0]])

coucou3 = Soustraire(coucou2, coucou)
coucou4 = np.delete(coucou, 3, axis=0)
print(coucou)
print("aled")
print(coucou2)
print("aled")
print(coucou3)
print("aled1")
print(coucou4)