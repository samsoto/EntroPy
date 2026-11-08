"""Empirical information measures for discrete observations, in bits."""

from collections import Counter
from math import log2

import pandas as pd

from information.bitpy import BitPy
from utilities.pyutils import as_frame, combine_dfs, discretize, discretize_pair


def _distribution(frame):
    counts = Counter(frame.itertuples(index=False, name=None))
    return {state: count / len(frame) for state, count in counts.items()}


def _entropy(frame):
    return -sum(p * log2(p) for p in _distribution(frame).values())


def _paired(x, y, bins):
    x, y = as_frame(x), as_frame(y)
    combine_dfs(x, y)  # validate observation alignment before grouping/resetting
    return discretize(x, bins), discretize(y, bins)


class EntroPy:
    """Each row is an observation; multiple columns form a joint state.

    Values are discrete symbols by default. Pass ``bins`` explicitly to bin
    numeric columns. Paired measures require identical row indexes and order.
    Distribution comparisons match columns by position, not by column name.
    """

    @staticmethod
    def shannon_entropy(x: pd.DataFrame, bins: int | None = None) -> float:
        """H(X): average uncertainty per observation, in bits."""
        return BitPy(x, bins=bins).entropy

    @staticmethod
    def joint_entropy(x, y, bins: int | None = None) -> float:
        """H(X,Y) for paired observations."""
        x, y = _paired(x, y, bins)
        return _entropy(combine_dfs(x, y))

    @staticmethod
    def conditional_entropy(x, given, bins: int | None = None) -> float:
        """H(X|given): uncertainty remaining after observing ``given``."""
        x, given = _paired(x, given, bins)
        return max(0.0, _entropy(combine_dfs(x, given)) - _entropy(given))

    @staticmethod
    def cross_entropy(x, y, bins: int | None = None) -> float:
        """H(P,Q) = -sum P log2 Q; X is observed, Y is the reference.

        Numeric bins use a shared range across both samples. If Q assigns zero
        mass to an observed P state, return infinity. No smoothing is applied.
        """
        x, y = discretize_pair(x, y, bins)
        p, q = _distribution(x), _distribution(y)
        if any(state not in q for state in p):
            return float("inf")
        return -sum(prob * log2(q[state]) for state, prob in p.items())

    @staticmethod
    def relative_entropy(x, y, bins: int | None = None) -> float:
        """D_KL(P||Q) = sum P log2(P/Q), with the same support rules as CE."""
        x, y = discretize_pair(x, y, bins)
        p, q = _distribution(x), _distribution(y)
        if any(state not in q for state in p):
            return float("inf")
        value = sum(prob * log2(prob / q[state]) for state, prob in p.items())
        return max(0.0, value)  # absorb floating-point roundoff at zero

    @staticmethod
    def mutual_information(x, y, bins: int | None = None) -> float:
        """I(X;Y): shared information between paired observations."""
        x, y = _paired(x, y, bins)
        return max(0.0, _entropy(x) + _entropy(y) - _entropy(combine_dfs(x, y)))

    @staticmethod
    def transfer_entropy(x, y, bins: int | None = None, lag: int = 1) -> float:
        """Information from Y's past about X's future, beyond X's past.

        Direction is ``y -> x`` (target first, source second), preserving the
        original argument order. Computes I(X[t]; Y[t-lag] | X[t-lag]) using
        one historical observation per variable, not a multi-step embedding.
        Rows must already be in chronological order at a regular sampling rate.
        Bins are fitted to each complete series before time slices are formed.
        """
        x, y = _paired(x, y, bins)
        if isinstance(lag, bool) or not isinstance(lag, int) or not 1 <= lag < len(x):
            raise ValueError("lag must be an integer from 1 to n_observations - 1")
        future = x.iloc[lag:].reset_index(drop=True)
        past = x.iloc[:-lag].reset_index(drop=True)
        source = y.iloc[:-lag].reset_index(drop=True)
        value = (
            _entropy(combine_dfs(future, past))
            + _entropy(combine_dfs(past, source))
            - _entropy(past)
            - _entropy(combine_dfs(future, past, source))
        )
        return max(0.0, value)
