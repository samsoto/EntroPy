from utilities.pyutils import as_tuple, combine_dfs, unique_values, column_names
from probability.mvprob import probs, probs_dict
from sklearn.preprocessing import MinMaxScaler
from sklearn.impute import SimpleImputer
from information.entropy import EntroPy
import matplotlib.pyplot as plt
import numpy as np
from typing import Tuple
import pandas as pd
from pandas import DataFrame
from typing import Any
import math


# --------------------------------------------------
# Get Stock Prices
# --------------------------------------------------
prices = pd.read_csv('../resources/stock_prices/stock_prices_750.txt', sep='\t', header=0, index_col=0).iloc[:, 10:15]

# -----------------------------------------------
# Clean Prices
# -----------------------------------------------
col_names = prices.columns
prices = SimpleImputer().fit_transform(prices)
prices = MinMaxScaler().fit_transform(prices)

bins = np.linspace(0, 1, 20)
prices = np.digitize(prices, bins, right=True)
prices = DataFrame(prices, columns=col_names)

# --------------------------------------------------
# Plot Stock Prices
# --------------------------------------------------
# _, ax = plt.subplots()
# ax.plot(prices.index.values.tolist(), prices)
# plt.show()

num_cols = len(col_names)
tre_matrix = np.zeros(shape=(num_cols, num_cols))

for i in range(num_cols):
    for j in range(num_cols):
        if j is not i:
            col_i = col_names[i]
            col_j = col_names[j]
            a = prices[[col_i]]
            b = prices[[col_j]]
            ab = EntroPy.transfer_entropy(a, b)
            ba = EntroPy.transfer_entropy(b, a)
            tre_matrix[i][j] = ab
            tre_matrix[j][i] = ba
            # print(f'TrEntropy A->B: {ab}')
            # print(f'TrEntropy B->A: {ba}')
            # print()

fig, ax = plt.subplots()
im = ax.imshow(tre_matrix, cmap='inferno')

# We want to show all ticks...
ax.set_xticks(np.arange(len(col_names)))
ax.set_yticks(np.arange(len(col_names)))
# ... and label them with the respective list entries
ax.set_xticklabels(col_names)
ax.set_yticklabels(col_names)

# Rotate the tick labels and set their alignment.
plt.setp(ax.get_xticklabels(), rotation=45, ha="right",rotation_mode="anchor")

# Loop over data dimensions and create text annotations.
for i in range(num_cols):
    for j in range(num_cols):
        d = round(tre_matrix[i][j], 2)
        text = ax.text(j, i, d, ha="center", va="center", color="w")

ax.set_title("Harvest of local farmers (in tons/year)")
fig.tight_layout()
plt.show()


tre_matrix = DataFrame(tre_matrix, columns=col_names, index=col_names)
print(tre_matrix)





