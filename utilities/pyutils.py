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


def as_frame(data) -> DataFrame:
    """Validate observations without silently dropping missing rows."""
    if isinstance(data, pd.Series):
        data = data.to_frame()
    if not isinstance(data, pd.DataFrame):
        raise TypeError("observations must be a pandas DataFrame or Series")
    if data.empty:
        raise ValueError("observations must contain at least one row and column")
    if not data.columns.is_unique:
        raise ValueError("input column names must be unique")
    if data.isna().any().any():
        raise ValueError("observations contain missing values; clean them explicitly first")
    for column in data:
        if pd.api.types.is_numeric_dtype(data[column]):
            if not np.isfinite(data[column].to_numpy(dtype=float)).all():
                raise ValueError("observations must contain only finite numeric values")
    return data.copy()


def _validate_bins(bins):
    if bins is not None and (isinstance(bins, bool) or not isinstance(bins, int) or bins < 1):
        raise ValueError("bins must be a positive integer or None")


def _numeric(series):
    return pd.api.types.is_numeric_dtype(series) and not pd.api.types.is_bool_dtype(series)


def discretize(df: DataFrame, bins: int | None = None) -> DataFrame:
    """Optionally bin numeric columns; preserve categorical symbols and booleans."""
    df = as_frame(df)
    _validate_bins(bins)
    if bins is not None:
        for column in df:
            if _numeric(df[column]):
                df[column] = pd.cut(df[column], bins=bins, labels=False, include_lowest=True)
    return df


def discretize_pair(x, y, bins=None):
    """Match distribution coordinates by position, using shared numeric bins."""
    x, y = as_frame(x), as_frame(y)
    _validate_bins(bins)
    if x.shape[1] != y.shape[1]:
        raise ValueError("distributions must have the same number of columns")
    x.columns = y.columns = range(x.shape[1])
    if bins is not None:
        for column in x:
            if _numeric(x[column]) != _numeric(y[column]):
                raise ValueError("corresponding columns must both be numeric or both categorical")
            if _numeric(x[column]):
                pooled = pd.concat([x[column], y[column]], ignore_index=True)
                codes = pd.cut(pooled, bins=bins, labels=False, include_lowest=True)
                x[column] = codes.iloc[:len(x)].to_numpy()
                y[column] = codes.iloc[len(x):].to_numpy()
    return x, y


def combine_dfs(*dfs: DataFrame) -> pd.DataFrame:
    """
    Combine paired observations, assigning unique positional column names.
    Indexes must already match exactly; there is no implicit alignment/drop.
    """
    frames = [as_frame(frame) for frame in dfs if frame is not None]
    if not frames:
        raise ValueError("at least one frame is required")
    if any(not frame.index.equals(frames[0].index) for frame in frames[1:]):
        raise ValueError("paired observations must have identical row indexes and order")
    return pd.concat(frames, axis=1, ignore_index=True)


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
