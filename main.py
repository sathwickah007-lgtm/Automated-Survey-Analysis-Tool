
import csv
import json
import sys
from pathlib import Path
positive_words = [
    "excellent", "happy", "friendly", "helpful",
    "good", "great", "amazing", "satisfied",
    "love", "wonderful", "quick"
]

negative_words = [
    "poor", "rude", "late", "bad", "slow",
    "long", "angry", "unhappy", "terrible",
    "worst", "not respond"
]

complaint_categories = {
    "Staff behaviour": ["rude", "angry"],
    "Delays and waiting": ["late", "slow", "long", "waiting time"],
    "Customer support": ["not respond", "support"],
    "Poor experience": ["poor", "bad", "unhappy", "terrible", "worst"],
    "Positive staff feedback": ["friendly", "helpful"],
    "Positive product feedback": ["product was good", "product was excellent", "great product"]
}

negative_keyword_counts = {}

for word in negative_words:
    negative_keyword_counts[word] = 0

input_file = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / "survey_responses.csv"

with open(input_file, "r", newline="", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file)

    if reader.fieldnames is None or "Rating" not in reader.fieldnames or "Feedback" not in reader.fieldnames:
        print("Error: CSV must contain Rating and Feedback columns.")
        exit()

    all_responses = list(reader)

missing_count = 0

for response in all_responses:
    if response["Rating"] == "":
        missing_count += 1

print("Total responses in CSV:", len(all_responses))
print("Missing ratings in CSV:", missing_count)

valid_responses = []
invalid_count = 0

for response in all_responses:
    rating_text = response["Rating"].strip()

    if rating_text == "":
        continue

    elif not rating_text.isdigit():
        invalid_count += 1
        continue

    elif int(rating_text) < 1 or int(rating_text) > 5:
        invalid_count += 1
        continue

    valid_responses.append(response)

responses = valid_responses
feedback_responses = []
missing_feedback_count = 0
junk_feedback_count = 0

for response in all_responses:
    feedback = response.get("Feedback", "").strip()

    if feedback == "":
        missing_feedback_count += 1

    elif not any(char.isalpha() for char in feedback):
        junk_feedback_count += 1

    else:
        feedback_responses.append(response)

print("Missing feedback:", missing_feedback_count)
print("Junk feedback skipped:", junk_feedback_count)
print("Usable feedback responses:", len(feedback_responses))
print("Invalid ratings skipped:", invalid_count)
print("\nCustomer feedback:")

for response in feedback_responses:
    print(response["Feedback"])

print("Total survey responses:", len(responses))

total_rating = 0

for response in responses:
    rating = int(response["Rating"])
    total_rating = total_rating + rating

if len(responses) > 0:
    average_rating = total_rating / len(responses)
    print("Average customer rating:", round(average_rating, 2))
else:
    average_rating = 0
    print("Average customer rating: No valid responses")


five_star_count = 0

for response in responses:
    rating = int(response["Rating"])

    if rating == 5:
        five_star_count = five_star_count + 1

print("Five-star ratings:", five_star_count)

low_rating_count = 0

for response in responses:
    rating = int(response["Rating"])

    if rating == 1 or rating == 2:
        low_rating_count = low_rating_count + 1

print("Low ratings (1 or 2):", low_rating_count)


if len(responses) > 0:
    five_star_percentage = (five_star_count / len(responses)) * 100
    print("Five-star rating percentage:", round(five_star_percentage, 2), "%")
else:
    five_star_percentage = 0
    print("Five-star rating percentage: No valid responses")

rating_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}

for response in responses:
    rating = int(response["Rating"])
    rating_counts[rating] += 1

print("Rating distribution:")

for rating in rating_counts:
    print(rating, "star:", rating_counts[rating])

satisfied_count = 0

for response in responses:
    rating = int(response["Rating"])

    if rating >= 4:
        satisfied_count += 1

if len(responses) > 0:
    csat_percentage = (satisfied_count / len(responses)) * 100
    print("CSAT:", round(csat_percentage, 2), "%")
else:
    csat_percentage = 0
    print("CSAT: No valid responses")

print("\nPositive words found in customer feedback:")

for response in feedback_responses:
    feedback = response["Feedback"].lower()

    for word in positive_words:
        if word in feedback:
            print(word, "->", response["Feedback"])

negative_feedback_count = 0

print("\nNegative words found in customer feedback:")

for response in feedback_responses:
    feedback = response["Feedback"].lower()
    found_negative = False

    for word in negative_words:
        if word in feedback:
            print(word, "->", response["Feedback"])
            found_negative = True

    if found_negative:
        negative_feedback_count += 1

print("Comments containing negative words:", negative_feedback_count)

positive_feedback_count = 0

for response in feedback_responses:
    feedback = response["Feedback"].lower()
    
    found_positive = False

    for word in positive_words:
        if word in feedback:
            found_positive = True

    if found_positive:
        positive_feedback_count += 1

print("Comments containing positive words:", positive_feedback_count)

if len(feedback_responses) > 0:
    positive_percentage = (positive_feedback_count / len(feedback_responses)) * 100
    negative_percentage = (negative_feedback_count / len(feedback_responses)) * 100

    print("Positive feedback percentage:", round(positive_percentage, 2), "%")
    print("Negative feedback percentage:", round(negative_percentage, 2), "%")
else:
    positive_percentage = 0
    negative_percentage = 0

    print("Positive feedback percentage: No valid responses")
    print("Negative feedback percentage: No valid responses")


print("\nNegative keyword frequency:")

for response in feedback_responses:
    feedback = response["Feedback"].lower()

    for word in negative_words:
        if word in feedback:
            negative_keyword_counts[word] += 1

for word in negative_keyword_counts:
    if negative_keyword_counts[word] > 0:
        print(word, ":", negative_keyword_counts[word])

print("\nMost Common Customer Complaints:")

highest_count = 0
most_common_complaints = []

for word in negative_keyword_counts:
    count = negative_keyword_counts[word]

    if count > highest_count:
        highest_count = count
        most_common_complaints = [word]
    elif count == highest_count and count > 0:
        most_common_complaints.append(word)

if highest_count > 0:
    for word in most_common_complaints:
        print(word, ":", highest_count, "mention(s)")
else:
    print("No negative keywords found.")

category_counts = {}

for category in complaint_categories:
    category_counts[category] = 0

for response in feedback_responses:
    feedback = response["Feedback"].lower()

    for category in complaint_categories:
        for word in complaint_categories[category]:
            if word in feedback:
                category_counts[category] += 1
                break

print("\nComplaint Category Summary:")

for category in category_counts:
    if category.startswith("Positive"):
        continue
    print(category, ":", category_counts[category], "comment(s)")

print("\nPositive Feedback Aspects:")

for category in category_counts:
    if category.startswith("Positive"):
        print(category, ":", category_counts[category], "comment(s)")

sentiment_counts = {
    "Positive": 0,
    "Negative": 0,
    "Mixed": 0,
    "Neutral": 0
}

print("\nFeedback labels:")

for response in feedback_responses:
    feedback = response["Feedback"].lower()
    found_positive = False
    found_negative = False

    negative_phrases = ["not good", "not helpful", "not happy", "not satisfied", "not friendly", "not excellent"]
    has_negative_phrase = any(phrase in feedback for phrase in negative_phrases)

    for word in positive_words:
        if word in feedback:
            found_positive = True

    for word in negative_words:
        if word in feedback:
            found_negative = True

    if found_positive and found_negative:
        label = "Mixed"
    elif has_negative_phrase:
        label = "Negative"
    elif found_positive:
        label = "Positive"
    elif found_negative:
        label = "Negative"
    else:
        label = "Neutral"
sentiment_results = []

sentiment_counts = {
    "Positive": 0,
    "Negative": 0,
    "Mixed": 0,
    "Neutral": 0
}

negative_phrases = [
    "not good", "not helpful", "not happy",
    "not satisfied", "not friendly", "not excellent"
]

for response in feedback_responses:
    feedback = response["Feedback"].lower()

    found_positive = any(word in feedback for word in positive_words)
    found_negative = any(word in feedback for word in negative_words)
    has_negative_phrase = any(
        phrase in feedback for phrase in negative_phrases
    )

    if found_positive and found_negative:
        label = "Mixed"
    elif has_negative_phrase:
        label = "Negative"
    elif found_positive:
        label = "Positive"
    elif found_negative:
        label = "Negative"
    else:
        label = "Neutral"

    sentiment_counts[label] += 1

    sentiment_results.append({
        "feedback": response["Feedback"],
        "sentiment": label
    })

    print(label, "->", response["Feedback"])



print("\nSentiment percentages:")

if len(feedback_responses) > 0:
    for label in sentiment_counts:
        percentage = (sentiment_counts[label] / len(feedback_responses)) * 100
        print(label, ":", round(percentage, 2), "%")
else:
    print("No valid responses to calculate sentiment percentages.")


print("\nBusiness Insight:")


if len(responses) == 0:
    print("Customer satisfaction cannot be evaluated without valid responses.")
elif csat_percentage >= 70:
    print("Customer satisfaction looks good.")
else:
    print("Customer satisfaction needs improvement.")


highest_category_count = 0
top_categories = []

for category in category_counts:
    if category.startswith("Positive"):
        continue

    count = category_counts[category]

    if count > highest_category_count:
        highest_category_count = count
        top_categories = [category]
    elif count == highest_category_count and count > 0:
        top_categories.append(category)

if highest_category_count > 0:
    print("\nMost reported complaint category:")

    for category in top_categories:
        print(category, "-", highest_category_count, "comment(s)")

        if category == "Delays and waiting":
            print("Recommendation: Review delivery times and waiting processes.")
        elif category == "Staff behaviour":
            print("Recommendation: Review staff communication and service training.")
        elif category == "Customer support":
            print("Recommendation: Improve customer support response times.")
        elif category == "Poor experience":
            print("Recommendation: Investigate the causes of poor customer experiences.")
else:
    print("No complaints matched the defined categories.")


# Save analysis results to a JSON file
results = {
    "total_responses": len(all_responses),
    "valid_ratings": len(responses),
    "missing_ratings": missing_count,
    "invalid_ratings": invalid_count,
    "usable_feedback": len(feedback_responses),
    "average_rating": round(average_rating, 2) if responses else None,
    "five_star_ratings": five_star_count,
    "low_ratings": low_rating_count,
    "rating_distribution": rating_counts,
    "csat_percentage": round(csat_percentage, 2),
    "positive_feedback_count": positive_feedback_count,
    "negative_feedback_count": negative_feedback_count,
    "positive_feedback_percentage": round(positive_percentage, 2),
    "negative_feedback_percentage": round(negative_percentage, 2),
    "negative_keyword_frequency": negative_keyword_counts,
    "complaint_categories": {
        category: count
        for category, count in category_counts.items()
        if not category.startswith("Positive")
    },
    "positive_feedback_aspects": {
        category: count
        for category, count in category_counts.items()
        if category.startswith("Positive")
    },
    "sentiment_counts": sentiment_counts,
    "sentiment_results": sentiment_results,
    "top_complaint_categories": top_categories
}

with open("survey_analysis_results.json", "w", encoding="utf-8") as file:
    json.dump(results, file, indent=4)

print("\nAnalysis results saved to survey_analysis_results.json")









   




