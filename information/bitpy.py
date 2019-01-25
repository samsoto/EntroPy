from utilities import pyutils
import pandas as pd
import numpy as np

BITS_COL = 'bits'
PROB_COL = 'probs'
WEIGHTED_BITS_COL = 'weighted_bits'


class BitPy(object):

    def __init__(self, timeseries: pd.DataFrame, bins: int=10):
        timeseries = pyutils.discretize(timeseries, bins)
        colnames = list(timeseries)
        totalcount = len(timeseries)
        timeseries[PROB_COL] = 0.0
        information = timeseries.groupby(colnames).count()
        information[PROB_COL] = information[PROB_COL] / totalcount
        information[BITS_COL] = np.log2(1/information[PROB_COL])
        information[WEIGHTED_BITS_COL] = information[PROB_COL] * information[BITS_COL]
        self.entropy = information[WEIGHTED_BITS_COL].sum()
        self.information = information

    def __getitem__(self, key) -> float:
        return self.information[key]

    def weighted_bits(self) -> pd.DataFrame:
        return self.information[[WEIGHTED_BITS_COL]]

    def bits(self) -> pd.DataFrame:
        return self.information[[BITS_COL]]

    def probs(self) -> pd.DataFrame:
        return self.information[[PROB_COL]]

    def as_df(self) -> pd.DataFrame:
        return self.information
