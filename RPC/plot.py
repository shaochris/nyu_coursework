import matplotlib.pyplot as plt
import numpy as np
import math 

ratio = np.arange(0.5, 1.6, 0.1)

x = np.arange(0, 1.1, 0.1)

Q_L = [2, 5, 10]

y = [[] for _ in range(3)]

for i in ratio:

	M_Vr = abs((0.96)/ (math.sqrt(1 + pow(Q_L[0], 2) * pow((i - 1/i),2)) ))
	y[0].append(M_Vr)

for i in ratio:
	M_Vr = abs((0.96)/ (math.sqrt(1 + pow(Q_L[1], 2) * pow((i - 1/i),2)) ))
	y[1].append(M_Vr)

for i in ratio:
	M_Vr = abs((0.96)/ (math.sqrt(1 + pow(Q_L[2], 2) * pow((i - 1/i),2)) ))
	y[2].append(M_Vr)

for i in range(3):
	plt.plot(x, y[i])

plt.show()