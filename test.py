import pandas as pd
import numpy as np
from probability import mvprob
from information.EntroPy import EntroPy


a = pd.DataFrame([0,1,3,2,1,1,1,2,3,1,2,1,3], columns=['a'])
b = pd.DataFrame([0,1,3,2,1,1,1,2,3,1,2,1,3], columns=['b'])
b['b2'] = [1,2,3,2,1,1,1,1,1,1,2,2,1]
c = pd.DataFrame([1,1,3,1,0,0,1,0,2,1,2,2,1], columns=['c'])

# foo = mvprob.jprobs(a, b)
# print(foo.head())
z = EntroPy.c_mutual_information(a, b, c)
print(z)

