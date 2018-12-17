import pandas as pd
from typing import Any, List, Tuple


def as_tuple(*objects: Any) -> tuple:
    tpl = ()
    for e in objects:
        if not isinstance(e, tuple):
            e = (e,)
        tpl += e
    return tpl


def combine_dfs(*dfs: pd.DataFrame) -> pd.DataFrame:
    """
    Given a list of DataFrames combine
    them into a Single DataFrames
    :param dfs: List of DataFrames
    :return: A single DataFrame
    """
    df = pd.DataFrame()
    for e in dfs:
        if e is not None:
            df = pd.concat([df, e], axis=1)
    return df


def keys_df(*dfs: pd.DataFrame) -> pd.DataFrame:
    p = []
    for e in dfs:
        if e is not None:
            distinct_df = e.drop_duplicates()
            distinct_list: list = distinct_df.to_records(index=False).tolist()
            p = p + distinct_list
    return pd.DataFrame(p).drop_duplicates()


def keys_tuple_list(*dfs: pd.DataFrame) -> List[Tuple]:
    p = []
    for e in dfs:
        if e is not None:
            distinct_df = e.drop_duplicates()
            distinct_list: list = distinct_df.to_records(index=False).tolist()
            p = p + distinct_list
    return list(set(p))
