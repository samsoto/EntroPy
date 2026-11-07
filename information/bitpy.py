"""Inspect the probabilities and information behind an entropy value."""

import numpy as np
import pandas as pd

from utilities.pyutils import discretize

BITS_COL = "bits"
PROB_COL = "probs"
WEIGHTED_BITS_COL = "weighted_bits"


class BitPy:
    def __init__(self, timeseries: pd.DataFrame, bins: int | None = None):
        timeseries = discretize(timeseries, bins)
        # size() avoids overwriting an input column named 'probs' or 'bits'.
        counts = timeseries.groupby(list(timeseries), observed=True, sort=False).size()
        information = (counts / len(timeseries)).to_frame(PROB_COL)
        information[BITS_COL] = -np.log2(information[PROB_COL])
        information[WEIGHTED_BITS_COL] = information[PROB_COL] * information[BITS_COL]
        self.entropy = float(information[WEIGHTED_BITS_COL].sum())
        self.information = information

    def __getitem__(self, key):
        return self.information[key]

    def weighted_bits(self):
        return self.information[[WEIGHTED_BITS_COL]].copy()

    def bits(self):
        return self.information[[BITS_COL]].copy()

    def probs(self):
        return self.information[[PROB_COL]].copy()

    def as_df(self):
        return self.information.copy()
