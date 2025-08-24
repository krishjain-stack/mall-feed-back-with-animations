# app.py
# -------------------------------
# EB Mall Feedback Sentiment Analysis
# With Background Effects (Toggle)
# -------------------------------

# Step 1: Import Libraries
import streamlit as st
import pandas as pd
import pickle
import requests
from streamlit_lottie import st_lottie

# Step 2: Page Config
st.set_page_config(page_title="EB Mall Feedback", page_icon="🛍️", layout="wide")

# Step 3: Sidebar Toggle for Background
st.sidebar.subheader("🎨 Background Effects")
enable_bg = st.sidebar.checkbox("Enable Animated Background", value=True)

# Step 4: Load Lottie Animations
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Step 5: Background Effects (only if enabled)
if enable_bg:
    # Background GIF
    st.markdown(
        """
        <style>
        .stApp {
            background: url("https://i.gifer.com/7efs.gif");
            background-size: cover;
            background-attachment: fixed;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Lottie Waves
    st_lottie(
        load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_kyu7xb1v.json"),
        speed=1,
        loop=True,
        quality="high",
        height=300,
        key="lottie-bg",
    )

    # Particles.js Effect
    st.markdown(
        """
        <script src="https://cdn.jsdelivr.net/npm/particles.js"></script>
        <div id="particles-js"></div>
        <style>
            #particles-js {
                position: fixed;
                width: 100%;
                height: 100%;
                top: 0;
                left: 0;
                z-index: -1;
            }
        </style>
        <script>
            particlesJS("particles-js", {
                "particles": {
                    "number": { "value": 80 },
                    "size": { "value": 3 },
                    "move": { "speed": 1 }
                }
            });
        </script>
        """,
        unsafe_allow_html=True
    )

# Step 6: Load ML Model
try:
    model = pickle.load(open("sentiment_model.pkl", "rb"))
    vectorizer = pickle.load(open("vectorizer.pkl", "rb"))
except Exception as e:
    st.error("Model files not found. Please upload sentiment_model.pkl and vectorizer.pkl")
    st.stop()

# Step 7: Main Title
st.title("🛍️ EB Mall Feedback Sentiment Analysis")

# Step 8: Input Section
user_input = st.text_area("✍️ Enter Customer Feedback:")

if st.button("Analyze Sentiment"):
    if user_input.strip() != "":
        transformed_input = vectorizer.transform([user_input])
        prediction = model.predict(transformed_input)[0]

        if prediction == 1:
            st.success("😊 Positive Feedback")
        else:
            st.error("😞 Negative Feedback")
    else:
        st.warning("⚠️ Please enter some feedback text.")

# Step 9: Footer
st.markdown("---")
st.caption("Built with ❤️ using Streamlit | EB Mall Project")
