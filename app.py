# app.py
# -------------------------------
# EB Mall Feedback Sentiment Analysis
# Frontend + Backend Integration with Animations & Interactive Charts
# -------------------------------

# Step 1: Import Libraries
import streamlit as st
import pandas as pd
import os
from textblob import TextBlob
import matplotlib.pyplot as plt
import plotly.express as px
from streamlit_lottie import st_lottie
import requests

# -------------------------------
# Step 2: Set Background & Page Config
# -------------------------------
st.set_page_config(page_title="EB Mall Feedback", page_icon="📝", layout="wide")

# CSS for background image
st.markdown(
    """
    <style>
    .stApp {
        background-image: url('https://images.unsplash.com/photo-1564866657319-0c1f8c16f3ef?auto=format&fit=crop&w=1950&q=80');
        background-size: cover;
        background-position: center;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------------
# Step 3: Load Lottie Animation
# -------------------------------
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_feedback = load_lottieurl("https://assets6.lottiefiles.com/packages/lf20_x62chJ.json")

# -------------------------------
# Step 4: Build Input Form with Columns
# -------------------------------
col1, col2 = st.columns([1, 2])

with col1:
    st_lottie(lottie_feedback, speed=1, width=200, height=200)

with col2:
    st.title("📝 EB Mall Feedback Sentiment Classifier")
    st.write("Your opinion matters! Enter your details and feedback below:")

with st.form(key='feedback_form'):
    name = st.text_input("Name")
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    age = st.number_input("Age", min_value=1, max_value=120)
    email = st.text_input("Email")
    feedback = st.text_area("Your Feedback")
    submit_button = st.form_submit_button(label='💌 Submit Feedback')

# -------------------------------
# Step 5: Analyze Sentiment Using TextBlob
# -------------------------------
if submit_button and feedback.strip() != "":
    blob = TextBlob(feedback)
    polarity = blob.sentiment.polarity

    # Determine sentiment
    if polarity > 0:
        sentiment = "Positive"
        st.success(f"Sentiment: ✅ Positive")
    elif polarity < 0:
        sentiment = "Negative"
        st.error(f"Sentiment: ❌ Negative")
    else:
        sentiment = "Neutral"
        st.info(f"Sentiment: ⚪ Neutral")
    
    st.caption(f"Confidence (polarity score): {polarity:.2f}")
    st.balloons()  # Celebrate feedback submission

# -------------------------------
# Step 6: Generate Reports
# -------------------------------
report_file = "EB mall_feedback.csv"

if submit_button and feedback.strip() != "":
    record = {
        "Name": name,
        "Gender": gender,
        "Age": age,
        "Email": email,
        "Feedback": feedback,
        "Sentiment": sentiment
    }

    if os.path.exists(report_file):
        df_existing = pd.read_csv(report_file)
        df_existing = pd.concat([df_existing, pd.DataFrame([record])], ignore_index=True)
        df_existing.to_csv(report_file, index=False)
    else:
        df_new = pd.DataFrame([record])
        df_new.to_csv(report_file, index=False)

    st.success("Feedback saved successfully!")

# -------------------------------
# Step 7: Display Feedback Report
# -------------------------------
if st.checkbox("Show Feedback Report"):
    if os.path.exists(report_file):
        df_report = pd.read_csv(report_file)
        st.dataframe(df_report)
    else:
        st.warning("No feedback data available yet.")

# -------------------------------
# Step 8: Visualize Sentiment Distribution
# -------------------------------
if st.checkbox("Show Sentiment Charts"):
    if os.path.exists(report_file):
        df_report = pd.read_csv(report_file)

        # Interactive Pie Chart using Plotly
        st.subheader("Sentiment Distribution - Interactive Pie Chart")
        fig = px.pie(df_report, names='Sentiment', title='Sentiment Distribution', 
                     color='Sentiment', color_discrete_map={'Positive':'green','Negative':'red','Neutral':'gray'})
        st.plotly_chart(fig)

        # Bar chart using Streamlit
        st.subheader("Sentiment Distribution - Bar Chart")
        sentiment_counts = df_report['Sentiment'].value_counts()
        st.bar_chart(sentiment_counts)
    else:
        st.warning("No feedback data available to show charts.")
