import itertools
import random
import unittest
from model import assemble, overlap

class AssemblyTests(unittest.TestCase):
    def test_overlap(self):
        self.assertEqual(overlap("tide", "delta"), 2)
        self.assertEqual(overlap("aa", "bb"), 0)

    def test_containment_and_duplicates(self):
        self.assertEqual(assemble(["moon", "oo", "moon"])["text"], "moon")

    def test_unique_chain(self):
        result = assemble(["dawn", "awning", "ingot"])
        self.assertEqual(result["text"], "dawningot")
        self.assertFalse(result["ambiguous"])

    def test_tied_solution(self):
        result = assemble(["ba", "ab"])
        self.assertEqual(result["text"], "aba")
        self.assertTrue(result["ambiguous"])

    def test_order_independence(self):
        self.assertEqual(assemble(["red", "eddy"])["text"], assemble(["eddy", "red"])["text"])

    def test_reject_bad_inputs(self):
        for value in [[], "abc", [" "], [3], ["x"*257], [str(i)+"!" for i in range(13)]]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                assemble(value)

    def test_random_cases_against_exhaustive_oracle(self):
        rng = random.Random(17)
        for _ in range(40):
            parts = rng.sample(["aa","ab","ac","ba","bb","bc","ca","cb","cc"], 4)
            candidates = set()
            for order in itertools.permutations(parts):
                text = order[0]
                for part in order[1:]:
                    if part not in text:
                        text += part[1:] if text.endswith(part[0]) else part
                candidates.add(text)
            size = min(map(len, candidates))
            best = sorted(s for s in candidates if len(s)==size)
            got = assemble(parts)
            self.assertEqual((got["text"],got["ambiguous"]), (best[0],len(best)>1))
