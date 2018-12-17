from utilities.pyutils import as_tuple, combine_dfs, keys_tuple_list
from probability.mvprob import probs, probs_dict
from math import log2, inf
from typing import Any
import pandas as pd


class EntroPy(object):

    @staticmethod
    def self_information(x: pd.DataFrame, a: Any) -> float:
        """

        :param x:
        :param a:
        :return:
        """
        x_dict = probs_dict(x)
        x_prob = x_dict.get(a) or 0.0
        return log2(1.0/x_prob) if x_prob != 0 else inf

    @staticmethod
    def shannon_entropy(x: pd.DataFrame) -> float:
        """

        :param x:
        :return:
        """
        x_dict = probs_dict(x)
        entropy = 0.0
        for x_key in x_dict:
            x_prob = x_dict.get(x_key)
            if x_prob != 0:
                entropy += x_prob * log2(1 / x_prob)
        return entropy

    @staticmethod
    def cross_entropy(x: pd.DataFrame, y: pd.DataFrame) -> float:
        """

        :param x:
        :param y:
        :return:
        """
        keys = keys_tuple_list(x, y)
        x_dict = probs_dict(x)
        y_dict = probs_dict(y)
        cross = 0.0
        for key in keys:
            if len(key) == 1:
                key = key[0]
            x_prob = x_dict.get(key) or 0.0
            y_prob = y_dict.get(key) or 0.0
            if x_prob != 0 and y_prob != 0:
                cross += x_prob * log2(1 / y_prob)
        return cross

    @staticmethod
    def relative_entropy(x: pd.DataFrame, y: pd.DataFrame) -> float:
        """
        Also know as: 'kullback-Leibler Divergence' Defined as: D_kl(X||Y)=SUM_i p(x_i)/p(y_i)
        X and Y are two probability distribution over the same set of symbols. In a sense
        relative entropy measures the distance between two probability distributions.
        :param x: Data frame X
        :param y: Data frame Y
        :return: the difference between the cross
        entropy of (X and Y), and the entropy of X
        amd
        """
        keys = keys_tuple_list(x, y)
        x_dict = probs_dict(x)
        y_dict = probs_dict(y)
        divergence = 0.0
        for key in keys:
            if len(key) == 1:
                key = key[0]
            x_prob = x_dict.get(key) or 0.0
            y_prob = y_dict.get(key) or 0.0
            if x_prob != 0 and y_prob != 0:
                divergence += x_prob * log2(x_prob / y_prob)
        return divergence

    @staticmethod
    def mutual_information(x: pd.DataFrame, y: pd.DataFrame) -> float:
        """

        :param x:
        :param y:
        :return:
        """
        joint = combine_dfs(x, y)
        x_dict = probs_dict(x)
        y_dict = probs_dict(y)
        joint_dict = probs_dict(joint)
        mi = 0.0
        for x_key in x_dict:
            for y_key in y_dict:
                joint_key = as_tuple(x_key, y_key)
                joint_prob = joint_dict.get(joint_key) or 0.0
                x_prob = x_dict.get(x_key)
                y_prob = y_dict.get(y_key)
                if x_prob != 0 and y_prob != 0 and joint_prob != 0:
                    mi += joint_prob * log2(joint_prob / (x_prob * y_prob))
        return mi

    @staticmethod
    def reyi_entropy(p, a) -> float:
        """

        :param p:
        :param a:
        :return:
        """
        pass

    @staticmethod
    def transfer_entropy(x, y) -> float:
        """

        :param x:
        :param y:
        :return:
        """
        x_future = x[1:]    # t: 1 -> n
        x_present = x[:-1]  # t: 0 -> n-1
        y_present = y[:-1]  # t: 0 -> n-1
        xy_present = combine_dfs(x_present, y_present)
        a_prob = probs(combine_dfs(x_future, x_present, y_present))
        n_prob = probs(x_future, given=xy_present)
        d_prob = probs(x_future, given=x_present)
        te = 0.0
        for key in a_prob:
            at1, at, bt = key
            x = a_prob[(at1, at, bt)] * log2(n_prob[(at1, (at, bt))] / d_prob[(at1, at)])
            te = te + x
        return te

    @staticmethod
    def conditional_mutual_information(x: pd.DataFrame, y: pd.DataFrame, z: pd.DataFrame) -> float:
        """

        :param x:
        :param y:
        :param z:
        :return:
        """
        yz = combine_dfs(y, z)
        mi1 = EntroPy.mutual_information(x, yz)
        mi2 = EntroPy.mutual_information(x, z)
        return mi1 - mi2
