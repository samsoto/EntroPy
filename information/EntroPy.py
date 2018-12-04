import pandas as pd


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
        p['p'] = 0.0
        p = p.groupby([0]).count()
        p['p'] = p['0'] / len(p)
        pass

    @staticmethod
    def reyi_entropy(p, a):
        pass

    @staticmethod
    def transfer_entropy(p, q):
        pass

    @staticmethod
    def cross_entropy(p, q):
        pass
