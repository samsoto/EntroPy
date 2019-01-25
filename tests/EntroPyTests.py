from information.entropy import EntroPy
import pandas as pd
import unittest


class EntroPyTests(unittest.TestCase):

    # ------------------------------------------------------------
    # Shannon Entropy Tests
    # ------------------------------------------------------------

    def test_shannon_entropy_zero_bits(self):
        x = pd.DataFrame([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], columns=['x'])
        entropy = EntroPy().shannon_entropy(x)
        self.assertEqual(entropy, 0.0)

    def test_shannon_entropy_one_bit(self):
        x = pd.DataFrame([0, 1, 0, 1, 0, 1, 0, 1, 0, 1], columns=['x'])
        entropy = EntroPy().shannon_entropy(x)
        self.assertEqual(entropy, 1.0)

    def test_shannon_entropy_two_bit(self):
        x = pd.DataFrame([0, 1, 2, 3, 0, 1, 2, 3], columns=['x'])
        entropy = EntroPy().shannon_entropy(x)
        self.assertEqual(entropy, 2.0)

    # ------------------------------------------------------------
    # Mutual Information Tests
    # ------------------------------------------------------------

    def test_mutual_information_zero_bits(self):
        x = pd.DataFrame([0, 1, 0, 1, 0, 1, 0, 1], columns=['x'])
        y = pd.DataFrame([0, 0, 1, 1, 0, 0, 1, 1], columns=['y'])
        entropy = EntroPy().mutual_information(x, y)
        self.assertEqual(entropy, 0.0)

    def test_mutual_information_one_bit(self):
        x = pd.DataFrame([0, 1, 0, 1, 0, 1, 0, 1], columns=['x'])
        y = pd.DataFrame([0, 1, 0, 1, 0, 1, 0, 1], columns=['y'])
        entropy = EntroPy().mutual_information(x, y)
        self.assertEqual(entropy, 1.0)

    # ------------------------------------------------------------
    # Cross Validation - Shannon, Relative, and Cross Entropy
    # ------------------------------------------------------------

    def test_shannon_relative_cross_entropy(self):
        x = pd.DataFrame([0, 2, 0, 2, 2, 1, 0, 1, 0, 2, 0, 1], columns=['x'])
        y = pd.DataFrame([0, 0, 1, 1, 2, 2, 2, 1, 2, 1, 0, 0], columns=['y'])
        relative = EntroPy().relative_entropy(x[:], y[:])
        cross = EntroPy().cross_entropy(x[:], y[:])
        shannon = EntroPy().shannon_entropy(x[:])
        self.assertAlmostEqual(cross, (relative + shannon), places=7)


if __name__ == '__main__':
    unittest.main()
