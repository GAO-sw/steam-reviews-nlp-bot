# analyzer.py
import pandas as pd
from textblob import TextBlob


def get_polarity(text):
    """Calculate the sentiment polarity score of a text (-1.0 to 1.0)"""
    return TextBlob(str(text)).sentiment.polarity


def get_sentiment_label(score):
    """Categorize score into Positive, Negative, or Neutral label"""
    if score > 0.05:
        return "Positive"
    elif score < -0.05:
        return "Negative"
    else:
        return "Neutral"


def analyze_reviews(reviews):
    """
    Analyze reviews using pandas and TextBlob.
    Returns sentiment statistics and keyword frequencies.
    """
    if not reviews:
        return None, None, None

    # Load reviews into a pandas DataFrame
    df = pd.DataFrame(reviews, columns=["review_text"])

    # Calculate sentiment polarity and labels without using lambda functions
    df["polarity"] = df["review_text"].apply(get_polarity)
    df["sentiment"] = df["polarity"].apply(get_sentiment_label)

    # 1. Count sentiment distributions
    sentiment_counts = df["sentiment"].value_counts().to_dict()
    for label in ["Positive", "Negative", "Neutral"]:
        sentiment_counts.setdefault(label, 0)

    # Calculate percentage for non-neutral reviews
    total_polarized = sentiment_counts["Positive"] + sentiment_counts["Negative"]
    pos_percent = (
        round((sentiment_counts["Positive"] / total_polarized * 100), 1)
        if total_polarized > 0
        else 0
    )
    neg_percent = (
        round((sentiment_counts["Negative"] / total_polarized * 100), 1)
        if total_polarized > 0
        else 0
    )
    sentiment_counts["pos_ratio"] = pos_percent
    sentiment_counts["neg_ratio"] = neg_percent

    # 2. Filter positive and negative reviews
    df_positive = df[df["sentiment"] == "Positive"]
    df_negative = df[df["sentiment"] == "Negative"]

    # Keywords to count
    pos_keywords = ["fun", "story", "masterpiece", "amazing", "love"]
    neg_keywords = ["bug", "lag", "crash", "waste", "bad"]

    # Count keywords in positive reviews
    pos_kw_counts = {}
    for kw in pos_keywords:
        contains_kw = df_positive["review_text"].str.contains(kw, case=False, na=False)
        pos_kw_counts[kw] = int(contains_kw.sum())

    # Count keywords in negative reviews
    neg_kw_counts = {}
    for kw in neg_keywords:
        contains_kw = df_negative["review_text"].str.contains(kw, case=False, na=False)
        neg_kw_counts[kw] = int(contains_kw.sum())

    return sentiment_counts, pos_kw_counts, neg_kw_counts
