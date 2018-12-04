import pandas as pd
import numpy as np
from probability import mvprob


a = pd.DataFrame([1,2,3,2,1,3,2,3,1,2,3,2,1], columns=['a'])
b = pd.DataFrame([1,2,2,1,2,1,3,2,1,1,2,3,1], columns=['b'])
b['c'] = [1,2,3,2,1,1,1,1,1,1,2,2,1]

e = mvprob.cprob(a, b)

print(e)




