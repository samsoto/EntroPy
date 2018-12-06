import pandas as pd


def as_tuple(e) -> tuple:
    if isinstance(e, tuple):
        return e
    return (e,)


def combine_dfs(*dfs: pd.DataFrame) -> pd.DataFrame:
    """
    If we are given a list of DataFrames
    combine them into a Single DataFrames
    :param dfs:
    :return:
    """
    p = pd.DataFrame()
    for e in dfs:
        p = pd.concat([p, e], axis=1)
    return p
