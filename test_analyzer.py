"""
Unit tests for the analyzer module.
"""
import unittest
from analyzer import get_polarity, get_sentiment_label, analyze_reviews


class TestAnalyzer(unittest.TestCase):
    """
    Test cases for checking sentiment scoring and review statistical analysis.
    """

    def test_get_polarity(self):
        """
        Test if positive text returns a sentiment polarity score greater than 0.
        """
        self.assertTrue(get_polarity("This game is absolutely amazing and fun!") > 0)
        self.assertTrue(get_polarity("This game is terrible, full of bugs and crash.") < 0)

    def test_get_sentiment_label(self):
        """
        Test the classification logic for sentiment labels based on scores.
        """
        self.assertEqual(get_sentiment_label(0.5), 'Positive')
        self.assertEqual(get_sentiment_label(-0.5), 'Negative')
        self.assertEqual(get_sentiment_label(0.0), 'Neutral')

    def test_analyze_reviews_empty(self):
        """
        Test if empty input is handled correctly and returns None values.
        """
        # Using underscores (_) for unused tuple variables to prevent W0612 warning
        sentiment, _, _ = analyze_reviews([])
        self.assertIsNone(sentiment)


if __name__ == '__main__':
    unittest.main()
