import math
import unittest

import numpy as np
import pandas as pd

from information import BitPy, EntroPy
from probability.mvprob import cprobs, probs, probs_dict
from utilities.pyutils import discretize_pair


def frame(values, name="state"):
    return pd.DataFrame({name: values})


class EntropyTests(unittest.TestCase):
    def test_known_entropies(self):
        for values, expected in [([0]*8, 0), ([0, 1]*4, 1), ([0, 1, 2, 3]*2, 2)]:
            with self.subTest(values=values):
                self.assertAlmostEqual(EntroPy.shannon_entropy(frame(values)), expected)

    def test_skewed_entropy(self):
        self.assertAlmostEqual(EntroPy.shannon_entropy(frame([0, 0, 0, 1])), 0.8112781244591328)

    def test_categorical_and_series(self):
        self.assertEqual(EntroPy.shannon_entropy(pd.Series(["ok", "fail"]*4)), 1)

    def test_unused_categories_do_not_create_infinity(self):
        data = frame(pd.Categorical(["a", "a"], categories=["a", "b", "c"]))
        result = BitPy(data).as_df()
        self.assertEqual(len(result), 1)
        self.assertEqual(BitPy(data).entropy, 0)
        self.assertTrue(np.isfinite(result.to_numpy()).all())

    def test_bin_empty_states(self):
        result = BitPy(frame([0, 1]*4), bins=10)
        self.assertEqual(result.entropy, 1)
        self.assertEqual(len(result.probs()), 2)

    def test_no_implicit_binning_of_discrete_values(self):
        self.assertAlmostEqual(EntroPy.shannon_entropy(frame(range(20))), math.log2(20))

    def test_reserved_column_names_do_not_overwrite_input(self):
        for name in ["probs", "bits", "weighted_bits", "prob"]:
            data = frame([0, 1], name)
            original = data.copy()
            self.assertEqual(BitPy(data).entropy, 1)
            pd.testing.assert_frame_equal(data, original)

    def test_cross_entropy_and_kl_known_values(self):
        p, q = frame([0]*3 + [1]), frame([0]*9 + [1], "reference")
        self.assertAlmostEqual(EntroPy.cross_entropy(p, q), 0.9444843438056281)
        self.assertAlmostEqual(EntroPy.relative_entropy(p, q), 0.13320621934649512)
        self.assertNotAlmostEqual(EntroPy.relative_entropy(p, q), EntroPy.relative_entropy(q, p))

    def test_missing_reference_state_is_infinite(self):
        for bins in [None, 10]:
            p, q = frame([0, 1]*4), frame([100, 101]*4)
            self.assertTrue(math.isinf(EntroPy.cross_entropy(p, q, bins)))
            self.assertTrue(math.isinf(EntroPy.relative_entropy(p, q, bins)))

    def test_reference_only_state_is_allowed(self):
        self.assertEqual(EntroPy.cross_entropy(frame([0, 0]), frame([0, 1])), 1)
        self.assertEqual(EntroPy.relative_entropy(frame([0, 0]), frame([0, 1])), 1)

    def test_identical_distributions(self):
        p = frame(["a"]*3 + ["b"])
        self.assertEqual(EntroPy.relative_entropy(p, p), 0)
        self.assertAlmostEqual(EntroPy.cross_entropy(p, p), EntroPy.shannon_entropy(p))

    def test_shared_bins_and_kl_identity(self):
        p, q = frame([0, 1, 2, 3]), frame([0, 2, 4, 6]*2)
        p_bins, q_bins = discretize_pair(p, q, 2)
        self.assertEqual(p_bins[0].tolist(), [0, 0, 0, 0])
        self.assertEqual(q_bins[0].tolist(), [0, 0, 1, 1]*2)
        self.assertEqual(EntroPy.relative_entropy(p, q, 2), 1)
        self.assertAlmostEqual(EntroPy.cross_entropy(p, q, 2),
                               EntroPy.shannon_entropy(p_bins) + EntroPy.relative_entropy(p, q, 2))

    def test_multivariate_distribution_matches_columns_by_position(self):
        p = pd.DataFrame({"a": [0, 0, 1, 1], "b": ["x", "y", "x", "y"]})
        q = p.rename(columns={"a": "c", "b": "d"}).iloc[::-1]
        self.assertEqual(EntroPy.relative_entropy(p, q), 0)
        self.assertEqual(EntroPy.cross_entropy(p, q), 2)

    def test_joint_conditional_and_mi(self):
        x, y = frame([0, 1]*4), frame([0, 0, 1, 1]*2)
        self.assertEqual(EntroPy.joint_entropy(x, y), 2)
        self.assertEqual(EntroPy.conditional_entropy(x, y), 1)
        self.assertEqual(EntroPy.mutual_information(x, y), 0)
        self.assertEqual(EntroPy.mutual_information(x, x), 1)
        self.assertEqual(EntroPy.conditional_entropy(x, x), 0)

    def test_xor_joint_state(self):
        x, y = frame([0, 0, 1, 1]), frame([0, 1, 0, 1])
        z = frame([0, 1, 1, 0])
        self.assertEqual(EntroPy.mutual_information(x, z), 0)
        self.assertEqual(EntroPy.mutual_information(pd.concat([x, y.rename(columns={"state": "y"})], axis=1), z), 1)

    def test_transfer_entropy_direction_and_index(self):
        # A cyclic binary de Bruijn sequence gives every triple exactly once.
        source_cycle = [0, 0, 0, 1, 0, 1, 1, 1]
        source = frame(source_cycle + source_cycle[:1])
        target = frame(source_cycle[-1:] + source_cycle)
        for index in [range(9), pd.date_range("2026-01-01", periods=9), range(20, 29)]:
            source.index = target.index = index
            self.assertEqual(EntroPy.transfer_entropy(target, source), 1)
            self.assertEqual(EntroPy.transfer_entropy(source, target), 0)
            self.assertEqual(EntroPy.transfer_entropy(source, source), 0)

    def test_multivariate_transfer_entropy(self):
        source = frame([0, 0, 0, 1, 0, 1, 1, 1, 0])
        target = frame([1, 0, 0, 0, 1, 0, 1, 1, 1])
        target["constant"] = "on"
        self.assertEqual(EntroPy.transfer_entropy(target, source), 1)

    def test_transfer_entropy_lag_two(self):
        cycle = [0, 0, 0, 1, 0, 1, 1, 1]
        source, target = frame(cycle + cycle[:2]), frame(cycle[-2:] + cycle)
        self.assertEqual(EntroPy.transfer_entropy(target, source, lag=2), 1)

    def test_probability_column_name_collision(self):
        result = probs(frame([0, 1], "prob"))
        self.assertEqual(result.columns.tolist(), ["state_0", "prob"])
        self.assertEqual(result["prob"].tolist(), [0.5, 0.5])

    def test_probability_helpers(self):
        p, given = frame([0, 0, 1, 1]), frame([0, 0, 0, 1])
        self.assertEqual(probs_dict(p), {0: 0.5, 1: 0.5})
        self.assertEqual(probs(p, key="x").columns[-1], "prob_x")
        conditional = cprobs(p, given)["prob"]
        self.assertAlmostEqual(conditional.loc[(0, 0)], 2/3)
        self.assertAlmostEqual(conditional.loc[(1, 0)], 1/3)
        self.assertEqual(conditional.loc[(1, 1)], 1)

    def test_invalid_inputs(self):
        for data in [pd.DataFrame(), frame([None]), frame([np.nan]), frame([np.inf])]:
            with self.subTest(data=data), self.assertRaises(ValueError):
                EntroPy.shannon_entropy(data)
        with self.assertRaises(TypeError):
            EntroPy.shannon_entropy([0, 1])
        with self.assertRaises(ValueError):
            EntroPy.shannon_entropy(pd.DataFrame([[1, 2]], columns=["x", "x"]))

    def test_invalid_bins(self):
        for bins in [0, -1, 1.5, True]:
            with self.subTest(bins=bins), self.assertRaises(ValueError):
                EntroPy.shannon_entropy(frame([0, 1]), bins)

    def test_invalid_lags(self):
        for lag in [0, -1, 4, True, 1.5]:
            with self.subTest(lag=lag), self.assertRaises(ValueError):
                EntroPy.transfer_entropy(frame([0]*4), frame([1]*4), lag=lag)

    def test_misaligned_observations_rejected(self):
        x, y = frame([0, 1]), frame([1, 0])
        y.index = [1, 2]
        for method in [EntroPy.joint_entropy, EntroPy.conditional_entropy,
                       EntroPy.mutual_information, EntroPy.transfer_entropy, cprobs]:
            with self.subTest(method=method), self.assertRaises(ValueError):
                method(x, y)

    def test_dimension_mismatch_rejected(self):
        with self.assertRaises(ValueError):
            EntroPy.relative_entropy(frame([0, 1]), pd.DataFrame({"x": [0], "y": [1]}))

    def test_against_scipy_on_random_distributions(self):
        try:
            from scipy.stats import entropy
        except ImportError:
            self.skipTest("install .[dev] for independent SciPy reference checks")
        rng = np.random.default_rng(712)
        for _ in range(30):
            pc, qc = rng.integers(1, 30, size=(2, 8))
            p, q = pc / pc.sum(), qc / qc.sum()
            x, y = frame(np.repeat(range(8), pc)), frame(np.repeat(range(8), qc))
            self.assertAlmostEqual(EntroPy.shannon_entropy(x), entropy(p, base=2))
            self.assertAlmostEqual(EntroPy.relative_entropy(x, y), entropy(p, q, base=2))
            self.assertAlmostEqual(EntroPy.cross_entropy(x, y), entropy(p, base=2) + entropy(p, q, base=2))


if __name__ == "__main__":
    unittest.main()
