from utilities.pyutils import combine_dfs, column_names
from probability.mvprob import probs_dict
from information.bitpy import BitPy, BITS_COL, PROB_COL
from pandas import DataFrame
from math import log2


class EntroPy(object):

    @staticmethod
    def shannon_entropy(x: DataFrame, bins: int=10) -> float:
        """
        Information entropy is the average rate at which information
        is produced by a stochastic source of data. The measure of
        information entropy associated with each possible data value.
        :param x:
        :param bins:
        :return:
        """
        return BitPy(x, bins=bins).entropy

    @staticmethod
    def joint_entropy(x: DataFrame, y: DataFrame, bins: int=10) -> float:
        """
        Information entropy is the average rate at which information
        is produced by a stochastic source of data. The measure of
        information entropy associated with each possible data value.
        :param x:
        :param y:
        :param bins:
        :return:
        """
        xy = combine_dfs(x, y)
        return EntroPy.shannon_entropy(xy, bins=bins)

    @staticmethod
    def cross_entropy(x: DataFrame, y: DataFrame, bins: int=10) -> float:
        """
        In information theory, the cross entropy between two probability
        distributions x and y over the same underlying set of events measures
        the average number of bits needed to identify an event drawn from
        the set, if a coding scheme is used that is optimized for an "artificial"
        probability distribution y, rather than the "true" distribution x.
        :param x:
        :param y:
        :param bins:
        :return:
        """
        x = BitPy(x, bins=bins).bits()
        y = BitPy(y, bins=bins).probs()
        z = x.join(y, how='inner')
        return (z[PROB_COL] * z[BITS_COL]).sum()

    @staticmethod
    def relative_entropy(x: DataFrame, y: DataFrame, bins: int=10) -> float:
        """
        Also know as: 'kullback-Leibler Divergence' Defined as:
        D_kl(X||Y) = SUM_i p(x_i) / p(y_i). X and Y are two probability
        distribution over the same set of symbols. In a sense relative entropy
        measures the distance between two probability distributions.
        :param x: Data frame X
        :param y: Data frame Y
        :param bins:
        :return: the difference between the cross
        entropy of (X and Y), and the entropy of X
        amd
        """
        entropy = EntroPy.shannon_entropy(x, bins=bins)
        cross_entropy = EntroPy.cross_entropy(x, y, bins=bins)
        return cross_entropy - entropy

    @staticmethod
    def mutual_information(x: DataFrame, y: DataFrame, bins: int=10) -> float:
        """
        In probability theory and information theory, the mutual
        information (MI) of two random variables is a measure of
        the mutual dependence between the two variables.
        :param x:
        :param y:
        :param bins:
        :return:
        """
        entropy_x = EntroPy.shannon_entropy(x, bins=bins)
        entropy_y = EntroPy.shannon_entropy(y, bins=bins)
        joint_entropy = EntroPy.joint_entropy(x, y, bins=bins)
        return entropy_x + entropy_y - joint_entropy

    @staticmethod
    def transfer_entropy(x: DataFrame, y: DataFrame) -> float:
        """

        :param x:
        :param y:
        :return:
        """
        x_future = x[1:]  # t: 1 -> n
        x_present = x[:-1]  # t: 0 -> n-1
        y_present = y[:-1]  # t: 0 -> n-1
        x_future = column_names(x_future, postfix='2')
        x_future = x_future.reset_index(drop=True)
        xy_present = combine_dfs(x_present, y_present)
        xf_xp_yp = combine_dfs(x_future, x_present, y_present)
        a_prob = probs_dict(xf_xp_yp)
        n_prob = probs_dict(x_future, given=xy_present)
        d_prob = probs_dict(x_future, given=x_present)
        te = 0.0
        for key in a_prob:
            at1, at, bt = key
            weight = a_prob[(at1, at, bt)]
            subtractive = d_prob[(at1, at)]
            additive = n_prob.get((at1, at, bt)) or 0.0
            if additive != 0.0 and subtractive != 0.0:
                x = weight * log2(additive / subtractive)
                te = te + x
        return te


