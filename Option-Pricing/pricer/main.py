import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import formulas

myOptionObject = formulas.Option()
greeks = myOptionObject.bsGreeks(parity='put', spot=20000, strike=18000, vol=0.30, intRate=0.01, divYield=0.02, timeToMat=1.0)
print(greeks['Delta'])

# plt.plot(timeToMats, thetas)
# plt.show()