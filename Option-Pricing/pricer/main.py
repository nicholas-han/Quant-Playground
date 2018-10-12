import sys
import numpy as np
import pandas as pd

import formulas



myOptionObject = formulas.Option(parity='call', spot=12.4, strike=12, vol=0.30, intRate=0.03, divYield=0.0, timeToMat=1)
myOptionObject.bsGreeks()