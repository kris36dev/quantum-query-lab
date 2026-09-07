import itertools
import unittest
import numpy as np
from algorithms import walsh, deutsch_jozsa, classical_dj, simon_table, simon_probabilities, recover_secret, gf2_nullspace


class QueryTests(unittest.TestCase):
    def test_walsh_unitarity(self):
        for n in range(1, 5):
            w = walsh(n)
            np.testing.assert_allclose(w @ w.T, np.eye(2**n), atol=1e-14)

    def test_all_three_bit_promised_oracles(self):
        for table in itertools.product((0, 1), repeat=8):
            if sum(table) in (0, 4, 8):
                p = deutsch_jozsa(table)
                self.assertAlmostEqual(p.sum(), 1)
                self.assertAlmostEqual(p[0], int(sum(table) in (0, 8)))
                label, cost = classical_dj(table)
                self.assertEqual(label == 'constant', p[0] > .5)
                self.assertLessEqual(cost, 5)

    def test_simon_promise_all_small_secrets(self):
        for n in range(2, 5):
            for secret in range(1, 2**n):
                table = simon_table(n, secret)
                self.assertTrue(all(table[x] == table[x ^ secret] for x in range(2**n)))
                self.assertTrue(all(v == 2 for v in np.unique(table, return_counts=True)[1]))
                p = simon_probabilities(n, secret)
                expected = [0 if (y & secret).bit_count() % 2 else 2/2**n for y in range(2**n)]
                np.testing.assert_allclose(p, expected, atol=1e-14)
                self.assertEqual(recover_secret(np.flatnonzero(p > 1e-10), n), secret)

    def test_underdetermined_samples(self):
        self.assertIsNone(recover_secret([0], 4))
        self.assertEqual(len(gf2_nullspace([], 4)), 4)

    def test_reject_broken_promise(self):
        with self.assertRaises(ValueError):
            deutsch_jozsa([0, 0, 0, 1])
        with self.assertRaises(ValueError):
            simon_table(3, 0)


if __name__ == '__main__':
    unittest.main()
