import numpy as np

a = np.array([[13.4731,3.948,1.],[13,948,1.],[1322,948,1.]])
a[[0, 1]] = a[[1, 0]]

print(a)