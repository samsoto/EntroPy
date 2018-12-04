import numpy as np
import pandas as pd


def joint(a: np.ndarray, b: np.ndarray, c: np.ndarray):
    """
    Join Probability
    :param a:
    :param b:
    :param c:
    :return:
    """
    p = np.array((a, b, c)).T
    p = pd.DataFrame(p, columns=['a', 'b', 'c'])
    total_count = len(p)
    p['probability'] = 0.0
    p = p.groupby(['a', 'b', 'c']).count()
    p['probability'] = p['probability'] / total_count
    return p.to_dict()['probability']


def conditional(a: np.ndarray, b):
    """
    Conditional Probability
    :param a:
    :param b:
    :return:
    """
    ab = pd.DataFrame(columns=['a', 'b', 'ab_sum'])
    ab['a'] = a
    ab['b'] = b
    ab['ab_sum'] = 1
    c_probs = ab.groupby(['a', 'b']).sum()
    grouping = c_probs.groupby([c_probs.index.get_level_values(1)])
    c_probs['b_sum'] = grouping['ab_sum'].transform(sum)
    c_probs['probability'] = c_probs['ab_sum'] / c_probs['b_sum']
    c_probs = c_probs.drop('b_sum', axis=1)
    c_probs = c_probs.drop('ab_sum', axis=1)
    return c_probs.to_dict()['probability']

