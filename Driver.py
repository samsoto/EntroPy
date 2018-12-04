import pandas as pd
import numpy as np
from information.TrEntropy import TrEntropy

cat = pd.read_csv("./resources/CAT.csv")['Adj Close']
de = pd.read_csv("./resources/DE.csv")['Adj Close']

cat = np.array(cat)
de = np.array(de)

te_de_2_cat = TrEntropy.calc_te(cat, de)
te_cat_to_de = TrEntropy.calc_te(de, cat)

# print(f'te_de_2_cat: {At}')
# print(f'B: {Bt}')

print(f'te(cat -> de): {te_cat_to_de}')
print(f'te(de -> cat): {te_de_2_cat}')

# te(cat -> de): 0.080091
# te(de -> cat): 0.047694
