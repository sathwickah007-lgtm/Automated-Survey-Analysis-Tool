
import json
from pathlib import Path
import streamlit as st
import matplotlib.pyplot as plt
import subprocess
import sys
import tempfile
st.set_page_config(
    page_title="Survey Analysis Dashboard",
    page_icon="📊",
    layout="wide"
)



st.title("Customer Survey Analytics")
st.write(
    "Monitor customer satisfaction, understand feedback, "
    "and identify areas for improvement."
)
st.caption("BUSINESS INSIGHTS • CUSTOMER EXPERIENCE")
st.subheader("📂 Upload Survey Data")

uploaded_file = st.file_uploader(
    "Choose a CSV file",
    type=["csv"]
)
if uploaded_file is not None:
    if st.button("Analyze Uploaded CSV"):
        with tempfile.NamedTemporaryFile(
            mode="wb",
            suffix=".csv",
            delete=False
        ) as temp_file:
            temp_file.write(uploaded_file.getvalue())
            temp_path = temp_file.name

        try:
            result = subprocess.run(
                [sys.executable, str(Path(__file__).parent / "main.py"), temp_path],
                cwd=str(Path(__file__).parent),
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                st.success("Uploaded CSV analyzed successfully!")
                st.subheader("📊 Survey Overview")
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Total Responses", results["total_responses"])
                col2.metric("Valid Ratings", results["valid_ratings"])
                col3.metric("Average Rating", f'{results["average_rating"]}/5')
                col4.metric("CSAT", f'{results["csat_percentage"]}%')
                st.divider()

                st.rerun()
            else:
                st.error("Analysis failed. Check the error below.")
                st.code(result.stderr or result.stdout)

        finally:
            Path(temp_path).unlink(missing_ok=True)
json_file = Path(__file__).parent / "survey_analysis_results.json"

if not json_file.exists():
    st.error("Results file not found. Please run main.py first.")
    st.stop()

with open(json_file, "r", encoding="utf-8") as file:
    results = json.load(file)
st.download_button(
    label="📥 Download Analysis Results (JSON)",
    data=json.dumps(results, indent=4),
    file_name="survey_analysis_results.json",
    mime="application/json"
)
st.success("Survey analysis results loaded successfully!")

# KPI cards
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Responses", results["total_responses"])
col2.metric("Valid Ratings", results["valid_ratings"])
col3.metric("Average Rating", f'{results["average_rating"]}/5')
col4.metric("CSAT", f'{results["csat_percentage"]}%')

st.divider()


# Rating and sentiment charts
rating_col, sentiment_col = st.columns(2, gap="large")

with rating_col:
    st.subheader("⭐ Rating Distribution")

    rating_data = results["rating_distribution"]
    ratings = list(rating_data.keys())
    counts = list(rating_data.values())

    fig1, ax1 = plt.subplots(figsize=(5, 4))
    bars = ax1.bar(ratings, counts, width=0.6)

    ax1.set_xlabel("Rating (out of 5)")
    ax1.set_ylabel("Number of Responses")
    ax1.set_title("Customer Ratings", pad=12)
    ax1.set_xticks(range(len(ratings)))
    ax1.set_xticklabels(ratings)
    ax1.bar_label(bars, padding=3)
    ax1.set_ylim(0, max(counts, default=1) + 1)

    fig1.tight_layout()
    st.pyplot(fig1, use_container_width=True)
    plt.close(fig1)

with sentiment_col:
    st.subheader("💬 Customer Feedback Sentiment")

    sentiment_data = results["sentiment_counts"]
    fig2, ax2 = plt.subplots(figsize=(5, 4))

    ax2.pie(
        sentiment_data.values(),
        labels=None,
        autopct="%1.1f%%",
        startangle=90,
        pctdistance=0.65
    )

    ax2.set_title("Feedback Sentiment", pad=12)
    ax2.legend(
        sentiment_data.keys(),
        title="Sentiment",
        loc="center left",
        bbox_to_anchor=(1.0, 0.5)
    )

    fig2.tight_layout()
    st.pyplot(fig2, use_container_width=True)
    plt.close(fig2)


st.caption(
    "Sentiment labels are based on the current project's "
    "keyword-based analysis."
)

st.divider()

# Complaint category analysis
st.subheader("⚠️ Complaint Category Analysis")

complaints = results["complaint_categories"]

if complaints:
    st.bar_chart(complaints)

    top_complaint = max(complaints, key=complaints.get)
    complaint_count = complaints[top_complaint]

    st.metric("Most Reported Complaint", top_complaint,
              f"{complaint_count} comments")

    st.info(
        f"Business recommendation: Review '{top_complaint}' "
        "and investigate ways to improve the customer experience."
    )
else:
    st.info("No complaint categories were found.")

st.divider()


# Individual customer feedback
st.divider()
# Business Recommendations
st.subheader("💡 Business Recommendations")

complaints = results["complaint_categories"]
positive_count = results["positive_feedback_count"]
negative_count = results["negative_feedback_count"]
csat = results["csat_percentage"]

if csat < 70:
    st.warning(
        f"Customer satisfaction is {csat}%. "
        "Review customer complaints and identify service improvements."
    )
else:
    st.success(
        f"Customer satisfaction is {csat}%. "
        "Continue monitoring feedback to maintain service quality."
    )

if complaints:
    top_complaint = max(complaints, key=complaints.get)
    top_count = complaints[top_complaint]

    if top_count > 0:
        st.info(
            f"**Priority area: {top_complaint}** — "
            f"Review the {top_complaint.lower()} issues reported "
            f"in {top_count} comment(s)."
        )

if negative_count > positive_count:
    st.write(
        "• Review negative feedback and investigate recurring customer problems."
    )
elif positive_count > 0:
    st.write(
        "• Continue practices that customers appreciate while addressing complaints."
    )

st.caption(
    "Recommendations are generated from the project's current "
    "keyword-based analysis and survey metrics."
)
st.divider()
st.subheader("💬 Individual Customer Feedback")

feedback_rows = results.get("sentiment_results", [])

if feedback_rows:
    sentiments = sorted({
        row["sentiment"] for row in feedback_rows
    })

    selected_sentiment = st.selectbox(
        "Filter feedback by sentiment",
        ["All"] + sentiments
    )

    if selected_sentiment == "All":
        filtered_rows = feedback_rows
    else:
        filtered_rows = [
            row for row in feedback_rows
            if row["sentiment"] == selected_sentiment
        ]

    st.caption(f"Showing {len(filtered_rows)} of {len(feedback_rows)} comments")

    st.dataframe(
        filtered_rows,
        use_container_width=True,
        hide_index=True
    )
    import pandas as pd

    feedback_df = pd.DataFrame(filtered_rows)

    st.download_button(
        label="📥 Download Filtered Feedback (CSV)",
        data=feedback_df.to_csv(index=False),
        file_name="filtered_customer_feedback.csv",
        mime="text/csv"
    )
    st.download_button(
    label="📄 Download Business Report (TXT)",
    data=(
        "CUSTOMER SURVEY BUSINESS REPORT\n"
        "================================\n\n"
        f"Total Responses: {results['total_responses']}\n"
        f"Valid Ratings: {results['valid_ratings']}\n"
        f"Average Rating: {results['average_rating']}/5\n"
        f"Customer Satisfaction (CSAT): {results['csat_percentage']}%\n\n"
        "SENTIMENT SUMMARY\n"
        "-----------------\n"
        f"Positive: {results['sentiment_counts']['Positive']}\n"
        f"Negative: {results['sentiment_counts']['Negative']}\n"
        f"Mixed: {results['sentiment_counts']['Mixed']}\n"
        f"Neutral: {results['sentiment_counts']['Neutral']}\n\n"
        "COMPLAINT CATEGORIES\n"
        "--------------------\n"
        + "\n".join(
            f"{category}: {count}"
            for category, count in results["complaint_categories"].items()
            if count > 0
        )
        + "\n\nTOP COMPLAINT AREAS\n"
        + "\n".join(
            f"- {category}"
            for category in results["top_complaint_categories"]
        )
    ),
    file_name="business_survey_report.txt",
    mime="text/plain"
)
else:
    st.info("No individual feedback results are available.")
