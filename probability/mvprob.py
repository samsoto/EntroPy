"""Joint and conditional frequencies of observed discrete states."""

import pandas as pd

from utilities.pyutils import as_frame, combine_dfs

PROB_COL = "prob"


def probs_dict(p, given=None) -> dict:
    return probs(p, given=given, reset_index=False)[PROB_COL].to_dict()


def probs(p, key=None, given=None, reset_index=True) -> pd.DataFrame:
    df = jprobs(p) if given is None else cprobs(p, given)
    probability_name = PROB_COL if key is None else f"{PROB_COL}_{key}"
    df.columns = [probability_name]
    if reset_index and probability_name in df.index.names:
        # An input symbol column may itself be named 'prob'. Preserve its
        # values while giving reset_index a noncolliding output label.
        names = list(df.index.names)
        for i, name in enumerate(names):
            if name == probability_name:
                replacement = f"state_{i}"
                while replacement in names or replacement == probability_name:
                    replacement = "_" + replacement
                names[i] = replacement
        df.index = df.index.set_names(names)
    return df.reset_index() if reset_index else df


def jprobs(p) -> pd.DataFrame:
    """P(state); only observed states are included."""
    p = as_frame(p)
    counts = p.groupby(list(p), observed=True, sort=False).size()
    return (counts / len(p)).to_frame(PROB_COL)


def cprobs(hyp, given) -> pd.DataFrame:
    """P(hyp | given) for rows aligned by identical indexes and order.

    Output index levels contain hypothesis states, followed by given states.
    Combined column labels are positional, so identical input labels are safe.
    """
    hyp, given = as_frame(hyp), as_frame(given)
    df = combine_dfs(hyp, given)
    counts = df.groupby(list(df), observed=True, sort=False).size()
    levels = list(range(hyp.shape[1], df.shape[1]))
    totals = counts.groupby(level=levels, observed=True).transform("sum")
    return (counts / totals).to_frame(PROB_COL)
