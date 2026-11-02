
import json
import matplotlib.pyplot as plt

# Read the analysis results
with open("survey_analysis_results.json", "r", encoding="utf-8") as file:
    results = json.load(file)

# Get sentiment counts
sentiments = results["sentiment_counts"]
labels = list(sentiments.keys())
counts = list(sentiments.values())

# Create a pie chart
plt.pie(
    counts,
    labels=labels,
    autopct=lambda pct: f"{pct:.1f}%\n({round(pct * sum(counts) / 100)} comments)",
    startangle=90
)
plt.title("Customer Feedback Sentiment")
plt.tight_layout()

# Save and display the chart
plt.savefig("sentiment_distribution.png")
plt.show()
