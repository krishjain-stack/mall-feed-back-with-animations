# app.py
# -------------------------------
# EB Mall Feedback Sentiment Analysis
# Enhanced with Electric Border, Cursor Glow, Animations, Charts
# -------------------------------

# -------------------------------
# Step 1: Import Libraries
# -------------------------------
import streamlit as st
import pandas as pd
import os
from textblob import TextBlob
import matplotlib.pyplot as plt
import plotly.express as px
import requests

# -------------------------------
# Step 2: Custom CSS & Electric Border
# -------------------------------
st.markdown("""
<style>
/* Glow effect for input fields */
input[type="text"], textarea, select, input[type="number"] {
    border: 2px solid #ddd;
    border-radius: 8px;
    padding: 8px;
    transition: all 0.3s ease-in-out;
}
input[type="text"]:hover, textarea:hover, select:hover, input[type="number"]:hover,
input[type="text"]:focus, textarea:focus, select:focus, input[type="number"]:focus {
    box-shadow: 0 0 15px #00f3ff;
    border-color: #00f3ff;
}

/* Cursor-following glow */
body { cursor: none; }
.cursor-glow {
    position: fixed;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    pointer-events: none;
    background: rgba(0, 255, 255, 0.5);
    box-shadow: 0 0 20px rgba(0, 255, 255, 0.8);
    transform: translate(-50%, -50%);
    transition: transform 0.05s ease;
    z-index: 9999;
}

/* Electric Border */
.electric-border {
  --electric-light-color: rgba(125,249,255,0.8);
  --eb-border-width: 2px;
  position: relative;
  border-radius: 16px;
  overflow: visible;
  isolation: isolate;
  padding: 20px;
  margin-bottom: 20px;
  background: rgba(0,0,0,0.3);
}

.electric-border::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  border: var(--eb-border-width) solid var(--electric-light-color);
  box-shadow: 0 0 15px var(--electric-light-color), 0 0 30px var(--electric-light-color);
  pointer-events: none;
  animation: glow 2s infinite alternate;
}

@keyframes glow {
  0% { box-shadow: 0 0 10px var(--electric-light-color), 0 0 20px var(--electric-light-color);}
  50% { box-shadow: 0 0 20px var(--electric-light-color), 0 0 40px var(--electric-light-color);}
  100% { box-shadow: 0 0 10px var(--electric-light-color), 0 0 20px var(--electric-light-color);}
}

/* Background Image */
.stApp {
    background-image: url('https://images.unsplash.com/photo-1564866657319-0c1f8c16f3ef?auto=format&fit=crop&w=1950&q=80');
    background-size: cover;
    background-position: center;
    color: white;
}
</style>

<div class="cursor-glow" id="glow"></div>

<script>
const glow = document.getElementById("glow");
document.addEventListener("mousemove", e => {
    glow.style.transform = `translate(${e.clientX}px, ${e.clientY}px)`;
});
</script>
""", unsafe_allow_html=True)

# -------------------------------
# Step 3: Page Configuration
# -------------------------------
st.set_page_config(page_title="EB Mall Feedback", page_icon="📝", layout="wide")

# -------------------------------
# Step 4: Feedback Form
# -------------------------------
st.markdown('<div class="electric-border">', unsafe_allow_html=True)

st.title("📝 EB Mall Feedback Sentiment Classifier")
st.write("Your opinion matters! Enter your details and feedback below:")

with st.form(key='feedback_form'):
    name = st.text_input("Name")
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    age = st.number_input("Age", min_value=1, max_value=120)
    email = st.text_input("Email")
    feedback = st.text_area("Your Feedback")
    submit_button = st.form_submit_button(label='💌 Submit Feedback')

st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# Step 5: Sentiment Analysis
# -------------------------------
if submit_button and feedback.strip() != "":
    blob = TextBlob(feedback)
    polarity = blob.sentiment.polarity

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
    st.balloons()  # Celebratory effect

# -------------------------------
# Step 6: Save Feedback
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
# Step 7: Show Report with Electric Border
# -------------------------------
if st.checkbox("Show Feedback Report"):
    st.markdown('<div class="electric-border">', unsafe_allow_html=True)
    if os.path.exists(report_file):
        df_report = pd.read_csv(report_file)
        st.dataframe(df_report)
    else:
        st.warning("No feedback data available yet.")
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# Step 8: Show Sentiment Charts with Electric Border
# -------------------------------
if st.checkbox("Show Sentiment Charts"):
    st.markdown('<div class="electric-border">', unsafe_allow_html=True)
    if os.path.exists(report_file):
        df_report = pd.read_csv(report_file)

        # Plotly Pie Chart
        st.subheader("Sentiment Distribution - Interactive Pie Chart")
        fig = px.pie(df_report, names='Sentiment', title='Sentiment Distribution', 
                     color='Sentiment', color_discrete_map={'Positive':'green','Negative':'red','Neutral':'gray'})
        st.plotly_chart(fig)

        # Bar Chart
        st.subheader("Sentiment Distribution - Bar Chart")
        sentiment_counts = df_report['Sentiment'].value_counts()
        st.bar_chart(sentiment_counts)
    else:
        st.warning("No feedback data available to show charts.")
    st.markdown('</div>', unsafe_allow_html=True)

