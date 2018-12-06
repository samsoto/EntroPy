from probability import mvprob
from utilities.pyutils import as_tuple, combine_dfs
import pandas as pd
import math


class EntroPy(object):

    @staticmethod
    def kl_divergence(p, q):
        p = mvprob.probs(p)
        q = mvprob.probs(q)
        pass

    @staticmethod
    def self_information(p, a):
        pdf = mvprob.probs(p).to_dict()[mvprob.PROB_COLUMN_NAME]
        p = pdf.get(a) or 0.0
        return math.log2(1.0/p) if p != 0 else 0.0

    @staticmethod
    def conditional_mi(x: pd.DataFrame, y: pd.DataFrame, z: pd.DataFrame):
        yg = combine_dfs(y, z)
        mi1 = EntroPy.mutual_information(x, yg)
        mi2 = EntroPy.mutual_information(x, z)
        mi = mi1 - mi2
        return mi

    @staticmethod
    def mutual_information(p: pd.DataFrame, q: pd.DataFrame):
        j = combine_dfs(p, q)
        pdf = mvprob.probs(p).to_dict()[mvprob.PROB_COLUMN_NAME]
        qdf = mvprob.probs(q).to_dict()[mvprob.PROB_COLUMN_NAME]
        jdf = mvprob.probs(j).to_dict()[mvprob.PROB_COLUMN_NAME]
        mi = 0.0
        for pkey in pdf:
            for qkey in qdf:
                jkey = as_tuple(pkey) + as_tuple(qkey)
                p = pdf.get(pkey)
                q = qdf.get(qkey)
                j = jdf.get(jkey) or 0.0
                mi += j * math.log2(j/(p*q)) if j != 0 else 0.0
        return mi

    @staticmethod
    def entropy(p, a=1, cross=None, given=None):
        pass

    @staticmethod
    def shannon_entropy(p: pd.DataFrame, given=None):
        pdf = mvprob.probs(p, given)
        pdf['given_prob'] = mvprob.probs(p, given) if given is not None else 1.0
        pdf = pdf.apply(lambda e: e.iloc[0] * math.log2(e.iloc[1]/e.iloc[0]))
        return pdf.sum()

    @staticmethod
    def reyi_entropy(p, a):
        pass

    @staticmethod
    def transfer_entropy(x, y):
        tA1 = x[1:]   # t: 1 -> n
        tA0 = x[:-1]  # t: 0 -> n-1
        tB0 = y[:-1]  # t: 0 -> n-1
        j = combine_dfs(tA1, tA0, tB0)
        j_prob = mvprob.probs(j)         # P(At1, At, Bt)
        c = combine_dfs(tA0, tB0)
        jc_prob = mvprob.probs(tA1, c)   # P(At1 | ABt)
        c_prob = mvprob.probs(tA1, tA0)  # P(At1 | At)
        te = 0.0
        for key in j_prob:
            at1, at, bt = key
            x = j_prob[(at1, at, bt)] * math.log2(jc_prob[(at1, (at, bt))] / c_prob[(at1, at)])
            te = te + x
        return te

    @staticmethod
    def cross_entropy(p, q, given=None):
        pdf = mvprob.probs(p, given)
        pdf['given_prob'] = mvprob.probs(p, given) if given is not None else 1.0
        pdf['q'] = mvprob.probs(q)
        pdf = pdf.apply(lambda e: e.iloc[2] * math.log2(e.iloc[1] / e.iloc[0]))
        return pdf.sum()
