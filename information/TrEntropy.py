import numpy as np
from probability import prob
import math


class TrEntropy(object):

    @staticmethod
    def calc_te(tA: np.ndarray, tB: np.ndarray):
        """
        Calculate Transfer information
        :param tA:
        :param tB:
        :return:
        """

        tA1 = tA[1:]  # t: 1 -> n
        tA0 = tA[:-1]  # t: 0 -> n-1
        tB0 = tB[:-1]  # t: 0 -> n-1

        j_prob = prob.joint(tA1, tA0, tB0)                    # P(At1, At, Bt)
        jc_prob = prob.conditional(tA1, list(zip(tA0, tB0)))  # P(At1 | ABt)
        c_prob = prob.conditional(tA1, tA0)                   # P(At1 | At)

        # Calculate Transfer information
        te = 0.0
        for key in j_prob:
            at1, at, bt = key
            x = j_prob[(at1, at, bt)] * math.log2(jc_prob[(at1, (at, bt))] / c_prob[(at1, at)])
            te = te + x

        return te

