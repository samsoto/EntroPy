import pandas as pd


PROB_COLUMN_NAME = 'prob'


def probs(p: pd.DataFrame, given: pd.DataFrame=None) -> pd.DataFrame:
    return jprobs(p) if given is None \
        else cprobs(p, given)


def jprobs(p: pd.DataFrame) -> pd.DataFrame:
    """
    Joint Probability Distribution Function
    :param: A list of
    :return:
    """
    p_cols = list(p)
    total_count = len(p)
    p[PROB_COLUMN_NAME] = 0.0
    p = p.groupby(p_cols).count()
    foo = p[PROB_COLUMN_NAME] / total_count
    p[PROB_COLUMN_NAME] = foo
    return p


def cprobs(hyp: pd.DataFrame, given: pd.DataFrame=None) -> pd.DataFrame:
    """
    Conditional Probability - P( hyp | given )
    The probability of 'hyp' in state 'h' given that.. 'given' is in stage 'g'
    Strategy: Group by all of the columns (hyp + given) and find the total.
    Then group by the 'given' columns and find the totals relative to the
    'given' cols. Then divide these two totals to find the conditional probabilities
    :param hyp: The hypothesis variable.
    :param given: The given variable
    :return: A DataFrame of the conditional probabilities, P( hyp | given )
    Key: '(hyp, give)'
    Value: Conditional probabilities
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
