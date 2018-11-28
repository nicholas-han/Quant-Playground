import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import formulas

timeToMats = 0.1 * np.arange(80)
thetas = []
myOptionObject = formulas.Option()
for timeToMat in timeToMats:
    greeks = myOptionObject.bsGreeks(parity='put', spot=12, strike=15, vol=0.30, intRate=0.02, divYield=0.0, timeToMat=float(timeToMat))
    thetas.append(greeks['Theta'])

plt.plot(timeToMats, thetas)
plt.show()