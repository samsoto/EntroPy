import pandas as pd
import math
from probability import mvprob

class EntroPy(object):

    @staticmethod
    def kl_divergence(p, q):
        pass

    @staticmethod
    def self_information(p, a):
        pass

    @staticmethod
    def mutual_information(p, q, given=None):
        pass

    @staticmethod
    def entropy(p, a=1, cross=None, given=None):
        pass

    @staticmethod
    def shannon_entropy(p: pd.DataFrame, given=None):
        pdf = mvprob.prob(p, given)
        pdf['given_prob'] = mvprob.prob(p, given) if given is not None else 1.0
        pdf = pdf.apply(lambda e: e.iloc[0] * math.log2(e.iloc[1]/e.iloc[0]))
        return pdf.sum()

    @staticmethod
    def reyi_entropy(p, a):
        pass

    @staticmethod
    def transfer_entropy(p, q):
        pass

    @staticmethod
    def cross_entropy(p, q):
        pass
