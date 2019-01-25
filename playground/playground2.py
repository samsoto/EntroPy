from utilities.pyutils import as_tuple, combine_dfs, unique_values, column_names
from probability.mvprob import probs, probs_dict
from sklearn.preprocessing import MinMaxScaler
from sklearn.impute import SimpleImputer
from information.entropy2 import EntroPy
import matplotlib.pyplot as plt
import numpy as np
from typing import Tuple
import pandas as pd
from pandas import DataFrame
from typing import Any
import math


def example1():
    x = np.random.random((5, 3))
    print('x---------------------')
    print(x)
    print(x.shape)
    print()

    y = x.reshape(5, 1, 3)
    print('rx--------------------')
    print(y)
    print(y.shape)
    print()

    z = np.zeros((5, 1, 3)) - x
    print('z--------------------')
    print(z)
    print(z.shape)
    print()


    xb = x.reshape((5, 3, 1)) + np.zeros((5, 3, 3))
    print('broadcast-------------')
    print(xb)
    print(xb.shape)
    print()

    yb = y + np.zeros((5, 3, 3))
    print('broadcast-------------')
    print(yb)
    print(yb.shape)
    print()

    diff = y - x
    print('diff--(x-y)--------------')
    print(diff)
    print(diff.shape)
    print()

    diff = xb - yb
    print('diff--(xb-yb)-------------')
    print(diff)
    print(diff.shape)
    print()


def example2():
    x = np.random.random(4)
    print('x---------------------')
    print(x)
    print(x.shape)
    print()

    d = x.reshape(1, 4)
    print('d--------------------')
    print(d)
    print(d.shape)
    print()

    c = x.reshape(4, 1)
    print('c--------------------')
    print(c)
    print(c.shape)
    print()

    e = d - c
    print('e-------(d - c)---------')
    print(e)
    print(e.shape)
    print()

    print('=====================================================')

    f = x.reshape(1, 4) + np.zeros((4, 4))
    print('f--------------------')
    print(f)
    print(f.shape)
    print()

    g = x.reshape(4, 1) + np.zeros((4, 4))
    print('g--------------------')
    print(g)
    print(g.shape)
    print()

    h = f - g
    print('h---------(f - g)---------')
    print(h)
    print(h.shape)
    print()


# example1()

x = np.random.random((5, 3))
print(f'x---------------------\n{x}, {x.shape}\n\n')

x = x.reshape(5, 1, 3)
print(f'x---------------------\n{x}, {x.shape}\n\n')

x = x.reshape(1, 5, 3) + np.zeros((5, 5, 3))
print(f'x---------------------\n{x}, {x.shape}\n\n')
