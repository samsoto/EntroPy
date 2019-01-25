from typing import Any, List, Tuple
from pandas import DataFrame
import pandas as pd
import numpy as np


def rename(df: DataFrame, col: list=None) -> DataFrame:
    df.columns = np.arange(len(df.columns)) \
        if col is None else col
    return df


def as_tuple(*objects: Any) -> tuple:
    tpl = ()
    for e in objects:
        if not isinstance(e, tuple):
            e = (e,)
        tpl += e
    return tpl


def discretize(df: DataFrame, bins: int) -> DataFrame:
    df = df.copy()
    for x in list(df):
        df[x] = pd.cut(df[x], bins=bins, labels=np.arange(bins), right=True)
    return df


def combine_dfs(*dfs: DataFrame) -> pd.DataFrame:
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


def unique_values(*dfs: pd.DataFrame) -> List[Tuple]:
    p = []
    for e in dfs:
        if e is not None:
            distinct_df = e.drop_duplicates()
            distinct_list: list = distinct_df.to_records(index=False).tolist()
            p = p + distinct_list
    return list(set(p))


def column_names(df: DataFrame, postfix: str=None):
    new_column_names = []
    for column_name in df.columns:
        new_column_names += [column_name + postfix]
    df.columns = new_column_names
    return df
