import pandas as pd
import numpy as np
from probability import mvprob
from information.EntroPy import EntroPy


a = pd.DataFrame([0, 1, 0, 1], columns=['a'])
b = pd.DataFrame([1,2,2,1,2,1,3,2,1,1,2,3,1], columns=['b'])
b['c'] = [1,2,3,2,1,1,1,1,1,1,2,2,1]

z = EntroPy.shannon_entropy(a)

print(z)

