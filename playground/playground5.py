from information.entropy import EntroPy
from information.bitpy import BitPy
import pandas as pd
import numpy as np
import scipy

adf = pd.DataFrame()
adf['A'] = np.random.uniform(0, 1, 10000)

bdf = pd.DataFrame()
bdf['B'] = np.random.uniform(0, 1, 10000)

mi = EntroPy.mutual_information(adf, bdf, bins=8)
print(mi)
