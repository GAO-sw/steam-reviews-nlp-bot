# pylint: disable=wrong-import-position
"""
Module for generating sentiment analysis charts using Matplotlib.
"""
import io

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def generate_charts(sentiment, pos_keywords, neg_keywords):
    """
    Generate professional donut chart and horizontal bar chart.
    """
    # Set standard sans-serif font
    plt.rcParams["font.sans-serif"] = "Arial"
    plt.rcParams["axes.unicode_minus"] = False

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5))
    fig.patch.set_facecolor("#F9F9FB")  # Set modern light gray background

    # ---- 1. Donut Chart ----
    labels_pie = ["Positive", "Neutral", "Negative"]
    sizes_pie = [sentiment["Positive"], sentiment["Neutral"], sentiment["Negative"]]
    colors_pie = ["#2ECC71", "#BDC3C7", "#E74C3C"]  # Morandi green, gray, red

    # Create donut chart by setting width=0.4
    _, texts, autotexts = ax1.pie(
        sizes_pie,
        labels=labels_pie,
        autopct="%1.1f%%",
        startangle=140,
        colors=colors_pie,
        wedgeprops=dict(width=0.4, edgecolor="w", linewidth=3),
        pctdistance=0.75,
    )

    # Customize text style
    for text in texts:
        text.set_color("#333333")
        text.set_fontsize(11)
    for autotext in autotexts:
        autotext.set_color("#FFFFFF")
        autotext.set_fontweight("bold")
        autotext.set_fontsize(11)

    # Put total reviews count in the center
    total_reviews = sum(sizes_pie)
    ax1.text(
        0,
        0,
        f"Total\n{total_reviews}",
        ha="center",
        va="center",
        fontsize=14,
        fontweight="bold",
        color="#2C3E50",
    )
    ax1.set_title(
        "Sentiment Distribution",
        fontsize=14,
        fontweight="bold",
        pad=20,
        color="#2C3E50",
    )

    # ---- 2. Horizontal Bar Chart ----
    words = list(pos_keywords.keys()) + list(neg_keywords.keys())
    counts = list(pos_keywords.values()) + list(neg_keywords.values())
    colors_bar = ["#2ECC71"] * 5 + ["#E74C3C"] * 5

    y_pos = range(len(words))

    # Plot horizontal bars
    bars = ax2.barh(
        y_pos, counts, color=colors_bar, height=0.6, edgecolor="#ffffff", alpha=0.9
    )
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(words, fontsize=11, fontweight="bold", color="#333333")
    ax2.invert_yaxis()  # Put top keywords on top

    # Add count values to the right of the bars
    for rect in bars:
        width = rect.get_width()
        ax2.text(
            width + 0.3,
            rect.get_y() + rect.get_height() / 2,
            f"{int(width)}",
            ha="left",
            va="center",
            fontsize=10,
            color="#555555",
            fontweight="bold",
        )

    # Style the bar chart axes
    ax2.set_facecolor("#F9F9FB")
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.spines["bottom"].set_color("#CCCCCC")
    ax2.spines["left"].set_color("#CCCCCC")
    ax2.xaxis.grid(True, linestyle="--", alpha=0.5, color="#CCCCCC")
    ax2.set_title(
        "Keyword Mentions (Green=Pos, Red=Neg)",
        fontsize=14,
        fontweight="bold",
        pad=20,
        color="#2C3E50",
    )

    plt.tight_layout()

    # Save chart to a memory buffer
    img_buf = io.BytesIO()
    plt.savefig(
        img_buf,
        format="png",
        dpi=150,
        bbox_inches="tight",
        facecolor=fig.get_facecolor(),
    )
    img_buf.seek(0)

    plt.close(fig)
    return img_buf
