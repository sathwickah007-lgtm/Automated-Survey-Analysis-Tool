
import json
import matplotlib.pyplot as plt

# Read results from the JSON file
with open("survey_analysis_results.json", "r", encoding="utf-8") as file:
    results = json.load(file)

# Get rating distribution automatically
rating_distribution = results["rating_distribution"]

ratings = [int(star) for star in rating_distribution.keys()]
counts = list(rating_distribution.values())

# Create the chart
plt.bar(ratings, counts)

plt.xlabel("Star Rating")
plt.ylabel("Number of Customers")
plt.title("Customer Rating Distribution")
plt.xticks(ratings)
plt.tight_layout()

plt.savefig("rating_distribution.png")
plt.show()
