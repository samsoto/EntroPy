from neo4j import GraphDatabase
from sklearn.preprocessing import MinMaxScaler
from sklearn.impute import SimpleImputer
from information.entropy import EntroPy
import matplotlib.pyplot as plt
from pandas import DataFrame
import pandas as pd
import numpy as np

# --------------------------------------------------
# Open Neo4J Connection
# --------------------------------------------------
uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "fubar"))


# --------------------------------------------------
# Get Stock Prices
# --------------------------------------------------
file_url = 'resources/stock_prices/stock_prices_750.txt'
prices = pd.read_csv(file_url, sep='\t', header=0, index_col=0).iloc[:, 1:5]
stocks = prices.columns


# --------------------------------------------------
# Create Stock Nodes
# --------------------------------------------------
def create_node(tx):
    for s in stocks:
        tx.run("CREATE (a:Stock { Name : {name} })", name=s)


def create_node_session():
    with driver.session() as session:
        session.read_transaction(create_node)


create_node_session()

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


# --------------------------------------------------
# Create Entropy Relation
# --------------------------------------------------
def create_relation(tx, ar, br, trr):
    command = """MATCH (a: Stock)
              WHERE a.Name = {a} 
              WITH a
              MATCH(b: Stock)
              WHERE b.Name = {b} 
              CREATE (m)-[:Entropy{value:{tr}}]->(n)"""

    tx.run(command, a=ar, b=br, tr=trr)


def create_relation_session(ar, br, tr):
    with driver.session() as session:
        session.read_transaction(create_relation, ar, br, tr)


num_cols = len(col_names)
for i in range(num_cols):
    for j in range(num_cols):
        if j is not i:
            col_i = col_names[i]
            col_j = col_names[j]
            a = prices[[col_i]]
            b = prices[[col_j]]
            ab = EntroPy.transfer_entropy(a, b)
            ba = EntroPy.transfer_entropy(b, a)
            create_relation_session(col_i, col_j, ab)
            create_relation_session(col_j, col_i, ba)
