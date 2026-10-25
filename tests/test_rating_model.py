import unittest

from rating_model import ContentRating, RATING_FACTORS


def rating_data(score=5, explanation="A short justification."):
    return {
        factor: {"score": score, "explanation": explanation}
        for factor in RATING_FACTORS
    }


class ContentRatingTests(unittest.TestCase):
    def test_valid_rating_calculates_overall_score(self):
        data = rating_data()
        data["curiosity_gap"]["score"] = 10
        data["broad_appeal"]["score"] = 0

        rating = ContentRating.from_dict(data)

        self.assertEqual(rating.raw_overall_score, 50.0)
        self.assertEqual(rating.overall_score, 50.0)
        self.assertEqual(rating.to_dict()["overall_score"], 50.0)
        self.assertEqual(rating.to_dict()["curiosity_gap"]["explanation"],
                         "A short justification.")

    def test_minimum_scores_produce_zero(self):
        rating = ContentRating.from_dict(rating_data(score=0))

        self.assertEqual(rating.overall_score, 0.0)

    def test_maximum_scores_produce_one_hundred(self):
        rating = ContentRating.from_dict(rating_data(score=10))

        self.assertEqual(rating.overall_score, 100.0)

    def test_decimal_scores_keep_precision_and_round_output(self):
        rating = ContentRating.from_dict(rating_data(score=1.234))

        self.assertAlmostEqual(rating.raw_overall_score, 12.34)
        self.assertEqual(rating.overall_score, 12.34)

    def test_missing_factor_is_rejected(self):
        data = rating_data()
        del data["consequence"]

        with self.assertRaisesRegex(ValueError, "missing rating factors: consequence"):
            ContentRating.from_dict(data)

    def test_out_of_range_scores_are_rejected(self):
        for score in (-0.01, 10.01):
            with self.subTest(score=score):
                with self.assertRaisesRegex(ValueError, "score must be"):
                    ContentRating.from_dict(rating_data(score=score))


if __name__ == "__main__":
    unittest.main()
