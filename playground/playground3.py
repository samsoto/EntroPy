import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

df = pd.DataFrame()
df['source'] = ['A', 'B', 'A', 'C']
df['destination'] = ['B', 'A', 'B', 'A']
df['tr_entropy'] = [1, 1, 1, 1]

G = nx.from_pandas_edgelist(df, 'source', 'destination', ['tr_entropy'])
nx.draw_networkx(G, arrows=True)
plt.draw()
plt.show()
