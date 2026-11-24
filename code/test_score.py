"""Tests for score.py. Run from the repository root: python3 -m unittest discover -s code"""
import unittest
from score import DEFAULT_MIN_NUMBER, nums, norm, score_answer, toks

Q = "ما نص المادة؟"
REF = "مادة ١ - يؤذن لكل من العشرين مواطناً بالحصول على القرض خلال ٣٠ يوماً"


class Normalisation(unittest.TestCase):
    def test_arabic_indic_digits_become_western(self):
        self.assertEqual(nums("مادة ١٢ لسنة ٢٠٢٠"), {"12", "2020"})

    def test_diacritics_and_alef_variants_are_ignored(self):
        self.assertEqual(toks("أُحمد"), toks("احمد"))

    def test_short_words_are_dropped(self):
        self.assertNotIn("من", toks("من الدولة"))


class Scoring(unittest.TestCase):
    def test_exact_copy_is_correct(self):
        self.assertEqual(score_answer(Q, REF, REF)[0], "correct")

    def test_missing_number_fails_even_with_all_words(self):
        label, recall, number_recall = score_answer(Q, REF, "يؤذن لكل من العشرين مواطناً بالحصول على القرض خلال يوماً")
        self.assertGreaterEqual(recall, 0.6)
        self.assertEqual(number_recall, 0.0)
        self.assertEqual(label, "wrong_or_partial")

    def test_ordinal_word_is_not_counted_as_the_number_one(self):
        # "المادة الأولى" for "مادة ١": the published rule does not accept this, see docs/SCORING.md
        answer = "المادة الأولى يؤذن لكل من العشرين مواطناً بالحصول على القرض خلال ٣٠ يوماً"
        self.assertEqual(score_answer(Q, REF, answer)[0], "wrong_or_partial")

    def test_decline_is_declined(self):
        self.assertEqual(score_answer(Q, REF, "لا أعلم")[0], "declined")

    def test_reference_without_numbers_ignores_the_number_rule(self):
        label, _, number_recall = score_answer(Q, "يؤذن لكل مواطن بالحصول على القرض", "يؤذن لكل مواطن بالحصول على القرض")
        self.assertIsNone(number_recall)
        self.assertEqual(label, "correct")

    def test_thresholds_can_be_changed(self):
        half = "يؤذن لكل من العشرين مواطناً"
        self.assertEqual(score_answer(Q, REF, half, min_recall=0.9)[0], "wrong_or_partial")

    def test_default_number_threshold_is_80_percent(self):
        self.assertEqual(DEFAULT_MIN_NUMBER, 0.8)


if __name__ == "__main__":
    unittest.main()
