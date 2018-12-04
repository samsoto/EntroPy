import pandas as pd


def prob(p: pd.DataFrame, given=None) -> pd.DataFrame:
    if given is not None:
        return cprobs(p, given)
    return jprobs(p)


def jprobs(x: pd.DataFrame) -> pd.DataFrame:
    x_cols = list(x)
    total_count = len(x)
    x['prob'] = 0.0
    x = x.groupby(x_cols).count()
    x['prob'] = x['prob'] / total_count
    return x


def cprobs(hyp: pd.DataFrame, given: pd.DataFrame) -> pd.DataFrame:
    """
    Conditional Probability - P( hyp | given )
    The probability of 'hyp' in state 'h' given that.. 'given' is in stage 'g'
    Strategy: Group by all of the columns (hyp + given) and find the total.
    Then group by the 'given' columns and find the totals, relative the the
    'given'. Then divide these two to find the conditional probabilities
    :param hyp: The hypothesis variable.
    :param given: The given variable
    :return: A dictionary of the conditional probability, P( hyp | given )
    Key: 'give'
    Value: ''
    """

    # Get column names
    hyp_cols = list(hyp)
    given_cols = list(given)
    cols = hyp_cols + given_cols

    # Combine hyp and given (column-wise)
    df = pd.concat([hyp, given], axis=1, join_axes=[hyp.index])
    df['sum'] = 1

    # Group by all of the cols to get the
    # total number of each distinct pair
    df = df.groupby(cols).sum()

    # Only get the levels that correspond to the 'given' columns.
    # ~ we start where 'hyp' ends and finish where 'given' ends
    keys = []
    for k in range(len(hyp_cols) - 1, len(hyp_cols + given_cols) - 1):
        level = df.index.get_level_values(k).values
        keys.append(level)

    # Group by and the 'given' levels, and then project the sum back onto the
    # original df. This will give us the sum for each distinct combination of
    # all cols, and the sum for each group relative to the 'give' columns.
    # Aka we setup to find the conditional probabilities
    grouping = df.groupby(keys)
    df['g_sum'] = grouping['sum'].transform(sum)

    # Calculate the conditional probabilities by taking the
    # sum of each distinct combination of all cols, divided
    # by the sum for each group relative to the 'give' columns.
    df['prob'] = df['sum'] / df['g_sum']
    df = df.drop('g_sum', axis=1)
    df = df.drop('sum', axis=1)

    return df
